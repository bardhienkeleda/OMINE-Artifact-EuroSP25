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

#include <core.p4>
#include <v1model.p4>

#include "../include/first_switch/first_switch_headers.p4"
#include "../include/first_switch/first_switch_parser.p4"
#include "../include/checksum.p4"
#include "../include/packet-io.p4"
#include "../include/forward.p4"
#include "../include/first_switch/fxpt-format.p4"
#include "../include/count.p4"

control IngressPipeImpl (inout parsed_headers_t hdr,
                         inout local_metadata_t local_metadata,
                         inout standard_metadata_t standard_metadata) {
    register<bit<16>> (1) weight;
    bit<16> temp_val;
    action read_and_increment(){
        weight.read(temp_val,(bit<32>)0);
        if(temp_val  <= WEIGHT_LIM - (bit<16>) hdr.results.incorrect_count){
            temp_val = temp_val + (bit<16>)hdr.results.incorrect_count;
        }
        weight.write((bit<32>)0, temp_val);
    }
    action read_and_attach_weight(){
        weight.read(temp_val,(bit<32>)0);
        hdr.outputs.weight = temp_val;
    }

    action read_and_decrement(){
        weight.read(temp_val, (bit<32>)0);
        if(temp_val > (bit<16>)hdr.results.incorrect_count){
            temp_val = temp_val - (bit<16>)hdr.results.incorrect_count;
        }
        weight.write((bit<32>)0, temp_val);
    }
 
    apply {
        //reach first then add header and setValid
        if(hdr.ipv4.protocol == 253 ){
            if(standard_metadata.ingress_port == 1){
                hdr.outputs.setValid();
                hdr.outputs.weight = 0;
                hdr.outputs.prediction = 0;
            }
            else if(standard_metadata.ingress_port == 2){
                if(hdr.results.isValid() && 
                        (hdr.results.truth == hdr.results.prediction)){
                    read_and_increment();
                }else if (hdr.results.isValid() &&
                    (hdr.results.truth != hdr.results.prediction)){
                    read_and_decrement();
                }
                hdr.truths.setValid();
                hdr.truths.truth = hdr.results.truth;
                hdr.truths.incorrect_count = hdr.results.incorrect_count;
                hdr.results.setInvalid(); 
                hdr.ts.setValid();
                hdr.ts.timestamp = standard_metadata.ingress_global_timestamp;
            }else if(standard_metadata.ingress_port == 3){
                count_control.apply(hdr, local_metadata, standard_metadata);
                read_and_attach_weight();
            }

            packetio_ingress.apply(hdr, standard_metadata);
            forward_control.apply(hdr, local_metadata, standard_metadata);
        }else {
            mark_to_drop(standard_metadata);
        }
    }
}

control EgressPipeImpl (inout parsed_headers_t hdr,
                        inout local_metadata_t local_metadata,
                        inout standard_metadata_t standard_metadata) {
    apply {
        fxpt_format_control.apply(hdr, local_metadata, standard_metadata);
        packetio_egress.apply(hdr, standard_metadata);
    }
}

V1Switch(
    ParserImpl(),
    VerifyChecksumImpl(),
    IngressPipeImpl(),
    EgressPipeImpl(),
    ComputeChecksumImpl(),
    DeparserImpl()
) main;
