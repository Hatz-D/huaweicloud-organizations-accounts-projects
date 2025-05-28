# huaweicloud-organizations-accounts-projects
This repository addresses the steps necessary to automatically list all the Project IDs of the child accounts of an organization on Huawei Cloud using Python HWC SDK

## Context
In Huawei Cloud, it is possible to create an organization in order to manage multiple child accounts under the same root account for governance purposes, as shown in the example below:

<img src="https://github.com/user-attachments/assets/3754ec47-c92c-41b0-8307-2f502f0a16fc" width=400>

<p>However, how to list all the Project IDs of the child accounts automatically?</p>

## 1. Dependencies
In order to use Huawei Cloud SDK, it is first necessary to download the dependencies. More information can be found on the original GitHub repository: <a href="https://github.com/huaweicloud/huaweicloud-sdk-python-v3">SDK Repo</a>. Besides that, it is also necessary to install <a href="https://pypi.org/project/requests/">Requests</a>.

## 2. Authentication
In order to delegate access to the Huawei account through the SDK, it is necessary to generate a AK/SK pair on Huawei Cloud console. After that, import the AK/SK as environment variables on the OS running the script, as shown below:
<p><code>export HUAWEISDK_AK={insert_your_ak_here}</code></p>
<p><code>export HUAWEISDK_SK={insert_your_sk_here}</code></p>

## 3. Configure the agencies file
In order to delegate access permission from one Huawei Cloud account to another, it is necessary to create agencies. Create an agency on all child accounts or use an existing agency that the organization management account have permissions over. After that, edit the <code>agenciesList</code> file to add the name of all the agencies created on the child accounts.

## 4. Run the script
In order to run the script, type <code>python3 projects.py agenciesList</code>. A CSV file called <code>projects.csv</code> will be generated containing all of the Project IDs of the child accounts.
