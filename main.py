#
# Author: Ualter Azambuja Junior
# ualter.junior@gmail.com
#
#
# pip install pyyaml
# https://pyyaml.org/wiki/PyYAMLDocumentation
# https://jgraph.github.io/drawio-tools/tools/csv.html
#
#

import os
import yaml
import json
import logging
import sys

FILL={}
FILL["stage"]="#f5f5f5"
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
IMAGE["stage"]="https://www.dropbox.com/s/ddf9xfjvete6xmv/stage-logo.png?raw=1"
IMAGE["job"]="https://www.dropbox.com/s/xinbwsjsh0ezi8n/job-logo.png?raw=1"
IMAGE["terraform"]="https://www.dropbox.com/s/ngptqgmji59j3h7/terraform-logo-1.png?raw=1"
IMAGE["branch"]="https://www.dropbox.com/s/vf0nzuvj8lr61u2/gitbranch-logo.png?raw=1"
IMAGE["ansible"]="https://www.dropbox.com/s/louj6pc6a3xb4gi/ansible-logo-1.png?raw=1"
IMAGE["manual"]="https://www.dropbox.com/s/gjw7xqd7de23wmp/manual-logo.png?raw=1"

PLAYBOOKS={}
PLAYBOOKS["make -e run_playbook_repository"]="deploy-repository.yaml"
PLAYBOOKS["make -e run_playbook_efs"]       ="deploy-efs.yaml"
PLAYBOOKS["make -e run_playbook_services"]  ="deploy-services.yaml"

HEADER="id,name,type,stage,when,terraform,branch,ansible,fill,stroke,image"


def main():
    if len(sys.argv) < 2 :
         print ("  ")
         print ("Missing argument! Check:")
         print ("Syntax: py-analyzer.py [Gitlab CI yaml file]")
         print ("  ")
         print ("  Example:")
         print ("    py-analyzer.py .gitlab-ci.yaml")
         print (" ")
         sys.exit()
    else:
         gitlabFile = sys.argv[1]     
            
    print("\n*********************************************************")
    loadYaml(gitlabFile)
    print("*********************************************************\n")


def loadYaml(gitlabFile):
    print("- Loading and Parsing " + gitlabFile)   
    with open(gitlabFile, 'r') as file:
        documents = yaml.load(file, Loader=yaml.FullLoader)

        drawio={}
        index=0

        for item, doc in documents.items() :
            if item == "stages" :
               loadStages(drawio, doc)

            elif isinstance(doc,dict):
                index += 1
                id_job = item + "-" + str(index) 
                drawio[id_job] = {}
                drawio[id_job]["id"]=id_job
                drawio[id_job]["name"]=item
                drawio[id_job]["type"]="job"
                drawio[id_job]["stage"]=drawio[doc["stage"]]["name"]
                if  'when' in doc:
                    drawio[id_job]["when"]=doc["when"]
                else:    
                    drawio[id_job]["when"]=""

                print("  - Parsing Job " + id_job + " (Stage " + drawio[id_job]["stage"] + ")")

                # Terraform Commands
                loadTerraformCommands(id_job, drawio, item, doc)

                # Git Branches Applied
                loadGitBranches(id_job, drawio, item, doc)

                # Ansible
                loadAnsible(id_job, drawio, item, doc)

        completeWihRelationShips(drawio)
        writeFile(drawio, gitlabFile)

def loadStages(drawio, doc):
      for stage in doc:
         print("  - Parsing Stage " + stage)
         drawio[stage]={}
         drawio[stage]["id"]=stage
         drawio[stage]["name"]=stage
         drawio[stage]["type"]="stage"
         drawio[stage]["stage"]=""
         drawio[stage]["when"]=""
         drawio[stage]["terraform"]=""
         drawio[stage]["branch"]=""
         drawio[stage]["ansible"]=""

def loadTerraformCommands(id_job, drawio, item, doc):
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
      drawio[id_job]["terraform"]=terraformCommands        

def loadGitBranches(id_job, drawio, item, doc):
      branches=""
      script = doc["only"]
      for lineBranch in script:
         if len(branches) > 0:
            branches=branches+","
         branches = branches + lineBranch
      drawio[id_job]["branch"]=branches

def loadAnsible(id_job, drawio, item, doc):
      playbooks=""
      script = doc["script"]
      for lineScript in script:
         for playbook in PLAYBOOKS:
            if playbook in lineScript:
               if len(playbooks) > 0:
                  playbooks=playbooks+","
               playbooks = playbooks + PLAYBOOKS[playbook]
      drawio[id_job]["ansible"]=playbooks

def completeWihRelationShips(drawio):
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
            drawio[terra]["id"]=terra
            drawio[terra]["name"]=terra
            drawio[terra]["type"]="terraform"
            drawio[terra]["stage"]=""
            drawio[terra]["when"]=""
            drawio[terra]["terraform"]=""
            drawio[terra]["branch"]=""
            drawio[terra]["ansible"]=""

      for git in listGitBranches:
         drawio[git]={}
         drawio[git]["id"]=git
         drawio[git]["name"]=git
         drawio[git]["type"]="branch"
         drawio[git]["stage"]=""
         drawio[git]["when"]=""
         drawio[git]["terraform"]=""
         drawio[git]["branch"]=""
         drawio[git]["ansible"]=""

      for ansible in listAnsiblePlaybook:
         drawio[ansible]={}
         drawio[ansible]["id"]=ansible
         drawio[ansible]["name"]=ansible
         drawio[ansible]["type"]="ansible"
         drawio[ansible]["stage"]=""
         drawio[ansible]["when"]=""
         drawio[ansible]["terraform"]=""
         drawio[ansible]["branch"]=""
         drawio[ansible]["ansible"]=""


def writeFile(drawio, gitlabFile):
   print("- CVS Writing...")
   fileName=gitlabFile.replace(".yaml","").replace(".yml","") + ".csv"
   fileNameNoLayout=gitlabFile.replace(".yaml","").replace(".yml","")+"-nolayout.csv"

   if os.path.exists(fileName):
      os.remove(fileName)
   if os.path.exists(fileNameNoLayout):
      os.remove(fileNameNoLayout)   

   f   = open(fileName, "w")
   fnl = open(fileNameNoLayout, "w")
   writeLayoutHeader(f)
   f.write(HEADER + "\n")
   fnl.write(HEADER + "\n")

   for name in drawio:
       line = composeLine(name, drawio)
       f.write(line + "\n")
       fnl.write(line + "\n")

   f.close()
   print("- CVS File writen")

def composeLine(name, drawio):
    fill   = FILL  [drawio[name]["type"]]
    stroke = STROKE[drawio[name]["type"]]
    image  = IMAGE [drawio[name]["type"]]

    if drawio[name]["when"] == "manual":
       image = IMAGE["manual"]

    line =       drawio[name]["id"] + \
         ","   + drawio[name]["name"] + \
         ","   + drawio[name]["type"] + \
         ","   + drawio[name]["stage"] + \
         ","   + drawio[name]["when"] + \
         ",\"" + drawio[name]["terraform"] + "\"" + \
         ",\"" + drawio[name]["branch"]    + "\"" + \
         ","   + drawio[name]["ansible"] + \
         ","   + fill + \
         ","   + stroke + \
         ","   + image
    return line

def writeLayoutHeader(f):
   with open('layout.py') as layout:
    for line in layout:
       f.write("#"+line)

def loadLayoutHeader():
   with open('layout.py') as f:
        my_list = list(f)
   return my_list    

if __name__ == '__main__':    main()