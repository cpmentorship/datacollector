from __future__ import print_function
import qwiic_sgp40
import time
import sys
def run_example():

    print("\nSparkFun Qwiic Air Quality Sensor - SGP40, Example 1\n")
    my_sgp40 = qwiic_sgp40.QwiicSGP40()

    if my_sgp40.begin() != 0:
        print("\nThe Qwiic SGP40 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    print("\nSGP40 ready!")

    while True:

        print("\nVOC Index is: " + str(my_sgp40.get_VOC_index()))

        time.sleep(1)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)