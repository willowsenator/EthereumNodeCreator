import argparse
import subprocess


def generate_enode_command(key_file_path, ip, tcp, udp):
    command = [
        'devp2p', 'key', 'to-enode',
        '-ip', ip, '-tcp', str(tcp), '-udp', str(udp),
        key_file_path
    ]
    return command


def invoke_enode_command(command):
    subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(description='Generate enode command')
    parser.add_argument('-key_file', required=True, help='Path to the key file')
    parser.add_argument('-ip', default='127.0.0.1', help='IP address')
    parser.add_argument('-tcp', type=int, default=30303, help='TCP port')
    parser.add_argument('-udp', type=int, default=30303, help='UDP port')
    args = parser.parse_args()

    enode_command = generate_enode_command(args.key_file, args.ip, args.tcp, args.udp)
    invoke_enode_command(enode_command)


if __name__ == "__main__":
    main()
