# EDIT THESE BEFORE USE
PG_WEB_URL=""
COOKIE_KEY=""
COOKIE_VALUE=""
# CODE BEGIN
from os import system
import requests
import json, sys,readline,signal
from tabulate import tabulate
def signal_handler(sig, frame):
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

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
    print tabulate(data["rows"], headers=data["columns"], tablefmt='orgtbl')

try:
  line = raw_input()
  if line != "":
    callAPI (line)
    sys.exit(0)
except:
  sys.exit(1)

while True:
    try:
      cmd = raw_input("pgweb# ").strip()
      if cmd == "" : continue
      if (cmd == "q" or cmd == "quit") : break
      if (cmd == "c" or cmd == "clear" ):
        _ = system('clear')
        continue
      if cmd == "h" or cmd == "help" :
        print "press c to clear screen, q to quit or pass the sql query."
        continue
      callAPI (cmd)
    except:
      print "Something went wrong."
      break
# CODE END
