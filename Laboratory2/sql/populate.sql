-- "Role" entity population

INSERT INTO "Role" ("Name", "Priority")
VALUES ('Manager', 2);

INSERT INTO "Role" ("Name", "Priority")
VALUES ('Default user', 4);

INSERT INTO "Role" ("Name", "Priority")
VALUES ('Premium user', 3);

INSERT INTO "Role" ("Name", "Priority")
VALUES ('Admin', 1);

-- "User" entity population
-- Crypt algo: HMAC-SHA256

INSERT INTO "User" ("Login", "RoleId", "PasswordHash", "RegistrationDate")
VALUES ('linus__torvalds', 4, '27157b4ee5a86bca3bd23a7fbfd8322f395200739da842b9908bb4882ae17e4b', '2019-10-24'); -- linux4legends

INSERT INTO "User" ("Login", "RoleId", "PasswordHash", "RegistrationDate")
VALUES ('andersHejlsberg', 4, 'c1198918dc5ff12860c4ab004e84b57581ad894cc716cd251fdc0cba58388e27', '2019-10-24'); -- dotnet4legends

INSERT INTO "User" ("Login", "RoleId", "PasswordHash", "RegistrationDate")
VALUES ('an0nimus', 2, '6eb8d9cc4f3f62143c364321e6dbbbd9174f66a17fb5a98d770414a8080b8893', '2019-10-24'); -- thequiteryoubecome...

INSERT INTO "User" ("Login", "RoleId", "PasswordHash", "RegistrationDate")
VALUES ('elliot_alderson', 3, '1dea63a84d480f73d2a965a98acb38b6497af27fefb94f809f263709b325fefb', '2019-10-24'); -- imcrazyimcrazyimcrazy

-- "Lecture" entity population

INSERT INTO "Lecture" ("UserLogin", "Header", "Content")
VALUES ('linus__torvalds', 'The Future of Open Source Is So Bright!', 'We began by asking, "What’s the future of Open Source software from your perspective?" Here’s what they told us: "Growth": Very bright: Docker has radically changed the way OSS is consumed, and now it’s very simple to distribute OSS to a wider audience. It will continue to accelerate and be integrated in different ways to solve problems and achieve results. Start caring about upgrades. Data shows people don’t upgrade and this results in tremendous liability. Some companies have an effort to look inside and start licensing components by hand to look at risk and to know what’s going on. Security and legal need to work together to assess risk.');

INSERT INTO "Lecture" ("UserLogin", "Header", "Content")
VALUES ('linus__torvalds', 'Main reasons why Linux is the best OS!', 'Main reasons why Linux is the best OS: 1) In Linux user has access to the source code of kernel and alter the code according to his need. It has its own advantages like bugs in OS will fix at a rapid pace and disadvantages like developers may take advantage of any weakness in OS if they found. 2) Linux has various distributions which are highly customizable based on user needs. 3) In Linux with GPL- Licensed operating system, users are free to modify the software, can re-use in any number of systems and even they can sell the modified version. 4) Linux is more secure than windows where hackers or developers of viruses will find difficult to break through Linux. 5) All software in Linux is free!');

INSERT INTO "Lecture" ("UserLogin", "Header", "Content")
VALUES ('an0nimus', 'NoSQL and Cassandra', 'What is Cassandra? The Apache Cassandra database is the right choice when you need scalability and high availability without compromising performance. Linear scalability and proven fault-tolerance on commodity hardware or cloud infrastructure make it the perfect platform for mission-critical data. Cassandra’s support for replicating across multiple datacenters is best-in-class, providing lower latency for your users and the peace of mind of knowing that you can survive regional outages.');

