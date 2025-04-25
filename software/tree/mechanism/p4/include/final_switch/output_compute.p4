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
    bit<32> sum_zero = 0;
    bit<32> sum_one = 0;
    register<bit<16>> (16) weight;
    bit<16> temp_val = 0;
    bit<16> voted_one = 0;
    bit<16> voted_zero = 0;

    action read(){
        weight.read(temp_val,(bit<32>)0);
    }


    action compute_sum_2(){
        if(hdr.outputs_2.prediction1 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_2.weight1;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_2.weight1;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_2.prediction2 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_2.weight2; 
            voted_zero = voted_zero + 1;      
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_2.weight2;
            voted_one = voted_one + 1;
        }
        if(sum_one > sum_zero){
            hdr.outputs_2.prediction3 = 1;
            local_metadata.final_prediction = 1;
        } else if(sum_one == sum_zero ){
            local_metadata.final_prediction = (voted_one > voted_zero) ? (bit<8>)1:0;
            hdr.outputs_2.prediction3 = (voted_one > voted_zero) ? (bit<8>)1:0;
        } else {
            hdr.outputs_2.prediction3 = 0;
            local_metadata.final_prediction = 0;
        }
    }

    action compute_sum_3(){
        if(hdr.outputs_3.prediction1 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_3.weight1;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>) hdr.outputs_3.weight1;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_3.prediction2 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_3.weight2;
            voted_zero = voted_zero + 1;                   
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_3.weight2;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_3.prediction3 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_3.weight3;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_3.weight3;
            voted_one = voted_one + 1;
        }
        if(sum_one > sum_zero){
            hdr.outputs_3.prediction4 = 1;
            local_metadata.final_prediction = 1;
        } else if(sum_one == sum_zero ){
            local_metadata.final_prediction = (voted_one > voted_zero) ? (bit<8>)1:0;
            hdr.outputs_3.prediction4 = (voted_one > voted_zero) ? (bit<8>)1:0;
        } else {
            hdr.outputs_3.prediction4 = 0;
            local_metadata.final_prediction = 0;
        }
    }

    action compute_sum_4(){
        if(hdr.outputs_4.prediction1 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_4.weight1;
            voted_zero = voted_zero + 1;     
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_4.weight1;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_4.prediction2 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_4.weight2;
            voted_zero = voted_zero + 1;        
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_4.weight2;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_4.prediction3 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_4.weight3;
            voted_zero = voted_zero + 1;             
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_4.weight3;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_4.prediction4 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_4.weight4;
            voted_zero = voted_zero + 1;             
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_4.weight4;
            voted_one = voted_one + 1;
        }            

        if(sum_one > sum_zero){
            hdr.outputs_4.prediction5 = 1;
            local_metadata.final_prediction = 1;
        } else if(sum_one == sum_zero ){
            local_metadata.final_prediction = (voted_one > voted_zero) ? (bit<8>)1:0;
            hdr.outputs_4.prediction5 = (voted_one > voted_zero) ? (bit<8>)1:0;
        } else {
            hdr.outputs_4.prediction5 = 0;
            local_metadata.final_prediction = 0;
        }
    }


    action compute_sum_5(){
        if(hdr.outputs_5.prediction1 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_5.weight1;
            voted_zero = voted_zero + 1;     
       
        }else{
            sum_one = sum_one + (bit<32>) hdr.outputs_5.weight1;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_5.prediction2 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_5.weight2; 
            voted_zero = voted_zero + 1;      
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_5.weight2;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_5.prediction3 == 0){
            sum_zero = sum_zero + (bit<32>) hdr.outputs_5.weight3;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_5.weight3;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_5.prediction4 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_5.weight4;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_5.weight4;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_5.prediction5 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_5.weight5;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_5.weight5;
            voted_one = voted_one + 1;
        }
        if(sum_one > sum_zero){
            hdr.outputs_5.prediction6 = 1;
            local_metadata.final_prediction = 1;
        } else if(sum_one == sum_zero ){
            local_metadata.final_prediction = (voted_one > voted_zero) ? (bit<8>)1:0;
            hdr.outputs_5.prediction6 = (voted_one > voted_zero) ? (bit<8>)1:0;
        } else {
            hdr.outputs_5.prediction6 = 0;
            local_metadata.final_prediction = 0;
        }
    }

    action compute_sum_6(){
        if(hdr.outputs_6.prediction1 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_6.weight1;
            voted_zero = voted_zero + 1;     
       
        }else{
            sum_one = sum_one + (bit<32>) hdr.outputs_6.weight1;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_6.prediction2 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_6.weight2; 
            voted_zero = voted_zero + 1;      
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_6.weight2;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_6.prediction3 == 0){
            sum_zero = sum_zero + (bit<32>) hdr.outputs_6.weight3;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_6.weight3;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_6.prediction4 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_6.weight4;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_6.weight4;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_6.prediction5 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_6.weight5;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_6.weight5;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_6.prediction6 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_6.weight6;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_6.weight6;
            voted_one = voted_one + 1;
        }        

        if(sum_one > sum_zero){
            hdr.outputs_6.prediction7 = 1;
            local_metadata.final_prediction = 1;
        } else if(sum_one == sum_zero ){
            local_metadata.final_prediction = (voted_one > voted_zero) ? (bit<8>)1:0;
            hdr.outputs_6.prediction7 = (voted_one > voted_zero) ? (bit<8>)1:0;
        } else {
            hdr.outputs_6.prediction7 = 0;
            local_metadata.final_prediction = 0;
        }
    }

    action compute_sum_7(){
        if(hdr.outputs_7.prediction1 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_7.weight1;
            voted_zero = voted_zero + 1;     
       
        }else{
            sum_one = sum_one + (bit<32>) hdr.outputs_7.weight1;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_7.prediction2 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_7.weight2; 
            voted_zero = voted_zero + 1;      
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_7.weight2;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_7.prediction3 == 0){
            sum_zero = sum_zero + (bit<32>) hdr.outputs_7.weight3;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_7.weight3;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_7.prediction4 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_7.weight4;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_7.weight4;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_7.prediction5 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_7.weight5;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_7.weight5;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_7.prediction6 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_7.weight6;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_7.weight6;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_7.prediction7 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_7.weight7;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_7.weight7;
            voted_one = voted_one + 1;
        }
        if(sum_one > sum_zero){
            hdr.outputs_7.prediction8 = 1;
            local_metadata.final_prediction = 1;
        } else if(sum_one == sum_zero ){
            local_metadata.final_prediction = (voted_one > voted_zero) ? (bit<8>)1:0;
            hdr.outputs_7.prediction8 = (voted_one > voted_zero) ? (bit<8>)1:0;
        } else {
            hdr.outputs_7.prediction8 = 0;
            local_metadata.final_prediction = 0;
        }
    }

    action compute_sum_8(){
        if(hdr.outputs_8.prediction1 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_8.weight1;
            voted_zero = voted_zero + 1;     
       
        }else{
            sum_one = sum_one + (bit<32>) hdr.outputs_8.weight1;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_8.prediction2 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_8.weight2; 
            voted_zero = voted_zero + 1;      
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_8.weight2;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_8.prediction3 == 0){
            sum_zero = sum_zero + (bit<32>) hdr.outputs_8.weight3;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_8.weight3;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_8.prediction4 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_8.weight4;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_8.weight4;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_8.prediction5 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_8.weight5;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_8.weight5;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_8.prediction6 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_8.weight6;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_8.weight6;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_8.prediction7 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_8.weight7;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_8.weight7;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_8.prediction8 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_8.weight8;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_8.weight8;
            voted_one = voted_one + 1;
        }
        if(sum_one > sum_zero){
            hdr.outputs_8.prediction9 = 1;
            local_metadata.final_prediction = 1;
        } else if(sum_one == sum_zero ){
            local_metadata.final_prediction = (voted_one > voted_zero) ? (bit<8>)1:0;
            hdr.outputs_8.prediction9 = (voted_one > voted_zero) ? (bit<8>)1:0;
        } else {
            hdr.outputs_8.prediction9 = 0;
            local_metadata.final_prediction = 0;
        }
    }

    action compute_sum_9(){
        if(hdr.outputs_9.prediction1 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_9.weight1;
            voted_zero = voted_zero + 1;     
       
        }else{
            sum_one = sum_one + (bit<32>) hdr.outputs_9.weight1;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_9.prediction2 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_9.weight2; 
            voted_zero = voted_zero + 1;      
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_9.weight2;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_9.prediction3 == 0){
            sum_zero = sum_zero + (bit<32>) hdr.outputs_9.weight3;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_9.weight3;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_9.prediction4 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_9.weight4;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_9.weight4;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_9.prediction5 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_9.weight5;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_9.weight5;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_9.prediction6 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_9.weight6;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_9.weight6;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_9.prediction7 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_9.weight7;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_9.weight7;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_9.prediction8 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_9.weight8;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_9.weight8;
            voted_one = voted_one + 1;
        }
        if(hdr.outputs_9.prediction9 == 0){
            sum_zero = sum_zero + (bit<32>)hdr.outputs_9.weight9;
            voted_zero = voted_zero + 1;       
        }else{
            sum_one = sum_one + (bit<32>)hdr.outputs_9.weight9;
            voted_one = voted_one + 1;
        }
        if(sum_one > sum_zero){
            hdr.outputs_9.prediction10 = 1;
            local_metadata.final_prediction = 1;
        } else if(sum_one == sum_zero ){
            local_metadata.final_prediction = (voted_one > voted_zero) ? (bit<8>)1:0;
            hdr.outputs_9.prediction10 = (voted_one > voted_zero) ? (bit<8>)1:0;
        } else {
            hdr.outputs_9.prediction10 = 0;
            local_metadata.final_prediction = 0;
        }
    }


    action incorrect_inc_2(){
        local_metadata.incorrect_count = 0; 
        if(hdr.outputs_2.prediction1 != hdr.outputs_2.prediction3){
            local_metadata.incorrect_count = local_metadata.incorrect_count + 1;
        }
        if(hdr.outputs_2.prediction2 != hdr.outputs_2.prediction3){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
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
        local_metadata.incorrect_count = 0; 
        if(hdr.outputs_5.prediction1 != hdr.outputs_5.prediction6){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_5.prediction2 != hdr.outputs_5.prediction6){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_5.prediction3 != hdr.outputs_5.prediction6){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_5.prediction4 != hdr.outputs_5.prediction6){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_5.prediction5 != hdr.outputs_5.prediction6){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
    }

    action incorrect_inc_6(){
        local_metadata.incorrect_count = 0; 
        if(hdr.outputs_6.prediction1 != hdr.outputs_6.prediction7){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_6.prediction2 != hdr.outputs_6.prediction7){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_6.prediction3 != hdr.outputs_6.prediction7){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_6.prediction4 != hdr.outputs_6.prediction7){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_6.prediction5 != hdr.outputs_6.prediction7){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_6.prediction6 != hdr.outputs_6.prediction7){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }        

    }

    action incorrect_inc_7(){
        local_metadata.incorrect_count = 0; 
        if(hdr.outputs_7.prediction1 != hdr.outputs_7.prediction8){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_7.prediction2 != hdr.outputs_7.prediction8){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_7.prediction3 != hdr.outputs_7.prediction8){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_7.prediction4 != hdr.outputs_7.prediction8){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_7.prediction5 != hdr.outputs_7.prediction8){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_7.prediction6 != hdr.outputs_7.prediction8){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }        
        if(hdr.outputs_7.prediction7 != hdr.outputs_7.prediction8){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }

    }

    action incorrect_inc_8(){
        local_metadata.incorrect_count = 0; 
        if(hdr.outputs_8.prediction1 != hdr.outputs_8.prediction9){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_8.prediction2 != hdr.outputs_8.prediction9){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_8.prediction3 != hdr.outputs_8.prediction9){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_8.prediction4 != hdr.outputs_8.prediction9){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_8.prediction5 != hdr.outputs_8.prediction9){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_8.prediction6 != hdr.outputs_8.prediction9){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }        
        if(hdr.outputs_8.prediction7 != hdr.outputs_8.prediction9){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_8.prediction8 != hdr.outputs_8.prediction9){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
    }

    action incorrect_inc_9(){
        local_metadata.incorrect_count = 0; 
        if(hdr.outputs_9.prediction1 != hdr.outputs_9.prediction10){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_9.prediction2 != hdr.outputs_9.prediction10){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_9.prediction3 != hdr.outputs_9.prediction10){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_9.prediction4 != hdr.outputs_9.prediction10){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_9.prediction5 != hdr.outputs_9.prediction10){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_9.prediction6 != hdr.outputs_9.prediction10){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }        
        if(hdr.outputs_9.prediction7 != hdr.outputs_9.prediction10){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_9.prediction8 != hdr.outputs_9.prediction10){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
        if(hdr.outputs_9.prediction9 != hdr.outputs_9.prediction10){
            local_metadata.incorrect_count = local_metadata.incorrect_count+ 1;
        }
    }

    action copy_predictions_2(){
        local_metadata.prediction1 = hdr.outputs_2.prediction1;
    }
    
    action copy_predictions_3(){
        local_metadata.prediction1 = hdr.outputs_3.prediction1;
        local_metadata.prediction2 = hdr.outputs_3.prediction2;
    }

    action copy_predictions_4(){
        local_metadata.prediction1 = hdr.outputs_4.prediction1;
        local_metadata.prediction2 = hdr.outputs_4.prediction2;
        local_metadata.prediction3 = hdr.outputs_4.prediction3;
    }

    action copy_predictions_5(){
        local_metadata.prediction1 = hdr.outputs_5.prediction1;
        local_metadata.prediction2 = hdr.outputs_5.prediction2;
        local_metadata.prediction3 = hdr.outputs_5.prediction3;
        local_metadata.prediction4 = hdr.outputs_5.prediction4;
    }

    
    action copy_predictions_6(){
        local_metadata.prediction1 = hdr.outputs_6.prediction1;
        local_metadata.prediction2 = hdr.outputs_6.prediction2;
        local_metadata.prediction3 = hdr.outputs_6.prediction3;
        local_metadata.prediction4 = hdr.outputs_6.prediction4;
        local_metadata.prediction5 = hdr.outputs_6.prediction5;
        local_metadata.prediction6 = hdr.outputs_6.prediction6;

    }

    
    action copy_predictions_7(){
        local_metadata.prediction1 = hdr.outputs_7.prediction1;
        local_metadata.prediction2 = hdr.outputs_7.prediction2;
        local_metadata.prediction3 = hdr.outputs_7.prediction3;
        local_metadata.prediction4 = hdr.outputs_7.prediction4;
        local_metadata.prediction5 = hdr.outputs_7.prediction5;
        local_metadata.prediction6 = hdr.outputs_7.prediction6;

    }
 
    action copy_predictions_8(){
        local_metadata.prediction1 = hdr.outputs_8.prediction1;
        local_metadata.prediction2 = hdr.outputs_8.prediction2;
        local_metadata.prediction3 = hdr.outputs_8.prediction3;
        local_metadata.prediction4 = hdr.outputs_8.prediction4;
        local_metadata.prediction5 = hdr.outputs_8.prediction5;
        local_metadata.prediction6 = hdr.outputs_8.prediction6;
        local_metadata.prediction7 = hdr.outputs_8.prediction7;
    }

    action copy_predictions_9(){
        local_metadata.prediction1 = hdr.outputs_9.prediction1;
        local_metadata.prediction2 = hdr.outputs_9.prediction2;
        local_metadata.prediction3 = hdr.outputs_9.prediction3;
        local_metadata.prediction4 = hdr.outputs_9.prediction4;
        local_metadata.prediction5 = hdr.outputs_9.prediction5;
        local_metadata.prediction6 = hdr.outputs_9.prediction6;
        local_metadata.prediction7 = hdr.outputs_9.prediction7;
        local_metadata.prediction8 = hdr.outputs_9.prediction8;
    }

    action increment(){
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
    


    apply{

        read();
        if(hdr.counts.count == 2 && hdr.outputs_2.isValid()){
            hdr.outputs_2.weight2 = temp_val;
            compute_sum_2();
            incorrect_inc_2();
            if(hdr.outputs_2.prediction2 == hdr.outputs_2.prediction3){
                increment();     
            } else {
                decrement_gtz();
            }
            copy_predictions_2();
            if(hdr.outputs_2.ing_port == 2){
                clone_preserving_field_list(CloneType.I2E,2,0);
            }else if (hdr.outputs_2.ing_port == 3){
                clone_preserving_field_list(CloneType.I2E,3,0);
            }
        }else if(hdr.counts.count == 3 && hdr.outputs_3.isValid()){
            hdr.outputs_3.weight3 = temp_val;
            compute_sum_3();
            incorrect_inc_3();
            if(hdr.outputs_3.prediction3 == hdr.outputs_3.prediction4){
                increment(); 
            } else {
                decrement_gtz();
            }
            copy_predictions_3();
            if(hdr.outputs_3.ing_port == 2){
                clone_preserving_field_list(CloneType.I2E,2,0);
            }else if (hdr.outputs_3.ing_port == 3){
                clone_preserving_field_list(CloneType.I2E,3,0);
            }
        }else if(hdr.counts.count == 4 && hdr.outputs_4.isValid()){
            hdr.outputs_4.weight4 = temp_val;
            compute_sum_4();
            incorrect_inc_4();
            if(hdr.outputs_4.prediction4 == hdr.outputs_4.prediction5){
                increment();     
            } else {
                decrement_gtz();
            }
            copy_predictions_4();
            if(hdr.outputs_4.ing_port == 2){
                clone_preserving_field_list(CloneType.I2E,2,0);
            }else if (hdr.outputs_4.ing_port == 3){
                clone_preserving_field_list(CloneType.I2E,3,0);
            }
        }else if(hdr.counts.count == 5 && hdr.outputs_5.isValid()){
            hdr.outputs_5.weight5 = temp_val;
            compute_sum_5();

            incorrect_inc_5();
            if(hdr.outputs_5.prediction5 == hdr.outputs_5.prediction6){
                increment();     
            } else {
                decrement_gtz();
            }
            copy_predictions_5();

            // Debug code 
            // hdr.debug.setValid();
            // hdr.debug.debug_pre_guard = 0xaa;
            // hdr.debug.sum_one_val = sum_one;
            // hdr.debug.sum_zero_val = sum_zero;
            // hdr.debug.incorrect_count_val = (bit<16>)local_metadata.incorrect_count;
            // hdr.debug.temp_val = temp_val;
            // hdr.debug.debug_post_guard = 0xbb;
            if(hdr.outputs_5.ing_port == 2){
                clone_preserving_field_list(CloneType.I2E,2,0);
            }else if (hdr.outputs_5.ing_port == 3){
                clone_preserving_field_list(CloneType.I2E,3,0);
            }
        }else if(hdr.counts.count == 6 && hdr.outputs_6.isValid()){
            hdr.outputs_6.weight6 = temp_val;
            compute_sum_6();
            incorrect_inc_6();
            if(hdr.outputs_6.prediction6 == hdr.outputs_6.prediction7){
                increment();     
            } else {
                decrement_gtz();
            }
            copy_predictions_6();
            if(hdr.outputs_6.ing_port == 2){
                clone_preserving_field_list(CloneType.I2E,2,0);
            }else if (hdr.outputs_6.ing_port == 3){
                clone_preserving_field_list(CloneType.I2E,3,0);
            }
        }else if(hdr.counts.count == 7 && hdr.outputs_7.isValid()){
            hdr.outputs_7.weight7 = temp_val;
            compute_sum_7();
            incorrect_inc_7();
            if(hdr.outputs_7.prediction7 == hdr.outputs_7.prediction8){
                increment();     
            } else {
                decrement_gtz();
            }
            copy_predictions_7();
            if(hdr.outputs_7.ing_port == 2){
                clone_preserving_field_list(CloneType.I2E,2,0);
            }else if (hdr.outputs_7.ing_port == 3){
                clone_preserving_field_list(CloneType.I2E,3,0);
            }
        }else if(hdr.counts.count == 8 && hdr.outputs_8.isValid()){
            hdr.outputs_8.weight8 = temp_val;
            compute_sum_8();
            incorrect_inc_8();
            if(hdr.outputs_8.prediction8 == hdr.outputs_8.prediction9){
                increment();     
            } else {
                decrement_gtz();
            }
            copy_predictions_8();
            if(hdr.outputs_8.ing_port == 2){
                clone_preserving_field_list(CloneType.I2E,2,0);
            }else if (hdr.outputs_8.ing_port == 3){
                clone_preserving_field_list(CloneType.I2E,3,0);
            }
        }else if(hdr.counts.count == 9 && hdr.outputs_9.isValid()){
            hdr.outputs_9.weight9 = temp_val;
            compute_sum_9();
            incorrect_inc_9();
            if(hdr.outputs_9.prediction9 == hdr.outputs_9.prediction10){
                increment();     
            } else {
                decrement_gtz();
            }
            copy_predictions_9();
            if(hdr.outputs_9.ing_port == 2){
                clone_preserving_field_list(CloneType.I2E,2,0);
            }else if (hdr.outputs_9.ing_port == 3){
                clone_preserving_field_list(CloneType.I2E,3,0);
            }
        }

    }
}
#endif // __OUTPUT_COMPUTE
