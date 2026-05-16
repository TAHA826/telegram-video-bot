import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from yt_dlp import YoutubeDL

TOKEN = "8747469017:AAFidiOa4Law82uPfHDEAOxElIzRGhXjX9U"

bot = Bot(token=TOKEN)
dp = Dispatcher()

os.makedirs("downloads", exist_ok=True)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("ارسل رابط الفيديو 🎥")

@dp.message()
async def download(message: Message):
    url = message.text

    msg = await message.answer("جاري التحميل...")

    try:
        opts = {
            "format": "mp4",
            "outtmpl": "downloads/%(title)s.%(ext)s"
        }

        loop = asyncio.get_event_loop()

        def run():
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)

        file_path = await loop.run_in_executor(None, run)

        await message.answer_video(
            video=FSInputFile(file_path)
        )

        os.remove(file_path)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(str(e))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())