INSERT INTO "Lecture" ("UserLogin", "Header", "Content")
VALUES ('elliot_alderson', 'Top 25 Kali Linux Penetration Testing Tools', 'Kali Linux is an open source distribution based on Debian focused on providing penetration testing and security auditing tools. Actively developed by Offensive Security, it’s one of the most popular security distributions in use by infosec companies and ethical hackers. One of the best things about Kali is the fact that it doesn’t require you to install the OS in your hard drive — it uses a live image that can be loaded in your RAM memory to test your security skills with the more than 600 ethical hacking tools it provides. It includes numerous security-hacker tools for information gathering, vulnerability analysis, wireless attacks, web applications, exploitation tools, stress testing, forensic tools, sniffing and spoofing, password cracking, reverse engineering, hardware hacking and much more. We’ve previously explored the Top 20 OSINT Tools available, and today we’ll go through the list of top-used Kali Linux software.');

-- "Resource" entity population

INSERT INTO "Resource" ("URL", "Description", "TimesVisited")
VALUES ('https://en.wikipedia.org/wiki/Linux', 'Wikipedia: Linux', 2);

INSERT INTO "Resource" ("URL", "Description", "TimesVisited")
VALUES ('http://cassandra.apache.org', 'Apache Cassandra', 1);

INSERT INTO "Resource" ("URL", "Description", "TimesVisited")
VALUES ('https://securitytrails.com/blog/kali-linux-penetration-testing-tools', 'Top 25 Kali Linux Penetration Testing Tools', 1);

INSERT INTO "Resource" ("URL", "Description", "TimesVisited")
VALUES ('http://www.linuxandubuntu.com/home/10-reasons-why-linux-is-better-than-windows', '10 Reasons Why Linux Is Better Than Windows', 1);

INSERT INTO "Resource" ("URL", "Description", "TimesVisited")
VALUES ('https://msdn.microsoft.com/ru-ru/', 'MSDN – сеть разработчиков Microsoft', 1);

-- "UserHasResources" entity population

INSERT INTO "UserHasResources" ("UserLogin", "ResourceURL")
VALUES ('linus__torvalds', 'https://en.wikipedia.org/wiki/Linux');

INSERT INTO "UserHasResources" ("UserLogin", "ResourceURL")
VALUES ('an0nimus', 'https://en.wikipedia.org/wiki/Linux');

INSERT INTO "UserHasResources" ("UserLogin", "ResourceURL")
VALUES ('linus__torvalds', 'http://www.linuxandubuntu.com/home/10-reasons-why-linux-is-better-than-windows');

INSERT INTO "UserHasResources" ("UserLogin", "ResourceURL")
VALUES ('andersHejlsberg', 'https://msdn.microsoft.com/ru-ru/');

INSERT INTO "UserHasResources" ("UserLogin", "ResourceURL")
VALUES ('elliot_alderson', 'https://securitytrails.com/blog/kali-linux-penetration-testing-tools');

-- "Component" entity population

INSERT INTO "Component" ("ResourceURL", "Tag", "Inner")
VALUES ('https://en.wikipedia.org/wiki/Linux', 'h1', 'Linux');

INSERT INTO "Component" ("ResourceURL", "Tag", "Inner")
VALUES ('https://en.wikipedia.org/wiki/Linux', 'p', 'Linux (/ˈlɪnəks/ (About this soundlisten) LIN-əks)[9][10] is a family of open source Unix-like operating systems based on the Linux kernel');

INSERT INTO "Component" ("ResourceURL", "Tag", "Inner")
VALUES ('http://cassandra.apache.org', 'h6', 'Apache Cassandra');

INSERT INTO "Component" ("ResourceURL", "Tag", "Inner")
VALUES ('http://cassandra.apache.org', 'p', 'The Apache Cassandra database is the right choice when you need scalability and high availability without compromising performance.');

-- "Attribute" entity population

INSERT INTO "Attribute" ("ComponentId", "Key", "Value")
VALUES (1, 'href', '/wiki/Linux_kernel');

INSERT INTO "Attribute" ("ComponentId", "Key", "Value")
VALUES (1, 'title', 'Linux kernel');

INSERT INTO "Attribute" ("ComponentId", "Key", "Value")
VALUES (3, 'href', 'http://techblog.netflix.com/2011/11/benchmarking-cassandra-scalability-on.html');

INSERT INTO "Attribute" ("ComponentId", "Key", "Value")
VALUES (4, 'class', 'lead');
