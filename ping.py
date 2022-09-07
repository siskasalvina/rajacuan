#!/usr/bin/env python3
import requests, time
import logging, sys
from halo import Halo
from apscheduler.schedulers.blocking import BlockingScheduler

# logging.basicConfig (filename = "log.txt", level = logging.DEBUG)

#################
### scheduler ###
#################
current_api = 15
sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=3)
def main():
  for i in range(current_api+1):
    try:
      LOADING = None
      start_time = time.time()
      HOST = "http://{}{}.herokuapp.com/ping".format("ping-00", i)
      with Halo(text = f'{i} Pinging {HOST} Started at {time.ctime()} [{start_time}]', text_color = "green", spinner = 'dots', placement = "right") as LOADING:			
        assert requests.get(HOST).status_code == 200, ""
        i+=1
        LOADING = None
      end_time = time.time()
      finished_time = end_time - start_time
      print(f"{i} {HOST} Finished with {int(finished_time)} /seconds delay..")
    except Exception as e:
      print(e);continue

@sched.scheduled_job('interval', minutes=30)
def restart():
  tokens=open('tokens.txt').read().splitlines()
  for i in range(current_api+1):
    token = tokens[i]
    baseurl = f'https://api.heroku.com/apps/ping-00{i}/dynos'
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.heroku+json; version=3',
      'Authorization': token
    }

    response = requests.delete(baseurl, headers=headers)
    i+=1
      
sched.start()