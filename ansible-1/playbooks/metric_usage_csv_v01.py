import paramiko
import argparse


def ssh_execute_command(hostname, username, command):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()

        # Automatically add host keys
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote host
        client.connect(hostname, username=username)

        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)

        # Read the output
        output = stdout.read().decode("utf-8")

        # Close the SSH connection
        client.close()

        return output.strip()  # Strip leading/trailing whitespaces
    except Exception as e:
        return str(e)


def read_inventory(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    hosts = []
    for line in lines:
        if line.startswith("#") or not line.strip():
            continue

        parts = line.strip().split()
        if len(parts) == 3:
            host = {
                "name": parts[0],
                "hostname": parts[1].split("=")[1],
                "username": parts[2].split("=")[1],
            }
            hosts.append(host)

    return hosts


memory_command = "free -m | sed -n '2p' | awk '{print $3;}'"
cpu_command = (
    "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1\"%\"}'"
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch memory and CPU usage from remote hosts")
    parser.add_argument("-i", "--inventory", required=True, help="Path to the Ansible inventory file")
    args = parser.parse_args()

    # Read host and login details from the inventory file
    inventory_path = args.inventory
    hosts = read_inventory(inventory_path)

    # Print the header
    print("Host\t\tMemory_Usage\tCPU_Usage")

    # Iterate through the hosts and fetch memory and CPU usage
    for host in hosts:
        memory_output = ssh_execute_command(host["hostname"], host["username"], memory_command)
        cpu_output = ssh_execute_command(host["hostname"], host["username"], cpu_command)

        # Format the output
        output = f"{host['hostname']}\t{memory_output}\t\t{cpu_output}"

        # Print the output
        print(output)
