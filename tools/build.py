#!/usr/bin/env python3
"""Build the School Drone site.

Reads src/game.html (the game) and writes index.html, the guide pages in
English (/) and Chinese (/zh/), 404.html and sitemap.xml.

Run from the repo root:  python3 tools/build.py
"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
U = "https://ultralabed.github.io/School-Drone/"
REPO = "https://github.com/ultralabed/School-Drone"
LI = "https://www.linkedin.com/in/edward-shih-43942786"
AUTHOR = {"@type": "Person", "name": "Edward Shih", "sameAs": [LI, "https://github.com/ultralabed"]}
NOTE = f"<!-- School Drone - MIT License - Copyright (c) 2026 Aaron Shih and Edward Shih - {LI} -->"
e = html.escape

def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False) + "\n</script>"

# ------------------------------------------------------------------ game page
GAME = {
    "en": dict(title="School Drone: Free Drone Flying Game for Kids",
               desc="A free browser game for kids. Fly a school drone in a library and let the robot teacher explain how drones go up, down, left, right and hover."),
    "zh": dict(title="學校無人機:免費兒童無人機飛行網頁遊戲",
               desc="免費的兒童網頁遊戲。在圖書館裡飛學校無人機,機器人老師會用簡單的話告訴你無人機怎麼上、下、左、右和懸停。"),
}

def build_index():
    src = (ROOT / "src/game.html").read_text()
    cut = src.index("</style>") + len("</style>\n")
    top = "\n".join(l for l in src[:cut].split("\n") if "claude:viewport-fit-sides" not in l)
    body = src[cut:]
    top = top.replace("<title>School Drone Library</title>", f"<title>{GAME['en']['title']}</title>")
    for lang, old_t, old_d in (("en", "title:'School Drone Library',desc:'A free kids game. Fly a school drone in a library and let the robot teacher explain how drones fly.'", None),
                               ("zh", None, None)):
        pass
    # search titles and descriptions follow the language picked in the game
    import re
    def swap(block_start, lang):
        nonlocal body
        i = body.index(block_start)
        j = body.index("h1:", i)
        new = f"{block_start}title:{json.dumps(GAME[lang]['title'], ensure_ascii=False)},desc:{json.dumps(GAME[lang]['desc'], ensure_ascii=False)},\n "
        body = body[:i] + new + body[j:]
    swap("en:{", "en"); swap("zh:{", "zh")
    game_ld = {"@context": "https://schema.org", "@type": ["VideoGame", "LearningResource"], "name": "School Drone",
               "alternateName": "學校無人機", "url": U, "image": U + "og.png", "description": GAME["en"]["desc"],
               "inLanguage": ["en", "zh-Hant-TW"], "isAccessibleForFree": True, "license": "https://opensource.org/licenses/MIT",
               "genre": "Educational", "gamePlatform": "Web browser", "applicationCategory": "Game", "operatingSystem": "Any",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
               "audience": {"@type": "EducationalAudience", "educationalRole": "student"},
               "teaches": ["How a drone goes up, down, left and right", "What hover means",
                           "Why pilots watch the battery and take turns", "Drone safety near people and walls",
                           "How quadcopters, helicopters and jets fly differently"],
               "author": AUTHOR, "publisher": AUTHOR,
               "contributor": {"@type": "Person", "name": "Aaron Shih", "description": "Original idea"}}
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "School Drone", "alternateName": "學校無人機",
               "url": U, "inLanguage": ["en", "zh-Hant-TW"], "author": AUTHOR}
    head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{NOTE}
<meta name="description" content="{e(GAME['en']['desc'])}">
<meta name="author" content="Aaron Shih and Edward Shih">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#ff8a1f">
<link rel="author" href="{LI}">
<link rel="canonical" href="{U}">
<link rel="alternate" hreflang="en" href="{U}">
<link rel="alternate" hreflang="zh-Hant-TW" href="{U}?lang=zh">
<link rel="alternate" hreflang="x-default" href="{U}">
<link rel="license" href="{REPO}/blob/main/LICENSE">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="School Drone">
<meta property="og:title" content="{e(GAME['en']['title'])}">
<meta property="og:description" content="{e(GAME['en']['desc'])}">
<meta property="og:url" content="{U}">
<meta property="og:image" content="{U}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Kids in a library watch a small orange drone fly above a blue rug.">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="zh_TW">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(GAME['en']['title'])}">
<meta name="twitter:description" content="{e(GAME['en']['desc'])}">
<meta name="twitter:image" content="{U}og.png">
{ld(game_ld)}
{ld(site_ld)}
"""
    (ROOT / "index.html").write_text(head + top + "</head>\n<body>\n" + body + "</body>\n</html>\n")

