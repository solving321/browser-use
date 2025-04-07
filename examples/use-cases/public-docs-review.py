import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import Agent
from pydantic import SecretStr

load_dotenv()

import asyncio

task = """
Navigate to 'https://www.browserstack.com/docs/accessibility/rules/a11y-engine/3.6/keyboard-focus-visible' and review the documentation with the following criteria:

1. Evaluate if the content is appropriate for the target audience (individuals and QA teams with limited accessibility knowledge)
2. Check if the rule examples are clear and helpful
3. Assess if the "How to fix" instructions are practical and easy to follow
4. Determine if the overall content is easy to understand
5. Check if the documentation is appropriately concise and to-the-point

Provide an array of specific comments and suggestions that could be included in a documentation review.
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
