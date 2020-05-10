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

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

def main():
    rootLogger = logging.getLogger()
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

    fileHandler = logging.FileHandler("{0}/{1}.log".format("./log", "py-analyzer"))
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.INFO)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    rootLogger.addHandler(consoleHandler)

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