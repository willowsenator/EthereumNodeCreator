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
conf_directory = "conf"

# Prefix for the nodes names
rpc_node_name = "rpc_"
miner_node_name = "miner_"
common_node_name = "node_"

# Toml Template
toml_template = "node_template.toml"

# Parameters for miner
etherbase = "Etherbase="


def create_conf_directories(args):
    path = os.path.join(base_directory, networks_directory, args.network_id, conf_directory)
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Configuración de nodos borrada {path}")
    create_rpc_node_conf_directory(args)
    create_miner_node_conf_directory(args)
    create_common_node_conf_directory(args)


def create_tomls(args):
    create_rpcs_toml(args)
    create_miners_toml(args)
    create_common_nodes_toml(args)


def create_rpcs_toml(args):
    rpc_toml_path = os.path.join(base_directory, networks_directory, args.network_id, conf_directory,
                                 rpc_nodes_directory)
    rpc_nodes_path = os.path.join(base_directory, networks_directory, args.network_id, rpc_nodes_directory)
    rpc_node_names = os.listdir(rpc_nodes_path)
    create_current_toml(args, rpc_node_names, rpc_toml_path)


def create_miners_toml(args):
    miner_toml_path = os.path.join(base_directory, networks_directory, args.network_id, conf_directory,
                                   miner_nodes_directory)
    miner_nodes_path = os.path.join(base_directory, networks_directory, args.network_id, miner_nodes_directory)
    miner_node_names = os.listdir(miner_nodes_path)
    create_current_toml(args, miner_node_names, miner_toml_path, "miner")


def create_common_nodes_toml(args):
    common_toml_path = os.path.join(base_directory, networks_directory, args.network_id, conf_directory,
                                    common_nodes_directory)
    common_nodes_path = os.path.join(base_directory, networks_directory, args.network_id, common_nodes_directory)
    common_node_names = os.listdir(common_nodes_path)
    create_current_toml(args, common_node_names, common_toml_path)


def create_current_toml(args, node_names, toml_path, node_type=""):
    toml_template_path = os.path.join(base_directory, templates_directory, toml_template)
    with open(toml_template_path, "r") as file:
        content = file.read()

    for item in node_names:
        modified_content = modified_toml_template(args, content, node_type, item)

        current_node_toml_path = os.path.join(toml_path, f"{item}.toml")
        with open(current_node_toml_path, "w") as file:
            file.write(modified_content)
        print(f"Creado toml {current_node_toml_path}")


def modified_toml_template(args, content, node_type, item):
    modified_content = content.replace("%NETWORK_ID%", args.network_id)
    if node_type == "miner":
        current_miner_path = os.path.join(base_directory, networks_directory, args.network_id, miner_nodes_directory
                                          , item, keystore_directory)
        current_miner_keystore = os.path.join(current_miner_path, os.listdir(current_miner_path)[0])
        modified_content = modified_content.replace("%ETHER_BASE%",
                                                    f'{etherbase}"{get_node_account(current_miner_keystore)}"')
    else:
        modified_content = modified_content.replace("%ETHER_BASE%", "")

    modified_content = modified_content.replace("%NODE_NAME%", item)

    return modified_content


def get_node_account(path):
    with open(path, "r") as file:
        json_data = json.load(file)
    return f"0x{json_data['address']}"


def create_miner_node_conf_directory(args):
    miner_conf_path = os.path.join(base_directory, networks_directory, args.network_id, conf_directory,
                                   miner_nodes_directory)
    os.makedirs(miner_conf_path)
    print(f"Creado {miner_conf_path}")


def create_rpc_node_conf_directory(args):
    rpc_conf_path = os.path.join(base_directory, networks_directory, args.network_id, conf_directory,
                                 rpc_nodes_directory)
    os.makedirs(rpc_conf_path)
    print(f"Creado {rpc_conf_path}")


def create_common_node_conf_directory(args):
    common_node_conf_path = os.path.join(base_directory, networks_directory, args.network_id, conf_directory,
                                         common_nodes_directory)
    os.makedirs(common_node_conf_path)
    print(f"Creado {common_node_conf_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate nodes toml")
    parser.add_argument("-network_id", required=True, help="Network id for the network")
    # parser.add_argument("-rpc_ports", required=True, help="Rpc ports")
    # parser.add_argument("-auth_ports", required=True, help="Auth ports")
    # parser.add_argument("-nodes_ports", required=True, help="Node ports")
    args = parser.parse_args()

    create_conf_directories(args)
    create_tomls(args)


if __name__ == "__main__":
    main()
