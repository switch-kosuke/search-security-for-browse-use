# import logging

# # ロギングを設定
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("browser_use").setLevel(logging.DEBUG)

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()
import os
os.environ["ANONYMIZED_TELEMETRY"] = "false"

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3. ",
        # llm=ChatOpenAI(model="gpt-4o"),
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b")
    )
    await agent.run()

asyncio.run(main())