# Linux Installation Playbook – SUSE Linux

## Splunk Search Head Prep

- Create an index for linux events (if not created already)

> Splunk Cloud SH > Settings > Indexes > Add > index Name – ex: linux

- Install the Splunk Linux Add-on https://splunkbase.splunk.com/app/833/

## Splunk Deployment Server Prep

- Create a Server Class for Linux hosts (if not created already)

> Deployment Server > Settings > Forwarder Management > Server Classes > Add

- Install the Splunk Linux Add-on to the Deployment Server and move the Add-on to the deployment-apps directory

`cp -r /opt/splunk/etc/apps/Splunk_TA_nix/ /opt/splunk/etc/deployment-apps/`

- Validate the app appears as a deployable app in the Deployment Server

> Deployment Server > Settings > Forwarder Management > Apps

- Within the Splunk Linux Add-on, create a local directory and add the inputs.conf file.

`mkdir /opt/splunk/etc/deployment-apps/Splunk_TA_nix/local/ && vi /opt/splunk/etc/deployment-apps/Splunk_TA_nix/local/inputs.conf`

- Enter monitoring Stanzas, the Splunk_TA_nix default/inputs.conf contains example monitoring inputs. For basic security monitoring, reference the input stanza below:

```
[monitoring:///var/log/audit]
disabled=false
index=linux
sourcetype=linux_audit
```

- Save the File and Add the App to the Linux Server Class

> Deployment Server > Settings > Forwarder Management > Server Classes > Add Apps > Make sure to set the App action to restart Splunkd

## Linux Host Prep as Deployment Client

- Download Splunk Universal Forwarder – Select the .rpm file for SUSE https://www.splunk.com/en_us/download/universal-forwarder.html

- On the SUSE host, the following command will install the Splunk Universal Forwarder Service to the path /opt/splunkforwarder.

`rpm install splunk-forwarder-<…>.rpm`

- Once installed, start the Splunk service, agree to the license, and create a user and password to run the Splunk service (prompted).

`/opt/splunkforwarder/bin/splunk start`

- Set the deployment client configuration file https://docs.splunk.com/Documentation/Splunk/8.2.1/Admin/Deploymentclientconf

`vi /opt/splunk/etc/system/local/deploymentclient.conf`

- Enter the following and edit the targetUri as the deployment server IP/FQDN and set the port to 8089.

```
[deployment-client]
# 10 minutes
# phoneHomeIntervalInSecs = 600

[target-broker:deploymentServer]
# Change the targetUri
targetUri = deploymentserver.splunk.mycompany.com:8089
```
- Validate the host appears as a client within the Forwarder Management page on the DS

> Deployment Server > Settings > Forwarder Management > Clients 
