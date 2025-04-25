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



// Switch code for 
#include <core.p4>
#include <v1model.p4>

#include "../include/defines.p4"
#include "../include/final_switch/final_switch_headers.p4"
#include "../include/final_switch/final_switch_parser.p4"
#include "../include/count.p4"
#include "../include/final_switch/output_compute.p4"
#include "../include/checksum.p4"
#include "../include/packet-io.p4"
#include "../include/forward.p4"

#define PKT_INSTANCE_TYPE_NORMAL 0
#define PKT_INSTANCE_TYPE_INGRESS_CLONE 1
#define PKT_INSTANCE_TYPE_EGRESS_CLONE 2
#define PKT_INSTANCE_TYPE_COALESCED 3
#define PKT_INSTANCE_TYPE_INGRESS_RECIRC 4
#define PKT_INSTANCE_TYPE_REPLICATION 5
#define PKT_INSTANCE_TYPE_RESUBMIT 6

// #include "../include/fxpt-format.p4"

control IngressPipeImpl (inout parsed_headers_t hdr,
                         inout local_metadata_t local_metadata,
                         inout standard_metadata_t standard_metadata) {

    apply {
        if(hdr.ethernet.isValid()){
            
            if(hdr.ipv4.protocol == 253){       
                // Note: the following ingress port need to match the
                // ingress port from the MapReduce module
                if(standard_metadata.ingress_port == 4){
                    if(hdr.counts.isValid()){
                        output_compute_control.apply(hdr, local_metadata, standard_metadata);
                    }
                }else{
                    hdr.ipv4.total_len = hdr.ipv4.total_len+5;
                    hdr.first_output.setValid();
                    hdr.first_output.weight = 0;
                    hdr.first_output.prediction = 0;
                    hdr.first_output.last_prediction = 0;
                    hdr.first_output.ing_port = (bit<8>)standard_metadata.ingress_port;
                    count_control.apply(hdr,local_metadata, standard_metadata);
                }
                packetio_ingress.apply(hdr, standard_metadata);
                forward_control.apply(hdr, local_metadata, standard_metadata);
            } else {
                mark_to_drop(standard_metadata);
            }       
        }
    }
}

control EgressPipeImpl (inout parsed_headers_t hdr,
                        inout local_metadata_t local_metadata,
                        inout standard_metadata_t standard_metadata) {
    action set_result_9(){
        hdr.results_9.setValid();
        hdr.results_9.truth = local_metadata.final_prediction;
        hdr.results_9.incorrect_count = local_metadata.incorrect_count;
        hdr.results_9.prediction8 = local_metadata.prediction8;
        hdr.results_9.prediction7 = local_metadata.prediction7;
        hdr.results_9.prediction6 = local_metadata.prediction6;
        hdr.results_9.prediction5 = local_metadata.prediction5;
        hdr.results_9.prediction4 = local_metadata.prediction4;
        hdr.results_9.prediction3 = local_metadata.prediction3;
        hdr.results_9.prediction2 = local_metadata.prediction2;
        hdr.results_9.prediction1 = local_metadata.prediction1;
    }

    action set_result_8(){
        hdr.results_8.setValid();
        hdr.results_8.truth = local_metadata.final_prediction;
        hdr.results_8.incorrect_count = local_metadata.incorrect_count;
        hdr.results_8.prediction7 = local_metadata.prediction7;
        hdr.results_8.prediction6 = local_metadata.prediction6;
        hdr.results_8.prediction5 = local_metadata.prediction5;
        hdr.results_8.prediction4 = local_metadata.prediction4;
        hdr.results_8.prediction3 = local_metadata.prediction3;
        hdr.results_8.prediction2 = local_metadata.prediction2;
        hdr.results_8.prediction1 = local_metadata.prediction1;
    }

    action set_result_7(){
        hdr.results_7.setValid();
        hdr.results_7.truth = local_metadata.final_prediction;
        hdr.results_7.incorrect_count = local_metadata.incorrect_count;
        hdr.results_7.prediction6 = local_metadata.prediction6;
        hdr.results_7.prediction5 = local_metadata.prediction5;
        hdr.results_7.prediction4 = local_metadata.prediction4;
        hdr.results_7.prediction3 = local_metadata.prediction3;
        hdr.results_7.prediction2 = local_metadata.prediction2;
        hdr.results_7.prediction1 = local_metadata.prediction1;
    }

    action set_result_6(){
        hdr.results_6.setValid();
        hdr.results_6.truth = local_metadata.final_prediction;
        hdr.results_6.incorrect_count = local_metadata.incorrect_count;
        hdr.results_6.prediction5 = local_metadata.prediction5;
        hdr.results_6.prediction4 = local_metadata.prediction4;
        hdr.results_6.prediction3 = local_metadata.prediction3;
        hdr.results_6.prediction2 = local_metadata.prediction2;
        hdr.results_6.prediction1 = local_metadata.prediction1;
    
    }

    action set_result_5(){
        hdr.results_5.setValid();
        hdr.results_5.truth = local_metadata.final_prediction;
        hdr.results_5.incorrect_count = local_metadata.incorrect_count;
        hdr.results_5.prediction4 = local_metadata.prediction4;
        hdr.results_5.prediction3 = local_metadata.prediction3;
        hdr.results_5.prediction2 = local_metadata.prediction2;
        hdr.results_5.prediction1 = local_metadata.prediction1;

    }

    action set_result_4(){
        hdr.results_4.setValid();
        hdr.results_4.truth = local_metadata.final_prediction;
        hdr.results_4.incorrect_count = local_metadata.incorrect_count;
        hdr.results_4.prediction3 = hdr.outputs_4.prediction3;
        hdr.results_4.prediction2 = hdr.outputs_4.prediction2;
        hdr.results_4.prediction1 = hdr.outputs_4.prediction1;
    }

    action set_result_3(){
        hdr.results_3.setValid();
        hdr.results_3.truth = local_metadata.final_prediction;
        hdr.results_3.incorrect_count = local_metadata.incorrect_count;
        hdr.results_3.prediction2 = local_metadata.prediction2;
        hdr.results_3.prediction1 = local_metadata.prediction1;
    }

    action set_result_2(){
        hdr.results_2.setValid();
        hdr.results_2.truth = local_metadata.final_prediction;
        hdr.results_2.incorrect_count = local_metadata.incorrect_count;
        hdr.results_2.prediction1 = local_metadata.prediction1;
    }

    apply {
        // check if this is a cloned packet
        // if it is then save local meta to result header
        // and set output header valid
        if(standard_metadata.instance_type == 1){ // cloned packet

            hdr.ethernet.ether_type = ETHERTYPE_BP;
            if(hdr.counts.count == 2){
                set_result_2();
            }else if(hdr.counts.count == 3){
                set_result_3();
            }else if(hdr.counts.count == 4){
                set_result_4();
            }else if(hdr.counts.count == 5){
                set_result_5();
            }else if(hdr.counts.count == 6){
                set_result_6();
            }else if(hdr.counts.count == 7){
                set_result_7();
            }else if(hdr.counts.count == 8){
                set_result_8();
            }else if(hdr.counts.count == 9){
                set_result_9();                
            }else{
                hdr.counts.count = 0xcc; // debugging code
            }

            // removing irrelavant headers
            hdr.counts.setInvalid();
            hdr.ipv4.setInvalid();
            hdr.ml_fields.setInvalid();

        } else{ // else apply original logic
            packetio_egress.apply(hdr, standard_metadata);
        }

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
