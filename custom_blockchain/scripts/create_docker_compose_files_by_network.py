import yaml
import argparse
import os
import json

# Directories for network and nodes types
base_directory = ".."
networks_directory = "networks"
miner_nodes_directory = "miners"
rpc_nodes_directory = "rpcs"
common_nodes_directory = "nodes"

keystore_directory = "keystore"
conf_directory = "conf"
geth_directory = "geth"
scripts_directory = "scripts"

# Prefix for the nodes names
rpc_node_name = "rpc_"
miner_node_name = "miner_"
common_node_name = "node_"

# NodeTypes
miner = "miner"
rpc = "rpc"
common_node = "node"

# Docker compose file names
rpc_docker_compose_name = "rpcs_docker_compose.yml"
miner_docker_compose_name = "miners_docker_compose.yml"
common_node_docker_compose_name = "nodes_docker_compose.yml"

network_docker_name = "eth_net_"

# Docker compose
geth_image = "ethereum/client-go:stable"
docker_compose_config = {
    'version': '3',
    'services': {},
    'networks': {}
}

common_docker_compose_service_config = {
    'image': geth_image,
    'ports': [],
    'volumes': [],
    'networks': [],
    'command': ''
}


def generate_rpc_command(rpc_config_toml):
    return f'--config {rpc_config_toml} --http'


def generate_miner_command(miner_config_toml, account):
    return f'--config {miner_config_toml} --allow-insecure-unlock --unlock "{account}" --password /pwd.txt  --mine'


def generate_common_node_command(common_node_config_toml):
    return f'--config {common_node_config_toml}'


def create_docker_compose_files(args):
    remove_docker_compose_files_if_exists(args)
    create_docker_compose_file(args, rpc)
    create_docker_compose_file(args, miner)

    num_common_nodes = get_num_nodes(args.network_id, common_nodes_directory)
    if num_common_nodes > 0:
        create_docker_compose_file(args, common_node)


def generate_docker_compose_ports_config(args, node_type, node_name):
    if node_type == rpc:
        rpc_ports = get_ports(args.rpc_ports)
        auth_rpc_ports = get_ports(args.auth_rpc_ports)
        listen_rpc_ports = get_ports(args.listen_rpc_ports)

        pattern_index = node_name[len(rpc_node_name):]

        current_rpc_port = rpc_ports[int(pattern_index)]
        current_auth_rpc_port = auth_rpc_ports[int(pattern_index)]
        current_listen_rpc_port = listen_rpc_ports[int(pattern_index)]

        ports = [
            f"{current_rpc_port}:{current_rpc_port}",
            f"{current_auth_rpc_port}:{current_auth_rpc_port}",
            f"{current_listen_rpc_port}:{current_listen_rpc_port}"
        ]

    elif node_type == miner:
        auth_miner_ports = get_ports(args.auth_miner_ports)
        listen_miner_ports = get_ports(args.listen_miner_ports)

        pattern_index = node_name[len(miner_node_name):]

        current_auth_miner_port = auth_miner_ports[int(pattern_index)]
        current_listen_miner_port = listen_miner_ports[int(pattern_index)]

        ports = [
            f"{current_auth_miner_port}:{current_auth_miner_port}",
            f"{current_listen_miner_port}:{current_listen_miner_port}"
        ]
    else:
        auth_common_node_ports = get_ports(args.auth_common_node_ports)
        listen_common_node_ports = get_ports(args.listen_common_node_ports)

        pattern_index = node_name[len(common_node_name):]

        current_auth_common_node_port = auth_common_node_ports[int(pattern_index)]
        current_listen_common_node_port = listen_common_node_ports[int(pattern_index)]

        ports = [
            f"{current_auth_common_node_port}:{current_auth_common_node_port}",
            f"{current_listen_common_node_port}:{current_listen_common_node_port}"
        ]

    return ports


def generate_docker_compose_command_config(node_type, node_name):
    command = ""
    if node_type == rpc:
        rpc_toml_docker_path = os.path.join(conf_directory, rpc_nodes_directory, f"{node_name}.toml")
        command = generate_rpc_command(rpc_toml_docker_path)
    return command


