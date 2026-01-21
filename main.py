import asyncio, random, os, time
from datetime import datetime
from telegram import Bot
import aiohttp

BOT_TOKEN = os.getenv("BOT_TOKEN", "8475807409:AAHNj5nCT4BnwOrMSHoviStSUDgRwn_QO4g")
CHANNEL_USERNAME = os.getenv("CHANNEL", "@MobWallpaper4k")
PEXELS_API_KEY = os.getenv("PEXELS_KEY", "uqqElRhVr61sx6K5VZUeyml919lAutZKeaFG3L52ALWkzl6HprAAs9Pu")

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
        
        print(f"🔍 البحث عن: {cat}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers, timeout=30) as r:
                    if r.status == 200:
                        data = await r.json()
                        if data.get("photos") and len(data["photos"]) > 0:
                            photo = random.choice(data["photos"])
                            img_url = photo["src"]["large2x"]
                            print(f"✅ وجدت صورة من {cat}")
                            
                            async with session.get(img_url, timeout=30) as img_r:
                                if img_r.status == 200:
                                    img_data = await img_r.read()
                                    print(f"✅ تم التحميل - {len(img_data)/1024:.1f}KB")
                                    return img_data, cat
                    
                    print(f"⚠️ استجابة غير متوقعة: {r.status}")
        except Exception as e:
            print(f"❌ خطأ في التحميل: {e}")
        
        return None, None
    
    async def post(self):
        try:
            img, cat = await self.get_wallpaper()
            if not img:
                print("❌ فشل التحميل، إعادة المحاولة...")
                return False
            
            # حفظ مؤقت
            filename = f"wallpaper_{int(time.time())}.jpg"
            with open(filename, 'wb') as f:
                f.write(img)
            
            # إنشاء الوصف
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
            
            print(f"📤 نشر في القناة...")
            
            # النشر
            with open(filename, 'rb') as photo:
                await self.bot.send_photo(
                    chat_id=CHANNEL_USERNAME,
                    photo=photo,
                    caption=caption
                )
            
            # حذف الملف
            os.remove(filename)
            
            self.count += 1
            print(f"✅ نشر بنجاح! المجموع: {self.count}")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"❌ خطأ في النشر: {e}")
            return False
    
    async def run(self):
        print("\n" + "╔" + "="*48 + "╗")
        print("║" + " "*12 + "🤖 بوت خلفيات الموبايل" + " "*12 + "║")
        print("╚" + "="*48 + "╝\n")
        print(f"📢 القناة: {CHANNEL_USERNAME}")
        print(f"⏰ النشر: كل 3 ساعات")
        print(f"🎨 المصدر: Pexels API")
        print(f"🚀 البوت جاهز!\n")
        print("="*50)
        
        # نشر أول خلفية
        print("\n🎬 نشر أول خلفية...")
        await self.post()
        
        # حلقة النشر
        while True:
            try:
                print(f"\n💤 السكون لمدة 3 ساعات...\n")
                await asyncio.sleep(10800)  # 3 ساعات
                
                success = await self.post()
                
                # إذا فشل، انتظر 5 دقائق وحاول مرة أخرى
                if not success:
                    print("⏳ إعادة المحاولة بعد 5 دقائق...")
                    await asyncio.sleep(300)
                    await self.post()
                    
            except Exception as e:
                print(f"\n❌ خطأ في الحلقة: {e}")
                print("🔄 إعادة المحاولة بعد دقيقة...")
                await asyncio.sleep(60)

if __name__ == "__main__":
    print("🚀 بدء تشغيل البوت...")
    try:
        bot = WallpaperBot()
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\n\n👋 توقف البوت!")
    except Exception as e:
        print(f"\n❌ خطأ قاتل: {e}")
```

**اضغط Commit changes**