# ---------------------------------------------------------------- guide pages
CSS = """
:root{--bg:#eaf4f1;--panel:#fff;--ink:#1b2a3a;--muted:#566878;--line:#cfe0d9;--orange:#ff8a1f;--orange-d:#c9620a;--blue:#1f6fc4;
--display:"Baloo 2","PingFang TC","Microsoft JhengHei","Noto Sans TC","Trebuchet MS",system-ui,sans-serif;
--body:"Nunito","PingFang TC","Microsoft JhengHei","Noto Sans TC","Segoe UI",system-ui,sans-serif}
@media (prefers-color-scheme:dark){:root{--bg:#13202b;--panel:#1c2c3a;--ink:#eaf2f6;--muted:#a2b5c3;--line:#31475a;--blue:#7ab8ff;color-scheme:dark}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:18px;line-height:1.6;padding:16px max(16px,env(safe-area-inset-right,0px)) 40px max(16px,env(safe-area-inset-left,0px))}
.wrap{max-width:760px;margin:0 auto}
header{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 20px;margin-bottom:18px}
.logo{font-family:var(--display);font-weight:800;font-size:26px;color:var(--ink);text-decoration:none;line-height:1}
.logo span{color:var(--orange)}
nav{display:flex;flex-wrap:wrap;gap:4px 18px;font-weight:800;font-size:16px}
a{color:var(--blue)}
nav a[aria-current]{color:var(--ink);text-decoration:none}
main{background:var(--panel);border:2px solid var(--line);border-radius:18px;padding:22px clamp(16px,4vw,34px) 28px}
h1{font-family:var(--display);font-weight:800;font-size:clamp(28px,6vw,40px);line-height:1.1;margin:0 0 10px;text-wrap:balance}
h2{font-family:var(--display);font-weight:600;font-size:23px;line-height:1.2;margin:28px 0 6px;text-wrap:balance}
p,ul,ol{margin:0 0 10px}
ul,ol{padding-left:1.3em}
li{margin-bottom:4px}
.lead{font-size:20px;font-weight:700}
table{border-collapse:collapse;width:100%;font-size:17px}
th,td{text-align:left;padding:6px 10px;border-bottom:2px solid var(--line)}
.scroll{overflow-x:auto}
.play{display:inline-block;margin-top:18px;background:var(--orange);color:#231200;font-family:var(--display);font-weight:800;font-size:22px;text-decoration:none;padding:10px 26px;border-radius:14px;border:2px solid var(--orange-d);box-shadow:0 5px 0 var(--orange-d)}
.play:active{transform:translateY(4px);box-shadow:0 1px 0 var(--orange-d)}
a:focus-visible{outline:3px solid var(--blue);outline-offset:3px}
footer{margin-top:18px;color:var(--muted);font-size:15px;font-weight:700;text-align:center}
"""

