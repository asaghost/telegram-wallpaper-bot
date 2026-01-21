import asyncio
import random
import os
import time
from datetime import datetime
from telegram import Bot
import aiohttp

BOT_TOKEN = "8475807409:AAHNj5nCT4BnwOrMSHoviStSUDgRwn_QO4g"
CHANNEL_USERNAME = "@MobWallpaper4k"
PEXELS_API_KEY = "uqqElRhVr61sx6K5VZUeyml919lAutZKeaFG3L52ALWkzl6HprAAs9Pu"

CATEGORIES = ["nature", "space", "city", "ocean", "mountains", "sunset", "cars", "architecture", "forest", "beach", "abstract", "night"]

class WallpaperBot:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.count = 0
        
    async def get_wallpaper(self):
        cat = random.choice(CATEGORIES)
        url = "https://api.pexels.com/v1/search"
        params = {
            "query": f"{cat} wallpaper", 
            "orientation": "portrait", 
            "per_page": 30,
            "page": random.randint(1, 10)
        }
        headers = {"Authorization": PEXELS_API_KEY}
        
        print(f"البحث عن: {cat}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers, timeout=30) as r:
                    if r.status == 200:
                        data = await r.json()
                        if data.get("photos") and len(data["photos"]) > 0:
                            photo = random.choice(data["photos"])
                            img_url = photo["src"]["large2x"]
                            print(f"وجدت صورة")
                            
                            async with session.get(img_url, timeout=30) as img_r:
                                if img_r.status == 200:
                                    img_data = await img_r.read()
                                    print(f"تم التحميل - {len(img_data)/1024:.1f}KB")
                                    return img_data, cat
                    
                    print(f"استجابة: {r.status}")
        except Exception as e:
            print(f"خطأ: {e}")
        
        return None, None
    
    async def post(self):
        try:
            img, cat = await self.get_wallpaper()
            if not img:
                print("فشل التحميل")
                return False
            
            filename = f"wallpaper_{int(time.time())}.jpg"
            with open(filename, 'wb') as f:
                f.write(img)
            
            emoji_map = {
                "nature": "🌿", "space": "🌌", "city": "🌃", "ocean": "🌊",
                "mountains": "🏔️", "sunset": "🌅", "cars": "🚗", "architecture": "🏛️",
                "forest": "🌲", "beach": "🏖️", "abstract": "🎨", "night": "🌙"
            }
            
            emoji = emoji_map.get(cat, "📱")
            caption = f"{emoji} خلفية {cat} حصرية\n\n"
            caption += "🔥 جودة HD فائقة\n"
            caption += f"📥 @MobWallpaper4k\n"
            caption += f"🎯 خلفية #{self.count + 1}"
            
            print(f"نشر في القناة...")
            
            with open(filename, 'rb') as photo:
                await self.bot.send_photo(
                    chat_id=CHANNEL_USERNAME,
                    photo=photo,
                    caption=caption
                )
            
            os.remove(filename)
            
            self.count += 1
            print(f"نشر بنجاح! المجموع: {self.count}")
            return True
            
        except Exception as e:
            print(f"خطأ: {e}")
            return False
    
    async def run(self):
        print("بوت خلفيات الموبايل")
        print(f"القناة: {CHANNEL_USERNAME}")
        print(f"النشر: كل 3 ساعات")
        print(f"جاهز!")
        
        await self.post()
        
        while True:
            try:
                print(f"السكون لمدة 3 ساعات...")
                await asyncio.sleep(10800)
                
                success = await self.post()
                
                if not success:
                    await asyncio.sleep(300)
                    await self.post()
                    
            except Exception as e:
                print(f"خطأ: {e}")
                await asyncio.sleep(60)

if __name__ == "__main__":
    print("بدء التشغيل...")
    try:
        bot = WallpaperBot()
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("توقف!")
    except Exception as e:
        print(f"خطأ: {e}")
