// 3.1 INSERT - SELECT queries

INSERT INTO lecturebot.user_lectures
(
login,
password_hash,
password_salt,
role,
resources,
lecture_id,
lecture_header,
lecture_content,
lecture_raw_view
)
VALUES
(
'linus__torvalds',
textAsBlob('af808f1169889895fd2bc8abd3fea576cb3c884ffe7473cea841eefd7b569625'), // password: everythingisbetterwithlinux
textAsBlob('9bbddaf7990c6a08885040b77a8e38c21f8a9ed288c6913b02703c1666010c8d'),
{
	"name": 'Super User', 
	"priority": 2, 
	"allowed_self_crud": true,
	"allow_unlimited_serialization": true,
	"allow_role_grant": false
},
{
	'https://en.wikipedia.org/wiki/Linux',
	'https://www.techradar.com/best/best-linux-distros',
	'https://www.wired.com/2012/05/torvalds-github'
},
1,
'Main reasons why Linux is the best OS!',
'Main reasons why Linux is the best OS: 1) In Linux user has access to the source code of kernel and alter the code according to his need. It has its own advantages like bugs in OS will fix at a rapid pace and disadvantages like developers may take advantage of any weakness in OS if they found. 2) Linux has various distributions which are highly customizable based on user needs. 3) In Linux with GPL- Licensed operating system, users are free to modify the software, can re-use in any number of systems and even they can sell the modified version. 4) Linux is more secure than windows where hackers or developers of viruses will find difficult to break through Linux. 5) All software in Linux is free!',
	[{
		'header': 'Main reasons why Linux is the best OS: ',
		'p': '1) In Linux user has access to the source code of kernel and alter the code according to his need. It has its own advantages like bugs in OS will fix at a rapid pace and disadvantages like developers may take advantage of any weakness in OS if they found.'
	}, 
	{
		'p': '2) Linux has various distributions which are highly customizable based on user needs.'
	}, 
	{
		'p': '3) In Linux with GPL- Licensed operating system, users are free to modify the software, can re-use in any number of systems and even they can sell the modified version.'
	}, 
	{
		'p': '4) Linux is more secure than windows where hackers or developers of viruses will find difficult to break through Linux.'
	}, 
	{
		'p': '5) All software in Linux is free!'
	}]
);





INSERT INTO lecturebot.user_lectures
(
login,
lecture_id,
lecture_header,
lecture_content,
lecture_raw_view
)
VALUES
(
'linus__torvalds',
2,
'The Future of Open Source Is So Bright!',
'We began by asking, "What’s the future of Open Source software from your perspective?" Here’s what they told us: "Growth": Very bright: Docker has radically changed the way OSS is consumed, and now it’s very simple to distribute OSS to a wider audience. It will continue to accelerate and be integrated in different ways to solve problems and achieve results. Start caring about upgrades. Data shows people don’t upgrade and this results in tremendous liability. Some companies have an effort to look inside and start licensing components by hand to look at risk and to know what’s going on. Security and legal need to work together to assess risk.',
	[{
		'h1': 'We began by asking, "What’s the future of Open Source software from your perspective?"',
		'h3': 'Here’s what they told us:'
	}, 
	{
		'span': '"Growth":',
		'p': 'Very bright: Docker has radically changed the way OSS is consumed, and now it’s very simple to distribute OSS to a wider audience. It will continue to accelerate and be integrated in different ways to solve problems and achieve results. Start caring about upgrades. Data shows people don’t upgrade and this results in tremendous liability. Some companies have an effort to look inside and start licensing components by hand to look at risk and to know what’s going on. Security and legal need to work together to assess risk.'
	}]
);





