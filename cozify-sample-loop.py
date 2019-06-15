#!/usr/bin/env python3
import time, logging, signal, sys

from cozify import hub, cloud
from cozifytemp import storage, cache, util

from influxdb.exceptions import InfluxDBServerError
from cozify.Error import APIError

def main():
    global sensors
    # loop until interrupted, can be for example run as a systemd service
    while True:
        # cozify.hub.getDevices will return the raw devices API call blob as a dictionary
        # it will also trigger cozify.cloud.authentication() if we don't have a valid hub key yet.
        # if auth fails it will throw an APIError exception and kill this loop, so we need to check for that
        try:
            # Check hub & cloud connectivity and have it auto-renewed if it's deemed time to do so.
            hub.ping()
            # Cloud checking is needed since the loop will run for a long time unattended and cloud tokens expire
            # every 28 days.
            cloud.ping()

            # Get all devices that have a temperature OR humidity capability.
            # Homogenize it to not have holes in the data.
            data = util.homogenize(hub.devices(capabilities=[hub.capability.TEMPERATURE, hub.capability.HUMIDITY]))
        except APIError as e:
            if e.status_code == 401: # auth failed
                logging.warning('Auth failed, this should not happen.')
            else:
                raise # we ignore all other APIErrors and let it burn to the ground
        else: # data retrieval succeeded
            # Data is extended into the list so that any previous cache is preserved and these are just added as new samples
            sensors.extend(data)

        # attempt storage if we have any to store
        if len(sensors) > 0:
            # InfluxDB writes can fail if for example IO conditions are bad
            # to mitigate this, we'll cache results and try again on the next loop with both old & new data
            try:
                print('writing to InfluxDB...')
                storage.storeMultisensor(sensors, verbose=False) # disable verbose output to make the script more daemonizable.
            except InfluxDBServerError:
                print('Data kept in cache(%s), issues writing to InfluxDB' % (len(sensors)))
            else:
                # write succeeded, drop cache
                print('write(%s) successful!' % len(sensors))
                sensors = []
                cache.clear()
        time.sleep(60)

# Handle cache dumping if killed.
def sigterm_handler(signal, frame):
    global sensors
    if len(sensors) > 0:
        cache.dump(sensors)
        logging.critical('SIGTERM, dumped cache to file')
    else:
        logging.critical('SIGTERM, no cache to dump')
    sys.exit(1)

sensors = [] # used as a cache for sensor data
if cache.exists(): # populate any existing cache dump
    sensors.extend(cache.read())

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    main()
