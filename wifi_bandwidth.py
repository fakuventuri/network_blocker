import sys
import time
from collections import defaultdict
from scapy.all import ARP, Ether, sniff
from tabulate import tabulate


def process_packet(packet):
    if packet.haslayer(ARP) or packet.haslayer(Ether):
        src_mac = packet[Ether].src
        dst_mac = packet[Ether].dst
        packet_size = len(packet)

        device_traffic[src_mac]["total"] += packet_size
        device_traffic[dst_mac]["total"] += packet_size

        print_table()


def print_table():
    sys.stdout.write(
        "\033[F" * (len(device_traffic) + 2)
    )  # Move cursor up to clear previous output

    table_data = []
    for mac, data in device_traffic.items():
        table_data.append([mac, data["total"]])

    print(
        tabulate(
            table_data, headers=["MAC Address", "Bandwidth (Bytes)"], tablefmt="grid"
        )
    )


def main():
    global device_traffic
    device_traffic = defaultdict(lambda: defaultdict(int))

    print("Monitoring Wi-Fi network bandwidth usage...")

    try:
        sniff(prn=process_packet, store=0)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
