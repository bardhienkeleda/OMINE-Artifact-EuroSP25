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

#ifndef __CHECKSUM__
#define __CHECKSUM__

control VerifyChecksumImpl(inout parsed_headers_t hdr,
                           inout local_metadata_t meta)
{
    apply {}
}

control ComputeChecksumImpl(inout parsed_headers_t hdr,
                            inout local_metadata_t meta) {
    apply {
        update_checksum(hdr.ipv4.isValid(),
                {
                    hdr.ipv4.version,
                    hdr.ipv4.ihl,
                    hdr.ipv4.dscp,
                    hdr.ipv4.ecn,
                    hdr.ipv4.total_len,
                    hdr.ipv4.identification,
                    hdr.ipv4.flags,
                    hdr.ipv4.frag_offset,
                    hdr.ipv4.ttl,
                    hdr.ipv4.protocol,
                    hdr.ipv4.src_addr,
                    hdr.ipv4.dst_addr
                },
                hdr.ipv4.hdr_checksum,
                HashAlgorithm.csum16
        );
    }
}

#endif
