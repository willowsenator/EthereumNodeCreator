### Usando GETH para crear blockchain privada personalizada

* Crear tres cuentas con el archivo de password pwd.txt

    `geth --datadir node01 account new --password ./pwd.txt`

    `geth --datadir node02 account new --password ./pwd.txt`

    `geth --datadir node03 account new --password ./pwd.txt`

* Añadir cuenta con fondos y cuentas validoras en el genesis.json
    * Cuenta con fondos
        * Añadir la cuenta que queramos con fondos
    * Cuentas validadores añadirlas al extrada
        * Añadir cuentas validadoras sin 0x al script generate_extrada.py y obtener el extrada

* Inicializar genesis en cada nodo

    `geth init --datadir node01 genesis.json`

    `geth init --datadir node02 genesis.json`

    `geth init --datadir node03 genesis.json`

* Generar boot.key
    
    `bootnode -genkey boot.key`

* Vamos a crear un zip con la configuración inicial de la blockchain initial_config.zip para partir de una base
