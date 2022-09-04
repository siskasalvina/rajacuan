#!/usr/bin/env python


import requests, time
import logging, sys
from halo import Halo
from apscheduler.schedulers.blocking import BlockingScheduler

# logging.basicConfig (filename = "log.txt", level = logging.DEBUG)

#################
### scheduler ###
#################
sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=3)
current_api = 10

for i in range(current_api):
  try:
    LOADING = None
    start_time = time.time()
    HOST = f"http://{}-{}.herokuapp.com/ping".format("ping-00", i)
    with Halo(text = f'{i} Pinging {HOST} Started at {time.ctime()} [{start_time}]', text_color = "green", spinner = 'dots', placement = "right") as LOADING:			
      assert requests.get(HOST).status_code == 200, ""
      i+=1
      LOADING = None
    end_time = time.time()
    finished_time = end_time - start_time
    print(f"{i} {HOST} Finished with {int(finished_time)} /seconds delay..")
  except Exception as e:
    print(e);continue
      
sched.start()
