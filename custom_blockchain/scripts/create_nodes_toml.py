import argparse
import os
import subprocess
import shutil
import json
import netifaces as ni

# Directories for network and nodes types
base_directory = ".."
networks_directory = "networks"
miner_nodes_directory = "miners"
rpc_nodes_directory = "rpcs"
common_nodes_directory = "nodes"

templates_directory = "templates"
keystore_directory = "keystore"
conf_directory = "conf"
geth_directory = "geth"

node_key = "nodekey"

# Prefix for the nodes names
rpc_node_name = "rpc_"
miner_node_name = "miner_"
common_node_name = "node_"

# Toml Template
toml_template = "node_template.toml"

# Parameters for miner
etherbase = "Etherbase="

# NodeTypes
miner = "miner"
rpc = "rpc"
common_node = "node"


def get_ip_address(interface):
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return ip


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
    create_current_toml(args, rpc_node_names, rpc_toml_path, rpc)


def create_miners_toml(args):
    miner_toml_path = os.path.join(base_directory, networks_directory, args.network_id, conf_directory,
                                   miner_nodes_directory)
    miner_nodes_path = os.path.join(base_directory, networks_directory, args.network_id, miner_nodes_directory)
    miner_node_names = os.listdir(miner_nodes_path)
    create_current_toml(args, miner_node_names, miner_toml_path, miner)


def create_common_nodes_toml(args):
    common_toml_path = os.path.join(base_directory, networks_directory, args.network_id, conf_directory,
                                    common_nodes_directory)
    common_nodes_path = os.path.join(base_directory, networks_directory, args.network_id, common_nodes_directory)
    common_node_names = os.listdir(common_nodes_path)
    create_current_toml(args, common_node_names, common_toml_path, common_node)


def create_current_toml(args, node_names, toml_path, node_type):
    toml_template_path = os.path.join(base_directory, templates_directory, toml_template)
    with open(toml_template_path, "r") as file:
        content = file.read()

    for item in node_names:
        modified_content = modified_toml_template(args, content, node_type, item)

        current_node_toml_path = os.path.join(toml_path, f"{item}.toml")
        with open(current_node_toml_path, "w") as file:
            file.write(modified_content)
        print(f"Creado toml {current_node_toml_path}")


def modified_ether_base_toml(args, content, node_type, node_name):
    if node_type == miner:
        current_miner_path = os.path.join(base_directory, networks_directory, args.network_id,
                                          miner_nodes_directory, node_name, keystore_directory)
        current_miner_keystore = os.path.join(current_miner_path, os.listdir(current_miner_path)[0])
        modified_content = content.replace("%ETHER_BASE%",
                                           f'{etherbase}"{get_node_account(current_miner_keystore)}"')
    else:
        modified_content = content.replace("%ETHER_BASE%", "")
    return modified_content


def modified_network_id_toml(args, content):
    return content.replace("%NETWORK_ID%", args.network_id)


def modified_node_name_toml(content, node_name):
    return content.replace("%NODE_NAME%", node_name)


def modified_auth_ports(args, content, node_type, node_name):
    if node_type == rpc:
        pattern_index = node_name[len(rpc_node_name):]
        auth_rpc_ports = get_ports(args.auth_rpc_ports)
        modified_content = content.replace("%AUTH_PORT%", f"{auth_rpc_ports[int(pattern_index)]}")
    elif node_type == miner:
        pattern_index = node_name[len(miner_node_name):]
        auth_miner_ports = get_ports(args.auth_miner_ports)
        modified_content = content.replace("%AUTH_PORT%", f"{auth_miner_ports[int(pattern_index)]}")
    else:
        pattern_index = node_name[len(common_node_name):]
        auth_common_node_ports = get_ports(args.auth_common_node_ports)
        modified_content = content.replace("%AUTH_PORT%", f"{auth_common_node_ports[int(pattern_index)]}")

    return modified_content


def modified_listen_ports(args, content, node_type, node_name):
    if node_type == rpc:
        pattern_index = node_name[len(rpc_node_name):]
        listen_rpc_ports = get_ports(args.listen_rpc_ports)
        modified_content = content.replace("%NODE_PORT%", f"{listen_rpc_ports[int(pattern_index)]}")
    elif node_type == miner:
        pattern_index = node_name[len(miner_node_name):]
        listen_miner_ports = get_ports(args.listen_miner_ports)
        modified_content = content.replace("%NODE_PORT%", f"{listen_miner_ports[int(pattern_index)]}")
    else:
        pattern_index = node_name[len(common_node_name):]
        listen_common_node_ports = get_ports(args.listen_common_node_ports)
        modified_content = content.replace("%NODE_PORT%", f"{listen_common_node_ports[int(pattern_index)]}")

    return modified_content


