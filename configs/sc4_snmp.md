# Splunk Connect for SNMP - Work in progress
Configuration for connector for SNMP.
Working versions for Centos 7, Ubuntu 20.04

## Architecture 
* Dedicated server/s for Microk8s service. (3 Nodes for cluster)
* Recommend 16 Core/32 Threads with 12Gb RAM
* 100 Gb Root directory storage

## Splunk Prep
* On-prem Splunk instances, install the Splunk App for Infrastructure: https://splunkbase.splunk.com/app/3975/
* Create the following indexes
  * em_metrics (metrics type)
  * em_meta (events type)
  * em_logs (events type)
* Create a HEC Token
  * Splunk Settings > Data Inputs > HTTP Event Collector Add New > Provide HEC Token Name > Next 
    * Source type : Automatic
    * Index : Empty
    * Default Index: Default > Review > Submit
  * Test HEC token

```
curl -k https://<splunk-IP>|FQDN:8088/services/collector/event \
     -H "Authorization: Splunk <TOKEN>" \ 
     -d '{"event": "HEC Token Works"}'
```
 
The snapd module is a required for installing microk8s. For Centos/RHEL, view the following [guide](https://snapcraft.io/docs/installing-snap-on-centos) for installing snapd.

 `sudo snap install microk8s --classic --channel=1.21`
