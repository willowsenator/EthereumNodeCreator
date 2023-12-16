import argparse
import os
import subprocess
import shutil
import json

# Directories for network and nodes types
base_directory = ".."
networks_directory = "networks"
miner_nodes_directory = "miners"
rpc_nodes_directory = "rpcs"
common_nodes_directory = "nodes"

templates_directory = "templates"
keystore_directory = "keystore"

# Prefix for the nodes names
rpc_node_name = "rpc_"
miner_node_name = "miner_"
common_node_name = "node_"

# Genesis template and custom genesis
genesis_template = "genesis_template.json"
custom_genesis = "genesis.json"

# Genesis template constants
genesis_network_id = "%NETWORK_ID%"
genesis_account_with_balance = "%ADDRESS_WITH_BALANCE%"
genesis_account_for_rewards = "%ADDRESS_FOR_REWARDS%"
genesis_extradata = "%EXTRADATA%"


def generate_account_command(path):
    command = ['geth', '--datadir', path, 'account', 'new', '--password', './pwd.txt']
    return command


def generate_extradata_command(signers):
    command = ['python3', 'generate_extradata.py', '-signer_addresses', signers]
    return command


def generate_init_node_command(datadir, args):
    genesis_path = os.path.join(base_directory, networks_directory, args.network_id, 'genesis.json')
    command = ['geth', 'init', '--datadir', datadir, genesis_path]
    return command


def invoke_command(command):
    subprocess.run(command, check=True)


def get_output_command(command):
    return subprocess.check_output(command, universal_newlines=True)


def init_nodes(args):
    init_rpc_nodes(args)
    init_miner_nodes(args)
    init_common_nodes(args)


def init_rpc_nodes(args):
    path = os.path.join(base_directory, networks_directory, args.network_id, rpc_nodes_directory)
    for i in range(int(args.num_rpc_nodes)):
        current_path = os.path.join(path, f"{rpc_node_name}{i}")
        init_node(current_path, args)


def init_miner_nodes(args):
    path = os.path.join(base_directory, networks_directory, args.network_id, miner_nodes_directory)
    for i in range(int(args.num_miner_nodes)):
        current_path = os.path.join(path, f"{miner_node_name}{i}")
        init_node(current_path, args)


def init_common_nodes(args):
    path = os.path.join(base_directory, networks_directory, args.network_id, common_nodes_directory)
    for i in range(int(args.num_common_nodes)):
        current_path = os.path.join(path, f"{common_node_name}{i}")
        init_node(current_path, args)


def create_network(args):
    if not int(args.num_rpc_nodes) >= 1:
        raise ValueError("El num de nodos RPC debe ser al menos 1")
    if not int(args.num_miner_nodes) >= 1:
        raise ValueError("El num de nodos mineros debe ser al menos 1")
    else:
        path = os.path.join(base_directory, networks_directory, args.network_id)

        if os.path.exists(path):
            print(f"La red {args.network_id} existe se va a borrar para recrearla")
            shutil.rmtree(path)
            print(f"Red {args.network_id} borrada")
        print(f"Creando red {args.network_id}...")

        create_rpc_nodes(args)
        create_miner_nodes(args)
        create_common_nodes(args)
        generate_custom_genesis(args)
        init_nodes(args)


def create_new_account(path):
    command = generate_account_command(path)
    invoke_command(command)


def create_rpc_nodes(args):
    rpc_nodes_path = os.path.join(base_directory, networks_directory, args.network_id, rpc_nodes_directory)
    if not os.path.exists(rpc_nodes_path):
        os.makedirs(rpc_nodes_path)

    for i in range(int(args.num_rpc_nodes)):
        current_path = os.path.join(rpc_nodes_path, f"{rpc_node_name}{str(i)}")
        create_new_account(current_path)


def create_miner_nodes(args):
    miner_nodes_path = os.path.join(base_directory, networks_directory, args.network_id, miner_nodes_directory)
    if not os.path.exists(miner_nodes_path):
        os.makedirs(miner_nodes_path)

    for i in range(int(args.num_miner_nodes)):
        current_path = os.path.join(miner_nodes_path, f"{miner_node_name}{str(i)}")
        create_new_account(current_path)


def create_common_nodes(args):
    common_nodes_path = os.path.join(base_directory, networks_directory, args.network_id, common_nodes_directory)
    if not os.path.exists(common_nodes_path):
        os.makedirs(common_nodes_path)

    for i in range(int(args.num_common_nodes)):
        current_path = os.path.join(common_nodes_path, f"{common_node_name}{str(i)}")
        create_new_account(current_path)


def generate_custom_genesis(args):
    input_path = os.path.join(base_directory, templates_directory, genesis_template)
    output_path = os.path.join(base_directory, networks_directory, args.network_id, custom_genesis)

    with open(input_path, "r") as file:
        content = file.read()
    # Modify genesis template with custom info
    modified_content = content.replace(genesis_network_id, args.network_id)
    modified_content = modified_content.replace(genesis_account_with_balance, get_address_from_first_rpc_node(args))
    modified_content = modified_content.replace(genesis_account_for_rewards, get_address_from_first_rpc_node(args))

    signers = get_all_signers_addresses_without_0x_from_miners_nodes(args)
    modified_content = modified_content.replace(genesis_extradata, get_extradata(signers))

    with open(output_path, "w") as file:
        file.write(modified_content)
    print(f"Creando custom genesis {output_path}")


def get_address_from_first_rpc_node(args):
    path = os.path.join(base_directory, networks_directory, args.network_id, rpc_nodes_directory,
                        f"{rpc_node_name}0", keystore_directory)

    path = os.path.join(path, os.listdir(path)[0])

    with open(path, "r") as file:
        json_data = json.load(file)
    return f"0x{json_data['address']}"


def get_all_signers_addresses_without_0x_from_miners_nodes(args):
    path = os.path.join(base_directory, networks_directory, args.network_id, miner_nodes_directory)
    contents = os.listdir(path)

    signers = ""

    count = 0
    for item in contents:
        current_path = os.path.join(path, item, keystore_directory)
        current_keystore_path = os.path.join(current_path, os.listdir(current_path)[0])

        with open(current_keystore_path) as file:
            json_data = json.load(file)
        if int(count) == 0:
            signers = (json_data['address'])
        else:
            signers += f",{json_data['address']}"

        count = int(count) + 1
    return signers


def get_extradata(signers):
    command = generate_extradata_command(signers)
    return json.loads(get_output_command(command))["extradata"]


def init_node(datadir, args):
    command = generate_init_node_command(datadir, args)
    invoke_command(command)


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
