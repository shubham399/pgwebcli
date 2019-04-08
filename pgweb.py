# EDIT THESE BEFORE USE
import os
PG_WEB_URL= os.getenv('PG_WEB_URL', 'https://localhost')
COOKIE_KEY = os.getenv('COOKIE_KEY','COOKIE_KEY')
COOKIE_VALUE = os.getenv('COOKIE_VALUE','COOKIE_VALUE')
# CODE BEGIN
from os import system
import requests
import json, sys,readline,signal
from tabulate import tabulate
def signal_handler(sig, frame):
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

isExpanded = False

cookies = {
    COOKIE_KEY: COOKIE_VALUE,
}

headers = {
    'cache-control': 'no-cache',
}

def callAPI (input):
  data = { 'query' : input}
  response = requests.post(PG_WEB_URL+'/api/query', headers=headers, cookies=cookies, data=data)
  data = response.json()
  if 'error' in data.keys():
    print data["error"]
  else:
    if not isExpanded :
      print tabulate(data["rows"], headers=data["columns"], tablefmt='psql')
    else :
      makeExtendedJSON(data)

def makeExtendedJSON (data):
  for i in range(len(data["rows"])):
    extendedData = []
    print "--------------------Row " + str((i+1))+ "-------------------------"
    for col in data["columns"]:
      index = data["columns"].index(col)
      d = data["rows"][i]
      value = [col,d[index]]
      extendedData.append(value)
    print tabulate(extendedData, tablefmt='psql')

try:
  line = raw_input()
  if line != "":
    callAPI (line)
    sys.exit(0)
except:
  sys.exit(1)

print "USING HOST: " + str(PG_WEB_URL)
while True:
    try:
      cmd = raw_input("pgweb# ").strip()
      if cmd == "" : continue
      if (cmd == "q" or cmd == "quit") : break
      if (cmd == "c" or cmd == "clear" ):
        _ = system('clear')
        continue
      if (cmd == "x" or cmd == "extend") :
          isExpanded = not isExpanded
          if isExpanded :
            print "Expanded display is on."
          else :
            print "Expanded display is off."
          continue
      if cmd == "h" or cmd == "help" :
        print "press c to clear screen, q to quit or pass the sql query."
        continue
      callAPI (cmd)
    except:
      break
# CODE END