UI = {
    "en": dict(lang="en", og="en_US", logo="School <span>Drone</span>", game="Game", play="▶ Play School Drone",
               other="中文", made="Idea by Aaron Shih. Built by his dad,", end=".", lic="Free and open source under the MIT license.", code="Code on GitHub",
               nav={"how-to-play": "How to play", "rules": "Rules", "faq": "Questions"}, base="", playurl=U + "?lang=en",
               nf_t="Page not found", nf_p="This page flew away. Go back to the game."),
    "zh": dict(lang="zh-Hant-TW", og="zh_TW", logo="學校<span>無人機</span>", game="遊戲", play="▶ 開始玩學校無人機",
               other="English", made="點子來自 Aaron Shih,由他的爸爸", end=" 製作。", lic="免費、開放原始碼,使用 MIT 授權。", code="GitHub 程式碼",
               nav={"how-to-play": "怎麼玩", "rules": "規則", "faq": "常見問題"}, base="zh/", playurl=U + "?lang=zh"),
}

# Each page: title, description, h1, lead, then sections of (heading, html).
PAGES = {
 "how-to-play": {
  "en": dict(title="How to Play School Drone: Fly the Drone Step by Step",
   desc="Learn how to play School Drone. Press Up to take off, use the arrows to fly, press Hover to stop, press 8 for the bee dance and Land to come home.",
   h1="How do you play School Drone?",
   lead="You press big buttons to fly a little drone around a library. A robot teacher inside the drone tells you what each button does.",
   steps=[("Take off", "Press Up. The propellers spin fast and the drone lifts off the yellow landing pad."),
          ("Fly around", "Press Up, Down, Left or Right. Hold a button to keep going that way."),
          ("Stop in the air", "Press Hover. The drone stays still in the air."),
          ("Point where to go", "Tap any place in the library picture. The drone flies to that spot."),
          ("Do the bee dance", "Press the 8 button. The drone flies a figure 8 two times and the kids cheer."),
          ("Watch the battery", "Look at the 3 batteries. When the flying battery gets low, the teacher tells you to land."),
          ("Land", "Press Land. The drone flies back to the yellow pad and comes down slowly."),
          ("Pick a drone", "Choose 4 propellers, helicopter, jet or 6 propellers. The teacher explains how each one flies.")],
   secs=[("How do you start playing?", "<p>Open the game and press <b>Up</b>. You do not need to install anything or sign in.</p>"),
         ("What does each button do?", "__STEPS__"),
         ("Which keys work on a keyboard?", "<p>The arrow keys fly the drone, the space bar is Hover, the 8 key is the bee dance and the L key is Land.</p><div class=\"scroll\"><table><tr><th>Key</th><th>What it does</th></tr><tr><td>↑ ↓ ← →</td><td>Up, down, left, right</td></tr><tr><td>Space</td><td>Hover</td></tr><tr><td>8</td><td>Bee dance (figure 8)</td></tr><tr><td>L</td><td>Land</td></tr></table></div>"),
         ("How do you change the language?", "<p>Press the <b>中文</b> or <b>English</b> button at the top of the game. The buttons and the teacher change language right away.</p>"),
         ("How do you turn the teacher's voice on or off?", "<p>Press <b>Voice: on</b> next to the teacher's words. The words always show on the screen, even when the voice is off.</p>")]),
  "zh": dict(title="學校無人機怎麼玩:一步一步學會飛無人機",
   desc="學校無人機怎麼玩?按「上」起飛,用方向按鈕飛行,按「懸停」停在空中,按 8 跳蜜蜂舞,按「降落」回家。",
   h1="學校無人機要怎麼玩?",
   lead="你只要按大大的按鈕,就可以讓小無人機在圖書館裡飛。無人機裡的機器人老師會告訴你每個按鈕在做什麼。",
   steps=[("起飛", "按「上」。螺旋槳轉得很快,無人機就從黃色降落墊飛起來。"),
          ("到處飛", "按「上、下、左、右」。按住不放,無人機會一直往那邊飛。"),
          ("停在空中", "按「懸停」。無人機會停在空中不動。"),
          ("用手指告訴它去哪裡", "點圖書館畫面上的任何地方,無人機就會飛過去。"),
          ("跳蜜蜂舞", "按「8」按鈕。無人機會飛兩次 8 字,小朋友會歡呼。"),
          ("看電池", "看那 3 顆電池。正在用的電池快沒電時,老師會提醒你降落。"),
          ("降落", "按「降落」。無人機會飛回黃色降落墊,慢慢下來。"),
          ("選無人機", "可以選 4 個螺旋槳、直升機、噴射機或 6 個螺旋槳。老師會說明每一種怎麼飛。")],
   secs=[("要怎麼開始玩?", "<p>打開遊戲,按「<b>上</b>」就可以了。不用安裝,也不用登入。</p>"),
         ("每個按鈕在做什麼?", "__STEPS__"),
         ("鍵盤可以用哪些按鍵?", "<p>方向鍵用來飛,空白鍵是懸停,8 是蜜蜂舞,L 是降落。</p><div class=\"scroll\"><table><tr><th>按鍵</th><th>做什麼</th></tr><tr><td>↑ ↓ ← →</td><td>上、下、左、右</td></tr><tr><td>空白鍵</td><td>懸停</td></tr><tr><td>8</td><td>蜜蜂舞(8 字飛行)</td></tr><tr><td>L</td><td>降落</td></tr></table></div>"),
         ("要怎麼換語言?", "<p>按遊戲最上面的「<b>中文</b>」或「<b>English</b>」按鈕。按鈕和老師說的話會馬上換語言。</p>"),
         ("要怎麼開或關老師的聲音?", "<p>按老師說話旁邊的「<b>聲音:開</b>」。就算關掉聲音,老師說的話還是會顯示在畫面上。</p>")]),
 },
 "rules": {
  "en": dict(title="School Drone Rules: Game Rules and Drone Safety for Kids",
   desc="The rules of School Drone: take turns with 3 batteries, land before the battery is empty, and keep the drone away from people, walls and bookshelves.",
   h1="What are the rules of School Drone?",
   lead="There are three big rules: take turns, land before the battery is empty, and keep the drone away from people and walls.",
   secs=[("Who gets to fly?", "<p>One kid flies with one battery. When the battery is empty, a fresh battery goes in and the next kid becomes the pilot. The pilot's name shows at the top of the game.</p>"),
         ("How do the 3 batteries work?", "<p>One battery is in the drone and the other two charge. A full battery flies for about 35 seconds, and an empty one takes about 50 seconds to fill up again.</p><ul><li>The battery only goes down while the drone is in the air.</li><li>When the battery is low, the teacher says it is time to land.</li><li>When the battery is empty, the drone flies back to the pad by itself.</li></ul>"),
         ("How high and how low can the drone fly?", "<p>The drone can fly up to 3.2 meters high, just under the ceiling. It will not go lower than 0.3 meters until you press Land.</p>"),
         ("Where is the drone not allowed to go?", "<p>The drone stops before the walls on the left and right. The teacher reminds you to keep away from walls and bookshelves.</p>"),
         ("Where does the drone land?", "<p>The drone always lands on the yellow pad in the middle of the blue rug. Press Land and it flies there by itself.</p>"),
         ("What are good safety rules for a real drone?", "<p>A real drone needs more care than a game drone. These are good habits for kids:</p><ul><li>Fly with a grown-up.</li><li>Keep the drone away from faces, people and pets.</li><li>Never touch the propellers while they spin.</li><li>Fly where there is lots of open space.</li><li>Always keep the drone where you can see it.</li><li>Land before the battery is empty.</li></ul><p>Rules for real drones are different in each country. Ask a grown-up to check the rules where you live.</p>")]),
  "zh": dict(title="學校無人機規則:遊戲規則和小朋友的無人機安全",
   desc="學校無人機的規則:3 顆電池大家輪流飛,沒電以前要降落,無人機要離人、牆壁和書櫃遠一點。",
   h1="學校無人機有哪些規則?",
   lead="有三條最重要的規則:要輪流、沒電以前要降落、無人機要離人和牆壁遠一點。",
   secs=[("誰可以飛?", "<p>一位小朋友用一顆電池飛。電池沒電以後,換上新的電池,下一位小朋友就變成小飛行員。小飛行員的名字會顯示在遊戲最上面。</p>"),
         ("3 顆電池是怎麼用的?", "<p>一顆電池在無人機裡,另外兩顆在充電。充飽的電池可以飛大約 35 秒,沒電的電池大約 50 秒可以充飽。</p><ul><li>無人機在空中的時候,電池才會變少。</li><li>電池快沒電時,老師會說該降落了。</li><li>電池完全沒電時,無人機會自己飛回降落墊。</li></ul>"),
         ("無人機可以飛多高、多低?", "<p>無人機最高可以飛到 3.2 公尺,就在天花板下面。在你按「降落」以前,它不會低於 0.3 公尺。</p>"),
         ("無人機不能去哪裡?", "<p>無人機飛到左邊和右邊的牆壁前面就會停下來。老師會提醒你離牆壁和書櫃遠一點。</p>"),
         ("無人機在哪裡降落?", "<p>無人機一定降落在藍色地毯中間的黃色降落墊。按「降落」,它就會自己飛過去。</p>"),
         ("飛真的無人機要注意哪些安全規則?", "<p>真的無人機比遊戲裡的更需要小心。這些是小朋友的好習慣:</p><ul><li>要有大人陪著一起飛。</li><li>無人機要離臉、人和寵物遠遠的。</li><li>螺旋槳在轉的時候,絕對不可以摸。</li><li>在空曠的地方飛。</li><li>無人機要一直在你看得到的地方。</li><li>沒電以前就降落。</li></ul><p>每個國家對真的無人機有不同的規定。請大人幫忙查你住的地方的規定。</p>")]),
 },
 "faq": {
  "en": dict(title="School Drone Questions and Answers (FAQ)",
   desc="Answers about School Drone: what it is, whether it is free, what kids learn, why the drone has 3 batteries, and who made it.",
   h1="School Drone questions and answers",
   lead="School Drone is a free game that teaches kids how drones fly. Here are short answers to common questions.",
   qa=[("What is School Drone?", "School Drone is a free web game where kids fly a drone inside a library. A robot teacher inside the drone explains each move in simple words."),
       ("Is School Drone free?", "Yes, School Drone is free. There are no ads, no sign-in and nothing to buy."),
       ("Do I need to install anything?", "No. School Drone runs in a web browser. Open the page and press Up."),
       ("Does it work on a phone or tablet?", "Yes. The buttons are big enough to tap, and you can also tap the library picture to send the drone there."),
       ("What do kids learn?", "Kids learn how a drone goes up, down, left and right, what hover means, why pilots watch the battery, and how to keep a drone away from people and walls."),
       ("Why does the drone have 3 batteries?", "Three batteries let every kid have a turn. One battery flies while the other two charge, so there is always a fresh one ready."),
       ("Why did the drone land by itself?", "The drone lands by itself when its battery is empty. A fresh battery goes in and the next kid becomes the pilot."),
       ("What does hover mean?", "Hover means the drone stays still in the air. The propellers push just hard enough to hold it up."),
       ("Why is the figure 8 called the bee dance?", "Honeybees dance in a figure 8 to show other bees where flowers are. The drone copies that shape."),
       ("Which drones can I pick?", "You can pick a drone with 4 propellers, a helicopter, a jet, or a drone with 6 propellers. The teacher explains how each one flies."),
       ("Which languages does the game have?", "The game has English and Traditional Chinese. Press the 中文 or English button at the top to switch."),
       ("Why can't I hear the teacher?", "The voice uses the speech built into your device, and some devices do not have one. Check that Voice is on and the sound is up. The teacher's words always show on the screen."),
       ("Who made School Drone?", f"The idea for School Drone came from Aaron Shih, and it was built by his dad, Edward Shih, as a kids' project. You can find Edward on <a href=\"{LI}\" rel=\"author noopener\">LinkedIn</a>."),
       ("Can teachers and parents use it or change it?", f"Yes. School Drone is open source under the MIT license, so you may use it, copy it and change it. Please keep the author's name. The code is on <a href=\"{REPO}\" rel=\"noopener\">GitHub</a>.")]),
  "zh": dict(title="學校無人機常見問題(FAQ)",
   desc="學校無人機常見問題:這是什麼遊戲、是不是免費、小朋友可以學到什麼、為什麼有 3 顆電池、是誰做的。",
   h1="學校無人機常見問題",
   lead="學校無人機是一個免費的遊戲,教小朋友無人機是怎麼飛的。下面用簡單的話回答大家常問的問題。",
   qa=[("學校無人機是什麼?", "學校無人機是一個免費的網頁遊戲,小朋友可以在圖書館裡飛無人機。無人機裡的機器人老師會用簡單的話說明每一個動作。"),
       ("學校無人機是免費的嗎?", "是的,學校無人機是免費的。沒有廣告,不用登入,也不用買任何東西。"),
       ("需要安裝什麼嗎?", "不用。學校無人機直接在瀏覽器裡玩,打開網頁、按「上」就可以了。"),
       ("手機或平板可以玩嗎?", "可以。按鈕夠大,用手指就能按,也可以直接點圖書館畫面,叫無人機飛過去。"),
       ("小朋友可以學到什麼?", "小朋友可以學到無人機怎麼上、下、左、右,什麼是懸停,為什麼飛行員要看電池,還有無人機要離人和牆壁遠一點。"),
       ("為什麼無人機有 3 顆電池?", "有 3 顆電池,每個小朋友都可以輪到。一顆在飛,另外兩顆在充電,所以隨時都有充飽的電池可以換。"),
       ("為什麼無人機會自己降落?", "電池沒電的時候,無人機會自己降落。換上新的電池以後,下一位小朋友就變成小飛行員。"),
       ("懸停是什麼意思?", "懸停就是無人機停在空中不動。螺旋槳的力氣剛剛好把它撐住。"),
       ("為什麼 8 字飛行叫做蜜蜂舞?", "蜜蜂會跳 8 字形的舞,告訴其他蜜蜂花在哪裡。無人機學的就是這個形狀。"),
       ("可以選哪些無人機?", "可以選 4 個螺旋槳的無人機、直升機、噴射機,或 6 個螺旋槳的無人機。老師會說明每一種怎麼飛。"),
       ("遊戲有哪些語言?", "遊戲有英文和繁體中文。按最上面的「中文」或「English」按鈕就可以換。"),
       ("為什麼聽不到老師的聲音?", "聲音是用你的裝置內建的語音,有些裝置沒有。請確認「聲音」是開的、音量有打開。老師說的話一定會顯示在畫面上。"),
       ("學校無人機是誰做的?", f"學校無人機的點子來自 Aaron Shih,由他的爸爸 Edward Shih 製作,是一個給小朋友的作品。你可以在 <a href=\"{LI}\" rel=\"author noopener\">LinkedIn</a> 找到 Edward。"),
       ("老師和家長可以使用或修改嗎?", f"可以。學校無人機是開放原始碼,使用 MIT 授權,你可以使用、複製和修改,請保留作者的名字。程式碼在 <a href=\"{REPO}\" rel=\"noopener\">GitHub</a>。")]),
 },
}

