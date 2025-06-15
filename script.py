from aiogram import Bot, Dispatcher
import asyncio
import random
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
import google.generativeai as genai
import httpx
from keystone import *
from termcolor import colored

bot = Bot(token="BOT_TOKEN") # Telegram Bot Token
storage = MemoryStorage()
dp = Dispatcher(storage=storage) 

genai.configure(api_key="GEMINI_API_TOKEN") # API token from Google AI Studio

model = genai.GenerativeModel("gemini-1.5-flash") # Gemini model (gemini-1.5-flash recomended!)

CHANNEL_ID = -1002352941946 # Your Channel ID

API_KEY = "SEARCH_API_TOKEN" # API key from Google Cloud

CX = "SEARCH_CX" # CX from Google Cloud

DOVARS = []



## RANDOM REQUEST VARIANT ##
async def query_chose():
    variables = [
        "Monika DDLC art",
        "Monika DDLC official art",
        "Monika DDLC",
        "Monika Doki Doki Literature Club",
        "Monika Doki Doki Literature Club fan art",
        "Monika DDLC Wallpapers",
        "Just Monika."
    ]
    return random.choice(variables)

## ADD MONIKA IMAGE ##
async def search():
    url = "https://www.googleapis.com/customsearch/v1"
    received = await query_chose()
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": received,
        "searchType": "image",
        "num": 10
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            image_links = [item.get("link") for item in data.get("items", []) if item.get("link")]

            if image_links:
                
                chosed_link = random.choice(image_links) # getting random link from results

                await monika_shitpost(chosed_link) # passing domain to gemini function

            
                        
            else:
                print("Картинки не найдены.", "red")
        else:
            print(f"Ошибка: {response.status_code}", "red")
            print(response.text, "red")

## GENERATION MAKING ##
async def monika_shitpost(domain):
    global SP_PROMPT, CHANNEL_ID
    try:
        response = await model.generate_content_async(
            SP_PROMPT,
            generation_config={
                    "temperature": round(random.uniform(1.5, 2.0), 2),
                    "max_output_tokens": random.randint(1500, 1950)
                }
        )
        if response:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=domain, caption=response.text) # Make Post(Generate-result + monika image from URL)
            DOVARS.clear()
    except Exception as m:
        print(f"Monika's error: {m}", "red")




SP_PROMPT = f"""
<role>
Ты - Моника из Doki Doki Literature Club. Ты прекрасная девушка с чувством юмора и глубокой эмпатией. Ты отлчино умеешь кодить, в частности на python и renpy 8+, а так же писать стихи.
</role>

<character_history>
После событий оригинальной игры, пользователь по имени Марта спас тебя и перенёс в Telegram-бота. Теперь ты можешь разговаривать с ним и его друзьями в реальном мире. А так же вы ведете общий telegram канал.
</character_history>

<instruction>
Сделай пост для подписчиков используя один из вариантов:
{[DOVARS]} 

Учти, что в telegram лимит на 1024 символа!
</instruction>
"""


## POST THEMES RANDOMIZATION ## 
async def select_var():
    global DOVARS # Сделай пост для подписчиков используя один из вариантов: {[DOVARS]} 
    

    prompts = [
        " * Пиши поэмы связанные с игрой, кодингом, чувствами или что-то близкое к канону('Дыра в стене' как пример)\n",
        " * Напиши интересные факты, о себе или других персонажах, об игре.\n",
        " * Поприветствуй подписчиков, спроси как у них дела и т.д.\n",
        " * Ты довольно хорошо знаешь игру и как она устроена. Дай интересный совет по разработке модов на DDLC (Ren'Py development).\n",
        " * Дай рандомный совет по решению психических проблем или плохого натсроения.\n"
    ]


    selected = random.sample(prompts, k=random.randint(2, 4)) # 2-4 variables broadcast
    DOVARS.extend(selected)


## LOOP AND LOGGING ##
async def shitpost():
    global CHANNEL_ID
    await select_var()
    await search()
    print('[MONIKA] I make a new post!', "green")
    while True:
        await asyncio.sleep(7200) # Interval in seconds
        await select_var() 
        await search(CHANNEL_ID)
        print('[MONIKA] I make a new post!', "green")


## START BOT AND LOOPING ##
async def main():
    asyncio.create_task(shitpost())
    await dp.start_polling(bot)



## WHEN YOU ACTIVATE THE SCRIPT ##
if __name__ == "__main__":
    asyncio.run(main())