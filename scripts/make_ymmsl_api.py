#!/usr/bin/env python3

import argparse
from textwrap import indent

from api_generator import (
        API, AssignmentOperator, Bool, Bytes, Char, Class, Constructor,
        Destructor, Double, Enum, EnumVal, EqualsOperator, Float,
        IndexAssignmentOperator, Int, Int16t, Int32t, Int64t, MemFun,
        MemFunTmpl, NamedConstructor, Namespace, Obj, OverloadSet,
        Sizet, String, T, VecDbl, Vec2Dbl, Void)


# These need to kept in sync with the values in the C++ implementation
operator_desc = Enum('Operator', [
        ('NONE', '0'),
        ('F_INIT', '1'),
        ('O_I', '2'),
        ('S', '3'),
        ('B', '4'),
        ('O_F', '5')
        ])


settings_desc = Class('Settings', None, [
    Constructor(),
    Destructor(),
    EqualsOperator(Obj('Settings', 'other')),
    MemFun(Sizet('size'), 'size'),
    MemFun(Bool('empty'), 'empty'),
    MemFunTmpl(
        [String(), Int32t(), Int64t(), Double(), Bool(), VecDbl(), Vec2Dbl()],
        Bool(), 'is_a', [String('key')], True,
        cpp_chain_call=lambda **kwargs: 'self_p->at({}).is_a<{}>()'.format(
            kwargs['cpp_args'], kwargs['tpl_type'])),
    IndexAssignmentOperator('set_character', [String('key'), String('value')]),
    IndexAssignmentOperator('set_int4', [String('key'), Int32t('value')]),
    IndexAssignmentOperator('set_int8', [String('key'), Int64t('value')]),
    IndexAssignmentOperator('set_real8', [String('key'), Double('value')]),
    IndexAssignmentOperator('set_logical', [String('key'), Bool('value')]),
    IndexAssignmentOperator('set_real8array', [String('key'), VecDbl('value')]),
    IndexAssignmentOperator('set_real8array2', [String('key'), Vec2Dbl('value')]),
    OverloadSet('set', [
        'set_character', 'set_int4', 'set_int8', 'set_real8', 'set_logical',
        'set_real8array', 'set_real8array2']),
    MemFunTmpl(
        [String(), Int32t(), Int64t(), Double(), Bool(), VecDbl('value'),
            Vec2Dbl('value')
            ],
        T(), 'get_as', [String('key')], True,
        cpp_chain_call=lambda **kwargs: 'self_p->at({}).as<{}>()'.format(
            kwargs['cpp_args'], kwargs['tpl_type'])),
    MemFun(Bool(), 'contains', [String('key')]),
    MemFun(Sizet('removed'), 'erase', [String('key')]),
    MemFun(Void(), 'clear'),
    MemFun(String(), 'key', [Sizet('i')], True,
        fc_override=(
            'void YMMSL_Settings_key_(\n'
            '        std::intptr_t self, std::size_t i,\n'
            '        char ** ret_val, std::size_t * ret_val_size,\n'
            '        int * err_code,\n'
            '        char ** err_msg, std::size_t * err_msg_len\n'
            ') {\n'
            '    Settings * self_p = reinterpret_cast<Settings *>(self);\n'
            '    if (i == 0 || i > self_p->size()) {\n'
            '       *err_code = 2;\n'
            '       *err_msg = const_cast<char*>("Key index out of range.");\n'
            '       *err_msg_len = strlen(*err_msg);\n'
            '       return;\n'
            '    }\n'
            '    *err_code = 0;\n'
            '    static std::string result;\n'
            '    result = std::string(std::next(self_p->begin(), i-1)->first);\n'
            '    *ret_val = const_cast<char*>(result.c_str());\n'
            '    *ret_val_size = result.size();\n'
            '    return;\n'
            '}\n\n'
            )
        ),
    ])


ymmsl_api_description = API(
        'ymmsl',
        [
            'ymmsl/ymmsl.hpp',
            'cstring',
            'stdexcept',
            'typeinfo'],
        [],
        [
            Namespace(
                'ymmsl', True, 'YMMSL',
                [operator_desc], [settings_desc]),
        ])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MUSCLE API Generator')
    parser.add_argument('--fortran-c-wrappers', action='store_true')
    parser.add_argument('--fortran-module', action='store_true')
    parser.add_argument('--fortran-exports', nargs=2)

    args = parser.parse_args()
    if args.fortran_c_wrappers:
        print(ymmsl_api_description.fortran_c_wrapper())
    elif args.fortran_module:
        print(ymmsl_api_description.fortran_module())
    elif args.fortran_exports:
        exports = ymmsl_api_description.fortran_exports()
        exports_txt = indent('\n'.join(exports), 8*' ') + '\n'

        in_name = args.fortran_exports[0]
        out_name = args.fortran_exports[1]
        with open(in_name, 'r') as in_file:
            with open(out_name, 'w') as out_file:
                for line in in_file:
                    if 'FORTRAN ABI' in line:
                        out_file.write(exports_txt)
                    else:
                        out_file.write(line)
