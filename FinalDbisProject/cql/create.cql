CREATE KEYSPACE IF NOT EXISTS "LectureBotDBIS"
WITH REPLICATION = 
{ 
'class' : 'SimpleStrategy', 
'replication_factor' : 5 
};

CREATE TABLE IF NOT EXISTS "LectureBotDBIS"."UserLectures"
(
	login text,
	role_name text STATIC,
	password_hash blob STATIC,
	registration_date date STATIC,
	
	lecture_header text,
	lecture_status text,
	lecture_content text,
	lecture_creation_date date,
	
	PRIMARY KEY (login, lecture_header)
);

CREATE TABLE IF NOT EXISTS "LectureBotDBIS"."Resources"
(
	login text,
	url text,
	description text,
	times_visited int,
	creation_date date,
	
	PRIMARY KEY(login, url)
);
