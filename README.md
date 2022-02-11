# gve_devnet_meraki_vpn_dynamic_assigner
prototype code that leverages Meraki's APIs and site to site VPN features to dynamically assign vpn spoke clients with hub clients that have the lowest load. 


## Contacts
* Jorge Banegas

## Solution Components
* Meraki
* MX

## Installation/Configuration

(optional) This first step is optional if user wants to leverage a virtual environment to install python packages

```shell
pip install virtualenv
virtualenv env
source env/bin/activate
```

Install python dependencies 

```shell
pip install -r requirements.txt
```

Make sure to fill out the variables inside the config.py file. 

Need help generating a Meraki API key ? Visit https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API

To generate the organization id, visit https://developer.cisco.com/meraki/api-v1/#!get-organizations and expand the headers and drop your Meraki API key

Enter what threshold number you would like the script to verify to offload spoke clients from that hub

![/IMAGES/config.png](/IMAGES/config.png)


## Usage

To launch enter command :

    (env) $ python main.py

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
