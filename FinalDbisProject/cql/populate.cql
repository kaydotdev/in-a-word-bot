INSERT INTO "LectureBotDBIS"."UserLectures"
(
login,
role_name,
password_hash,
lecture_status,
lecture_header,
lecture_content
)
VALUES
(
'linus__torvalds',
'admin',
textAsBlob('af808f1169889895fd2bc8abd3fea576cb3c884ffe7473cea841eefd7b569625'),
'Pending',
'The Future of Open Source Is So Bright!',
'We began by asking, "What’s the future of Open Source software from your perspective?" Here’s what they told us: "Growth": Very bright: Docker has radically changed the way OSS is consumed, and now it’s very simple to distribute OSS to a wider audience. It will continue to accelerate and be integrated in different ways to solve problems and achieve results. Start caring about upgrades. Data shows people don’t upgrade and this results in tremendous liability. Some companies have an effort to look inside and start licensing components by hand to look at risk and to know what’s going on. Security and legal need to work together to assess risk.'
);

INSERT INTO "LectureBotDBIS"."UserLectures"
(
login,
lecture_status,
lecture_header,
lecture_content
)
VALUES
(
'linus__torvalds',
'Pending',
'Main reasons why Linux is the best OS!',
'Main reasons why Linux is the best OS: 1) In Linux user has access to the source code of kernel and alter the code according to his need. It has its own advantages like bugs in OS will fix at a rapid pace and disadvantages like developers may take advantage of any weakness in OS if they found. 2) Linux has various distributions which are highly customizable based on user needs. 3) In Linux with GPL- Licensed operating system, users are free to modify the software, can re-use in any number of systems and even they can sell the modified version. 4) Linux is more secure than windows where hackers or developers of viruses will find difficult to break through Linux. 5) All software in Linux is free!'
);

INSERT INTO "LectureBotDBIS"."Resources"
(
login,
url,
description,
times_visited
)
VALUES
(
'linus__torvalds',
'https://en.wikipedia.org/wiki/Linux',
'Main reasons why Linux is the best OS!',
1
);

INSERT INTO "LectureBotDBIS"."Resources"
(
login,
url,
description,
times_visited
)
VALUES
(
'linus__torvalds',
'http://www.linuxandubuntu.com/home/10-reasons-why-linux-is-better-than-windows',
'10 Reasons Why Linux Is Better Than Windows',
1
);