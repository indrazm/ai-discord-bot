from openai import AsyncOpenAI

from app.core.settings import settings

openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
