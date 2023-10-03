import subprocess
import re
import argparse
from datetime import datetime

def main(inventory_path, playbook_path):
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

    # Iterate over the lists and print the data in the desired format
    for ip, mem, cpu in zip(ip_addresses, memory_usage, cpu_usage):
        print(f"{ip}\t{mem}\t\t{cpu}")

    end_time = datetime.now()
    print(f"Script ended at: {end_time}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract data from Ansible playbook and print in the desired format")
    parser.add_argument("-i", "--inventory", required=True, help="Path to the Ansible inventory")
    parser.add_argument("-p", "--playbook", required=True, help="Path to the Ansible playbook")
    args = parser.parse_args()
    main(args.inventory, args.playbook)
