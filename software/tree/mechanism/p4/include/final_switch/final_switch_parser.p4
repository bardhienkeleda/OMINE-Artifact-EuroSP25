//*************************************************************************
//
// Copyright 2025 Enkeleda Bardhi (TU Delft),
//                Chenxing Ji (TU Delft),
//                Ali Imran (University of Michigan),
//                Muhammad Shahbaz (University of Michigan),
//                Riccardo Lazzeretti (Sapienza University of Rome),
//                Mauro Conti (University of Padua),
//                Fernando Kuipers (TU Delft)
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
//*************************************************************************

#ifndef __PARSER__
#define __PARSER__

#include "../defines.p4"

parser ParserImpl (packet_in packet,
                   out parsed_headers_t hdr,
                   inout local_metadata_t local_metadata,
                   inout standard_metadata_t standard_metadata)
{
    state start {
        transition select(standard_metadata.ingress_port) {
            CPU_PORT: parse_packet_out;
            default: parse_ethernet;
        }
    }

    state parse_packet_out {
        packet.extract(hdr.packet_out);
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.ether_type){
            ETHERTYPE_ARP: parse_arp;
            ETHERTYPE_IPV4: parse_ipv4;
            
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        local_metadata.ip_proto = hdr.ipv4.protocol;
        transition select(hdr.ipv4.protocol) {
            PROTO_TCP: parse_tcp;
            PROTO_UDP: parse_udp;
            PROTO_ICMP: parse_icmp;
            PROTO_ML: parse_ml;
            default: accept;
        }
    }

    state parse_arp {
        packet.extract(hdr.arp);
        transition accept;
    }

    state parse_tcp {
        packet.extract(hdr.tcp);
        local_metadata.l4_src_port = hdr.tcp.src_port;
        local_metadata.l4_dst_port = hdr.tcp.dst_port;
        transition accept;
    }

    state parse_udp {
        packet.extract(hdr.udp);
        local_metadata.l4_src_port = hdr.udp.src_port;
        local_metadata.l4_dst_port = hdr.udp.dst_port;
        transition accept;
    }

    state parse_icmp {
        packet.extract(hdr.icmp);
        local_metadata.icmp_type = hdr.icmp.type;
        transition accept;
    }

    state parse_ml {
        packet.extract(hdr.ml_fields);
        transition transition_ports;
    }

    state transition_ports {
        transition select(standard_metadata.ingress_port){
            4: parse_output; // parse outputs
            default: parse_count;
        }
    }

    state parse_count {
        packet.extract(hdr.counts);
        transition accept;
    }

    state parse_output{
        packet.extract(hdr.counts);
        transition select(hdr.counts.count){
            2: parse_output_2;
            3: parse_output_3;
            4: parse_output_4;
            5: parse_output_5;
            6: parse_output_6;
            7: parse_output_7;
            8: parse_output_8;
            9: parse_output_9;
            default: accept;
        }
    }

    state parse_output_2{
        packet.extract(hdr.outputs_2);
        transition accept;
    }

    state parse_output_3{
        packet.extract(hdr.outputs_3);
        transition accept;
    }
    state parse_output_4{
        packet.extract(hdr.outputs_4);
        transition accept;
    }
    state parse_output_5{
        packet.extract(hdr.outputs_5);
        transition accept;
    }
    state parse_output_6{
        packet.extract(hdr.outputs_6);
        transition accept;
    }
    state parse_output_7{
        packet.extract(hdr.outputs_7);
        transition accept;
    }
    state parse_output_8{
        packet.extract(hdr.outputs_8);
        transition accept;
    }
    state parse_output_9{
        packet.extract(hdr.outputs_9);
        transition accept;
    }
}

control DeparserImpl(packet_out packet, in parsed_headers_t hdr) {
    apply {
        packet.emit(hdr.packet_in);
        packet.emit(hdr.ethernet);
        packet.emit(hdr.results_2);
        packet.emit(hdr.results_3);
        packet.emit(hdr.results_4);
        packet.emit(hdr.results_5);
        packet.emit(hdr.results_6);
        packet.emit(hdr.results_7);
        packet.emit(hdr.results_8);
        packet.emit(hdr.results_9);
        packet.emit(hdr.arp);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
        packet.emit(hdr.udp);
        packet.emit(hdr.icmp);
        packet.emit(hdr.ml_fields);
        packet.emit(hdr.counts);
        packet.emit(hdr.first_output);
        packet.emit(hdr.outputs_2);
        packet.emit(hdr.outputs_3);
        packet.emit(hdr.outputs_4);
        packet.emit(hdr.outputs_5);
        packet.emit(hdr.outputs_6);
        packet.emit(hdr.outputs_7);
        packet.emit(hdr.outputs_8);
        packet.emit(hdr.outputs_9);
        packet.emit(hdr.debug);
    }
}

#endif
