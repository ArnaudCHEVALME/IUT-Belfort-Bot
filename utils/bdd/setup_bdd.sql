# DROP TABLE IF EXISTS POLLS;
# DROP TABLE IF EXISTS DEVOIRS;
# DROP TABLE IF EXISTS SUBJECTS;
# DROP TABLE IF EXISTS GUILDS;
CREATE TABLE IF NOT EXISTS GUILDS(
    guild_id INT AUTO_INCREMENT,
    guild_discord_id VARCHAR(100),
    PRIMARY KEY (guild_id)
);
CREATE TABLE IF NOT EXISTS SUBJECTS(
    subject_id INT AUTO_INCREMENT,
    subject_name VARCHAR(50),
    PRIMARY KEY (subject_id)
);
CREATE TABLE if NOT EXISTS DEVOIRS(
    devoir_id INT AUTO_INCREMENT,
    subject_id INT,
    devoir_name VARCHAR(100),
    devoir_due_time DATE,
    guild_id INT,
    PRIMARY KEY (devoir_id),
    FOREIGN KEY (subject_id) REFERENCES SUBJECTS(subject_id),
    FOREIGN KEY (guild_id) REFERENCES GUILDS(guild_id)
);
CREATE TABLE if NOT EXISTS POLLS(
    poll_id INT AUTO_INCREMENT,
    message_id VARCHAR(100),
    guild_id INT,
    PRIMARY KEY (poll_id),
    FOREIGN KEY (guild_id) REFERENCES GUILDS(guild_id)
);
INSERT INTO SUBJECTS (subject_name)
VALUES ('Web');
INSERT INTO SUBJECTS (subject_name)
VALUES ('Qualité Dev');
INSERT INTO SUBJECTS (subject_name)
VALUES ('Communication');
INSERT INTO SUBJECTS (subject_name)
VALUES ('Crypto');
INSERT INTO SUBJECTS (subject_name)
VALUES ('Anglais');