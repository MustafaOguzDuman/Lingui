drop table if exists word_to_id;
drop table if exists word_to_video;
drop table if exists caption;

drop sequence word_id_seq;

-- TODO: add foreign key constraints

CREATE SEQUENCE IF NOT EXISTS word_id_seq;

CREATE TABLE IF NOT EXISTS word_strength_due_list (
    user_id INT NOT NULL,
    word_id INT NOT NULL,
    due_date TIMESTAMP NOT NULL,
    strength INT DEFAULT 1,
    PRIMARY KEY (user_id, word_id)
);

CREATE TABLE IF NOT EXISTS word_to_id (
    word VARCHAR(255) PRIMARY KEY NOT NULL,
    word_id INT DEFAULT nextval('word_id_seq') NOT NULL
);

CREATE TABLE IF NOT EXISTS word_to_video (
    word_id INT NOT NULL PRIMARY KEY,
    video_id TEXT[],
    thumbnail TEXT
);

CREATE TABLE IF NOT EXISTS caption (
    video_id TEXT NOT NULL,
    word_id_array INT[],
    start_time FLOAT8 NOT NULL,
    duration FLOAT8 NOT NULL,
    content TEXT NOT NULL,
    thumbnail TEXT NOT NULL,
    PRIMARY KEY (video_id, start_time)
);