import re
def strip(h): return re.sub(r"<[^>]+>", "", h)

def page(slug, lang):
    P, ui = PAGES[slug][lang], UI[lang]
    url = U + ui["base"] + slug + ".html"
    up = "../" if lang == "zh" else ""
    alt = {"en": U + slug + ".html", "zh": U + "zh/" + slug + ".html"}
    other = "zh" if lang == "en" else "en"
    base_ld = {"@context": "https://schema.org", "url": url, "inLanguage": ui["lang"], "author": AUTHOR,
               "isPartOf": {"@type": "WebSite", "name": "School Drone", "url": U}}
    if slug == "faq":
        body = "".join(f"<h2>{e(q)}</h2>\n<p>{a}</p>\n" for q, a in P["qa"])
        data = dict(base_ld, **{"@type": "FAQPage", "name": P["h1"], "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in P["qa"]]})
    else:
        body = ""
        for h, c in P["secs"]:
            if c == "__STEPS__":
                c = "<ol>" + "".join(f"<li><b>{e(n)}:</b> {e(t)}</li>" for n, t in P["steps"]) + "</ol>"
            body += f"<h2>{e(h)}</h2>\n{c}\n"
        if slug == "how-to-play":
            data = dict(base_ld, **{"@type": "HowTo", "name": P["h1"], "description": P["desc"], "image": U + "og.png",
                        "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t} for i, (n, t) in enumerate(P["steps"])]})
        else:
            data = dict(base_ld, **{"@type": "Article", "headline": P["h1"], "description": P["desc"], "image": U + "og.png"})
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "School Drone", "item": U},
        {"@type": "ListItem", "position": 2, "name": ui["nav"][slug], "item": url}]}
    nav = f'<a href="{ui["playurl"]}">{ui["game"]}</a>' + "".join(
        f'<a href="{s}.html"{" aria-current=\"page\"" if s == slug else ""}>{e(n)}</a>' for s, n in ui["nav"].items())
    nav += f'<a href="{alt[other]}" lang="{UI[other]["lang"]}" hreflang="{UI[other]["lang"]}">{ui["other"]}</a>'
    return f"""<!doctype html>
<html lang="{ui['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{NOTE}
<title>{e(P['title'])}</title>
<meta name="description" content="{e(P['desc'])}">
<meta name="author" content="Aaron Shih and Edward Shih">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="author" href="{LI}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{alt['en']}">
<link rel="alternate" hreflang="zh-Hant-TW" href="{alt['zh']}">
<link rel="alternate" hreflang="x-default" href="{alt['en']}">
<link rel="icon" href="{up}icon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:site_name" content="School Drone">
<meta property="og:title" content="{e(P['title'])}">
<meta property="og:description" content="{e(P['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{U}og.png">
<meta property="og:locale" content="{ui['og']}">
<meta name="twitter:card" content="summary_large_image">
{ld(data)}
{ld(crumbs)}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&family=Nunito:wght@500;700;800&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header><a class="logo" href="{ui['playurl']}">{ui['logo']}</a><nav>{nav}</nav></header>
<main>
<h1>{e(P['h1'])}</h1>
<p class="lead">{e(P['lead'])}</p>
{body}<a class="play" href="{ui['playurl']}">{ui['play']}</a>
</main>
<footer>{ui['made']} <a href="{LI}" rel="author noopener">Edward Shih</a>{ui['end']} {ui['lic']} <a href="{REPO}" rel="noopener">{ui['code']}</a></footer>
</div>
</body>
</html>
"""

def build():
    build_index()
    urls = [(U, U + "?lang=zh")]
    (ROOT / "zh").mkdir(exist_ok=True)
    for slug in PAGES:
        (ROOT / f"{slug}.html").write_text(page(slug, "en"))
        (ROOT / "zh" / f"{slug}.html").write_text(page(slug, "zh"))
        a, b = U + slug + ".html", U + "zh/" + slug + ".html"
        urls += [(a, b)]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    for en, zh in urls:
        for loc in ([en] if en == U else [en, zh]):
            sm += f'  <url><loc>{loc}</loc><xhtml:link rel="alternate" hreflang="en" href="{en}"/><xhtml:link rel="alternate" hreflang="zh-Hant-TW" href="{e(zh)}"/><xhtml:link rel="alternate" hreflang="x-default" href="{en}"/></url>\n'
    (ROOT / "sitemap.xml").write_text(sm + "</urlset>\n")
    (ROOT / "404.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | School Drone</title><meta name="robots" content="noindex"><style>{CSS}</style></head>
<body><div class="wrap"><header><a class="logo" href="{U}">School <span>Drone</span></a></header>
<main><h1>This page flew away</h1><p class="lead">We could not find that page. 找不到這一頁。</p>
<a class="play" href="{U}">▶ Play School Drone 開始玩</a></main></div></body></html>
""")

if __name__ == "__main__":
    build()
    print("built")
