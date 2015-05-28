#!/usr/bin/python

import pdb
import logging
import re
import sys
import time
import datetime
import csv
import itertools
import json



def runFile():
  # Open the CSV
  f = open( sys.argv[1], 'rU' )
  outputfile = sys.argv[2]
  #mfilter = sys.argv[3]

  try:
    mintime = sys.argv[4]
    maxtime = sys.argv[5]
  except:
    mintime = 0
    maxtime = 1462365131

  limit = 2
  totaldict = dict()

  # TS: 20-05-2015 20:10:00
  #output['unixtime']=int(time.mktime(time.strptime(rowdict['Poll_Time'], "%d/%m/%Y %H:%M:%S")))

  letters=['a', 'c', 'b', 'e', 'd', 'g', 'f', 'i', 'h', 'k', 'j', 'm', 'l', 'o', 'n', 'q', 'p', 's', 'r', 't','u','v','x','A','B','C']
  tags= ['PowerState','Guest','NumCpu','MemoryGB','HardDisks','NetworkAdapters','Host','VMHost','ResourcePoolId','ResourcePool','PersistentId','UsedSpaceGB','ProvisionedSpaceGB','DatastoreIdList','Name','Id']

  lines=f.readlines()
  count1 = 0
  count2 = 0
  prevkey = ""
  output = {}
  collection = []
  vmcollection = []
  vmMap = {}
  newlist = []
  vmdata = {}
  allvms = {}
  first = 1
  veryfirst = 1
  lastrun = 0
  change = 0
  keyname = "aa"

  for line in lines:
    logging.debug("------------------")
    logging.debug("\n")
    m = re.match('^[A-Z]', line)
    if line[0] == "d":
      if first == 1 and veryfirst == 0:
        #pdb.set_trace()
        vmcollection.append(vmMap)
        vmMap = {}
        first = 0

      #pdb.set_trace()
      splitLine=line.split(' ')
      newlist=filter(lambda x: len(x)>0, splitLine)
      ts = newlist[1] + " " + newlist[2]

      try:
        tmptime=int(time.mktime(time.strptime(ts, "%d-%m-%Y %H:%M:%S")))
        logging.debug(str(tmptime) + "\n")
      except:
        logging.debug("error on polltime")
        continue

      #pdb.set_trace()
      collection.append([keyname,tmptime,ts,newlist[3]])

    elif m:
      # into vm-info
      first = 1
      veryfirst = 0
      newlist = line.split(':')
      key=newlist[0].replace(' ','')
      if key not in tags:
        continue
      if key == "Guest":
        if count2 > 20:
          count1 += 1
          count2 = 0
        else:
          count2 += 1
        value=newlist[1]
        if value == "":
          continue
        vmMap[key] = value
        logging.debug(key + "=>" + str(vmMap[key]))
        logging.debug("\n")
        keyname = letters[count1] + letters[count2]
        keyname = value.replace(' ','')
        logging.debug("set new keyname: " + keyname)
        logging.debug("\n")

      else:
        newArr=newlist[1:]
        value=':'.join(newArr)
        if value == "":
          continue
        vmMap[key] = value
        logging.debug(key + "=>" + str(vmMap[key]))
        logging.debug("\n")


  vmcollection.append(vmMap)

  with open(outputfile,'wb') as f:
    wr = csv.writer(f,delimiter=',', quoting=csv.QUOTE_ALL)
    wr.writerows(collection)

  for item in collection:
    logging.info(str(item))
    logging.debug("\n")
  for item in vmcollection:
    logging.info(str(item))
    logging.debug("\n")
  f.close()


def main():
  myhome="/home/thw"
  logging.basicConfig(filename=myhome+'/logs/thw.log',level=logging.INFO)
  runFile()
if __name__ == '__main__':
  main()

