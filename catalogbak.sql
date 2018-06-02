BEGIN TRANSACTION;
CREATE TABLE category (
	id INTEGER NOT NULL, 
	title VARCHAR(40) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO category VALUES(1,'Ties');
INSERT INTO category VALUES(2,'Jackets');
INSERT INTO category VALUES(3,'Underpants');
CREATE TABLE item (
	id INTEGER NOT NULL, 
	title VARCHAR(60) NOT NULL, 
	description VARCHAR(500), 
	category_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES category (id)
);
INSERT INTO item VALUES(1,'Red Striped','Text text for fancy red  striped tie.',1);
INSERT INTO item VALUES(2,'Blue','Fancy Blue description. Twelve  inches long and pointy on the end.',1);
INSERT INTO item VALUES(3,'Purple','Purple tie description.',1);
INSERT INTO item VALUES(4,'Black','Shiny black jacket with zipper and adjustable waist.',2);
INSERT INTO item VALUES(5,'Khakis','Khakis with pleats and loopholes for an amazing belt of your choice!',3);
INSERT INTO item VALUES(6,'Suede','Brown suede with buttons.',2);
COMMIT;

