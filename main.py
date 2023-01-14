import amanobot
import random
import asyncio
from amanobot.aio.loop import MessageLoop
from amanobot.namedtuple import ReplyKeyboardMarkup, ReplyKeyboardRemove
import psycopg2
from datetime import date

token = "5823459380:AAEEjXYYb-1s_Ifir7rEDCQV2We0mkuikvI"   
DB_URI="postgresql://postgres:P1zFD7DtHd9ggJDBHvJT@containers-us-west-43.railway.app:8037/railway"
bot = amanobot.aio.Bot(token)

conn = psycopg2.connect(DB_URI,sslmode="require")
cur = psycopg2.cursor()
print("connected to db...")

queue = []
occupied = {}

async def handle(msg):
  id = msg['chat']['id']
  if 'text' in msg:
    text = msg['text']
  else:
    if id in occupied :
      if 'photo' in msg:
        captionphoto = msg["caption"] if "caption" in msg else None
        photo = msg['photo'][0]['file_id']
        await bot.sendPhoto(occupied[id], photo, caption=captionphoto)
      if 'video' in msg:
        captionvideo = msg["caption"] if "caption" in msg else None
        video = msg['video']['file_id']
        await bot.sendVideo(occupied[id], video, caption=captionvideo)
      if 'document' in msg:
        captionducument = msg["caption"] if "caption" in msg else None
        document = msg['document']['file_id']
        await bot.sendDocument(occupied[id], document, caption=captionducument)
      if 'audio' in msg:
        captionaudio = msg["caption"] if "caption" in msg else None
        audio = msg['audio']['file_id']
        await bot.sendAudio(occupied[id], audio, caption=captionaudio)
      if 'video_note' in msg:
        video_note = msg['video_note']['file_id']
        await bot.sendVideoNote(occupied[id], video_note)
      if 'voice' in msg:
        captionvoice = msg["caption"] if "caption" in msg else None
        voice = msg['voice']['file_id']
        await bot.sendVoice(occupied[id], voice, caption=captionvoice)
      if 'sticker' in msg:
        sticker = msg['sticker']['file_id']
        await bot.sendSticker(occupied[id], sticker)
      if 'contact' in msg:
        nama = msg["contact"]["first_name"]
        contact = msg['contact']['phone_number']
        await bot.sendContact(occupied[id], contact, first_name=nama, last_name=None)
  if text == "/start" and id not in queue and id not in occupied:
    keyboard = ReplyKeyboardMarkup(keyboard=[['/Male'],['/Female'],['/Neither']], resize_keyboard=True, one_time_keyboard=True)
    await bot.sendMessage(id, "🤖: _Hello new user. Please state your gender._ ", parse_mode= 'Markdown', reply_markup=keyboard)
  if text == "/Male" or text == '/Female' or text == '/Neither':
    ReplyKeyboardRemove(remove_keyboard = True)
    indb=cur.execute("SELECT uid FROM userdata WHERE uid=?",(int(id),)).fetchall()
    gender = text[1]
    if not indb:
      cur.execute("INSERT INTO userdata VALUES (?,?,'N','N',0,?)",(int(id),gender,str(date.today())))
      await bot.sendMessage(id, "🤖: _Thank you. You can now start chatting using menu option Start new chat🟢. Have fun. _", parse_mode= 'Markdown',reply_markup=ReplyKeyboardRemove(remove_keyboard = True))
      print(cur.execute("SELECT * FROM userdata").fetchall())
    else:
      cur.execute("UPDATE userdata SET gender=? WHERE uid=?",(gender,int(id)))
      await bot.sendMessage(id, "🤖:_Gender has been changed._", parse_mode= 'Markdown',reply_markup=ReplyKeyboardRemove(remove_keyboard = True))
      print(cur.execute("SELECT * FROM userdata").fetchall())
  elif text == "/new" and id not in queue and id not in occupied:
    await bot.sendMessage(id, "🤖: _Please wait...finding partner..._", parse_mode= 'Markdown')
    queue.append(id)
    await asyncio.sleep(5)
    if len(queue) <= 1 :
      await asyncio.sleep(10)
      if id in queue :
        await bot.sendMessage(id, "🤖: _Sorry couldnt find partner. Press Start new chat🟢 in menu to try again._", parse_mode= 'Markdown')
        queue.remove(id)
    else:
      queue.remove(id)
      partnerid = random.choice(queue)
      occupied[id]=partnerid
      occupied[partnerid]=id
      queue.remove(partnerid)
      await bot.sendMessage(id, "🤖: _Partner found. Press Exit🔴 in menu to leave chat._", parse_mode= 'Markdown')
      await bot.sendMessage(occupied[id], "🤖: _Partner found. Press Exit🔴 in menu to leave chat._", parse_mode= 'Markdown')
  elif text =='/new' and id in occupied:
    await bot.sendMessage(id, "🤖: _The chat has ended. Finding new partner..._", parse_mode= 'Markdown')
    await bot.sendMessage(occupied[id], "🤖: _The chat has ended. Press Start new chat🟢 in menu to find partner._", parse_mode= 'Markdown')
    occupied.pop(id)
    occupied.pop(occupied[id])
    queue.append(id)
    await asyncio.sleep(5)
    if len(queue) <= 1 :
      await asyncio.sleep(10)
      if id in queue :
        await bot.sendMessage(id, "🤖: _Sorry couldnt find partner. Press Start new chat🟢 in menu to try again._", parse_mode= 'Markdown')
        queue.remove(id)
    else:
      queue.remove(id)
      partnerid = random.choice(queue)
      occupied[id]=partnerid
      occupied[partnerid]=id
      queue.remove(partnerid)
      await bot.sendMessage(id, "🤖: _Partner found say Hi. Press Exit🔴 in menu to leave chat._", parse_mode= 'Markdown')
      await bot.sendMessage(occupied[id], "🤖: _Partner found say Hi. Press Exit🔴 in menu to leave chat._", parse_mode= 'Markdown')
  elif text == "/exit":
    if id in occupied:
      await bot.sendMessage(id, "🤖: _The chat has ended. Press Start new chat🟢 in menu to find partner._", parse_mode= 'Markdown')
      await bot.sendMessage(occupied[id], "🤖: _The chat has ended. Press Start new chat🟢 in menu to find partner._", parse_mode= 'Markdown')
      occupied.pop(occupied[id])
      occupied.pop(id)
    elif id in queue:
      queue.pop()
      await bot.sendMessage(id, "🤖: _Removed from queue. Press Start new chat🟢 in menu to find partner._", parse_mode= 'Markdown')
    else:
      await bot.sendMessage(id, "🤖: _Press Start new chat🟢 in menu to find partner._", parse_mode= 'Markdown')
  elif text == '/gender':
    keyboard = ReplyKeyboardMarkup(keyboard=[['/Male'],['/Female'],['/Neither']], resize_keyboard=True, one_time_keyboard=True)
    await bot.sendMessage(id, "🤖: _Please state your gender._ ", parse_mode= 'Markdown', reply_markup=keyboard)
  elif text == "/premium":
    await bot.sendMessage(id, "🤖: _Premium users will be allowed to choose the gender they want to match with. This feature is currently unavailable but please look forward to it in a couple of days. _", parse_mode= 'Markdown')
  else :
    await bot.sendMessage(occupied[id], text)

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot,handle).run_forever())
print('Listening ...')
loop.run_forever()
