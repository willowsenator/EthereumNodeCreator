	SET statement_timeout = 0;
	SET lock_timeout = 0;
	SET client_encoding = 'UTF8';
	SET standard_conforming_strings = on;
	SET check_function_bodies = false;
	SET client_min_messages = warning;
	SET default_tablespace = '';
	SET default_with_oids = false;
    
---
--- drop tables
---

	DROP TABLE IF EXISTS public.nodes;

--
-- Name: Nodes; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE public.nodes (
	id serial4 NOT NULL,
	name_node varchar(100) NULL,
	n_red varchar(5) NULL,
	category int4 NULL,
	date_creation timestamp NULL,
	date_deleted timestamp NULL,
	node_active bool NULL,
	updated bool NULL,
	CONSTRAINT nodes_pkey PRIMARY KEY (id)
);