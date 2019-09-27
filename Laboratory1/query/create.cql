CREATE KEYSPACE IF NOT EXISTS lecturebot 
WITH REPLICATION = 
{ 
'class' : 'SimpleStrategy', 
'replication_factor' : 5 
};

CREATE TYPE IF NOT EXISTS lecturebot.role_type
(
	name text,
	priority int,
	allowed_self_crud boolean,
	allow_unlimited_serialization boolean,
	allow_role_grant boolean
);

CREATE TABLE IF NOT EXISTS lecturebot.user
(
	login text,
	password_hash blob,
	password_salt blob,
	role FROZEN<role_type>,
	resources set<text>,
	PRIMARY KEY (login)
);

CREATE TABLE IF NOT EXISTS lecturebot.resource
(
	url text,
	description text,
	times_visited int,
	PRIMARY KEY(url)
);

CREATE TABLE IF NOT EXISTS lecturebot.lecture
(
	id int,
	header text,
	content text,
	raw_view list<FROZEN<map<text, text>>>,
	
	user_login text,
	
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS lecturebot.component
(
	id int,
	tag text,
	attributes map<text, text>,
	inner text,
	
	resource_url text,
	
	PRIMARY KEY (id)
);