Telegram бот для мониторинга курса двух самых значимых криптовалют на сегодняшний день: Bitcoin & Ethereum <br />
Данные берутся с запросов котировок в гугл по данным криптовалютам <br />
<br />

<br />
Использование с Docker:<br /><br />
<i>Перед запуском docker run в переменную окружения TELEGRAM_API_TOKEN проставить API токен бота <i/><br />
<br />
  <code>sudo docker build -t t-bot-ggtxru .</code><br />
  <code>docker run -e TELEGRAM_API_TOKEN="" t-bot-ggtxru</code>
<br />
<br />
<i>
-d — запуск образа в detached mode

--restart=always — перезагрузка docker-контейнера при сбое

--e DIRECTORY='/tmp/test' — передаём при помощи переменных окружения каталог, который нужно отслеживать

-v /tmp/:/tmp/ — монтируем каталог /tmp в каталог /tmp контейнера Docker
t-bot — имя запускаемого образа
</i>