def modified_http_ports(args, content, node_type, node_name):
    if node_type == rpc:
        pattern_index = node_name[len(rpc_node_name):]
        rpc_ports = get_ports(args.rpc_ports)
        modified_content = content.replace("%HTTP_PORT%", f"{rpc_ports[int(pattern_index)]}")
    else:
        modified_content = content.replace("%HTTP_PORT%", "0")
    return modified_content


def modified_static_boot_nodes(args, content):
    static_boot_nodes_enode_urls = generate_enode_urls(args)
    static_boot_nodes_enode_urls += "\n"

    modified_content = content.replace("%STATIC_NODES%", static_boot_nodes_enode_urls)
    return modified_content


def modified_node_type(content, node_type):
    if node_type == rpc:
        modified_content = content.replace("%NODE_TYPE%", rpc_nodes_directory)
    elif node_type == miner:
        modified_content = content.replace("%NODE_TYPE%", miner_nodes_directory)
    else:
        modified_content = content.replace("%NODE_TYPE%", common_nodes_directory)
    return modified_content


def modified_toml_template(args, content, node_type, node_name):
    modified_content = modified_network_id_toml(args, content)
    modified_content = modified_ether_base_toml(args, modified_content, node_type, node_name)
    modified_content = modified_node_name_toml(modified_content, node_name)
    modified_content = modified_http_ports(args, modified_content, node_type, node_name)
    modified_content = modified_auth_ports(args, modified_content, node_type, node_name)
    modified_content = modified_listen_ports(args, modified_content, node_type, node_name)
    modified_content = modified_static_boot_nodes(args, modified_content)
    modified_content = modified_node_type(modified_content, node_type)

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


def validate(args):
    validate_rpcs(args)
    validate_miners(args)
    validate_common_nodes(args)


def validate_rpcs(args):
    validate_num_rpc_ports(args)
    validate_num_auth_rpc_ports(args)
    validate_num_listen_rpc_ports(args)


def validate_miners(args):
    validate_num_auth_miner_ports(args)
    validate_num_listen_miner_ports(args)


def validate_common_nodes(args):
    validate_num_auth_common_node_ports(args)
    validate_num_listen_common_node_ports(args)


def get_ports(values):
    ports = []
    if ',' in values:
        for item in values.split(','):
            ports.append(item)
    else:
        ports.append(values)
    return ports


def get_num_nodes(network_id, node_directory):
    nodes_path = os.path.join(base_directory, networks_directory, network_id, node_directory)
    nodes = os.listdir(nodes_path)
    return len(nodes)


def validate_num_rpc_ports(args):
    rpc_ports = get_ports(args.rpc_ports)
    num_rpc_nodes = get_num_nodes(args.network_id, rpc_nodes_directory)

    if not num_rpc_nodes == len(rpc_ports):
        raise ValueError(
            f"Num de puertos rpc tiene que ser igual al número de nodos rpc. Num nodos rpc: {num_rpc_nodes}")


def validate_num_auth_rpc_ports(args):
    auth_rpc_ports = get_ports(args.auth_rpc_ports)
    num_rpc_nodes = get_num_nodes(args.network_id, rpc_nodes_directory)

    if not num_rpc_nodes == len(auth_rpc_ports):
        raise ValueError(
            f"Num de puertos rpc auth tiene que ser igual al número de nodos rpc. Num nodos rpc: {num_rpc_nodes}")


def validate_num_listen_rpc_ports(args):
    listen_rpc_ports = get_ports(args.listen_rpc_ports)
    num_rpc_nodes = get_num_nodes(args.network_id, rpc_nodes_directory)

    if not num_rpc_nodes == len(listen_rpc_ports):
        raise ValueError(
            f"Num de puertos rpc de escucha tiene que ser igual al número de nodos rpc. "
            f"Num nodos rpc: {num_rpc_nodes}")


def validate_num_auth_miner_ports(args):
    auth_miner_ports = get_ports(args.auth_miner_ports)
    num_miner_nodes = get_num_nodes(args.network_id, miner_nodes_directory)

    if not num_miner_nodes == len(auth_miner_ports):
        raise ValueError(
            f"Num de puertos mineros auth tiene que ser igual al número de nodos mineros. "
            f"Num nodos mineros: {num_miner_nodes}")


def validate_num_listen_miner_ports(args):
    listen_miner_ports = get_ports(args.listen_miner_ports)
    num_miner_nodes = get_num_nodes(args.network_id, miner_nodes_directory)

    if not num_miner_nodes == len(listen_miner_ports):
        raise ValueError(
            f"Num de puertos mineros de escucha tiene que ser igual al número de nodos minero. "
            f"Num nodos mineros: {num_miner_nodes}")


