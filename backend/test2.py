import asyncio
import os
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

async def main():
    response = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": "Hello"}
        ]
    )
    print(response.choices[0].message.content)

asyncio.run(main())