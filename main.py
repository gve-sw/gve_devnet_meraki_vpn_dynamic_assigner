""" Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

import meraki 
import config
import helper_functions as hf


dashboard = meraki.DashboardAPI(api_key=config.api_key,output_log=False)

# query list of all vpn connections available for the pertaining organization
vpns = dashboard.appliance.getOrganizationApplianceVpnStatuses(organizationId=config.organization_id)

hubs = []
spokes = []

# seperating hub/spoke client into two different lists while querying the utilization score for each hub client
for vpn in vpns:
    if vpn['vpnMode'] == 'hub':
        utilization_score = dashboard.appliance.getDeviceAppliancePerformance(serial=vpn['deviceSerial'])
        vpn['utilization_score'] = utilization_score['perfScore']
        hubs.append(vpn)
    if vpn['vpnMode'] == 'spoke':
        spokes.append(vpn)

# iterate through each hub and verify if threshold has been met to offload the hub from spoke clients
for hub in hubs:
    if hub['utilization_score'] >= config.treshold_score:
            hf.change_hub(peers=hub['merakiVpnPeers'],hubs=hubs,hub=hub,spokes=spokes)