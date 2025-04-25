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

#ifndef __HEADER__
#define __HEADER__

#include "../defines.p4"

@controller_header("packet_in")
header packet_in_header_t {
    bit<9> ingress_port;
    bit<7> _pad;
}

@controller_header("packet_out")
header packet_out_header_t {
    bit<9> egress_port;
    bit<7> _pad;
}

header ethernet_t {
    bit<48> dst_addr;
    bit<48> src_addr;
    bit<16> ether_type;
}

header ipv4_t {
    bit<4> version;
    bit<4> ihl;
    bit<6> dscp;
    bit<2> ecn;
    bit<16> total_len;
    bit<16> identification;
    bit<3> flags;
    bit<13> frag_offset;
    bit<8> ttl;
    bit<8> protocol;
    bit<16> hdr_checksum;
    bit<32> src_addr;
    bit<32> dst_addr;
}

header arp_t {
    bit<16> hw_type;
    bit<16> proto_type;
    bit<8> hw_addr_len;
    bit<8> proto_addr_len;
    bit<16> opcode;
}

header tcp_t {
    bit<16> src_port;
    bit<16> dst_port;
    bit<32> seq_no;
    bit<32> ack_no;
    bit<4>  data_offset;
    bit<3>  res;
    bit<3>  ecn;
    bit<6>  ctrl;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgent_ptr;
}

header udp_t {
    bit<16> src_port;
    bit<16> dst_port;
    bit<16> len;
    bit<16> checksum;
}

header icmp_t {
    bit<8> type;
    bit<8> icmp_code;
    bit<16> checksum;
    bit<16> identifier;
    bit<16> sequence_number;
    bit<64> timestamp;
}

header ml_fields_t {
    bit<32> field0;
    bit<32> field1;
    bit<32> field2;
    bit<32> field3;
    bit<32> field4;
    bit<32> field5;
    bit<32> field6;
    bit<8>  label;
}
header count_t {
    bit<8> count;
}
header first_outputs_t{
    bit<16> weight;
    bit<8> prediction;
    bit<8> last_prediction;
}

header outputs_3_t { 
    bit<16> weight3; 
    bit<8> prediction3;
    bit<8> prediction4;
    bit<16> weight2; 
    bit<8> prediction2;
    bit<16> weight1;
    bit<8> prediction1;

}
header outputs_4_t { 
    bit<16> weight4; 
    bit<8> prediction4;
    bit<8> prediction5;
    bit<16> weight3; 
    bit<8> prediction3;
    bit<16> weight2;
    bit<8> prediction2;
    bit<16> weight1;
    bit<8> prediction1;
}
header outputs_5_t { 
    bit<16> weight5; 
    bit<8> prediction5;
    bit<8> prediction6;
    bit<16> weight4; 
    bit<8> prediction4;
    bit<16> weight3;
    bit<8> prediction3;
    bit<16> weight2;
    bit<8> prediction2;
    bit<16> weight1;
    bit<8> prediction1;
    bit<8> incorrect_count;
}

// Back-propagation does not require results of switch 5
header result_5_t{ //result_t header goes backward
    bit<8> truth;
    bit<8> incorrect_count;
    bit<8> prediction4;
    bit<8> prediction3;
    bit<8> prediction2;
    bit<8> prediction1;
    bit<16> debug;
}

header result_4_t{ //result_t header goes backward
    bit<8> truth;
    bit<8> incorrect_count;
    bit<8> prediction3;
    bit<8> prediction2;
    bit<8> prediction1;
}
header result_3_t{ //result_t header goes backward
    bit<8> truth;
    bit<8> counts;
    bit<8> incorrect_count;
    bit<8> prediction2;
    bit<8> prediction1;
}

header inc_count_t{
    bit<16> inc_count;
}

header debug_t {
    bit<16> incorrect_count_val;
}
// Packet header definition
struct parsed_headers_t {
    packet_in_header_t packet_in;
    packet_out_header_t packet_out;
    ethernet_t ethernet;
    ipv4_t ipv4;
    arp_t arp;
    tcp_t tcp;
    udp_t udp;
    icmp_t icmp;
    ml_fields_t ml_fields;
    count_t counts;
    first_outputs_t first_output; // goes to MR
    outputs_3_t outputs_3;
    outputs_4_t outputs_4;
    outputs_5_t outputs_5;
    result_3_t results_3;
    result_4_t results_4;
    result_5_t results_5;
    debug_t debug;
    inc_count_t inc_count;
}

// Custom metadata definition
struct local_metadata_t {
    bit<8> ip_proto;
    bit<8> icmp_type;
    bit<16> l4_src_port;
    bit<16> l4_dst_port;
    @field_list(0)
    bit<8> incorrect_count;
    @field_list(0)
    bit<8> final_prediction;
    @field_list(0)
    bit<8> sw1_prediction;
    @field_list(0)
    bit<8> sw2_prediction;
    @field_list(0)
    bit<8> sw3_prediction;
    @field_list(0)
    bit<8> sw4_prediction;
}



#endif