INSERT INTO lecturebot.user_lectures
(
login,
password_hash,
password_salt,
role,
resources,
lecture_id,
lecture_header,
lecture_content,
lecture_raw_view
)
VALUES
(
'admin',
textAsBlob('333ec8d94e056af0e465a3efb3bfac786ea4e8e2e5fea318dc9e07016fbb9752'), // password: admin
textAsBlob('8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'),
{
	"name": 'Admin', 
	"priority": 1, 
	"allowed_self_crud": true,
	"allow_unlimited_serialization": true,
	"allow_role_grant": true
},
{
	'http://cassandra.apache.org/',
	'https://docs.datastax.com/en/archived/cql/3.3/cql/cqlIntro.html',
	'https://www.techighness.com/post/nosql-one-to-many-relation-bound-unbound-examples/'
},
1,
'NoSQL and Cassandra',
'What is Cassandra? The Apache Cassandra database is the right choice when you need scalability and high availability without compromising performance. Linear scalability and proven fault-tolerance on commodity hardware or cloud infrastructure make it the perfect platform for mission-critical data. Cassandra’s support for replicating across multiple datacenters is best-in-class, providing lower latency for your users and the peace of mind of knowing that you can survive regional outages.',
	[{
		'h3': 'What is Cassandra?',
		'p': 'The Apache Cassandra database is the right choice when you need scalability and high availability without compromising performance. Linear scalability and proven fault-tolerance on commodity hardware or cloud infrastructure make it the perfect platform for mission-critical data. Cassandra’s support for replicating across multiple datacenters is best-in-class, providing lower latency for your users and the peace of mind of knowing that you can survive regional outages.'
	}]
);





SELECT JSON * FROM lecturebot.user_lectures;





INSERT INTO lecturebot.resource_components
(
url,
description,
times_visited,
component_id,
component_tag,
component_attributes,
component_inner
)
VALUES
(
'https://en.wikipedia.org/wiki/Linux',
'Wikipedia: Linux',
2,
1,
'h1',
{
	'id': 'firstHeading',
	'class': 'firstHeading',
	'lang': 'en'
},
'Linux'
);





INSERT INTO lecturebot.resource_components
(
url,
component_id,
component_tag,
component_attributes,
component_inner
)
VALUES
(
'https://en.wikipedia.org/wiki/Linux',
2,
'p',
{
	'id': 'firstHeading',
	'class': 'firstHeading',
	'lang': 'en'
},
'Linux (/ˈlɪnəks/ (About this soundlisten) LIN-əks)[9][10] is a family of open source Unix-like operating systems based on the Linux kernel,[11] an operating system kernel first released on September 17, 1991, by Linus Torvalds.[12][13][14] Linux is typically packaged in a Linux distribution. Distributions include the Linux kernel and supporting system software and libraries, many of which are provided by the GNU Project. Many Linux distributions use the word "Linux" in their name, but the Free Software Foundation uses the name GNU/Linux to emphasize the importance of GNU software, causing some controversy.[15][16] Popular Linux distributions[17][18][19] include Debian, Fedora, and Ubuntu. Commercial distributions include Red Hat Enterprise Linux and SUSE Linux Enterprise Server. Desktop Linux distributions include a windowing system such as X11 or Wayland, and a desktop environment such as GNOME or KDE Plasma 5. Distributions intended for servers may omit graphics altogether, or include a solution stack such as LAMP. Because Linux is freely redistributable, anyone may create a distribution for any purpose. Linux was originally developed for personal computers based on the Intel x86 architecture, but has since been ported to more platforms than any other operating system.[20] Linux is the leading operating system on servers and other big iron systems such as mainframe computers, and the only OS used on TOP500 supercomputers (since November 2017, having gradually eliminated all competitors).[21][22][23] It is used by around 2.3 percent of desktop computers.[24][25] The Chromebook, which runs the Linux kernel-based Chrome OS, dominates the US K–12 education market and represents nearly 20 percent of sub-$300 notebook sales in the US.[26] Linux also runs on embedded systems, i.e. devices whose operating system is typically built into the firmware and is highly tailored to the system. This includes routers, automation controls, televisions,[27][28] digital video recorders, video game consoles, and smartwatches.[29] Many smartphones and tablet computers run Android and other Linux derivatives.[30] Because of the dominance of Android on smartphones, Linux has the largest installed base of all general-purpose operating systems.[31] Linux is one of the most prominent examples of free and open-source software collaboration. The source code may be used, modified and distributed—commercially or non-commercially—by anyone under the terms of its respective licenses, such as the GNU General Public License.'
);





