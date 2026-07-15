# -*- coding: utf-8 -*-
import asyncio
import os
import re
import random
import sys
import time
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# --- ⚙️ BOLD PILLAR SETTINGS ---
TABS_PER_MACHINE = 2    
PULSE_DELAY = 100       
CYCLE_DURATION = 60     
SESSION_MAX_SEC = 21000 
sys.stdout.reconfigure(encoding='utf-8')

# --- 🎬 AUXILIARY HUMAN BEHAVIOR FLOW (REELS) ---
async def fast_human_behavior_reels(context, machine_id):
    """
    Ek naya temporary tab open karke quick reels simulation run karta hai
    taaki primary task tab disturb na ho.
    """
    print(f"🎬 [Machine {machine_id}] Starting Quick Reels Simulation (Max ~20 Seconds)...")
    try:
        # Naya temporary tab open karna
        reels_page = await context.new_page()
        # Media abort karna taaki load fast ho aur resources save hon
        await reels_page.route("**/*.{png,jpg,jpeg,gif,webp,svg,mp4,woff,woff2,ttf}", lambda route: route.abort())
        
        await reels_page.goto("https://www.instagram.com/reels/", wait_until="commit", timeout=15000)
        await reels_page.wait_for_timeout(random.uniform(1500, 2500))
        
        total_reels = 15
        reels_to_like = random.randint(2, 4)
        like_indices = random.sample(range(1, total_reels + 1), reels_to_like)
        
        for current_reel in range(1, total_reels + 1):
            if current_reel in like_indices:
                # Like karne wali reel par hold (1.5 to 2.5 sec)
                await reels_page.wait_for_timeout(random.uniform(1500, 2500))
                try:
                    # Center screen par double click simulate karna reel like karne ke liye
                    await reels_page.mouse.dblclick(x=200, y=150)
                    print(f"❤️ [Machine {machine_id}] | Reel {current_reel}: Liked.")
                except:
                    pass
                await reels_page.wait_for_timeout(random.uniform(500, 1000))
            else:
                # Normal scrolling reel par hold (0.5 to 1.2 sec)
                await reels_page.wait_for_timeout(random.uniform(500, 1200))
            
            # Simulated Keyboard event next reel par scroll karne ke liye
            await reels_page.keyboard.press("ArrowDown")
            await reels_page.wait_for_timeout(random.uniform(300, 600))
            
        # Task poora hone par temporary tab close karna
        await reels_page.close()
        print(f"✅ [Machine {machine_id}] Reels Simulation Done. Temporary tab closed.")
    except Exception as e:
        print(f"⚠️ [Machine {machine_id}] Reels Simulation bypassed due to context constraint.")

# --- 🔱 MAIN EXECUTION ENGINE ---
async def run_strike(node_id, cookie, target_id, target_name):
    async with async_playwright() as p:
        user_agent = "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
        profile_path = os.path.join(os.getcwd(), f"n_{node_id}")
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=profile_path,
            headless=True,
            user_agent=user_agent,
            viewport={'width': 400, 'height': 300},
            args=[
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-background-timer-throttling",
                "--disable-threaded-scrolling"
            ]
        )

        await Stealth().apply_stealth_async(context)

        sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
        await context.add_cookies([{
            'name': 'sessionid', 'value': sid.strip(), 
            'domain': '.instagram.com', 'path': '/', 'secure': True, 'httpOnly': True
        }])

        # ⚡ PRIMARY INJECTION SCRIPT
        strike_script = """
            (name, delay) => {
                const getBlock = () => {
                    const emojis = ["💙", "❤️", "💚", "💛", "💜", "🖤", "🤍", "🤎", "🧡", "💖"];
                    const currentEmoji = emojis[Math.floor(Math.random() * emojis.length)];
                    const line = "ᴘʀᴀᴛɪᴋ-ᴠᴇᴇʀ-ꜱᴜʀᴀᴊ-ɴᴇᴍᴇꜱɪꜱ 𝚃𝙼𝙺𝙲 " + currentEmoji + "་༘࿐";
                    
                    let text = "";
                    for(let i = 0; i < 10; i++) { 
                        text += line + "\\n\\n\\n\\n"; 
                    }
                    return text;
                }

                const pulse = () => {
                    const box = document.querySelector('div[role="textbox"], [contenteditable="true"]');
                    if (box) {
                        const text = getBlock();
                        const dataTransfer = new DataTransfer();
                        dataTransfer.setData('text/plain', text);
                        
                        const pasteEvent = new ClipboardEvent('paste', {
                            clipboardData: dataTransfer,
                            bubbles: true,
                            cancelable: true
                        });
                        
                        box.focus();
                        box.dispatchEvent(pasteEvent);
                        box.dispatchEvent(new Event('input', { bubbles: true }));
                        
                        setTimeout(() => {
                            const sendBtn = Array.from(document.querySelectorAll('div[role="button"], button')).find(el => 
                                el.textContent === 'Send' || el.innerText === 'Send'
                            );
                            if (sendBtn) {
                                sendBtn.click();
                            } else {
                                const fallbackBtn = document.querySelector('form button[type="button"], div[aria-label="Send"]');
                                if (fallbackBtn) fallbackBtn.click();
                            }
                        }, 200);
                    }
                    setTimeout(() => { requestAnimationFrame(pulse); }, delay);
                }
                pulse();
            }
        """

        elapsed = 0
        last_reels_time = time.time()
        # Reels activation interval dynamic rakhne ke liye random seconds generate karna (5 to 10 minutes)
        next_reels_interval = random.randint(300, 600)

        while elapsed < SESSION_MAX_SEC:
            pages = []
            
            # --- INTERACTION STATE CHECK ---
            current_time = time.time()
            if current_time - last_reels_time >= next_reels_interval:
                # Har machine background me Reels simulation execute karegi
                await fast_human_behavior_reels(context, node_id)
                # Timers ko reset karna agle phase ke liye
                last_reels_time = time.time()
                next_reels_interval = random.randint(300, 600)
            
            # --- MAIN FLOODING TASK ---
            for i in range(TABS_PER_MACHINE):
                pg = await context.new_page()
                await pg.route("**/*.{png,jpg,jpeg,gif,webp,svg,mp4,woff,woff2,ttf}", lambda route: route.abort())
                try:
                    # GitHub Environment variable se automated dynamic routing
                    await pg.goto(f"https://www.instagram.com/direct/t/{target_id}/", wait_until="commit", timeout=15000)
                    await pg.evaluate(strike_script, [target_name, PULSE_DELAY])
                    pages.append(pg)
                except: 
                    pass
            
            await asyncio.sleep(CYCLE_DURATION)
            for pg in pages: 
                try: await pg.close()
                except: pass
            elapsed += CYCLE_DURATION

        await context.close()

async def main():
    cookie = os.environ.get("INSTA_COOKIE")
    target_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "TARGET")
    m_id = os.environ.get("MACHINE_ID", "1")
    if cookie and target_id:
        await run_strike(m_id, cookie, target_id, target_name)

if __name__ == "__main__":
    asyncio.run(main())
    
