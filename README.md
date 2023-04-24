# network_blocker
 
**Linux CLI tool to block network access of devices in LAN written in Python.**

<br />
<br />

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/fakuventuri/network_blocker)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-brightgreen.svg)](https://github.com/fakuventuri/network_blocker/blob/main/LICENSE)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Features

* **WiFi** network scanning with [scapy](https://github.com/secdev/scapy).
* **ARP spoofing** with arpspoof.
* **Table** display with [python-tabulate](https://github.com/astanin/python-tabulate).


## Requirements

* **Linux** root privileges
* Python
* dsniff(arpspoof)
* scapy
* python-tabulate

## Usage

In the path you want to save the script, run:
```
wget https://raw.githubusercontent.com/fakuventuri/network_blocker/main/network_blocker.py
```

Then:

```
sudo python3 network_blocker.py
```

## License

`network_blocker` by [@fakuventuri](https://github.com/fakuventuri). Released under the [GPL 3 license](https://github.com/fakuventuri/network_blocker/blob/main/LICENSE).


[//]: # "## Stargazers over time"

[//]: # "[![Stargazers over time](https://starchart.cc/fakuventuri/network_blocker.svg)](https://starchart.cc/fakuventuri/network_blocker)"
