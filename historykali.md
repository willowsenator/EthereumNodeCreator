history
    1  ant
    2  AntivirusBypass
    3  dit
    4  dir
    5  ls
    6  apt/get update
    7  apt-get update
    8  sudo apt-get update
    9  sudo apt-get upgrade
   10  poweroff
   11  python
   12  sudo apt-get install build-essential procps curl file git
   13  test -d ~/.linuxbrew && eval "$(~/.linuxbrew/bin/brew shellenv)"\ntest -d /home/linuxbrew/.linuxbrew && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"\necho "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.bashrc
   14  200~/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   15  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   16  brew -v
   17  source .bashrc
   18  brew -v
   19  nano .zshrc
   20  cd Proyectos
   21  ls
   22  cd EthereumNodeCreator
   23  ls
   24  cd custom_blockchain/scripts
   25  ls
   26  python3 generate_network.py
   27  python3 generate_network.py -network_id 12345 -num_miner_nodes 2 -num_rpc_nodes 2 -num_common_nodes 4  
   28  cd ..
   29  ls
   30  cd networks
   31  ls
   32  cd 12345
   33  ls
   34  cd nodes
   35  cd..
   36  cd ..
   37  ls
   38  cat genesis.json
   39  ls
   40  cd miners
   41  ls
   42  cd miner_0
   43  ls
   44  cd keystore
   45  ls
   46  cat UTC--2023-12-10T20-33-54.533438690Z--a4a4f1f09cb46a0eae5a8de181adb57e4660b0bd
   47  history
   48  brew install docker\n[21:45]\nbrew install docker-compose
   49  docker
   50  cd Proyectos
   51  ls
   52  cd EthereumNodeCreator
   53  ls
   54  cd BD
   55  ls
   56  cat Readme.md
   57  docker-compose up -d\n
   58  brew uninstall docker
   59  sudo apt install -y docker.io
   60  sudo systemctl enable docker --now
   61  docker
   62  sudo usermod -aG docker $USER
   63  docker-compose up -d\n
   64  cd P
   65  cd Proyectos
   66  cd EthereumNodeCreator/bd
   67  cd EthereumNodeCreator/BD
   68  ls
   69  docker-compose up -d\n
   70  sudo docker-compose up -d\n
   71  curl -fsSL https://download.docker.com/linux/debian/gpg |\n  sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker-ce-archive-keyring.gpg
   72  docker-compose up -d\n
   73  sudo apt update
   74  sudo apt install -y docker-ce docker-ce-cli containerd.io
   75  printf '%s\n' "deb https://download.docker.com/linux/debian bullseye stable" |\n  sudo tee /etc/apt/sources.list.d/docker-ce.list
   76  sudo apt update
   77  sudo apt install -y docker-ce docker-ce-cli containerd.io
   78  docker-compose up -d\n
   79  cd P
   80  cd Proyectos
   81  cd EthereumNodeCreator/BD
   82  brew unistall docker-compose
   83  brew uninstall docker-compose
   84  docker-compose up -d\n
   85  sudo usermod -aG docker $USER\n
   86  sudo service docker restart\n
   87  docker-compose up -d\n
   88  ls -l /var/run/docker.sock\n
   89  sudo chmod 666 /var/run/docker.sock\n
   90  docker-compose up -d\n
   91  docker ps
   92  docker exec
   93  docker exec -it 35b bash
   
  193 cd EthereumNodeCreator
  195  git branch
  196  git pull
  197  ls
  198  cd custom_blockchain
  199  cd scripts
  200  ls
  201  python3 generate_network.py
  202  python3 generate_network.py -h
  203  python3 generate_network.py -network_id 112233 --num_rpc_nodes 3 -num_miner_nodes 3
  204  python3 generate_network.py -network_id 112233 -num_rpc_nodes 3 -num_miner_nodes 3
  205  python3 generate_network.py -network_id 112233 -num_rpc_nodes 3 -num_miner_nodes 3 -num_common_nodes 0
  206  ls
  207  python3 create_nodes_toml.py
  208  python3 create_nodes_toml.py -h
  209  python3 create_nodes_toml.py -network_id 112233 -rpc_ports 1000,2000,3000 -auth_rpc_ports 4000,5000,6000  -listen_rpc_ports 30300,30301,30302 -auth_miner_ports 7000,8000,9000 -listen_miner_ports 30303,30304,30305
  210  ls
  211  cat ../networks/112233/conf/rpcs/rpc_2.toml