#pragma once

#include <libmuscle/data.hpp>
#include <libmuscle/util.hpp>
#include <ymmsl/ymmsl.hpp>


namespace libmuscle { namespace impl { namespace mcp {

/** A MUSCLE Communication Protocol message.
 *
 * Messages carry the identity of their sender and receiver, so that they can
 * be routed by a MUSCLE Transport Overlay when we get to multi-site running in
 * the future.
 */
struct Message {
    /** Create an MCP Message.
     *
     * Senders and receivers are referred to by a Reference, which
     * contains Instance[InstanceNumber].Port[Slot].
     *
     * The port_length field is only used if two vector ports are connected
     * together. In that case the number of slots is not determined by the
     * number of instances, and must be set by the sender and then
     * communicated to the receiver in this additional field in all
     * messages sent on the port.
     *
     * This is the on-the-wire object, the user-facing one is in
     * libmuscle/communicator.hpp.
     */
    Message(
            ::ymmsl::Reference const & sender, ::ymmsl::Reference const & receiver,
            ::libmuscle::impl::Optional<int> port_length,
            double timestamp, ::libmuscle::impl::Optional<double> next_timestamp,
            DataConstRef const & settings_overlay,
            DataConstRef const & data);

    ::ymmsl::Reference sender;
    ::ymmsl::Reference receiver;
    ::libmuscle::impl::Optional<int> port_length;
    double timestamp;
    ::libmuscle::impl::Optional<double> next_timestamp;
    DataConstRef settings_overlay;
    DataConstRef data;
};

} } }