def generate_docker_compose_volumes_config(node_type):
    volumes = []
    if node_type == rpc:
        current_rpc_node_config_path = os.path.join(".", conf_directory)
        current_rpc_node_docker_config_path = os.path.join("/", conf_directory)

        current_rpc_nodes_directory_path = os.path.join(".", rpc_nodes_directory)
        current_rpc_nodes_docker_directory_path = os.path.join("/", rpc_nodes_directory)

        volumes = [
            f"{current_rpc_node_config_path}:{current_rpc_node_docker_config_path}",
            f"{current_rpc_nodes_directory_path}:{current_rpc_nodes_docker_directory_path}"
        ]
    return volumes


def create_docker_compose_file(args, node_type):
    network_path = os.path.join(base_directory, networks_directory, args.network_id)

    if node_type == rpc:
        docker_compose_path = os.path.join(network_path, rpc_docker_compose_name)
        node_path = os.path.join(network_path, rpc_nodes_directory)
    elif node_type == miner:
        docker_compose_path = os.path.join(network_path, miner_docker_compose_name)
        node_path = os.path.join(network_path, miner_nodes_directory)
    else:
        docker_compose_path = os.path.join(network_path, common_node_docker_compose_name)
        node_path = os.path.join(network_path, common_nodes_directory)

    nodes = os.listdir(node_path)

    custom_docker_compose_config = docker_compose_config.copy()
    custom_docker_compose_service_by_node_name = {}

    for item in nodes:
        custom_docker_compose_service_config = common_docker_compose_service_config.copy()

        custom_docker_compose_service_config['ports'] = generate_docker_compose_ports_config(args, node_type, item)
        custom_docker_compose_service_config['command'] = generate_docker_compose_command_config(node_type, item)
        custom_docker_compose_service_config['volumes'] = generate_docker_compose_volumes_config(node_type)
        custom_docker_compose_service_config['networks'] = [f"{network_docker_name}{args.network_id}"]

        custom_docker_compose_service_by_node_name[item] = custom_docker_compose_service_config

    custom_docker_compose_config['services'] = custom_docker_compose_service_by_node_name
    custom_docker_compose_config['networks'] = {
        f"{network_docker_name}{args.network_id}": {
            'driver': 'bridge'
        }
    }

    with open(docker_compose_path, "w") as file:
        yaml.safe_dump(custom_docker_compose_config, file)
        print(f"Creado docker-compose para nodos tipo {node_type}: {docker_compose_path}")


def remove_docker_compose_files_if_exists(args):
    remove_rpc_docker_compose_file(args)
    remove_miner_docker_compose_file(args)
    remove_common_node_docker_compose_file(args)


def remove_rpc_docker_compose_file(args):
    path = os.path.join(base_directory, networks_directory, args.network_id)
    rpc_docker_compose_path = os.path.join(path, rpc_docker_compose_name)
    if os.path.exists(rpc_docker_compose_path):
        os.remove(rpc_docker_compose_path)
        print(f"docker-compose para nodos rpc borrado: {rpc_docker_compose_path}")


def remove_miner_docker_compose_file(args):
    path = os.path.join(base_directory, networks_directory, args.network_id)
    miner_docker_compose_path = os.path.join(path, miner_docker_compose_name)
    if os.path.exists(miner_docker_compose_path):
        os.remove(miner_docker_compose_path)
        print(f"docker-compose para nodos mineros borrado: {miner_docker_compose_path}")


def remove_common_node_docker_compose_file(args):
    path = os.path.join(base_directory, networks_directory, args.network_id)
    common_node_docker_compose_path = os.path.join(path, common_node_docker_compose_name)
    if os.path.exists(common_node_docker_compose_path):
        os.remove(common_node_docker_compose_path)
        print(f"docker-compose para nodos normales borrado: {common_node_docker_compose_path}")


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


def main():
    parser = argparse.ArgumentParser(description="Generate docker-compose files for node types")
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
    create_docker_compose_files(args)


if __name__ == "__main__":
    main()
