#pragma once

#include <muscle_manager_protocol/muscle_manager_protocol.pb.h>
#include <ymmsl/compute_element.hpp>


namespace libmuscle {

/** Convert a gRPC Port to a ymmsl port.
 *
 * @param port The port to convert.
 * @return The same port, as the ymmsl type.
 */
::ymmsl::Port port_from_grpc(::muscle_manager_protocol::Port const & port);

/** Convert a ymmsl Port to a gRPC port.
 *
 * @param port The port to convert.
 * @return The same port, as the gRPC type.
 */
::muscle_manager_protocol::Port port_from_grpc(::ymmsl::Port const & port);

}

