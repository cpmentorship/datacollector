# First Time Setup Instructions

## Step 1: Setup the Virtual Environment

First, set up a virtual environment for the project. This keeps your dependencies organized and separate from other projects.
```
python3 -m venv alviso
source alviso/bin/activate
```

## Step 2: Enable I2C Interface on Raspberry Pi

To communicate with the SGP40 sensor, the I2C interface on your Raspberry Pi needs to be enabled:

1. Run `sudo raspi-config` in the terminal.
2. Navigate to `Interfacing Options` > `I2C`.
3. Select `Enable` and then reboot your Raspberry Pi.

## Step 3: Clone the Repository

Clone the repository to get the source code on your Raspberry Pi:

```
git clone git@github.com:cpmentorship/datacollector.git
```

## Step 4: Install Required Packages

Change your directory to `datacollector` and install the required Python packages:

```
cd datacollector
pip install -r requirements.txt
```

## Step 5: Run `test.py`

Finally, run the `test.py` script to start collecting data:

```
python test.py
```


### Expected Output

Upon successful execution, you should see an output similar to the following, indicating that the sensor is operational:

```
SparkFun Qwiic Air Quality Sensor - SGP40, Example 1

Waiting 10 seconds for the SGP40 to warm-up.

SGP40 ready!

VOC Index is: 65
VOC Index is: 64
VOC Index is: 63

```
