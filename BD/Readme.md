CREACION BD EN DOCKER(PostgresSQL)

docker run -d --name pg -e POSTGRES_PASSWORD=my-secret-pw -p 5432:5432 


CONFIGURACION BD CON DBEAVER

Ajustes de conexion:

Connect by: Host
Host: localhost
Database: postgres
Port: 5432
Nombre de Usuario: postgres
Contraseña: my-secret-pw
Local Client: PostgreSQL Binaries

General:

Nombre conexion: EthereumNodeCreator
Tipo de conexion: Development
Vista de navegador: Avanced

Connection Test:

Server: PostgreSQL 16.0 (Debian 16.0-1.pgdg120+1)
	PostgreSQL 16.0 (Debian 16.0-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit

Driver: PostgreSQL JDBC Driver 42.5.0



