#!/usr/bin/env python3

from cozify import cloud, hub, multisensor
from cozify-temp import storage

data = hub.getDevices()
sensors = multisensor.getMultisensorData(data)
storage.storeMultisensor(sensors)
