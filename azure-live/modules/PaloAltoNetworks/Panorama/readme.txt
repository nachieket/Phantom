####################################
# Panorama Deployment Manual Steps
# before running terraform
####################################

1. Pre-requisites:

    a. Install azure CLI on Mac or Windows
    b. Install Terraform 0.12.13
    c. Create a folder azure-live and download below files from G Drive to it

        interfaces.tf, main.tf, outputs.tf, public_ips.tf, storage_account.tf, vars.tf

2. Execute az login and login to the account to which Panorama needs to be deployed

3. Execute az account list and copy the 'id' parameter which is subscription_id.

4. Manually search Palo Alto Networks Panorama under market place and click on 'Get Started' next to 'Want to deploy programmatically?'

5. Scroll down on left hand pane and switch status to 'enable' next to your subscription id.

6. Use below to get subnet_id of the subnet under which you would like to deploy Panorama

https://docs.microsoft.com/en-us/rest/api/virtualnetwork/subnets/get

The subnet id will look something like below:

/subscriptions/87278e-7f1-454-9c4-4523bfcc3/resourceGroups/PANW/providers/Microsoft.Network/virtualNetworks/Corporate/subnets/default"

7. Execute below to create a role

az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/<subscription-id>"

8. The above command will give you below output.

Use appId under client_id variable in vars.tf file.
Use password under client_secret in vars.tf file.
use tenant under tenant_id in vars.tf file.

{
  "appId": "<id>",
  "displayName": "azure-cli-2020-04-26-13-12-50",
  "name": "http://azure-cli-2020-04-26-13-12-50",
  "password": "<id>",
  "tenant": "<id>"
}

9. Make sure all the variables in vars.tf are replaced as per your requirement.

10. run 'terraform init' to initialize

11. run 'terraform plan' to plan the deployment

12. run 'terraform apply' to deploy Panorama to version 8.1.2
