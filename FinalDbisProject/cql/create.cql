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
	
	lecture_header text,
	lecture_status text,
	lecture_content text,
	
	PRIMARY KEY (login, lecture_header)
);

CREATE TABLE IF NOT EXISTS "LectureBotDBIS"."Resources"
(
	login text,
	url text,
	description text,
	times_visited int,
	
	PRIMARY KEY(login, url)
);
