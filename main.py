from telethon.sync import TelegramClient, events
from collections import defaultdict
import time

# Укажите ваши данные авторизации (номер телефона, код подтверждения и сессионные данные)
api_id = 20288272
api_hash = 'c105f028226982bd7db257ea79c2623b'
phone_number = '79060694044'  # Укажите ваш номер телефона
client = TelegramClient('session_name', api_id, api_hash)

user_states = defaultdict(int)

# Определить заготовленные ответы для каждого состояния пользователя
responses = {
    0: f'Опять привет, [имя пользователя]!), как настроение? ✨',
    1: 'Слушай [имя пользователя], мне нужна твоя помощь! Я в долгу не останусь! 💋 если ты понимаешь о чем я! Поможешь мне?',
    2: 'Я же моделью работаю, у нас сейчас конкурс проходит, сможешь пожалуйста проголосовать за меня? 1 голос 5000сум стоит, если проголосуешь за мной должок!😍 Ссылка - ТЫК',
    3: 'Мне кажется ты еще не проголосовал  😞, мне очень сильно поможет твой голос зайка, как проголосуешь отправь скриншот пожалуйста, а дальше проси всё что хочешь!💋💋'
}
# Обработка входящих сообщений
@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    # Фильтруем сообщения только от пользователя (не от бота) в личные сообщения
    if event.is_private and not (await event.get_sender()).bot:
        sender = await event.get_sender()
        name = sender.first_name
        text = event.message.text
        # Отправляем ответное сообщение от вашего аккаунта
        user_id = event.chat_id

        # Получить состояние пользователя из памяти длинного хранения
        state = user_states[user_id]
        entity = await client.get_entity(user_id)
        user_name = entity.first_name

        # Отправить ответ пользователю на основе его состояния
        response = responses[state].replace('[имя пользователя]', f'{user_name}')
        time.sleep(20)
        await event.respond(response)

        # Обновить состояние пользователя в памяти
        new_state = (state + 1) % 4
        user_states[user_id] = new_state
# Запускаем клиент и ждем сообщений
client.start(phone_number)
client.run_until_disconnected()