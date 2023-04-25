# network_blocker
 
**Python CLI tool to block network access of devices in LAN**

<br />

[![Version](https://img.shields.io/badge/version-1.5.2-blue)](https://github.com/fakuventuri/network_blocker)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-brightgreen.svg)](https://github.com/fakuventuri/network_blocker/blob/main/LICENSE)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Features

* **WiFi** network scanning with [scapy](https://github.com/secdev/scapy).
* **Table** to display the detected devices info with [python-tabulate](https://github.com/astanin/python-tabulate).
* **Block connection of multiple devices simultaneously** with ARP spoofing and subprocess.


## Requirements

* **Linux root** privileges or **Windows Administrator** privileges.
* Python
* scapy
* python-tabulate


## Usage

**These are examples**. You can also download the script in another way and run it.

`python3` may need to be replaced by `python` depending on your system configuration.

For these examples you need **git** to clone the repo.

* ### Linux

  #### 1) Clone repo

     In the path you want to save the folder:

       git clone https://github.com/fakuventuri/network_blocker


  #### 2) Enter the folder:

       cd network-blocker
      

  #### 3) Run the script:

       sudo python3 network_blocker.py

* ### Windows

  #### 1) Clone repo

     In the path you want to save the folder:

       git clone https://github.com/fakuventuri/network_blocker


  #### 2) Enter the folder:

       cd network-blocker
      

  #### 3) Run the script:

       python3 network_blocker.py


[//]: # "wget https://raw.githubusercontent.com/fakuventuri/network_blocker/main/network_blocker.py"

## Update (Linux only)

Run `sh update.sh` to update the scripts. This will clone the main branch into `/tmp/network_blocker` and overwrite the local files.

<br />

You can also update the cloned repo.


## Contributing

Contributions are very welcome!


## Disclaimer

This script is for educational and research purposes only. Use it responsibly and ethically, ensuring you have proper authorization and consent from the network owner or administrator. The developer and repository owner are not responsible for any misuse or damages caused by this script. By using it, you accept full responsibility for your actions and agree to comply with all applicable laws and regulations. If you are unsure about legality or ethics, consult a legal or cybersecurity professional.


## License

`network_blocker` released under the [GPL 3 license](https://github.com/fakuventuri/network_blocker/blob/main/LICENSE).


[//]: # "## Stargazers over time"

[//]: # "[![Stargazers over time](https://starchart.cc/fakuventuri/network_blocker.svg)](https://starchart.cc/fakuventuri/network_blocker)"
