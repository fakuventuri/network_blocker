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

#### 1) Download the script with wget or any other way.
* wget:

  In the path you want to save the script:
 ```
 wget https://raw.githubusercontent.com/fakuventuri/network_blocker/main/network_blocker.py
 ```

#### 2) Run the script:

```
sudo python3 network_blocker.py
```

## Contributing

Contributions are very welcome!


## Disclaimer

This script is for educational and research purposes only. Use it responsibly and ethically, ensuring you have proper authorization and consent from the network owner or administrator. The developer and repository owner are not responsible for any misuse or damages caused by this script. By using it, you accept full responsibility for your actions and agree to comply with all applicable laws and regulations. If you are unsure about legality or ethics, consult a legal or cybersecurity professional.


## License

`network_blocker` by [@fakuventuri](https://github.com/fakuventuri). Released under the [GPL 3 license](https://github.com/fakuventuri/network_blocker/blob/main/LICENSE).


[//]: # "## Stargazers over time"

[//]: # "[![Stargazers over time](https://starchart.cc/fakuventuri/network_blocker.svg)](https://starchart.cc/fakuventuri/network_blocker)"
