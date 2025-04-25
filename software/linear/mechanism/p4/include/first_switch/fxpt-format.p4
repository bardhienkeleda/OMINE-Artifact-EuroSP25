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
#ifndef __FXPT_FORMAT__
#define __FXPT_FORMAT__

#include "first_switch_headers.p4"
#include "../defines.p4"

control fxpt_format_control(inout parsed_headers_t hdr,
                            inout local_metadata_t local_metadata,
                            inout standard_metadata_t standard_metadata) {

    action shift_fields() {
        hdr.ml_fields.field0 = hdr.ml_fields.field0 << 16;
        hdr.ml_fields.field1 = hdr.ml_fields.field1 << 16;
        hdr.ml_fields.field2 = hdr.ml_fields.field2 << 16;
        hdr.ml_fields.field3 = hdr.ml_fields.field3 << 16;
        hdr.ml_fields.field4 = hdr.ml_fields.field4 << 16;
        hdr.ml_fields.field5 = hdr.ml_fields.field5 << 16;
        hdr.ml_fields.field6 = hdr.ml_fields.field6 << 16;
    }

    table fxpt_format_table {
        key = {
            local_metadata.ip_proto: ternary;
            standard_metadata.egress_port: ternary;
        }
        actions = {
            shift_fields;
        }
    }

    apply {
        fxpt_format_table.apply();
    }
}

#endif
