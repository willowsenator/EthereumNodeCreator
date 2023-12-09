import argparse
import os
import subprocess

base_directory = ".."
networks_directory = "networks"
miner_nodes_directory = "miners"
rpc_nodes_directory = "rpcs"
common_nodes_directory = "nodes"

rpc_node_name = "rpc_"
miner_node_name = "miner_"
common_node_name = "node_"


def generate_account_comand(path):
    print(path)
    command = ['geth', '--datadir', path, 'account', 'new', '--password', './pwd.txt']
    return command


def invoke_create_account_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def create_network(args):
    create_rpc_nodes(args)
    create_miner_nodes(args)
    create_common_nodes(args)


def create_new_account(path):
    command = generate_account_comand(path)
    try:
        invoke_create_account_command(command)
    except Exception as e:
        print(f"Error: {e}")


def create_rpc_nodes(args):
    rpc_nodes_path = os.path.join(base_directory, networks_directory, args.network_id, rpc_nodes_directory)
    if not os.path.exists(rpc_nodes_path):
        os.makedirs(rpc_nodes_path)

    for i in range(int(args.num_rpc_nodes)):
        current_path = os.path.join(rpc_nodes_path, rpc_node_name + str(i))
        create_new_account(current_path)


def create_miner_nodes(args):
    miner_nodes_path = os.path.join(base_directory, networks_directory, args.network_id, miner_nodes_directory)
    if not os.path.exists(miner_nodes_path):
        os.makedirs(miner_nodes_path)

    for i in range(int(args.num_miner_nodes)):
        current_path = os.path.join(miner_nodes_path, miner_node_name + str(i))
        create_new_account(current_path)


def create_common_nodes(args):
    common_nodes_path = os.path.join(base_directory, networks_directory, args.network_id, common_nodes_directory)
    if not os.path.exists(common_nodes_path):
        os.makedirs(common_nodes_path)

    for i in range(int(args.num_common_nodes)):
        current_path = os.path.join(common_nodes_path, common_node_name + str(i))
        create_new_account(current_path)


def main():
    parser = argparse.ArgumentParser(description="Generate a new network")
    parser.add_argument("-network_id", required=True, help="Network id to generate the network")
    parser.add_argument("-num_rpc_nodes", required=True, help="Num rpc nodes")
    parser.add_argument("-num_miner_nodes", required=True, help="Num miner nodes")
    parser.add_argument("-num_common_nodes", required=True, help="Num common nodes")
    args = parser.parse_args()

    create_network(args)


if __name__ == "__main__":
    main()