def validate_num_auth_common_node_ports(args):
    num_common_nodes = get_num_nodes(args.network_id, common_nodes_directory)
    if num_common_nodes > 0:
        if hasattr(args, "auth_common_node_ports") and getattr(args, "auth_common_node_ports") is not None:
            auth_common_node_ports = get_ports(args.auth_common_node_ports)
            if not num_common_nodes == len(auth_common_node_ports):
                raise ValueError(
                    f"Num de puertos auth de nodo normal tiene que ser igual al número de nodos normales. "
                    f"Num nodos normales: {num_common_nodes}")
        else:
            raise ValueError(
                f"Num de puertos auth de nodo normal tiene que ser igual al número de nodos normales. "
                f"Num nodos normales: {num_common_nodes}")


def validate_num_listen_common_node_ports(args):
    num_common_nodes = get_num_nodes(args.network_id, common_nodes_directory)
    if num_common_nodes > 0:
        if hasattr(args, "listen_common_node_ports") and getattr(args, "listen_common_node_ports") is not None:
            listen_common_node_ports = get_ports(args.listen_common_node_ports)

            if not num_common_nodes == len(listen_common_node_ports):
                raise ValueError(
                    f"Num de puertos de nodos normales de escucha tiene que ser igual al número de nodos normales. "
                    f"Num nodos normales: {num_common_nodes}")
        else:
            raise ValueError(
                f"Num de puertos de nodos normales de escucha tiene que ser igual al número de nodos normales. "
                f"Num nodos normales: {num_common_nodes}")


def generate_enode_url_command(port, keyfile):
    command = ["python3", "generate_enode_url.py", "-key_file", keyfile, "-ip", get_ip_address("eth0"),
               "-tcp", port, "-udp", port]
    return command


def get_output_command(command):
    return subprocess.check_output(command, universal_newlines=True)


def get_enode_url(port, keyfile):
    command = generate_enode_url_command(port, keyfile)
    return get_output_command(command)


def generate_enode_urls(args):
    static_boot_nodes = generate_rpc_enode_urls(args)
    static_boot_nodes += generate_miner_enode_urls(args)

    num_common_nodes = get_num_nodes(args.network_id, common_nodes_directory)
    if num_common_nodes > 0:
        static_boot_nodes += generate_common_enode_urls(args)

    return static_boot_nodes


def generate_rpc_enode_urls(args):
    boot_nodes = f"\n{generate_enode_urls_by_node_type(args.network_id, args.listen_rpc_ports, rpc)}"
    return boot_nodes


def generate_miner_enode_urls(args):
    boot_nodes = f",\n{generate_enode_urls_by_node_type(args.network_id, args.listen_miner_ports, miner)}"
    return boot_nodes


def generate_common_enode_urls(args):
    boot_nodes = f",\n"
    boot_nodes += generate_enode_urls_by_node_type(args.network_id, args.listen_common_node_ports,
                                                   common_node)
    return boot_nodes


def generate_enode_urls_by_node_type(network_id, values, node_type):
    path = os.path.join(base_directory, networks_directory, network_id)
    if node_type == rpc:
        path = os.path.join(path, rpc_nodes_directory)
        node_name = rpc_node_name
    elif node_type == miner:
        path = os.path.join(path, miner_nodes_directory)
        node_name = miner_node_name
    else:
        path = os.path.join(path, common_nodes_directory)
        node_name = common_node_name

    nodes = os.listdir(path)

    static_boot_nodes = ""
    index = 0
    for item in nodes:
        pattern_index = item[len(node_name):]
        ports = get_ports(values)
        current_node_key_path = os.path.join(path, item, geth_directory, node_key)
        enode_url = get_enode_url(ports[int(pattern_index)], current_node_key_path)
        if index > 0:
            static_boot_nodes += ",\n"
        static_boot_nodes += f'"{enode_url.strip()}"'
        index += 1
    return static_boot_nodes


def main():
    parser = argparse.ArgumentParser(description="Generate nodes toml")
    parser.add_argument("-network_id", required=True, help="Network id for the network")
    parser.add_argument("-rpc_ports", required=True, help="Rpc port or several rpc ports separated by ,")
    parser.add_argument("-auth_rpc_ports", required=True, help="Auth rpc port or several auth rpc ports "
                                                               "separated by ,")
    parser.add_argument("-listen_rpc_ports", required=True, help="Listen rpc port or several listen rpc "
                                                                 "ports separated by ,")
    parser.add_argument("-auth_miner_ports", required=True, help="Auth miner port or several "
                                                                 "auth miner ports separated by ,")
    parser.add_argument("-listen_miner_ports", required=True, help="Listen miner port or several "
                                                                   "listen miner ports separated by ,")
    parser.add_argument("-auth_common_node_ports", help="Auth common node port or several "
                                                        "auth common nodes ports separated by ,")
    parser.add_argument("-listen_common_node_ports", help="Listen common node port or several "
                                                          "listen common nodes ports separated by ,")
    args = parser.parse_args()

    validate(args)
    create_conf_directories(args)
    create_tomls(args)


if __name__ == "__main__":
    main()
