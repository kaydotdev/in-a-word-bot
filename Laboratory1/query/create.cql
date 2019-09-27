CREATE KEYSPACE IF NOT EXISTS lecturebot 
WITH REPLICATION = 
{ 
'class' : 'SimpleStrategy', 
'replication_factor' : 5 
};

CREATE TYPE lecturebot.role_type
(
	name text,
	priority int,
	allowed_self_crud boolean,
	allow_unlimited_serialization boolean,
	allow_role_grant boolean
);

CREATE TABLE IF NOT EXISTS lecturebot.user_lectures
(
	login text,
	password_hash blob STATIC,
	password_salt blob STATIC,
	role FROZEN<role_type> STATIC,
	resources set<text> STATIC,
	
	lecture_id int,
	lecture_header text,
	lecture_content text,
	lecture_raw_view list<FROZEN<map<text, text>>>,
	
	PRIMARY KEY (login, lecture_id)
);

CREATE TABLE IF NOT EXISTS lecturebot.resource_components
(
	url text,
	description text STATIC,
	times_visited int STATIC,
	
	component_id int,
	component_tag text,
	component_attributes map<text, text>,
	component_inner text,
	
	PRIMARY KEY(url, component_id)
);