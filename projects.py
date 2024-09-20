import os
import sys
import json
import requests
import csv

from huaweicloudsdkcore.auth.credentials import GlobalCredentials
from huaweicloudsdkiam.v3 import *
from huaweicloudsdkiam.v3.region.iam_region import IamRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkorganizations.v1 import *
from huaweicloudsdkorganizations.v1.region.organizations_region import OrganizationsRegion


def main(file_path):
    # Initializing the Pandas dataframe with the 'account' and 'project_id' columns

    with open("projects.csv", mode='w', newline='') as df:
        writer = csv.writer(df)
        writer.writerow(["Account", "Project_id"])

    childAccounts = []
    rootAccount = ""

    file = open(file_path, "r")
    agencies_list = file.read().split("\n")

    # Authenticating with Huawei Cloud using the AK/SK configured on the system environment variables
    credentials = GlobalCredentials(os.getenv("HUAWEISDK_AK"), os.getenv("HUAWEISDK_SK"))
    client = IamClient.new_builder().with_credentials(credentials).with_region(IamRegion.value_of("sa-brazil-1")).build()

    # List the organizational root account ID
    try:
        request = KeystoneListAuthDomainsRequest()
        response = client.keystone_list_auth_domains(request)
        rootAccount = json.loads(str(response))["domains"][0]["name"]

    except exceptions.ClientRequestException:
        print("\nError on listing the root account ID!")

    # Creating a client for the Organizations API in order to list all the accounts under the organization
    orgClient = OrganizationsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(OrganizationsRegion.value_of("cn-north-4")) \
        .build()
    
    # List all the accounts under the organization and append them on the 'childAccounts' list
    try:
        request = ListAccountsRequest()
        response = orgClient.list_accounts(request)
        account_list = json.loads(str(response))["accounts"]

        for data in account_list:
            if data["name"] != rootAccount:
                childAccounts.append(data["name"])

    except exceptions.ClientRequestException:
        print("\nError on listing the accounts under the organization!")

    # For each account listed in the API above
    for i in range(len(childAccounts)):
        # For each agency listed in the agencies file
        for j in range(len(agencies_list) -1):
            try:
                # Call an API to create an authentication token for the [i] child account
                request = KeystoneCreateAgencyTokenRequest()
                assumeRoleIdentity = AgencyTokenAssumerole(
                    domain_name=childAccounts[i],
                    agency_name=agencies_list[j]
                )

                listMethodsIdentity = ["assume_role"]
                identityAuth = AgencyTokenIdentity(
                    methods=listMethodsIdentity,
                    assume_role=assumeRoleIdentity
                )

                authbody = AgencyTokenAuth(identity=identityAuth)
                request.body = KeystoneCreateAgencyTokenRequestBody(auth=authbody)
                response = client.keystone_create_agency_token(request)

                # Query through the json response for the authentication token
                auth = json.loads(str(response))["X-Subject-Token"]
            
                # Call the API to list the enterprise projects of the [i] child account 
                headers = {"X-Auth-Token":auth}
                response = requests.get("https://iam.sa-brazil-1.myhuaweicloud.com/v3/projects", headers=headers).json()
           
                projects_list = response["projects"]

                # Append each enterprise project of the [i] child account to the dataframe
                for project in projects_list:
                    with open("projects.csv", mode='a', newline='') as df:
                        writer = csv.writer(df)
                        writer.writerow([childAccounts[i], project["name"]])
                        
                # If the API is successful, skip the remaining agencies provided in the list
                break

            except exceptions.ClientRequestException:
                # If the API call has been unsuccessful to all the agencies in the list
                if j == len(agencies_list)-2:
                    print("Account: {} failed to be accessed by all agencies provided!".format(childAccounts[i]))

    # Save the dataframe to a csv file
    print("\nFile saved successfully! File name: 'projects.csv'")


# Check whether the agency name has been provided as an argument
if len(sys.argv) == 2:
    main(sys.argv[1])

else:
    print("\nPlease input the agencies file path!")
    print("Each line of the file should have exactly one agency.")
