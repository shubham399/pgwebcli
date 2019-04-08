import requests
import json, sys,readline,signal,select,os
from os import system
from tabulate import tabulate

# SET ENV FOR THESE
PG_WEB_URL= os.getenv('PG_WEB_URL', 'https://localhost')
COOKIE_KEY = os.getenv('COOKIE_KEY','COOKIE_KEY')
COOKIE_VALUE = os.getenv('COOKIE_VALUE','COOKIE_VALUE')
schema = ""
# CODE BEGIN
isExpanded = False
cookies = {
    COOKIE_KEY: COOKIE_VALUE,
}
headers = {
    'cache-control': 'no-cache',
}

def main ():
  handlePipe()
  getShell()

def handlePipe():
  try:
    line, w, x = select.select([sys.stdin], [], [], 0)
    if  len(line) > 0:
      query(line[0])
      sys.exit(0)
  except:
    sys.exit(1)

def getShell():
  print "USING HOST: " + str(PG_WEB_URL)
  while True:
    try:
      cmd = raw_input("pgweb# ").strip()
      rescode = commandHandler(cmd)
      if rescode == 0:
        continue
      elif rescode == 1:
        break
      elif rescode == 2:
        query(cmd)
    except:
      break

def commandHandler(cmd):
  command = cmd.split(" ")
  if command[0] == "" : return 0
  if (command[0] == "\\q" or command[0] == "quit") : return 1
  if (command[0] == "\\c" or command[0] == "clear" ):
    _ = system('clear')
    return 0
  if (command[0] == "\\x" or command[0] == "extend") :
    global isExpanded
    isExpanded = not isExpanded
    if isExpanded :
      print "Expanded display is on."
    else :
      print "Expanded display is off."
    return 0
  if command[0] == "\\h" or command[0] == "help" :
    print "press \\c to clear screen, \\q to quit, \\d to list tables \\d tablename to structure or pass the sql query."
    return 0
  if command[0] == "\\d":
    if len(command) != 2:
      printObject()
      return 0
    else :
      expandTable(command[1])
      return 0
  if len(command) == 3 :
    if command[0].upper() == "SET" and command[1].upper() == "SCHEMA" :
      global schema
      schema = command[2].replace("\'","").replace("\"","").replace(";","")

  return 2

def expandTable(input):
  input = input.replace("\"","")
  input = input if schema in input else schema + "."+input
  response = requests.get(PG_WEB_URL+'/api/tables/'+str(input), headers=headers, cookies=cookies)
  data = response.json()
  if 'error' in data.keys():
    print data["error"]
  else:
    print tabulate(data["rows"], headers=data["columns"], tablefmt='psql')
    printIndexs(input)

def printIndexs(input):
  response = requests.get(PG_WEB_URL+'/api/tables/'+str(input)+"/indexes", headers=headers, cookies=cookies)
  data = response.json()
  if 'error' in data.keys():
    print data["error"]
  else:
    print tabulate(data["rows"], headers=data["columns"], tablefmt='psql')

def printObject():
  response = requests.get(PG_WEB_URL+'/api/objects', headers=headers, cookies=cookies)
  data = response.json()
  if 'error' in data.keys():
    print data["error"]
  else:
    key = data.keys()[0]
    print tabulate(data[key], tablefmt='psql')

def query(input):
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


def signal_handler(sig, frame):
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    main()
