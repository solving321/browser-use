import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import Agent
from pydantic import SecretStr

load_dotenv()

import asyncio

task = """
Navigate to 'https://en.wikipedia.org/wiki/Internet' and scroll to the string 'The vast majority of computer'
"""


chrome_binary_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

config = BrowserConfig(
    browser_binary_path=chrome_binary_path,
    headless=False,
    user_data_dir="~/Library/Application Support/Google/Chrome",
    profile_directory="Default",
)

browser = Browser(config=config)
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

agent = Agent(
	task=task,
	llm=llm,
	browser=browser,
)


async def main():
	await agent.run()
	input('Press Enter to close the browser...')
	await browser.close()


if __name__ == '__main__':
	asyncio.run(main())
