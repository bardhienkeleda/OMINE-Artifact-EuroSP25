/*****************************************************************************
 *
 *     This file is part of Purdue CS 422.
 *
 *     Purdue CS 422 is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *
 *     Purdue CS 422 is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *
 *     You should have received a copy of the GNU General Public License
 *     along with Purdue CS 422. If not, see <https://www.gnu.org/licenses/>.
 *
 *****************************************************************************/

package org.dataplane.pipelines.forward;

import org.onosproject.net.pi.model.PiPipeconfId;
import org.onosproject.net.pi.model.PiActionId;
import org.onosproject.net.pi.model.PiActionParamId;
import org.onosproject.net.pi.model.PiActionProfileId;
import org.onosproject.net.pi.model.PiMeterId;
import org.onosproject.net.pi.model.PiPacketMetadataId;
import org.onosproject.net.pi.model.PiCounterId;
import org.onosproject.net.pi.model.PiMatchFieldId;
import org.onosproject.net.pi.model.PiTableId;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Constants for pipeline.
 */
public final class Constants {

    // hide default constructor
    private Constants() {
    }

    public static final String APP_NAME = "org.dataplane.pipelines.forward";

    // List of application names
    public static final String[] APP_NAMES = {
                "org.dataplane.pipelines.forward1",
                "org.dataplane.pipelines.forward2",
                "org.dataplane.pipelines.forward3",        
                "org.dataplane.pipelines.forward4",
                "org.dataplane.pipelines.forward5",
                "org.dataplane.pipelines.forward6",
                "org.dataplane.pipelines.forward7",
                "org.dataplane.pipelines.forward8",
                "org.dataplane.pipelines.forward9",
                "org.dataplane.pipelines.forward10",
                "org.dataplane.pipelines.forward11",
                "org.dataplane.pipelines.forward12",
                "org.dataplane.pipelines.forward13",      
                "org.dataplane.pipelines.forward14"             
        };


    public static final String TEST_STRING = "org.dataplane.pipelines.test";

    // Header field IDs
    public static final PiMatchFieldId HDR_HDR_IPV4_PROTOCOL =
            PiMatchFieldId.of("hdr.ipv4.protocol");
    public static final PiMatchFieldId HDR_HDR_IPV4_SRC_ADDR =
            PiMatchFieldId.of("hdr.ipv4.src_addr");
    public static final PiMatchFieldId HDR_HDR_ETHERNET_ETHER_TYPE =
            PiMatchFieldId.of("hdr.ethernet.ether_type");
    public static final PiMatchFieldId HDR_HDR_ETHERNET_SRC_ADDR =
            PiMatchFieldId.of("hdr.ethernet.src_addr");
    public static final PiMatchFieldId HDR_LOCAL_METADATA_L4_DST_PORT =
            PiMatchFieldId.of("local_metadata.l4_dst_port");
    public static final PiMatchFieldId HDR_LOCAL_METADATA_L4_SRC_PORT =
            PiMatchFieldId.of("local_metadata.l4_src_port");
    public static final PiMatchFieldId HDR_STANDARD_METADATA_INGRESS_PORT =
            PiMatchFieldId.of("standard_metadata.ingress_port");
    public static final PiMatchFieldId HDR_HDR_IPV4_DST_ADDR =
            PiMatchFieldId.of("hdr.ipv4.dst_addr");
    public static final PiMatchFieldId HDR_HDR_ETHERNET_DST_ADDR =
            PiMatchFieldId.of("hdr.ethernet.dst_addr");
    // Table IDs
    public static final PiTableId INGRESS_FORWARD_TABLE =
            PiTableId.of("IngressPipeImpl.forward_control.forward_table");
    // Action IDs
    public static final PiActionId INGRESS_DROP =
            PiActionId.of("IngressPipeImpl.forward_control.drop");
    public static final PiActionId NO_ACTION =
            PiActionId.of("NoAction");
    public static final PiActionId INGRESS_SET_OUTPUT_PORT =
            PiActionId.of("IngressPipeImpl.forward_control.set_output_port");
    public static final PiActionId INGRESS_SEND_TO_CPU =
            PiActionId.of("IngressPipeImpl.forward_control.send_to_cpu");
    // Action Param IDs
    public static final PiActionParamId PORT_NUM =
            PiActionParamId.of("port_num");
    // Packet Metadata IDs
    public static final PiPacketMetadataId INGRESS_PORT =
            PiPacketMetadataId.of("ingress_port");
    public static final PiPacketMetadataId EGRESS_PORT =
            PiPacketMetadataId.of("egress_port");

    // Switch-specific settings
    // Generic CPU PORT FILE (CPU PORT: 255)
    public static final String BMV2_CPU_PORT_PATH = "/bmv2/cpu_port.txt";

    public static final PiPipeconfId[] BMV2_PIPECONF_IDS = {
                new PiPipeconfId(APP_NAMES[0] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[1] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[2] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[3] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[4] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[5] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[6] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[7] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[8] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[9] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[10] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[11] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[12] + ".bmv2"),
                new PiPipeconfId(APP_NAMES[13] + ".bmv2")
    };

    public static final PiPipeconfId BMV2_PIPECONF_TEST_IDS = new PiPipeconfId(TEST_STRING + ".bmv2");
    public static final String BMV2_P4INFO_TEST_PATHS = "/bmv2/test/p4info.txt";
    public static final String S_JSON_TEST_PATHS = "/bmv2/test/bmv2.json";



    public static final String[] BMV2_P4INFO_PATHS = {
                "/bmv2/s1/p4info.txt", "/bmv2/s2/p4info.txt",
                "/bmv2/s3/p4info.txt", "/bmv2/s4/p4info.txt",
                "/bmv2/s5/p4info.txt", "/bmv2/s6/p4info.txt",
                "/bmv2/s7/p4info.txt", "/bmv2/s8/p4info.txt",
                "/bmv2/s9/p4info.txt", "/bmv2/s10/p4info.txt",
                "/bmv2/s11/p4info.txt","/bmv2/s12/p4info.txt",
                "/bmv2/s13/p4info.txt","/bmv2/s14/p4info.txt"
    };

    public static final String[] S_JSON_PATHS = {
                "/bmv2/s1/bmv2.json", "/bmv2/s2/bmv2.json",
                "/bmv2/s3/bmv2.json", "/bmv2/s4/bmv2.json",
                "/bmv2/s5/bmv2.json", "/bmv2/s6/bmv2.json",
                "/bmv2/s7/bmv2.json", "/bmv2/s8/bmv2.json",
                "/bmv2/s9/bmv2.json", "/bmv2/s10/bmv2.json",
                "/bmv2/s11/bmv2.json","/bmv2/s12/bmv2.json",
                "/bmv2/s13/bmv2.json","/bmv2/s14/bmv2.json"
        };


    public static final int DEFAULT_FLOW_RULE_PRIORITY = 10;

    public static final int ING2_CLONE_SESSION_ID = 2;
    public static final int ING3_CLONE_SESSION_ID = 3;
    public static final int BMV2_CPU_PORT = 255;
    public static final int ING2_BACK_PROPAGATION_PORT = 2;
    public static final int ING3_BACK_PROPAGATION_PORT = 3;
}
