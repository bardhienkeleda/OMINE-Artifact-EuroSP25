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
    
    register<bit<16>> (1) weight;
    bit<16> temp_val;
    // might not need this
    // store output1-5 into the meta data as well as the truth label
    // action store_into_meta(){
    //     // local_metadata.meta_outputs.count = hdr.outputs.count;
    //     local_metadata.meta_outputs.prediction1 = hdr.outputs.prediction1;
    //     local_metadata.meta_outputs.prediction2 = hdr.outputs.prediction2;
    //     local_metadata.meta_outputs.prediction3 = hdr.outputs.prediction3;
    //     local_metadata.meta_outputs.prediction4 = hdr.outputs.prediction4;
    //     // the truth label has already been computed
    // }
    action read_and_attach_weight(){
            weight.read(temp_val,(bit<32>)0);
            if(hdr.counts.count == 5){
                hdr.outputs_5.weight5 = temp_val;
            }else if(hdr.counts.count == 4){
                hdr.outputs_4.weight4 = temp_val;
            }else if(hdr.counts.count == 3){
                hdr.outputs_3.weight3 = temp_val;
            }
    //     hdr.outputs.weight5 = temp_val;
    }
    action increment(){ // TODO: need to fix this +1
        if(temp_val <= WEIGHT_LIM - (bit<16>) local_metadata.incorrect_count){
            temp_val = temp_val + (bit<16>)local_metadata.incorrect_count;
        }      
        weight.write((bit<32>)0, temp_val);
    }
    action decrement_gtz(){
        if(temp_val > (bit<16>)local_metadata.incorrect_count){
            temp_val = temp_val - (bit<16>) local_metadata.incorrect_count;
        }
        weight.write((bit<32>)0, temp_val);
    }
    apply {
        if(hdr.ipv4.protocol == 253 ){
            if(standard_metadata.ingress_port == 1){
                hdr.first_output.setValid();
                hdr.first_output.weight = 0;
                hdr.first_output.prediction = 0;
                hdr.first_output.last_prediction = 0;
                count_control.apply(hdr,local_metadata, standard_metadata);
            }
            else if(standard_metadata.ingress_port == 3){
                if(hdr.counts.isValid()){
                    read_and_attach_weight();
                    output_compute_control.apply(hdr, local_metadata, standard_metadata);
                    clone_preserving_field_list(CloneType.I2E,5,0);
                    if(hdr.outputs_5.isValid() && hdr.outputs_5.prediction5 == hdr.outputs_5.prediction6){
                        increment();     
                    } else {
                        decrement_gtz();
                    }
                }

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

    action set_result_5(){

        hdr.results_5.setValid();
        hdr.results_5.truth = local_metadata.final_prediction;
        hdr.results_5.incorrect_count = local_metadata.incorrect_count;
        hdr.results_5.prediction4 = local_metadata.sw4_prediction;
        hdr.results_5.prediction3 = local_metadata.sw3_prediction;
        hdr.results_5.prediction2 = local_metadata.sw2_prediction;
        hdr.results_5.prediction1 = local_metadata.sw1_prediction;
        // hdr.results_5.debug = 0xffff;

    }

    action set_result_4(){
        hdr.results_4.setValid();
        hdr.results_4.truth = hdr.outputs_4.prediction5;
        hdr.results_4.incorrect_count = local_metadata.incorrect_count;
        hdr.results_4.prediction3 = hdr.outputs_4.prediction3;
        hdr.results_4.prediction2 = hdr.outputs_4.prediction2;
        hdr.results_4.prediction1 = hdr.outputs_4.prediction1;
    
        hdr.outputs_4.setInvalid();
    }

    action set_result_3(){
        hdr.results_3.setValid();
        hdr.results_3.truth = hdr.outputs_3.prediction4;
        hdr.results_3.incorrect_count = local_metadata.incorrect_count;
        hdr.results_3.prediction2 = hdr.outputs_3.prediction2;
        hdr.results_3.prediction1 = hdr.outputs_3.prediction1;
        hdr.outputs_3.setInvalid();
    }

    apply {

        if(standard_metadata.instance_type == 1){ // cloned packet
            // // remove outputs replace with new backward hearder
            if(hdr.counts.count == 3){
                set_result_3();
            }else if(hdr.counts.count == 4){
                set_result_4();
            }else if(hdr.counts.count == 5){
                set_result_5();
            }else{
                hdr.counts.count = 6;
                hdr.outputs_5.setInvalid();
            }

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
