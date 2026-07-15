# -*- coding: utf-8 -*-
import asyncio
import os
import re
import sys
import uuid
import random
import requests
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from pyvirtualdisplay import Display

# --- ⚙️ CONFIGURATION ---
sys.stdout.reconfigure(encoding='utf-8')
SIGNATURE = "༺ρ 𝕣 ꪜ 𝕣 अब्बू ☽༻"
BASE_TEXT = "ᴘʀᴀᴛɪᴋ-ᴠᴇᴇʀ-ꜱᴜʀᴀᴊ-ɴᴇᴍᴇꜱɪꜱ Ƭяу мσм кє ѕαтн вєᴅ ᴍᴀỉɴ  ᴍᴀsᴛỉ кᴀяυggᴀ"
EMOJIS = ["🔥", "🌟", "✨", "💫", "🚀", "💎", "🌙", "🧿", "🍃", "🦋"]

# --- 🛡️ NAME GUARDIAN ---
async def run_name_guardian(sid, tid, sig):
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0", "X-IG-App-ID": "936619743392459"})
    session.cookies.set("sessionid", sid, domain=".instagram.com")
    while True:
        try:
            resp = session.get(f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/")
            if resp.status_code == 200:
                if resp.json().get("thread", {}).get("thread_title") != sig:
                    csrf = session.cookies.get("csrftoken", "")
                    session.post(f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/update_title/",
                                 data={"title": sig, "_csrftoken": csrf, "_uuid": str(uuid.uuid4())},
                                 headers={"X-CSRFToken": csrf})
        except: pass
        await asyncio.sleep(60)

# --- 🔥 STRIKE ENGINE ---
async def run_strike(cookie, target_id, thread_idx, start_delay):
    # Stagger thread start to avoid API hammering
    await asyncio.sleep(start_delay)
    
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=f"n_{thread_idx}", 
            headless=False, 
            channel="chrome",
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage", "--mute-audio"]
        )
        await Stealth().apply_stealth_async(context)
        page = await context.new_page()
        
        # Block unnecessary resources to load faster
        await page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font"] else route.continue_())
        
        sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
        await context.add_cookies([{'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com', 'path': '/'}])
        
        print(f"[T{thread_idx}] Navigating...")
        # Use domcontentloaded to fix the timeout error
        await page.goto(f"https://www.instagram.com/direct/t/{target_id}/", wait_until="domcontentloaded")
        
        textbox_selector = 'div[role="textbox"][contenteditable="true"]'
        await page.wait_for_selector(textbox_selector, timeout=30000)

        while True:
            try:
                # Reload using domcontentloaded
                await page.reload(wait_until="domcontentloaded")
                await page.wait_for_selector(textbox_selector, timeout=30000)
                
                for i in range(11):
                    if i < 10:
                        text_to_send = ("\n" * 7).join([f"{BASE_TEXT} {random.choice(EMOJIS)}"] * 7)
                    else:
                        text_to_send = SIGNATURE
                    
                    await page.focus(textbox_selector)
                    await page.keyboard.insert_text(text_to_send)
                    await asyncio.sleep(0.003) 
                    await page.keyboard.press("Enter")
                    
                    print(f"[T{thread_idx}] Block {i+1}/11 sent.")
                    await asyncio.sleep(random.uniform(0.3, 0.6)) 
                
            except Exception as e:
                print(f"[T{thread_idx}] Warning: {e}. Resetting...")
                await asyncio.sleep(5)

async def main():
    cookie = os.environ.get("INSTA_COOKIE")
    tid = os.environ.get("TARGET_THREAD_ID")
    
    if cookie and tid:
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        try:
            await asyncio.gather(
                run_name_guardian(cookie, tid, SIGNATURE),
                run_strike(cookie, tid, 1, 0),   # Start thread 1 immediately
                run_strike(cookie, tid, 2, 5)    # Start thread 2 after 5s delay
            )
        finally:
            display.stop()

if __name__ == "__main__":
    asyncio.run(main())
