#! /usr/local/bin/python3
# Author : Sunil Akella

# Healthify Updates
"""
    Upcoming Features:
      1 - 
      2 - 
     
    Revision History Updates:
      1.0 :  Healthify Tool - Initial Draft
    
"""



# Python Built-in Imports
import os
import sys
import json
import multiprocessing
from time import ctime, sleep

# Tool Imports
tool_path = os.getcwd()
tool_data_path = os.path.join(tool_path, 'data')
sys.path.insert(0, tool_path)
from  AppUI import run_app

# Globals
tool_image_path = os.path.join(tool_path, 'images')
tool_data_path = os.path.join(tool_path, 'data')




# ----------------------
# Healthify App Logic
# ----------------------

def healthify():
    print("\n\nHealthify - Initiated")  
    tc_dict = json.loads(open(os.path.join(tool_data_path, 'app_controls.JSON')).read())
    while True: 
        # Reading Health Tip Controls - data
        print("\t- Reading Health-Tip-Controls Data")
        htc_dict = json.loads(open(os.path.join(tool_data_path, 'health_tip_controls.JSON')).read())
        # Fetching Month and Year ( This output is parsed based on Platform : MacOS / Darwin / Windows)
        day, month, date, time, year = ctime().split()
        hrs, mns, sec = time.split(':')
        check_mns = str(mns)
        print("\t- Received Check-Point: %s" % check_mns)
        if check_mns in htc_dict:
            print("\t- Check-point Arrived: %s" % check_mns)
            name = htc_dict[check_mns]['name']
            msg = htc_dict[check_mns]['msg']
            print("\t- Invoking UI..")
            # Invoking as a process
            m_process = multiprocessing.Process(target=run_app, args=(name, msg))
            m_process.start()
            sleep(int(tc_dict['auto_close_counter']))
            m_process.terminate()
        else:
            print("\t- Criteria not met for Invoking UI")
        print("\n\nWaiting for next 60 Seconds..")
        sleep(60)
        print("\t- Done waiting..")


# Invoke Main
if __name__ == '__main__':
    try:
        healthify()
    except KeyboardInterrupt: 
        print("\n\nReceived CTRL+C ! .. Exiting Gracefully")
        sys.exit()
    except Exception as UIerr:
        print("\n\nUnknown Exception Occured..: %s" % UIerr) 
        sys.exit()
