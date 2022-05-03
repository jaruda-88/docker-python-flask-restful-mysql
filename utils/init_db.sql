-- use project1;

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
    title VARCHAR(100) NOT NULL COMMENT '제목',
    content LONGTEXT NULL COMMENT '내용',
    create_at DATETIME NULL COMMENT '생성날짜',
    update_at DATETIME NULL COMMENT '수정날짜',
    PRIMARY KEY(id)
)ENGINE=INNODB;

ALTER TABLE tb_board COMMENT '게시판 테이블';

CREATE TABLE IF NOT EXISTS tb_board_comment(
    id INT NOT NULL AUTO_INCREMENT COMMENT 'PK',
    user_id INT NOT NULL COMMENT 'board id',
    board_id INT NOT NULL COMMENT 'board id',
    content VARCHAR(100) NOT NULL COMMENT '내용',
    create_at DATETIME NULL COMMENT '생성날짜',
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES tb_user(id),
    FOREIGN KEY(board_id) REFERENCES tb_board(id) ON DELETE CASCADE
)ENGINE=INNODB;

ALTER TABLE tb_board_comment COMMENT '게시판 댓글 테이블';
