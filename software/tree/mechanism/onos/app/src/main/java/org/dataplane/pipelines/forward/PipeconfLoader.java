//*************************************************************************
//
// Copyright 2025 Enkeleda Bardhi (TU Delft),
//                Chenxing Ji (TU Delft),
//                Ali Imran (Purdue University),
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

        int numSwitches = Constants.APP_NAMES.length;
        log.info("Registering {} switches for onos.",numSwitches);

        // Registers all pipeconf at component activation.
        for(int i = 0; i < numSwitches; i++){
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

    }

    @Deactivate
    public void deactivate() {
        log.info("Registering deactivate.");
        for(int i = 0; i < Constants.APP_NAMES.length; i++){
            PiPipeconfId BMV2_PIPECONF_ID = Constants.BMV2_PIPECONF_IDS[i];
            if (piPipeconfService.getPipeconf(BMV2_PIPECONF_ID).isPresent()) {
                piPipeconfService.unregister(BMV2_PIPECONF_ID);
            }
            removePipeconfDrivers(BMV2_PIPECONF_ID);
        }
        log.info("Deactivate completed.");

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
