from __future__ import print_function
import qwiic_sgp40
import time
import sys, os
import requests
from datetime import datetime
import pytz
from dotenv import load_dotenv
from smbus2 import SMBus
# some how, if we expose the key to github, the adafruit will reset our key. So we hide the key into environ.
load_dotenv()

bus = SMBus(1)

# I2C address
address = 0x48

# Registers
I2C_REG_VERSION		= 0x00
I2C_REG_ID3			= 0x01
I2C_REG_ID2			= 0x02
I2C_REG_ID1			= 0x03
I2C_REG_ID0			= 0x04
I2C_REG_SCRATCH		= 0x05
I2C_REG_CONTROL		= 0x06
I2C_REG_TAVG_HIGH	= 0x07
I2C_REG_TAVG_LOW	= 0x08
I2C_REG_RESET		= 0x09
I2C_REG_DECIBEL		= 0x0A
I2C_REG_MIN			= 0x0B
I2C_REG_MAX			= 0x0C
I2C_REG_THR_MIN     = 0x0D
I2C_REG_THR_MAX     = 0x0E
I2C_REG_HISTORY_0	= 0x14
I2C_REG_HISTORY_99	= 0x77

###############################################
# Settings
def write(value):
        bus.write_byte_data(address, 0, value)
        return -1

def soundlevel():
        sound = bus.read_byte_data(address, I2C_REG_DECIBEL)
        return sound

def send_air_data(value):
    simple_error_count = 0
    url = os.getenv("DATA_URL")
    air_feed = os.getenv("AIR_QUALITY")
    
    air_url = f"{url}/{air_feed}/data"
    
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
        response = requests.post(air_url, headers=headers, json=data)
        print("JSON Response ", response.json())

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


def send_sound_data(value):
    simple_error_count = 0
    url = os.getenv("DATA_URL")
    sound_feed = os.getenv("SOUND_LEVEL")
    sound_url = f"{url}/{sound_feed}/data"
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
        response = requests.post(sound_url, headers=headers, json=data)
        print("JSON Response ", response.json())

    except Exception as e:
        print(f"We got error post the data to {url}")
        print(f"Error {e}")
        simple_error_count += 1
    
    # try:
    #     data = {
    #                     "sgp40":{
    #                         "device_id": "dashpi00",
    #                         "sample": value,
    #                         "sample_time" : now_str
    #                         }
    #                 }
    #     print(f"sending request to {api_url}")
    #     print(f"data {data}")
    #     api_resp = requests.post(api_url, headers=headers, json=data)
    #     print(f"API response {api_resp}")
    #     print(f"API Resp {api_resp.content}")
    #     print("api_server JSON Response ", api_resp.json())

    # except Exception as e:
    #     print(f"We got error post the data to {api_url}")
    #     print(f"Error {e}")
    #     simple_error_count += 1    

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


    print("\nPCB Artists Sound Level Sensor\n")
    
    # Read device ID to make sure that we can communicate with the sensor
    data = bus.read_byte_data(address, I2C_REG_VERSION)
    print("dbMeter VERSION = ",data)
    count = 0
    largest = 0
    while True:
        if (count == 60):
            count = 0
            voc = my_sgp40.get_VOC_index()
            print("\Sound Level dB is: " + str(largest))
            print("\nVOC Index is: " + str(voc))
            send_air_data(voc)
            send_sound_data(largest)
            largest = 0
        time.sleep(1)
        sound = soundlevel()
        if (sound>largest):
            largest = sound
        count += 1

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)