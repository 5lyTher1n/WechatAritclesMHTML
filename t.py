from playwright.sync_api import Playwright, sync_playwright, expect
import time


# context = browser.new_context()
#
# # Open new page
# page = context.new_page()
#
# # Go to https://mp.weixin.qq.com/s?__biz=MzIzMTIzNTM0MA==&amp;mid=2247485605&amp;idx=1&amp;sn=082cb4eee3dc245710a02a6d00c1dbf5&amp;chksm=e8a602c6dfd18bd0820086a952721fdfbf74cf900de23625e4c7bb7bb3ab4f848c1bd3499c29&amp;scene=27#wechat_redirect
# page.goto(
#     "https://mp.weixin.qq.com/s?__biz=MzIzMTIzNTM0MA==&amp;mid=2247485605&amp;idx=1&amp;sn=082cb4eee3dc245710a02a6d00c1dbf5&amp;chksm=e8a602c6dfd18bd0820086a952721fdfbf74cf900de23625e4c7bb7bb3ab4f848c1bd3499c29&amp;scene=27#wechat_redirect")
#
# time.sleep(1)
# # Click text=喜欢此内容的人还喜欢
# page.locator("text=喜欢此内容的人还喜欢").click()
#
# # Click #page-content
# page.locator("#page-content").click(button="right")
# time.sleep(1)
# # Press s with modifiers
# page.locator(
#     "body:has-text(\"寻找更多IDOR漏洞的几种方法 迪哥讲事 迪哥讲事 微信号 growing0101 功能介绍 记录自己的成长之路... 2022-06-25 22:33 发表于\")").press(
#     "Control+s")
# time.sleep(1)
# # Close page
# page.close()
#
# # ---------------------
# context.close()
# browser.close()
from playwright.sync_api import sync_playwright
url = "https://mp.weixin.qq.com/s?__biz=MzIzMTIzNTM0MA==&amp;mid=2247485605&amp;idx=1&amp;sn=082cb4eee3dc245710a02a6d00c1dbf5&amp;chksm=e8a602c6dfd18bd0820086a952721fdfbf74cf900de23625e4c7bb7bb3ab4f848c1bd3499c29&amp;scene=27#wechat_redirect"

import asyncio
from playwright.async_api import async_playwright

# async def main():
#     async with async_playwright() as p:
#
#         browser = await p.chromium.launch()
#         page = await browser.new_page()
#         await page.goto(url)
#         locator = page.locator("text=正文结束")
#         # locator.hover()
#         locator.click()
#         await page.screenshot(path=f'example1.png',full_page=True)
#         await browser.close()



with sync_playwright() as p:
    # browser = p.chromium.launch()
    # page = browser.new_page()
    # browser.start_tracing(page)
    # page.goto(url)
    # # page.screenshot(path=f'example-2.png',full_page=True)
    # # locator = page.locator("text=正文结束")
    # # locator.hover()
    # # locator.click()
    # browser.stop_tracing()
    # browser.close()
    browser = p.chromium.launch()
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True)
    page = context.new_page()
    page.goto(url)
    context.tracing.stop(path="trace1.zip")

# asyncio.run(main())
# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     await page.goto(url)
#
#     await page.screenshot(path=f'example.png')
#     await browser.close()
#
#
# with sync_playwright() as playwright:
#     run(playwright)
