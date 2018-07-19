
CREATE TABLE posts ( content TEXT,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL );

UPDATE posts SET content = "cheese" WHERE content LIKE "%spam%";