INSERT INTO lecturebot.resource_components
(
url,
description,
times_visited,
component_id,
component_tag,
component_attributes,
component_inner
)
VALUES
(
'http://cassandra.apache.org',
'Apache Cassandra',
1,
1,
'p',
{
	'id': 'firstHeading',
	'class': 'firstHeading',
	'lang': 'en'
},
'The Apache Cassandra database is the right choice when you need scalability and high availability without compromising performance. <a href="http://techblog.netflix.com/2011/11/benchmarking-cassandra-scalability-on.html">Linear scalability</a> and proven fault-tolerance on commodity hardware or cloud infrastructure make it the perfect platform for mission-critical data. Cassandra’s support for replicating across multiple datacenters is best-in-class, providing lower latency for your users and the peace of mind of knowing that you can survive regional outages.'
);





SELECT JSON * FROM lecturebot.resource_components;





// 3.2: UPDATE - SELECT queries




// Updating user data structure
UPDATE lecturebot.user_lectures
SET role = {
	"name": 'Admin', 
	"priority": 1, 
	"allowed_self_crud": true,
	"allow_unlimited_serialization": true,
	"allow_role_grant": true
}
WHERE login = 'linus__torvalds';


SELECT JSON * FROM lecturebot.user_lectures;




// Updating static fields for 'user_lectures'
UPDATE lecturebot.user_lectures
SET password_hash = textAsBlob('4b849020eb3fdb780f0cbe7c27ff56a32765e235b4ee44c273f39ff887d5f804'), // New password: linux4legends
password_salt = textAsBlob('848c33bde00fc7f426b92d922c50b85d917d26603e38af170971d351d56d8bc5')
WHERE login = 'linus__torvalds';


SELECT JSON * FROM lecturebot.user_lectures;




// Updating regular field for 'user_lectures'
UPDATE lecturebot.user_lectures
SET lecture_header='Linus Torvalds: Main reasons why Linux is the best OS!'
WHERE login = 'linus__torvalds' AND lecture_id = 1;


SELECT JSON * FROM lecturebot.user_lectures;




// Updating static fields for 'resource_components'
UPDATE lecturebot.resource_components
SET times_visited = 5
WHERE url = 'https://en.wikipedia.org/wiki/Linux';


SELECT JSON * FROM lecturebot.resource_components;




// Updating regular fields for 'resource_components'
UPDATE lecturebot.resource_components
SET component_tag = 'a'
WHERE url = 'https://en.wikipedia.org/wiki/Linux' AND component_id = 2;


SELECT JSON * FROM lecturebot.resource_components;





// 3.3: Custom queries



// Set premium plan to the user by login
UPDATE lecturebot.user_lectures
SET role = {
	"name": 'Super User', 
	"priority": 2, 
	"allowed_self_crud": true,
	"allow_unlimited_serialization": true,
	"allow_role_grant": false
}
WHERE login = 'user_to_promote';



// Get raw view of requested resource
SELECT component_inner FROM lecturebot.resource_components
WHERE url = 'https://en.wikipedia.org/wiki/Linux';



// Get all serialized lectures of user
SELECT lecture_header, lecture_content FROM lecturebot.user_lectures
WHERE login = 'linus__torvalds';



// Visit requested resource
UPDATE lecturebot.resource_components
SET times_visited = 1
WHERE url = 'https://en.wikipedia.org/wiki/Linux';





// 3.4: DELETE queries





DELETE FROM lecturebot.user_lectures
WHERE login = 'admin' AND lecture_id = 1;


DELETE FROM lecturebot.user_lectures
WHERE login = 'linus__torvalds' AND lecture_id = 2;


DELETE FROM lecturebot.user_lectures
WHERE login = 'linus__torvalds' AND lecture_id = 1;





DELETE FROM lecturebot.resource_components
WHERE url = 'http://cassandra.apache.org' AND component_id = 1;


DELETE FROM lecturebot.resource_components
WHERE url = 'https://en.wikipedia.org/wiki/Linux' AND component_id = 2;


DELETE FROM lecturebot.resource_components
WHERE url = 'https://en.wikipedia.org/wiki/Linux' AND component_id = 1;
