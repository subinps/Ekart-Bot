import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import os

API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
EKART_API_URL=os.environ.get("EKART_API_URL", "")

HOME_TEXT = "Helo, [{}](tg://user?id={})\n\nThis is a simple bot by [SUBIN](tg://user?id=1494078019) written in Python to track shipments shipped through Ekart Logistics.\n\nSend me a tracking ID to proceed."

bot = Client(
    "Ekart",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    workers=10
    )
@bot.on_message(filters.command("start") & filters.private)
async def start(bot, cmd):
    await cmd.reply_text(
        HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id), 
        parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("👨🏼‍💻 Developer", url='https://t.me/subinps'),
						InlineKeyboardButton("⚙️ Update Channel", url="https://t.me/subin_works/84")
					],
                    [
                        InlineKeyboardButton("👨🏼‍🦯How To Use", callback_data="help"),
                        InlineKeyboardButton("🧩 Source Code", url="https://github.com/subinps/Ekart-Bot")


                    ]
					
				]
			)
		)
@bot.on_callback_query()
async def cb_handler(bot: Client, query: CallbackQuery):
    if query.data=="help":
        await query.message.edit_text("Nothing much to do.\n\nJust send a Ekart tracking ID")

@bot.on_message(filters.text & filters.private & filters.incoming)
async def start(bot, cmd):         
    trid=cmd.text
    if trid.startswith("OD"):
        await cmd.reply_text("This is your Flipkart Order ID, Not Ekart Tracking ID.\nSend me the tracking ID")
        return
    msg=await cmd.reply_text("Fetching Details from Ekart...")
    response = requests.get(f"{EKART_API_URL}/check?id={trid}")
    s=response.json()
    p=s["success"]
    if p==False:
        await msg.edit("🤔 The given ID is Invalid, Kindly recheck and send again.")
        return
    else:
        id=s["tracking_id"]
        merchant=s["merchant_name"]
        status=s["order_status"]
        dtime=s["time"]
        tr=""
        detail=s["updates"]
        for m in detail:
            d=m["Date"]
            t=m["Time"]
            p=m["Place"]
            k=m["Status"]
            s=f"🔸{d}: {t} - Place: {p} - {k}\n"
            tr+=s
        await msg.edit(f"<b>Here is the tracking updates for Tracking ID 👉 {id}</b>\n\nMerchant Name :  {merchant}\n\nOrder Status : {status}\n\nDelivery Time :  {dtime}\n\n<b>Detailed Updates</b> 👇\n\n<code>{tr}</code>")

bot.run()