# Prior to Cribl Installation 

### Architecture 

For this example, this architecture will be a linux host with a Universal Forwarder routing data to Cribl then to Splunk via HEC token. 

### Hardware 

This doc below provides estimating specs. For my instance, I am using 1 core and 2gb RAM. Cribl estimates 1 core can handle up 400GB per day.  

- https://docs.cribl.io/docs/scaling#span-idestimating-requirements-estimating-core-requirements-span 

### Splunk Search Head Configuration 

Create HEC token: 

> Settings > Data Inputs > HTTP Event Collector > Add New 

- Name: Cribl HEC 
- Sourcetype: Automatic 
- App Context: Search & Reporting (or dedicated App) 
- Default index: Create a catchall index for cribl events, the Splunk inputs.conf "index=<index> will still route data to corresponding indexes.  
- Enable the HEC token 
> Settings > Data Inputs > HTTP Event Collector > Global Settings > Enabled 

## Cribl Initial installation 

### Download & Configuration 

```
cd /tmp 
curl -Lso - $(curl -s https://cdn.cribl.io/dl/latest) | tar zxvf -  
sudo mv cribl /opt/ 
sudo adduser cribl 
sudo chown -R cribl: /opt/cribl/ 
sudo su cribl 
$cribl_home/bin/cribl start 
Open browser to <cribl ip|hostname>:9000 
Default creds admin:admin 
```
 

## Configure source and destination routes 

### Splunk UF data source 

Within Cribl 
> Data > Sources > Splunk TCP  

You can created a new type for custom configurations: Specific IPs, TLS, etc. I just used the default 'in_splunk_tcp' to accept all addresses over port 9997 

Splunk HEC Token Endpoint 

### Data Destinations 

Within Cribl: 
>Data > Destinations > Splunk HEC > Add New 
- Output ID: Title of output - 'cribl_hec' 
Splunk HEC Endpoint: If SSL is enabled, endpoint will be: 
`https://<ip|hostname>:8088/services/collector/event` 
HEC Auth Token: HEC Token 
Backpressure Behavior: For this example, block. Recommend looking into a persistent queue to avoid data loss.  
Leave all other settings default 
Open the newly created HEC destination and select Test. Cribl does have dummy data for each test, so select Run Test and validate the test data arrives within Splunk. When successful, move to next step.  
Once configured, go to Data > Destinations > Default, and change the Default Output ID to the Output ID created within the Splunk HEC Destination configuration.  

### Splunk Forwarder Configs 

Whether you're managing forwarders on the hosts themselves or using a deployment server, the primary configuration is the outputs.conf. All traffic will be routed to directly to Cribl instead of routing to an initial Splunk instance. 

- outputs.conf 
```
[tcpout] 
defaultGroup = <cribl_ip> 
[tcpout:cribl_ip] 
server = <cribl_ip>:9997 
```             

### Monitoring Successful Routing to Splunk 

Within Cribl go to the Monitoring tab to view an overall metrics panel, and select sources. "in_splunk_tcp" should show as "live" along the most right column. Select "Live" - this will show real time incoming logs over the last 10 seconds. Select Destinations and view the logs through the same method.  

### Manipulating Data Through Pipelines 

The Pipelines tab allows to add functions to manage raw data. Along the right window pane, select Capture New to preview and sample new incoming logs. If you have a specific set of data you are looking for, select Capture New and adjust the "Filter Expression" to your specific subset. Once captured, the formatted events should appear under the IN selection tab. Now, you can start adding functions to the raw logs. 

Select the function Eval: 

- Filter: True 
- Add field 
- Field Name: Test 
- Field Value: 'successful' (Single quote required) 
- Click Save and the IN selection tab should change to OUT and the Test field should be highlight amongst the raw logs.  
- Take a look at the other functions for manipulating data. For a high volume of lower fidelity alerts, select the Drop function. 
- This method will use the JavaScript search() method to search the raw events for the target pattern. Example for filtering out Successes if we only wanted Error messages: 

`_raw.search(/success/i)>=0`
