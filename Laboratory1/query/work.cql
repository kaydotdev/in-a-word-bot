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
'<b>Linux</b> (<span class="nowrap"><span class="IPA nopopups noexcerpt"><a href="/wiki/Help:IPA/English" title="Help:IPA/English">/<span style="border-bottom:1px dotted"><span title="/ˈ/: primary stress follows">ˈ</span><span title="’l’ in ’lie’">l</span><span title="/ɪ/: ’i’ in ’kit’">ɪ</span><span title="’n’ in ’nigh’">n</span><span title="/ə/: ’a’ in ’about’">ə</span><span title="’k’ in ’kind’">k</span><span title="’s’ in ’sigh’">s</span></span>/</a></span> <span class="nowrap" style="font-size:85%">(<span class="unicode haudio"><span class="fn"><span style="white-space:nowrap;margin-right:.25em;"><a href="/wiki/File:Linus-linux.ogg" title="About this sound"><img alt="About this sound" src="//upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Loudspeaker.svg/11px-Loudspeaker.svg.png" decoding="async" width="11" height="11" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Loudspeaker.svg/17px-Loudspeaker.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Loudspeaker.svg/22px-Loudspeaker.svg.png 2x" data-file-width="20" data-file-height="20"></a></span><a href="//upload.wikimedia.org/wikipedia/commons/0/03/Linus-linux.ogg" class="internal" title="Linus-linux.ogg">listen</a></span></span>)</span></span> <a href="/wiki/Help:Pronunciation_respelling_key" title="Help:Pronunciation respelling key"><i title="English pronunciation respelling"><span style="font-size:90%">LIN</span>-əks</i></a>)<sup id="cite_ref-pronunciation-2_11-0" class="reference"><a href="#cite_note-pronunciation-2-11">[9]</a></sup><sup id="cite_ref-Foldoc09Jun06_12-0" class="reference"><a href="#cite_note-Foldoc09Jun06-12">[10]</a></sup> is a family of <a href="/wiki/Free_and_open-source_software" title="Free and open-source software">open source</a> <a href="/wiki/Unix-like" title="Unix-like">Unix-like</a> <a href="/wiki/Operating_system" title="Operating system">operating systems</a> based on the <a href="/wiki/Linux_kernel" title="Linux kernel">Linux kernel</a>,<sup id="cite_ref-13" class="reference"><a href="#cite_note-13">[11]</a></sup> an <a href="/wiki/Kernel_(computing)" class="mw-redirect" title="Kernel (computing)">operating system kernel</a> first released on September 17, 1991, by <a href="/wiki/Linus_Torvalds" title="Linus Torvalds">Linus Torvalds</a>.<sup id="cite_ref-14" class="reference"><a href="#cite_note-14">[12]</a></sup><sup id="cite_ref-15" class="reference"><a href="#cite_note-15">[13]</a></sup><sup id="cite_ref-16" class="reference"><a href="#cite_note-16">[14]</a></sup> Linux is typically <a href="/wiki/Package_manager" title="Package manager">packaged</a> in a <a href="/wiki/Linux_distribution" title="Linux distribution">Linux distribution</a>.'
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