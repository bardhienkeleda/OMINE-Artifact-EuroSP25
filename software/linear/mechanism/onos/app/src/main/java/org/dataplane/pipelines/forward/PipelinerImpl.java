/*
 * Copyright 2018-present Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.dataplane.pipelines.forward;

import org.onosproject.net.PortNumber;
import org.onosproject.net.DeviceId;
import org.onosproject.net.behaviour.NextGroup;
import org.onosproject.net.behaviour.Pipeliner;
import org.onosproject.net.behaviour.PipelinerContext;
import org.onosproject.net.driver.AbstractHandlerBehaviour;
import org.onosproject.net.flow.DefaultFlowRule;
import org.onosproject.net.flow.FlowRule;
import org.onosproject.net.flow.FlowRuleService;
import org.onosproject.net.flowobjective.FilteringObjective;
import org.onosproject.net.flowobjective.ForwardingObjective;
import org.onosproject.net.flowobjective.NextObjective;
import org.onosproject.net.flowobjective.ObjectiveError;
import org.onosproject.net.group.GroupDescription;
import org.onosproject.net.group.GroupService;
import org.dataplane.pipelines.forward.common.Utils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import java.util.Collections;
import java.util.List;


/**
 * Pipeliner implementation for p4 program that maps all forwarding objectives to
 * forward table. All other types of objectives are not supported.
 */
public class PipelinerImpl extends AbstractHandlerBehaviour implements Pipeliner {

    private final Logger log = LoggerFactory.getLogger(getClass());

    private FlowRuleService flowRuleService;
    private GroupService groupService;
    private DeviceId deviceId;

    private static boolean Installed = false;
    
    @Override
    public void init(DeviceId deviceId, PipelinerContext context) {
        this.deviceId = deviceId;
        this.flowRuleService = context.directory().get(FlowRuleService.class);
        this.groupService = context.directory().get(GroupService.class);
    }

    @Override
    public void filter(FilteringObjective obj) {
        obj.context().ifPresent(c -> c.onError(obj, ObjectiveError.UNSUPPORTED));
    }

    @Override
    // Foward is activated multiple times so 
    public void forward(ForwardingObjective obj) {
        if (obj.treatment() == null) {
            obj.context().ifPresent(c -> c.onError(obj, ObjectiveError.UNSUPPORTED));
        }
        

        final FlowRule.Builder ruleBuilder = DefaultFlowRule.builder()
                .forTable(Constants.INGRESS_FORWARD_TABLE)
                .forDevice(deviceId)
                .withSelector(obj.selector())
                .fromApp(obj.appId())
                .withPriority(obj.priority())
                .withTreatment(obj.treatment());

        if (obj.permanent()) {
            ruleBuilder.makePermanent();
        } else {
            ruleBuilder.makeTemporary(obj.timeout());
        }


        // execute only once
        // clone the packets to the backpropagate port 
        if(!Installed && deviceId.toString().equals("device:s5")){ 
            log.info( deviceId.toString());
            final GroupDescription cloneGroup = Utils.buildCloneGroup(
                    obj.appId(),
                    deviceId,
                    Constants.CLONE_SESSION_ID,
                    Collections.singleton(PortNumber.portNumber(
                        Constants.S5_BACK_PROPAGATION_PORT)));
            groupService.addGroup(cloneGroup);
            Installed = true;
        }


        switch (obj.op()) {
            case ADD:
                flowRuleService.applyFlowRules(ruleBuilder.build());
                break;
            case REMOVE:
                flowRuleService.removeFlowRules(ruleBuilder.build());
                break;
            default:
                log.warn("Unknown operation {}", obj.op());
        }

        obj.context().ifPresent(c -> c.onSuccess(obj));
    }

    @Override
    public void next(NextObjective obj) {
        obj.context().ifPresent(c -> c.onError(obj, ObjectiveError.UNSUPPORTED));
    }

    @Override
    public List<String> getNextMappings(NextGroup nextGroup) {
        // We do not use nextObjectives or groups.
        return Collections.emptyList();
    }
}
