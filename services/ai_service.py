from openai import AsyncOpenAI
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def get_ai_response(messages, model="gpt-4o"):
    response = await client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

async def analyze_image(image_url, prompt):
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ],
            }
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content
