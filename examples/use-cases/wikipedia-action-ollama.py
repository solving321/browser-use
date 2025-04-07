import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import Agent

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

# Use Ollama with DeepSeek R1 8B model
llm = ChatOllama(
    model='qwen2.5:14b',  # Using DeepSeek Coder 1.3B as it's similar to R1 8B
    num_ctx=16000,  # Setting context window
)

agent = Agent(
    task=task,
    llm=llm,
    use_vision=False,
    browser=browser,
)

async def main():
    await agent.run()
    input('Press Enter to close the browser...')
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
