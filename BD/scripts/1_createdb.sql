-- createdb.sql
CREATE DATABASE ETHEREUM_NODES;

CREATE TABLE PUBLIC.NODES (
	id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	name_node VARCHAR(100) NULL,
	n_red VARCHAR(5) NULL,
	category_node INT NOT NULL DEFAULT 1,
    category_rpc INT ,
    category_miner INT ,
	date_creation TIMESTAMP NULL,
	date_deleted TIMESTAMP NULL,
	node_active INT NULL,
	updated INT NULL
);