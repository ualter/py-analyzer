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
import gitlab as gitlab


def main():
    if len(sys.argv) < 3 :
         print (" ")
         print ("Missing argument!")
         print (" ")
         print ("Check:")
         print (" Syntax: python py-analyzer.py -gitlab [Gitlab CI yaml file]")
         print ("  ")
         print (" Example:")
         print ("    python py-analyzer.py -gitlab .gitlab-ci.yaml")
         print (" ")
         sys.exit()
    else:
         type = sys.argv[1]
         file = sys.argv[2]     
            
    if type == "-gitlab":        
       gitlab.startAnalysis(file)
    else:
       print (" ")
       print(" Type " + type + "not expected!")  
       print (" ") 


if __name__ == '__main__':    main()