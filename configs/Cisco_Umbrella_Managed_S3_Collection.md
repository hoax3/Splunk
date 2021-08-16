# Cisco Umbrella Managed S3 Collection - Windows
Playbook for collecting umbrella events from Cisco managed S3. 

### Enable Cisco Managed S3 
- Navigate to Admin > Log Management and select Use a Cisco-managed Amazon S3 bucket. 
- Set 7 days retention, since all logs will be stored in Splunk.
- Store the provided keys, since they will be used later.

### Splunk Prep
**Note:** _Recommended to configure on Heavy Forwarder_
- Install the Cisco Umbrella add-on on the necessary components - Heavy Forwarder and Search Head. 
- https://splunkbase.splunk.com/app/3926/
- Create new folder called *data* in $SPLUNK_HOME/etc/apps/TA_cisco-umbrella/
- Create Cisco Umbrella Index: cisco_umbrella

### Windows Batch setup
- RDP to the Heavy Forwarder and install the AWS CLI msi file:
- Make sure to validate the install was sucessfull `aws --version`
- https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html#cliv2-windows-install
- Create a .bat file in $SPLUNK_HOME/bin/scripts/umbrella_pull.bat
- Edit the bat file and instert the following:
```
aws configure set aws_access_key_id <access_key_id>
aws configure set aws_secret_access_key <secret_access_key>
aws configure set default.region <region> 
aws s3 sync s3://<cisco bucket path> $SPLUNK_HOME/etc/apps/TA_cisco-umbrella/data
```
Validate the batch file works by running as Splunk
`$SPLUNK_HOME/bin/splunk.exe cmd $SPLUNK_HOME/bin/scripts/umbrella_pull.bat`

### Configure Splunk Inputs
Monitoring input
```
[monitor://<splunk_home>/etc/apps/TA_cisco-umbrella/data/]
disabled=0
sourcetype=opendns:dnslogs
index=cisco_umbrella
```
Script Input
```
[script://<splunk_home>/bin/scripts/umbrella_pull.bat]
disabled=0
interval=300
index=_internal
sourcetype=cisco:umbrella:input
```

Validate Logs are being collected into the umbrella index. 
