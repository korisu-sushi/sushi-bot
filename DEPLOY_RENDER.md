# Деплой Sushi Bot на Render

## Подготовка репозитория

1. Убедитесь, что проект загружен на GitHub/GitLab

2. Создайте файл `render.yaml` в корне проекта (опционально, для Blueprint):
```yaml
services:
  - type: worker
    name: sushi-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot.py
    envVars:
      - key: BOT_TOKEN
        sync: false
      - key: GOOGLE_SPREADSHEET_ID
        sync: false
      - key: ORDERS_CHANNEL_ID
        sync: false
      - key: ENVIRONMENT
        value: production
```

## Деплой на Render

### Шаг 1: Создание сервиса

1. Зайдите на [render.com](https://render.com) и авторизуйтесь
2. Нажмите **New** → **Background Worker**
   > Важно: выбирайте **Background Worker**, не Web Service (бот использует polling, а не webhook)

### Шаг 2: Подключение репозитория

1. Выберите **Connect a repository**
2. Подключите GitHub/GitLab если ещё не подключен
3. Найдите и выберите репозиторий `sushi_bot`

### Шаг 3: Настройка сервиса

Заполните параметры:

| Параметр | Значение |
|----------|----------|
| **Name** | `sushi-bot` (или любое другое) |
| **Region** | Frankfurt (EU) или ближайший к вам |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |

### Шаг 4: Переменные окружения

Нажмите **Advanced** → **Add Environment Variable** и добавьте:

| Key | Value | Обязательно |
|-----|-------|-------------|
| `BOT_TOKEN` | Токен от @BotFather | Да |
| `ENVIRONMENT` | `production` | Да |
| `GOOGLE_SPREADSHEET_ID` | ID вашей Google таблицы | Нет |
| `ORDERS_CHANNEL_ID` | ID Telegram канала для уведомлений | Нет |
| `MIN_ORDER_AMOUNT` | `15` | Нет |
| `DELIVERY_FEE` | `15` | Нет |
| `FREE_DELIVERY_THRESHOLD` | `75` | Нет |

### Шаг 5: Google Credentials (если используете Google Sheets)

Для работы с Google Sheets нужно добавить credentials:

**Вариант 1: Через переменную окружения**

1. Откройте файл `credentials/service_account.json`
2. Скопируйте всё содержимое
3. Добавьте переменную `GOOGLE_CREDENTIALS_JSON` со значением JSON
4. Измените код в `config.py` для чтения из переменной (потребует доработки)

**Вариант 2: Через Secret File**

1. В настройках сервиса найдите **Secret Files**
2. Нажмите **Add Secret File**
3. Filename: `credentials/service_account.json`
4. Вставьте содержимое JSON файла

### Шаг 6: Запуск

1. Нажмите **Create Background Worker**
2. Дождитесь завершения билда (2-5 минут)
3. Проверьте логи во вкладке **Logs**

## Проверка работы

В логах должно появиться:
```
INFO | Starting bot in Environment.PRODUCTION mode
INFO | Bot: @korisu_bot (Korisu)
INFO | Starting polling...
```

Откройте Telegram и отправьте `/start` вашему боту.

## Управление

- **Логи**: вкладка Logs в панели сервиса
- **Перезапуск**: Manual Deploy → Deploy latest commit
- **Остановка**: Settings → Delete Service (или Suspend)

## Стоимость

- **Free tier**: 750 часов/месяц (достаточно для одного бота 24/7)
- Background Worker на Free tier может "засыпать" при неактивности
- Для стабильной работы рекомендуется план **Starter** ($7/месяц)

## Решение проблем

### Бот не запускается
- Проверьте логи на наличие ошибок
- Убедитесь что `BOT_TOKEN` указан правильно

### TelegramConflictError
- Остановите все другие экземпляры бота (локально или на других хостингах)
- Один токен = один запущенный экземпляр

### Google Sheets не работает
- Проверьте что `service_account.json` добавлен в Secret Files
- Убедитесь что сервисный аккаунт имеет доступ к таблице

### Бот засыпает
- Free tier имеет ограничения по времени работы
- Рассмотрите переход на платный план или используйте webhook вместо polling
