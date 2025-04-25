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
#include "final_switch_headers.p4"
#include "../defines.p4"


#ifndef __OUTPUT_COMPUTE__
#define __OUTPUT_COMPUTE__


control output_compute_control(inout parsed_headers_t hdr,
                            inout local_metadata_t local_metadata,
                            inout standard_metadata_t standard_metadata
                            ) {
    bit<16> sum_zero = 0;
    bit<16> sum_one = 0;
    bit<16> voted_one = 0;
    bit<16> voted_zero = 0;



    action compute_sum_3(){
        if(hdr.outputs_3.prediction1 == 0){
            sum_zero = sum_zero + hdr.outputs_3.weight1;       
        }else{
            sum_one = sum_one + hdr.outputs_3.weight1;
        }
        if(hdr.outputs_3.prediction2 == 0){
            sum_zero = sum_zero + hdr.outputs_3.weight1;       
        }else{
            sum_one = sum_one + hdr.outputs_3.weight1;
        }
        if(hdr.outputs_3.prediction3 == 0){
            sum_zero = sum_zero + hdr.outputs_3.weight3;       
        }else{
            sum_one = sum_one + hdr.outputs_3.weight3;
        }
        hdr.outputs_3.prediction4 = (sum_one > sum_zero) ? (bit<8>)1 : 0; 
    }

    action compute_sum_4(){
        if(hdr.outputs_4.prediction1 == 0){
            sum_zero = sum_zero + hdr.outputs_4.weight1;       
        }else{
            sum_one = sum_one + hdr.outputs_4.weight1;
        }
        if(hdr.outputs_4.prediction2 == 0){
            sum_zero = sum_zero + hdr.outputs_4.weight2;       
        }else{
            sum_one = sum_one + hdr.outputs_4.weight2;
        }
        if(hdr.outputs_4.prediction3 == 0){
            sum_zero = sum_zero + hdr.outputs_4.weight3;       
        }else{
            sum_one = sum_one + hdr.outputs_4.weight3;
        }
        if(hdr.outputs_4.prediction4 == 0){
            sum_zero = sum_zero + hdr.outputs_4.weight4;       
        }else{
            sum_one = sum_one + hdr.outputs_4.weight4;
        }            
        hdr.outputs_4.prediction5 = (sum_one > sum_zero) ? (bit<8>)1 : 0; 

    }


    action compute_sum_5(){
        if(hdr.outputs_5.prediction1 == 0){
            sum_zero = sum_zero + hdr.outputs_5.weight1;  
            voted_zero=voted_zero+1;     
        }else{
            sum_one = sum_one + hdr.outputs_5.weight1;
            voted_one=voted_one+1;     

        }
        if(hdr.outputs_5.prediction2 == 0){
            sum_zero = sum_zero + hdr.outputs_5.weight2; 
            voted_zero=voted_zero+1;     
      
        }else{
            sum_one = sum_one + hdr.outputs_5.weight2;
            voted_one=voted_one+1;     

        }
        if(hdr.outputs_5.prediction3 == 0){
            sum_zero = sum_zero + hdr.outputs_5.weight3; 
            voted_zero=voted_zero+1;     
      
        }else{
            sum_one = sum_one + hdr.outputs_5.weight3;
            voted_one=voted_one+1;     

        }
        if(hdr.outputs_5.prediction4 == 0){
            sum_zero = sum_zero + hdr.outputs_5.weight4;
            voted_zero=voted_zero+1;     
       
        }else{
            sum_one = sum_one + hdr.outputs_5.weight4;
            voted_one=voted_one+1;     
        
        }
        if(hdr.outputs_5.prediction5 == 0){
            sum_zero = sum_zero + hdr.outputs_5.weight5;
            voted_zero=voted_zero+1;     
       
        }else{
            sum_one = sum_one + hdr.outputs_5.weight5;
            voted_one=voted_one+1;     
        
        }
        if(sum_one > sum_zero){
            hdr.outputs_5.prediction6 = 1; 
            local_metadata.final_prediction =  1; 
        }else if(sum_one == sum_zero){
            hdr.outputs_5.prediction6 = (voted_one > voted_zero) ? (bit<8>)1 : 0; 
            local_metadata.final_prediction =  (voted_one > voted_zero) ? (bit<8>)1 : 0; 
        }else {
            hdr.outputs_5.prediction6 = 0; 
            local_metadata.final_prediction =  0; 
        }
        //hdr.outputs_5.prediction6 = (sum_one > sum_zero) ? (bit<8>)1 : 0; 

    }

 action incorrect_inc_3(){
         local_metadata.incorrect_count = 0; 
        if(hdr.outputs_3.prediction1 != hdr.outputs_3.prediction4){
            local_metadata.incorrect_count = local_metadata.incorrect_count + 1;
        }
        if(hdr.outputs_3.prediction2 != hdr.outputs_3.prediction4){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_3.prediction3 != hdr.outputs_3.prediction4){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
    }

 action incorrect_inc_4(){
        // hdr.results.incorrect_count = 0;  
        local_metadata.incorrect_count = 0; 
        if(hdr.outputs_4.prediction1 != hdr.outputs_4.prediction5){
            local_metadata.incorrect_count = local_metadata.incorrect_count + 1;
        }
        if(hdr.outputs_4.prediction2 != hdr.outputs_4.prediction5){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_4.prediction3 != hdr.outputs_4.prediction5){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_4.prediction4 != hdr.outputs_4.prediction5){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }

    }


    action incorrect_inc_5(){
        // hdr.results.incorrect_count = 0;  
        local_metadata.incorrect_count =0;

        if(hdr.outputs_5.prediction1 != local_metadata.final_prediction){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_5.prediction2 != local_metadata.final_prediction){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_5.prediction3 != local_metadata.final_prediction){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_5.prediction4 != local_metadata.final_prediction){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_5.prediction5 != local_metadata.final_prediction){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }

    }


    action copy_predictions(){
        local_metadata.sw1_prediction = hdr.outputs_5.prediction1;
        local_metadata.sw2_prediction = hdr.outputs_5.prediction2;
        local_metadata.sw3_prediction = hdr.outputs_5.prediction3;
        local_metadata.sw4_prediction = hdr.outputs_5.prediction4;
    }

    apply{
        local_metadata.final_prediction = 0;
        if(hdr.counts.count == 3 && hdr.outputs_3.isValid()){
            // hdr.outputs_3.weight3 = temp_val;
            compute_sum_3();
            incorrect_inc_3();
        }else if(hdr.counts.count == 4 && hdr.outputs_4.isValid()){
            // hdr.outputs_4.weight4 = temp_val;
            compute_sum_4();
            incorrect_inc_4();
        }else if(hdr.counts.count == 5 && hdr.outputs_5.isValid()){
            // hdr.outputs_5.weight5 = temp_val;
            compute_sum_5();
            incorrect_inc_5();
            copy_predictions();
            hdr.outputs_5.incorrect_count = local_metadata.incorrect_count;
        }
    }
}
#endif
