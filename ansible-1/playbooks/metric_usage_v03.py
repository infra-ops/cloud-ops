import subprocess
import re
import argparse
import csv
from datetime import datetime

def main(inventory_path, playbook_path, output_csv):
    # Run the Ansible playbook and capture the output

    start_time = datetime.now()
    print(f"Script started at: {start_time}")

    playbook_command = f"ansible-playbook -i {inventory_path} {playbook_path}"
    result = subprocess.run(playbook_command, shell=True, stdout=subprocess.PIPE, text=True)

    # Get the stdout of the playbook execution
    playbook_output = result.stdout

    # Extract IP address, memory usage, and CPU usage using regular expressions
    ip_address_matches = re.findall(r'"ansible_default_ipv4\.address": "(.*?)"', playbook_output)
    memory_usage_matches = re.findall(r'"msg": "([0-9]+)"', playbook_output)
    cpu_usage_matches = re.findall(r'"msg": "([0-9.]+%)"', playbook_output)


    # Check if matches were found and store the values in separate lists
    ip_addresses = []
    memory_usage = []
    cpu_usage = []

    if ip_address_matches:
        ip_addresses.extend(ip_address_matches)

    if memory_usage_matches:
        memory_usage.extend(memory_usage_matches)

    if cpu_usage_matches:
        cpu_usage.extend(cpu_usage_matches)

    # Print the header
    print("IP_Address\tMemory_Usage\tCPU_Usage")

    # Write data to CSV file
    with open(output_csv, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["IP_Address", "Memory_Usage", "CPU_Usage"])

        # Iterate over the lists and print and write the data
        for ip, mem, cpu in zip(ip_addresses, memory_usage, cpu_usage):
            output = f"{ip}\t{mem}\t\t{cpu}"
            print(output)
            #print(f"{ip}\t{mem}\t\t{cpu}")
            csv_writer.writerow([ip, mem, cpu])

    end_time = datetime.now()
    print(f"Script ended at: {end_time}")
    print(f"Data written to {output_csv}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract data from Ansible playbook and print in the desired format and write to CSV")
    parser.add_argument("-i", "--inventory", required=True, help="Path to the Ansible inventory")
    parser.add_argument("-p", "--playbook", required=True, help="Path to the Ansible playbook")
    parser.add_argument("-o", "--output", required=True, help="Path to the output CSV file")
    args = parser.parse_args()
    main(args.inventory, args.playbook, args.output)
