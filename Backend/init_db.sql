-- 1. Тестовые пользователи (api_key = name для простоты)
INSERT INTO users (name, api_key) VALUES
(1, 'user1', 'api-key-user1'),
(2, 'user2', 'api-key-user2'),
(3, 'user3', 'api-key-user3'),
(4, 'alice', 'api-key-alice'),
(5, 'bob', 'api-key-bob');

-- 2. Тестовые медиафайлы (только file_path)
INSERT INTO medias (id, file_path) VALUES
(1, './media/test1.jpg'),
(2, './media/test2.png'),
(3, './media/test3.webp');

-- 3. Тестовые твиты с медиа
INSERT INTO tweets (id, content, user_id) VALUES
(1, 'Привет из Twitter Clone! #fastapi', 1),
(2, 'FastAPI + PostgreSQL = ❤️', 2),
(3, 'Docker Compose упрощает деплой!', 3),
(4, 'Твит с картинкой!', 1);

-- 4. Привязка медиа к твитам
INSERT INTO tweet_medias (tweet_id, media_id) VALUES
(4, 1),
(4, 2);

-- 5. Подписки (1 фолловит 2,3; 2↔1; 3→1)
INSERT INTO follows (follower_id, followed_id) VALUES
(1, 2),
(1, 3),
(2, 1),
(3, 1);

-- 6. Лайки (популярность для сортировки ленты)
INSERT INTO likes (user_id, tweet_id) VALUES
-- Твит 1: 2 лайка (user2, user3)
(2, 1),
(3, 1),
-- Твит 2: 3 лайка (самый популярный)
(1, 2),
(3, 2),
(4, 2),
-- Твит 3: 1 лайк
(1, 3);

-- Проверка данных
SELECT 'Users created' as status, count(*) as count FROM users
UNION ALL
SELECT 'Tweets created', count(*) FROM tweets
UNION ALL
SELECT 'Medias created', count(*) FROM medias
UNION ALL
SELECT 'Follows created', count(*) FROM follows
UNION ALL
SELECT 'Likes created', count(*) FROM likes;