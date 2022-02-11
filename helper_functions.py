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

import config
import meraki

dashboard = meraki.DashboardAPI(api_key=config.api_key,output_log=False)

def change_hub(peers,hubs,hub,spokes):
    hubs = hubs
    peers=peers

    # sort hubs based on utilization score - least to greatest 
    hubs.sort(key = lambda x:x['utilization_score'])

    # select the first hub from the list - hub with the least utilization score
    selected_hub = hubs[0]
    peer_list = []

    for peer in peers:
        peer_list.append(peer['networkId'])

    # verify if the selected hub is a peer to the hub client that requires offloading
    if selected_hub['networkId'] in peer_list:
        for spoke in spokes:
            
            # verify if network tag contains templated_networks_tag to verify if network is bounded to a template
            if config.templated_networks_tag in dashboard.networks.getNetwork(spoke['networkId'])['tags']:

                # case where network is bounded to a template 
                network_appliance_vlans = dashboard.appliance.getNetworkApplianceVlans(networkId=spoke['networkId'])
                get_site_to_site = dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(networkId=spoke['networkId'])
                subnets = get_site_to_site['subnets']
                unbind = dashboard.networks.unbindNetwork(networkId=spoke['networkId'])

                body = network_appliance_vlans[0]

                vlan_id_template = body['id']

                vlans = dashboard.appliance.getNetworkApplianceVlans(networkId=spoke['networkId'])

                vlan_ids = []

                for vlan in vlans:
                    vlan_ids.append(vlan['id'])

                if vlan_id_template in vlan_ids:
                    resp = dashboard.appliance.updateNetworkApplianceVlan(networkId=spoke['networkId'],name=body['name'],vlanId=vlan_id_template,subnet=body['subnet'],applianceIp=body['applianceIp'])
                else:
                    resp = dashboard.appliance.createNetworkApplianceVlan(networkId=spoke['networkId'],name=body['name'],id=body['id'],subnet=body['subnet'],applianceIp=body['applianceIp'])

                update_site_to_site = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(networkId=spoke['networkId'],mode='spoke',subnets=subnets,hubs=[{'hubId':selected_hub['networkId'],'useDefaultRoute': 'true'}])
            else:

                # case where network is not bounded to a template
                get_site_to_site = dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(networkId=spoke['networkId'])
                subnets = get_site_to_site["subnets"]
                update_site_to_site = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(networkId=spoke['networkId'],mode='spoke',subnets=subnets,hubs=[{"hubId":selected_hub['networkId'],"useDefaultRoute": "true"}])

            