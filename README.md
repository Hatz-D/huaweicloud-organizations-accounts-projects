# Huawei-Cloud-List-All-Enterprise-Projects-on-an-Organization
This repository addresses the steps necessary to automatically list all the enterprise projects of the child accounts of an organization on Huawei Cloud using Python HWC SDK

## Context
In Huawei Cloud, it is possible to an organization in order to manage multiple child accounts under the same root account, as shown in the example below:

<img src="">

However, how to list all the enterprise projects of the child accounts automatically? 

## 1. Dependencies
In order to use Huawei Cloud SDK, it is necessary to download the dependencies. More information can be found on the original GitHub repository: <a href="https://github.com/huaweicloud/huaweicloud-sdk-python-v3" GitHub Repository>

## 2. Authentication
In order to delegate access to the Huawei account through the SDK, it is necessary to generate a AK/SK pair on Huawei Cloud console. After that, import the AK/SK as environment variables on the OS running the script, as shown below:
<code>export HUAWEISDK_AK={insert_your_ak_here}</code>
<code>export HUAWEISDK_SK={insert_your_sk_here}</code>

## 3. Configure the agencies file
In order to delegate access permission from one Huawei Cloud account to another, it is possible to create agencies. Create an agency on all child accounts or use an existing agency.

## 4. Run the script
In order to run the script, type <code>python3 script.py agenciesFile</code>
