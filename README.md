# cozify-temp
Pull sensor data from Cozify Hub into InfluxDB. At current temperature & humidity data is supported but expanding that is trivial.

Authentication and other Cozify details are handled by python-cozify bindings developed separately: [github.com/Artanicus/python-cozify](https://github.com/Artanicus/python-cozify) but this repo acts as an official example.

## installation
- Install dependencies:

```
sudo pip3 install -Ur requirements.txt
```

- For storage, create a InfluxDB bucket called for example `cozify`. You will also need to configure your organization and generate a token that has write access to the bucket.
- The easiest way is to use the web interface of InfluxDB 2.0 by navigating to http://localhost:8086 or which ever hostname your InfluxDB server is hosted at.
- Run `cozify-single-sample.py`. It won't work but you'll generate the default config to modify.
- Edit ~/.config/cozify-temp/influxdb.cfg to include your DB url, token, organization and bucket names.
- Test connection by running cozify-single-sample.py to get a single snapshot and push it to InfluxDB. The single-sample script is more naive but simpler to get started with.
- if a single sample was fine, run cozify-sample-loop.py to get and push data on a 60s interval. The loop script is more robust than the single sample and is usable as a systemd daemon.
- To explore all options run `cozify-sample-loop.py --help`

![example Grafana graphs][graphs]

[graphs]: https://i.imgur.com/TwrfXES.png "example Grafana graphs"
