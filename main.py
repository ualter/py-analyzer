#
# Author: Ualter Azambuja Junior
# ualter.junior@gmail.com
#
#
# pip install pyyaml
# https://pyyaml.org/wiki/PyYAMLDocumentation
#
#

import yaml
import json


FILL={}
FILL["stage"]="#dae9fc"
FILL["job"]="#dae8fc"
FILL["terraform"]="#99ffcc"
FILL["branch"]="#d5e8d4"
FILL["ansible"]="#f8cecc"

STROKE={}
STROKE["stage"]="#6c9ebf"
STROKE["job"]="#6c8ebf"
STROKE["terraform"]="#82b366"
STROKE["branch"]="#82b366"
STROKE["ansible"]="#82b366"

IMAGE={}
IMAGE["stage"]=""
IMAGE["job"]="https://www.dropbox.com/s/xinbwsjsh0ezi8n/job-logo.png?raw=1"
IMAGE["terraform"]="https://www.dropbox.com/s/ngptqgmji59j3h7/terraform-logo-1.png?raw=1"
IMAGE["branch"]="https://www.dropbox.com/s/vf0nzuvj8lr61u2/gitbranch-logo.png?raw=1"
IMAGE["ansible"]="https://www.dropbox.com/s/louj6pc6a3xb4gi/ansible-logo-1.png?raw=1"

PLAYBOOKS={}
PLAYBOOKS["make -e run_playbook_repository"]="deploy-repository.yaml"
PLAYBOOKS["make -e run_playbook_efs"]       ="deploy-efs.yaml"
PLAYBOOKS["make -e run_playbook_services"]  ="deploy-services.yaml"

def main():
    loadYaml()


def loadYaml():   
    #with open(".gitlab-ci.yml", 'r') as stream:
    #    try:
    #        print(yaml.safe_load(stream))
    #    except yaml.YAMLError as exc:
    #        print(exc)

    # mydict={}

    with open(".gitlab-ci.yml", 'r') as file:
        documents = yaml.full_load(file)

        drawio={}

        for item, doc in documents.items() :
            if item == "stages" :
               loadStages(drawio, doc)
               #for stage in doc:
               #    drawio[stage]={}
               #    drawio[stage]["name"]=stage
               #    drawio[stage]["type"]="stage"
               #    drawio[stage]["stage"]=""
               #    drawio[stage]["terraform"]=""
               #    drawio[stage]["branch"]=""
               #    drawio[stage]["ansible"]=""
                   
            elif  item == "image" :
                  s = ""
                  #print(item + ": " + doc)         

            elif isinstance(doc,dict):
                drawio[item] = {}
                drawio[item]["name"]=item
                drawio[item]["type"]="job"
                drawio[item]["stage"]=drawio[doc["stage"]]["name"]

                # Terraform Commands
                terraformCommands=""
                script = doc["script"]
                for lineScript in script:
                    if    "make -e init" in lineScript:
                          if len(terraformCommands) > 0:
                             terraformCommands=terraformCommands+","
                          terraformCommands = terraformCommands + "init"
                    elif "make -e plan" in lineScript:     
                          if len(terraformCommands) > 0:
                             terraformCommands=terraformCommands+","  
                          terraformCommands = terraformCommands + "plan"
                    elif "make -e apply" in lineScript:      
                          if len(terraformCommands) > 0:
                             terraformCommands=terraformCommands+","
                          terraformCommands = terraformCommands + "apply"
                    elif "make -e destroy" in lineScript:      
                          if len(terraformCommands) > 0:
                             terraformCommands=terraformCommands+","
                          terraformCommands = terraformCommands + "destroy"            
                drawio[item]["terraform"]=terraformCommands

                # Git Branches Applied
                branches=""
                script = doc["only"]
                for lineBranch in script:
                    if len(branches) > 0:
                        branches=branches+","
                    branches = branches + lineBranch
                drawio[item]["branch"]=branches

                # Ansible
                playbooks=""
                script = doc["script"]
                for lineScript in script:
                    for playbook in PLAYBOOKS:
                        if playbook in lineScript:
                          if len(playbooks) > 0:
                             playbooks=playbooks+","
                          playbooks = playbooks + PLAYBOOKS[playbook]
                drawio[item]["ansible"]=playbooks

        # Inserting the others in order the relationship works
        listTerraformCommands=[]
        listGitBranches=[]
        listAnsiblePlaybook=[]
        for name in drawio:

            for str in drawio[name]["terraform"].split(","):
                if str != "":
                   listTerraformCommands.append(str)

            for str in drawio[name]["branch"].split(","):
                if str != "":
                   listGitBranches.append(str)

            for str in drawio[name]["ansible"].split(","):
                if str != "":
                   listAnsiblePlaybook.append(str)              

        listTerraformCommands = list(dict.fromkeys(listTerraformCommands))
        listGitBranches       = list(dict.fromkeys(listGitBranches))
        listAnsiblePlaybook   = list(dict.fromkeys(listAnsiblePlaybook))

        for terra in listTerraformCommands:
            drawio[terra]={}
            drawio[terra]["name"]=terra
            drawio[terra]["type"]="terraform"
            drawio[terra]["stage"]=""
            drawio[terra]["terraform"]=""
            drawio[terra]["branch"]=""
            drawio[terra]["ansible"]=""

        for git in listGitBranches:
            drawio[git]={}
            drawio[git]["name"]=git
            drawio[git]["type"]="branch"
            drawio[git]["stage"]=""
            drawio[git]["terraform"]=""
            drawio[git]["branch"]=""
            drawio[git]["ansible"]=""

        for ansible in listAnsiblePlaybook:
            drawio[ansible]={}
            drawio[ansible]["name"]=ansible
            drawio[ansible]["type"]="ansible"
            drawio[ansible]["stage"]=""
            drawio[ansible]["terraform"]=""
            drawio[ansible]["branch"]=""
            drawio[ansible]["ansible"]=""    

        writeFile(drawio)   


def loadStages(drawio, doc):
    for stage in doc:
        drawio[stage]={}
        drawio[stage]["name"]=stage
        drawio[stage]["type"]="stage"
        drawio[stage]["stage"]=""
        drawio[stage]["terraform"]=""
        drawio[stage]["branch"]=""
        drawio[stage]["ansible"]=""

def writeFile(drawio):

   header="name,type,stage,terraform,branch,ansible,fill,stroke,image"
   f = open("gitlab-ci.csv", "w")
   f.write(header + "\n")

   for name in drawio:
       fill=FILL[drawio[name]["type"]]
       stroke=STROKE[drawio[name]["type"]]
       image=IMAGE[drawio[name]["type"]]

       line =       drawio[name]["name"] + \
              "," + drawio[name]["type"] + \
              "," + drawio[name]["stage"] + \
              ",\"" + drawio[name]["terraform"] + "\"" + \
              ",\"" + drawio[name]["branch"]    + "\"" + \
              "," + drawio[name]["ansible"] + \
              "," + fill + \
              "," + stroke + \
              "," + image

       print(line)
       f.write(line + "\n")

   f.close()
       


if __name__ == '__main__':    main()