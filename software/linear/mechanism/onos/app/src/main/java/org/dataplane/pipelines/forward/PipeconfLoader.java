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

import com.google.common.collect.ImmutableList;
import org.onosproject.core.CoreService;
import org.onosproject.net.behaviour.Pipeliner;
import org.onosproject.net.driver.DriverAdminService;
import org.onosproject.net.driver.DriverProvider;
import org.onosproject.net.pi.model.DefaultPiPipeconf;
import org.onosproject.net.pi.model.PiPipeconf;
import org.onosproject.net.pi.model.PiPipeconfId;
import org.onosproject.net.pi.model.PiPipelineInterpreter;
import org.onosproject.net.pi.model.PiPipelineModel;
import org.onosproject.net.pi.service.PiPipeconfService;
import org.onosproject.p4runtime.model.P4InfoParser;
import org.onosproject.p4runtime.model.P4InfoParserException;
import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Deactivate;
import org.osgi.service.component.annotations.Reference;
import org.osgi.service.component.annotations.ReferenceCardinality;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.URL;
import java.util.List;
import java.util.Collection;
import java.util.stream.Collectors;

import javax.swing.DefaultBoundedRangeModel;

import static org.onosproject.net.pi.model.PiPipeconf.ExtensionType.*;

/**
 * Component that produces and registers the basic pipeconfs when loaded.
 */
@Component(immediate = true)
public final class PipeconfLoader {

    private final Logger log = LoggerFactory.getLogger(getClass());
    

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private PiPipeconfService piPipeconfService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private CoreService coreService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private DriverAdminService driverAdminService;

    @Activate
    public void activate() { // register both s1 and s2
        coreService.registerApplication(Constants.APP_NAME);
    

        // Check the sanity of switch configuration related constants.
        // if( Constants.APP_NAMES.length != Constants.BMV2_PIPECONF_IDS.length ||
        //     Constants.APP_NAMES.length != Constants.BMV2_P4INFO_PATHS.length ||
        //     Constants.APP_NAMES.length != Constants.S_JSON_PATHS.length ){
        //     log.info("ERROR: The number of items does not match for switch configurations");
        // }

        // NOTE: Registering test configuration TODO!
        // TO DO Linear properly comment out the next section
        /* ******** TEST configuration load BEGIN ********* */

        // log.info("Registering test config");

        // if (piPipeconfService.getPipeconf(Constants.BMV2_PIPECONF_TEST_IDS).isPresent()) {
        //     piPipeconfService.unregister(Constants.BMV2_PIPECONF_TEST_IDS);
        // }
        
        // removePipeconfDrivers(Constants.BMV2_PIPECONF_TEST_IDS);
        // log.info("Registering {} with {}, {}, and {}",i, Constants.BMV2_P4INFO_PATHS[i],
                // Constants.BMV2_PIPECONF_TEST_IDS, Constants.S_JSON_PATHS[i]);
        // piPipeconfService.register(buildBMV2SwitchPipeconf(
        //         Constants.BMV2_P4INFO_TEST_PATHS,
        //         Constants.BMV2_PIPECONF_TEST_IDS,
        //         Constants.S_JSON_TEST_PATHS,
        //         Constants.BMV2_CPU_PORT_PATH
        // ));
        // log.info("RETURNING and not registering s1 to sx ");
        // return;
        /* ******** TEST configuration load END ********* */

        int numSwitches = Constants.APP_NAMES.length;
        // // int numSwitches = 3;
        log.info("Registering {} switches for onos.",numSwitches);

        // Registers all pipeconf at component activation.
        for(int i = 0; i < numSwitches; i++){
            // PiPipeconfId  PIPECONF_ID = new PiPipeconfId(Constants.BMV2_PIPECONF_IDS[i[]]);
            if (piPipeconfService.getPipeconf(Constants.BMV2_PIPECONF_IDS[i]).isPresent()) {
                piPipeconfService.unregister(Constants.BMV2_PIPECONF_IDS[i]);
            }
            
            removePipeconfDrivers(Constants.BMV2_PIPECONF_IDS[i]);
            log.info("Registering {} with {}, {}, and {}",i, Constants.BMV2_P4INFO_PATHS[i],
                    Constants.BMV2_PIPECONF_IDS[i], Constants.S_JSON_PATHS[i]);
            piPipeconfService.register(buildBMV2SwitchPipeconf(
                    Constants.BMV2_P4INFO_PATHS[i],
                    Constants.BMV2_PIPECONF_IDS[i],
                    Constants.S_JSON_PATHS[i],
                    Constants.BMV2_CPU_PORT_PATH
            ));
        }

        // removePipeconfDrivers(Constants.BMV2_PIPECONF_ID);
        // piPipeconfService.register(buildBmv2Pipeconf());
        // removePipeconfDrivers(Constants.BMV2_PIPECONF_ID2);
        // piPipeconfService.register(buildS2Pipeconf()); // build s2

    }

