import subprocess
import re
import csv
import argparse
from datetime import datetime


def main(inventory_path, playbook_path, output_csv):
    # Run the Ansible playbook and capture the output

    start_time = datetime.now()
    print(f"Script started at: {start_time}")

    playbook_command = f"ansible-playbook -i {inventory_path} {playbook_path}"
    result = subprocess.run(playbook_command, shell=True, stdout=subprocess.PIPE, text=True)

    # Get the stdout of the playbook execution
    playbook_output = result.stdout

    # Extract nodename, IP address, and memory usage using regular expressions
    nodename_matches = re.findall(r'"ansible_nodename": "(.*?)"', playbook_output)
    ip_address_matches = re.findall(r'"ansible_default_ipv4\.address": "(.*?)"', playbook_output)
    memory_usage_matches = re.findall(r'"msg": "(.*?)"', playbook_output)

    # Initialize data for CSV
    csv_data = []

    # Check if matches were found and store the values in a list
    if nodename_matches:
        csv_data.extend(nodename_matches)
        print(f"Nodenames: {', '.join(nodename_matches)}")

    if ip_address_matches:
        csv_data.extend(ip_address_matches)
        print(f"IP Addresses: {', '.join(ip_address_matches)}")

    if memory_usage_matches:
        csv_data.extend(memory_usage_matches)
        print(f"Memory Usages: {', '.join(memory_usage_matches)}")

    # Write data to CSV file
    with open(output_csv, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["NodeName", "IPAddress", "MemoryUsage"])
        csv_writer.writerow(csv_data)

    end_time = datetime.now()
    print(f"Script ended at: {end_time}")

    print(f"Data written to {output_csv}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract data from Ansible playbook and write it to a CSV file")
    parser.add_argument("-i", "--inventory", required=True, help="Path to the Ansible inventory")
    parser.add_argument("-p", "--playbook", required=True, help="Path to the Ansible playbook")
    parser.add_argument("-o", "--output", required=True, help="Path to the output CSV file")
    args = parser.parse_args()
    main(args.inventory, args.playbook, args.output)
