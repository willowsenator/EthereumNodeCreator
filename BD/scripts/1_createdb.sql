-- createdb.sql
CREATE DATABASE ethereumnodes;

\c ethereumnodes

CREATE TABLE public.nodes (
	id INT PRIMARY KEy GENERATED ALWAYS AS IDENTITY,
	name_node varchar(100) NULL,
	n_red varchar(5) NULL,
	category_node INT NOT NULL DEFAULT 1,
    category_rpc INT ,
    category_miner INT ,
	date_creation timestamp NULL,
	date_deleted timestamp NULL,
	node_active INT NULL,
	updated INT NULL
);