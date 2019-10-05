// Template implementation. Do not include directly!

namespace ymmsl {

template<>
inline bool SettingValue::is_a<std::string>() const {
    return type_ == Type_::STRING;
}

template<>
inline bool SettingValue::is_a<int64_t>() const {
    return type_ == Type_::INT;
}

template<>
inline bool SettingValue::is_a<double>() const {
    return type_ == Type_::FLOAT;
}

template<>
inline bool SettingValue::is_a<bool>() const {
    return type_ == Type_::BOOL;
}

template<>
inline bool SettingValue::is_a<std::vector<double>>() const {
    return type_ == Type_::LIST_FLOAT;
}

template<>
inline bool SettingValue::is_a<std::vector<std::vector<double>>>() const {
    return type_ == Type_::LIST_LIST_FLOAT;
}

template <typename T>
bool SettingValue::is_a() const {
    static_assert(sizeof(T) == 0, "Invalid type specified for SettingValue::is_a()");
    return false;   // remove warning
}

template<>
inline std::string SettingValue::as<std::string>() const {
    if (!is_a<std::string>())
        throw std::bad_cast();
    return string_value_;
}

template<>
inline int64_t SettingValue::as<int64_t>() const {
    if (!is_a<int64_t>())
        throw std::bad_cast();
    return int_value_;
}

template<>
inline double SettingValue::as<double>() const {
    if (!is_a<double>())
        throw std::bad_cast();
    return float_value_;
}

template<>
inline bool SettingValue::as<bool>() const {
    if (!is_a<bool>())
        throw std::bad_cast();
    return bool_value_;
}

template<>
inline std::vector<double> SettingValue::as<std::vector<double>>() const {
    if (!is_a<std::vector<double>>())
        throw std::bad_cast();
    return list_value_;
}

template<>
inline std::vector<std::vector<double>> SettingValue::as<std::vector<std::vector<double>>>() const {
    if (!is_a<std::vector<std::vector<double>>>())
        throw std::bad_cast();
    return list_list_value_;
}

template <typename T>
T SettingValue::as() const {
    static_assert(sizeof(T) == 0, "Invalid type specified for SettingValue::as()");
    return T(); // remove warning
}

}

