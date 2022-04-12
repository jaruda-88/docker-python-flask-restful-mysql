use project1;

-- CREATE TABLE IF NOT EXISTS tb_todo(
--     id INT AUTO_INCREMENT,
--     todo VARCHAR(255) NOT NULL,
--     PRIMARY KEY(id)
-- )ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS tb_user(
    id INT NOT NULL AUTO_INCREMENT COMMENT 'PK',
    userid VARCHAR(30) NOT NULL COMMENT '유저 id',
    username VARCHAR(30) NULL COMMENT '유저명',
    pw VARCHAR(100) NOT NULL COMMENT '비밀번호',
    create_at DATETIME NULL COMMENT '생성날짜',
    update_at DATETIME NULL COMMENT '갱신날짜',
    connected_at DATETIME NULL COMMENT '접속날짜',
    activate TINYINT DEFAULT 1 NOT NULL COMMENT 'row 활성화 상태',
    PRIMARY KEY(id)
)ENGINE=INNODB;

ALTER TABLE tb_user COMMENT '유저 테이블';

CREATE TABLE IF NOT EXISTS tb_board(
    id INT NOT NULL AUTO_INCREMENT COMMENT 'PK',
    writer VARCHAR(50) NOT NULL COMMENT '작성자',
    content LONGTEXT NULL COMMENT '내용',
    create_at DATETIME NULL COMMENT '생성날짜',
    update_at DATETIME NULL COMMENT '수정날짜',
    PRIMARY KEY(id)
)ENGINE=INNODB;

ALTER TABLE tb_board COMMENT '게시판 테이블';
