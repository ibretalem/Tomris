import os, logging, asyncio

from telegraph import upload_file

from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID","25828762"))
api_hash = os.environ.get("API_HASH","b72c75adf06405b0534294c4fca5cb7a")
bot_token = os.environ.get("TOKEN","7428612133:AAHpsyhTQhlWvP6J48VbfOot86gbcTb1fvU")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

moment_worker = []


#start
@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("^_^ SELAM🤝 BEN GELİŞMEKTE OLAN BİR ETİKET BOTUYUM. n\ BENİ GRUBUNA EKLEMEYİ UNUTMA. ",
                    buttons=(
                      [
                         Button.url('DESTEK ⚙️', 'https://t.me/knsybots'), 
                         Button.url('GELİŞTİRİCİ 📿', 'https://t.me/bykonsey'), 
                      ], 
                      [
                        Button.url('» BENİ GRUBA EKLE «', 'https://t.me/TomrisTaggerBot?startgroup=true'),   
                      ]
                   ), 
                    link_preview=False
                   )

#help
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "Tomris Yardım Menüsü\n\nKOMUTLAR: \n /all : BU KOMUTLA KELİME YAZARAK ETİKETLEYEBİLİRSİN. \n /all SELAM👋 n\ /cancel : BU KOMUTLA SONLANDIRILIR."
  await event.reply(helptext,
                    buttons=(
                      [
                         Button.url('DESTEK ⚙️', 'https://t.me/knsybots'), 
                         Button.url('GELİŞTİRİCİ 📿', 'https://t.me/bykonsey'), 
                      ], 
                      [
                        Button.url('» BENİ GRUBA EKLE «', 'https://t.me/TomrisTaggerBot?startgroup=true'),   
                      ]
                   ), 
                    link_preview=False
                   )

#Wah bhaiya full ignorebazzi

#bsdk credit de dena verna maa chod dege

#tag
@client.on(events.NewMessage(pattern="^/tagall|/call|/tall|/all|#all|@all?(.*)"))
async def mentionall(event):
  global moment_worker
  if event.is_private:
    return await event.respond("BUNU KANAL VEYA GRUBTA KULLAN.!")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("KULLANMAK İÇİN YÖNETİCİ OLMALISIN.!")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("GEÇMİŞ GÖNDERİDEKİ ÜYELERDEN BASSETMİYORUM.!")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("BANA BİR ARGÜMAN VER . ÖRNEK: `/tag SELAM ARKADAŞLAR.`")
  else:
    return await event.respond("MESAJI YANITLAYIN VE BASSETMEK İÇİN BİR METİN VERİN.!")
    
  if mode == "text_on_cmd":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("Stopped!")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    moment_worker.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("Stopped")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


#telegraph 
@client.on(events.NewMessage(pattern="^/t$"))
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply("Desteklenen Bir Medya Dosysı Yanıtla.")
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (
            replied.video
            and replied.video.file_name.endswith(".mp4")
            and replied.video.file_size <= 5242880
        )
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4"),
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await message.reply("DESTEKLENMİYOR 🙁")
        return
    download_location = await client.download_media(
        message=message.reply_to_message,
        file_name="root/downloads/",
    )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.reply(message, text=document)
    else:
        await message.reply(
            f"**Hey You...!\nLoook At This\n\n👉 https://telegra.ph{response[0]}**",
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)



print("BOT ÇALIYOR ✔️ -DESTEĞE KATILIN")
print("¯\_(ツ)_/¯ YARDIM İÇİN  @knsybots")
client.run_until_disconnected()
