from __future__ import print_function
import qwiic_sgp40
import time
import sys, os
import requests
from datetime import datetime
import pytz
from dotenv import load_dotenv
# some how, if we expose the key to github, the adafruit will reset our key. So we hide the key into environ.
load_dotenv()

def send_data(value):
    simple_error_count = 0
    url = os.getenv("DATA_URL")
    api_url = os.getenv("API_SERVER")
    headers = {"Content-Type": "application/json", 
                "charset":"utf-8", 
                "X-AIO-Key":os.getenv("AIO_KEY"), 
                "x-api-key":os.getenv("API_KEY")}
   



    # pst_tz = pytz.timezone('US/Pacific')
    # now = datetime.now()
    # now_pst = pst_tz.localize(now)

    # Add formatting
    # fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    # now_str = now_pst.strftime(fmt)
    # pydantic does not support localized time, so we use gmt
    now = datetime.utcnow()
    fmt = '%Y-%m-%d %H:%M:%S'
    now_str = now.strftime(fmt)

    try:
        data = {"value":value, "created_at":now_str}
        response = requests.post(url, headers=headers, json=data)
        print("JSON Response ", response.json(url))

    except Exception as e:
        print(f"We got error post the data to {url}")
        print(f"Error {e}")
        simple_error_count += 1
    
    try:
        data = {
                        "sgp40":{
                            "device_id": "dashpi00",
                            "sample": value,
                            "sample_time" : now_str
                            }
                    }
        print(f"sending request to {api_url}")
        print(f"data {data}")
        api_resp = requests.post(api_url, headers=headers, json=data)
        print(f"API response {api_resp}")
        print(f"API Resp {api_resp.content}")
        print("api_server JSON Response ", api_resp.json())

    except Exception as e:
        print(f"We got error post the data to {api_url}")
        print(f"Error {e}")
        simple_error_count += 1    

    if simple_error_count >= 2:
        #You can not have two date sinks all down
        raise Exception("Both data destinations are down. We stop!")

def run_example():

    print("\nSparkFun Qwiic Air Quality Sensor - SGP40, Example 1\n")
    my_sgp40 = qwiic_sgp40.QwiicSGP40()

    if my_sgp40.begin() != 0:
        print("\nThe Qwiic SGP40 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    print("\nSGP40 ready!")

    while True:
        voc = my_sgp40.get_VOC_index()
        print("\nVOC Index is: " + str(voc))

        send_data(voc)
        time.sleep(60) #every minute

if __name__ == '__main__':
    try:
        
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)