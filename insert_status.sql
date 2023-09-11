
INSERT INTO status (number, description)
VALUES (0, 'don`t open'),
       (1, 'opened'),
       (2, 'first try'),
       (3, 'second try'),
       (4, 'third try'),
       (5, 'forth try'),
       (6, 'fifth try'),
       (7, 'finished');

INSERT INTO "group" (label, level, status) VALUES ('group1', 1, true);
INSERT INTO word (word_en, word_ru, example_ru, example_en, group_id, transcription)
VALUES
    ('Apple', 'Яблоко', 'Я люблю есть яблоко.', 'I love to eat apple.', 1, '[ˈæpl]'),
    ('Banana', 'Банан', 'Мне нравится есть банан.', 'I enjoy eating banana.', 1, '[bəˈnænə]'),
    ('Orange', 'Апельсин', 'Апельсин - это цитрусовый фрукт.', 'The orange is a citrus fruit.', 1, '[ˈɔrɪndʒ]'),
    ('Pear', 'Груша', 'Ей нравится есть груши.', 'She likes to eat pears.', 1, '[per]'),
    ('Mandarin', 'Мандарин', 'Мне нравится есть мандарины зимой.', 'I like to eat mandarins in winter.', 1, '[ˌmæn.dəˈrɪn]'),
    ('Dog', 'Собака', 'Моя собака очень дружелюбная.', 'My dog is very friendly.', 1, '[dɔg]'),
    ('Cat', 'Кошка', 'Кошка спит на диване.', 'The cat is sleeping on the couch.', 1, '[kæt]'),
    ('Elephant', 'Слон', 'Слоны - самые крупные сухопутные животные.', 'Elephants are the largest land animals.', 1, '[ˈɛl.ɪ.fənt]'),
    ('Sun', 'Солнце', 'Солнце ярко светит на небе.', 'The sun is shining brightly in the sky.', 1, '[sʌn]'),
    ('Moon', 'Луна', 'Луна видна на ночном небе.', 'The moon is visible in the night sky.', 1, '[muːn]'),
    ('Star', 'Звезда', 'Ночное небо полно звезд.', 'The night sky is full of stars.', 1, '[stɑːr]'),
    ('Planet', 'Планета', 'Земля - это планета в нашей солнечной системе.', 'Earth is a planet in our solar system.', 1, '[ˈplæn.ɪt]'),
    ('Giraffe', 'Жираф', 'У жирафов длинные шеи.', 'Giraffes have long necks.', 1, '[dʒɪˈræf]'),
    ('Tiger', 'Тигр', 'Тигры - мощные хищники.', 'Tigers are powerful predators.', 1, '[ˈtaɪɡər]'),
    ('Lion', 'Лев', 'Львы известны как короли джунглей.', 'Lions are known as the kings of the jungle.', 1, '[ˈlaɪən]'),
    ('Dolphin', 'Дельфин', 'Дельфины - умные морские млекопитающие.', 'Dolphins are intelligent marine mammals.', 1, '[ˈdɒlfɪn]'),
    ('Butterfly', 'Бабочка', 'Бабочки разнообразны по цвету и узору.', 'Butterflies come in various colors and patterns.', 1, '[ˈbʌtərflaɪ]'),
    ('Bird', 'Птица', 'Птицы могут летать в небе.', 'Birds can fly in the sky.', 1, '[bɜːrd]'),
    ('Woman', 'Женщина', 'Сильная и независимая женщина может добиться всего', 'A strong and independent woman can achieve anything.', 1, '[ˈwʊmən]'),
    ('Man', 'Мужчина', 'Он честный мужчина', 'He is an honest man', 1, '[mæn]');