    @Deactivate
    public void deactivate() {
        for(int i = 0; i < Constants.APP_NAMES.length; i++){
            PiPipeconfId BMV2_PIPECONF_ID = Constants.BMV2_PIPECONF_IDS[i];
            if (piPipeconfService.getPipeconf(BMV2_PIPECONF_ID).isPresent()) {
                piPipeconfService.unregister(BMV2_PIPECONF_ID);
            }
            removePipeconfDrivers(BMV2_PIPECONF_ID);
        }
    }

    private static PiPipeconf buildBMV2SwitchPipeconf(String BMV2_P4INFO_PATH, 
            PiPipeconfId BMV2_PIPECONF_ID, String BMV2_JSON_PATH, String BMV2_CPU_PORT_PATH){
        
        
        final URL p4InfoUrl = PipeconfLoader.class.getResource(BMV2_P4INFO_PATH);
        final PiPipelineModel pipelineModel = parseP4Info(p4InfoUrl);
        
        return DefaultPiPipeconf.builder()
                .withId(BMV2_PIPECONF_ID)
                .withPipelineModel(pipelineModel)
                .addBehaviour(PiPipelineInterpreter.class, InterpreterImpl.class)
                .addBehaviour(Pipeliner.class, PipelinerImpl.class)
                .addExtension(P4_INFO_TEXT, p4InfoUrl)
                .addExtension(BMV2_JSON,
                        PipeconfLoader.class.getResource(BMV2_JSON_PATH))
                .addExtension(CPU_PORT_TXT,
                        PipeconfLoader.class.getResource(BMV2_CPU_PORT_PATH))
                .build();
    }

    // private static PiPipeconf buildBmv2Pipeconf() {
    //     final URL p4InfoUrl = PipeconfLoader.class.getResource(Constants.BMV2_P4INFO_PATH);
    //     final PiPipelineModel pipelineModel = parseP4Info(p4InfoUrl);

    //     return DefaultPiPipeconf.builder()
    //             .withId(Constants.BMV2_PIPECONF_ID)
    //             .withPipelineModel(pipelineModel)
    //             .addBehaviour(PiPipelineInterpreter.class, InterpreterImpl.class)
    //             .addBehaviour(Pipeliner.class, PipelinerImpl.class)
    //             .addExtension(P4_INFO_TEXT, p4InfoUrl)
    //             .addExtension(BMV2_JSON,
    //                     PipeconfLoader.class.getResource(Constants.BMV2_JSON_PATH))
    //             .addExtension(CPU_PORT_TXT,
    //                     PipeconfLoader.class.getResource(Constants.BMV2_CPU_PORT_PATH))
    //             .build();
    // }

    // private static PiPipeconf buildS2Pipeconf(){
    //     final URL p4InfoUrl2 = PipeconfLoader.class.getResource(Constants.S2_P4INFO_PATH);
    //     final PiPipelineModel pipelineModel2 = parseP4Info(p4InfoUrl2);
    //     return DefaultPiPipeconf.builder()
    //             .withId(Constants.BMV2_PIPECONF_ID2)
    //             .withPipelineModel(pipelineModel2)
    //             .addBehaviour(PiPipelineInterpreter.class, InterpreterImpl.class)
    //             .addBehaviour(Pipeliner.class, PipelinerImpl.class)
    //             .addExtension(P4_INFO_TEXT, p4InfoUrl2)
    //             .addExtension(BMV2_JSON,
    //                     PipeconfLoader.class.getResource(Constants.S2_JSON_PATH))
    //             .addExtension(CPU_PORT_TXT,
    //                     PipeconfLoader.class.getResource(Constants.BMV2_CPU_PORT_PATH))
    //             .build();

    // }   

    private static PiPipelineModel parseP4Info(URL p4InfoUrl) {
        try {
            return P4InfoParser.parse(p4InfoUrl);
        } catch (P4InfoParserException e) {
            throw new IllegalStateException(e);
        }
    }

    private void removePipeconfDrivers(PiPipeconfId piPipeconfId) {
        List<DriverProvider> driverProvidersToRemove = driverAdminService
                .getProviders().stream()
                .filter(p -> p.getDrivers().stream()
                        .anyMatch(d -> d.name().endsWith(piPipeconfId.id())))
                .collect(Collectors.toList());

        if (driverProvidersToRemove.isEmpty()) {
            log.info("There are not outdated drivers found for pipeconf {}, nothing to remove.",
                    piPipeconfId);
            return;
        }

        log.info("Found {} outdated drivers for pipeconf '{}', removing...",
                driverProvidersToRemove.size(), piPipeconfId);

        driverProvidersToRemove.forEach(driverAdminService::unregisterProvider);
    }

}
