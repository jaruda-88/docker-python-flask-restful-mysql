use project1;

CREATE TABLE tb_todo (
    id INT AUTO_INCREMENT,
    todo VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
)ENGINE=INNODB;

CREATE TABLE tb_user (
    id INT AUTO_INCREMENT,
    userid VARCHAR(30) NOT NULL,
    username VARCHAR(30),
    pw VARCHAR(100) NOT NULL,
    create_at datetime(6),
    PRIMARY KEY(id)
)ENGINE=INNODB;
/*CREATE DATABASE IF NOT EXISTS project1 default CHARACTER SET UTF8;*/