from pyrogram import Client, enums
import random
import time
import cfg
import os

start_print = '''
-----------------------------------
User Tag Telegram
(Тегает всех в чате)
-----------------------------------
'''
print(start_print)
print("Наши паблики: \n\thttps://vk.com/opolchenie_rf\n\thttps://vk.com/alliance_antifurry_klm")


def get_list(f_name):
    return [row for row in open(f_name, encoding="utf-8").read().split("\n") if row]

app = Client(
    "alice",
    api_id=cfg.api_id, api_hash=cfg.api_hash
)


app.start()
dialogs = [dialog for dialog in app.get_dialogs(limit=20) if dialog.chat.id < 0]
x = 1
for dialog in dialogs:
    print(f"{x}. Айди чата: {dialog.chat.id}\t Название чата: {dialog.chat.title}\t Количество участников: {dialog.chat.members_count}")
    print("============================")
    x += 1
chat_id = dialogs[int(input())-1].chat.id
print(chat_id)
bad_list = []
my_id = app.get_me().id
members = [member for member in app.get_chat_members(chat_id, limit=20) if member.user.id != my_id]
x = 1
while True:
    for member in members:
        u_info = member.user
        first_name = u_info.first_name
        last_name = u_info.last_name
        if not last_name:
            last_name = ""
        print(f"{x}. Айди участника: {u_info.id}\t Имя: {first_name} {last_name}")
        x += 1
    x = 1
    user_ch = int(input("\n0. Запустить!\n"))
    if user_ch == 0:
        break
    else:
        bad_id = members[user_ch-1].user.id
        bad_list.append(bad_id)
    print(f"Список выбранных айдишников {bad_list}")

words = get_list("sentences.txt")
push_text = get_list("push_text.txt")
chat_check = list(range(10))
photos = os.listdir("photos")


while True:
    try:
        word = random.choice(words)
        push = random.choice(push_text)
        bad_id = random.choice(bad_list)
        msg = f"<a href='tg://user?id={bad_id}'>{push}</a> {word}"
        ch = random.choice(chat_check)
        if ch == 5 and cfg.chat_name:
            chat = app.get_chat(chat_id)
            title = chat.title
            if title != cfg.chat_name:
                app.set_chat_title(chat_id, cfg.chat_name)
                app.delete_chat_photo(chat_id)
        if photos:
            app.send_chat_action(chat_id, enums.ChatAction.UPLOAD_PHOTO)
            time.sleep(cfg.send_time)
            photo = f"photos/{random.choice(photos)}"
            app.send_photo(chat_id, photo, caption=msg, parse_mode=enums.ParseMode.HTML)
        else:
            app.send_chat_action(chat_id, enums.ChatAction.TYPING)
            time.sleep(cfg.send_time)
            app.send_message(chat_id, msg, parse_mode=enums.ParseMode.HTML)
    except KeyboardInterrupt:
        break
    except:
        pass
    
    
app.stop()
