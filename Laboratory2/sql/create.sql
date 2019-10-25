CREATE TABLE "Role" (
  "Id" serial NOT NULL,
  "Name" VARCHAR (50) NOT NULL,
  "Priority" INT NOT NULL,
  
  PRIMARY KEY ("Id")
);


CREATE TABLE "User" (
  "Login" VARCHAR (250) NOT NULL,
  "RoleId" INT NOT NULL,
  
  "PasswordHash" TEXT NOT NULL,
  "RegistrationDate" DATE NOT NULL,
  
  PRIMARY KEY ("Login"),
	
  CONSTRAINT "UserToRoleFK" FOREIGN KEY ("RoleId") 
	REFERENCES "Role"("Id") MATCH FULL 
	ON UPDATE NO ACTION 
	ON DELETE NO ACTION 
);


CREATE TABLE "Lecture" (
  "Id" serial NOT NULL,
  "UserLogin" VARCHAR (250) NOT NULL,

  "Header" VARCHAR(250) NOT NULL,
  "Content" VARCHAR(5000) NOT NULL,
	
  PRIMARY KEY ("Id"),

  CONSTRAINT "LectureToUserFK" FOREIGN KEY ("UserLogin") 
	REFERENCES "User"("Login") MATCH FULL 
	ON UPDATE NO ACTION 
	ON DELETE CASCADE
);


CREATE TABLE "Resource" (
  "URL" VARCHAR(2048) NOT NULL,

  "Description" VARCHAR(250) NULL,
  "TimesVisited" INT NOT NULL,
	
  PRIMARY KEY ("URL")
);


CREATE TABLE "UserHasResources" (
  "UserLogin" VARCHAR(250) NOT NULL,
  "ResourceURL" VARCHAR(2048) NOT NULL,
	
  PRIMARY KEY ("UserLogin", "ResourceURL"),
	
  CONSTRAINT "UserHasResourcesToUserFK" FOREIGN KEY ("UserLogin") 
	REFERENCES "User"("Login") MATCH FULL 
	ON UPDATE NO ACTION 
	ON DELETE NO ACTION,
	
  CONSTRAINT "UserHasResourcesToResourcesFK" FOREIGN KEY ("ResourceURL") 
	REFERENCES "Resource"("URL") MATCH FULL 
	ON UPDATE NO ACTION 
	ON DELETE NO ACTION
);


CREATE TABLE "Component" (
  "Id" serial NOT NULL,
  "ResourceURL" VARCHAR(2048) NOT NULL,
	
  "Tag" VARCHAR(250) NOT NULL,
  "Inner" VARCHAR(5000) NULL,
	
  PRIMARY KEY ("Id"),
	
  CONSTRAINT "ComponentToResourcesFK" FOREIGN KEY ("ResourceURL") 
	REFERENCES "Resource"("URL") MATCH FULL 
	ON UPDATE NO ACTION 
	ON DELETE NO ACTION
);


CREATE TABLE "Attribute" (
  "Id" serial NOT NULL,
  "ComponentId" INT NOT NULL,
	
  "Key" VARCHAR(250) NOT NULL,
  "Value" VARCHAR(250) NOT NULL,
	
  PRIMARY KEY ("Id"),
	
  CONSTRAINT "AttributeToComponentFK" FOREIGN KEY ("ComponentId") 
	REFERENCES "Component"("Id") MATCH FULL 
	ON UPDATE NO ACTION 
	ON DELETE CASCADE
);
