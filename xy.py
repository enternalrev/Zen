# ══════════════════════════════════════════════════════════════════════════════
#   s1n HOSTER · OPERATOR MASTER EDITION
# ══════════════════════════════════════════════════════════════════════════════

import asyncio, json, os, shutil, signal, subprocess, sys, html, re
from datetime import datetime, timezone
from pathlib import Path

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message,
)

from telethon import TelegramClient
from telethon.errors import (
    PasswordHashInvalidError, PhoneCodeExpiredError,
    PhoneCodeInvalidError, PhoneNumberInvalidError, SessionPasswordNeededError,
    PeerFloodError, FloodWaitError, RPCError,
)
from telethon.sessions import StringSession

# ─── CONFIG ───────────────────────────────────────────────────────
BOT_TOKEN = "8259729023:AAHqZEuFGJ9kqewQS1eU5U-0iprNqq_dKxQ"
OWNER_ID = 8661785324
OWNER_USERNAME = "sinConviction" # Do NOT put @ here

HOSTED_DIR = Path("Revhosted")
USERBOT_SCRIPT = Path("s1n_userbot.py")
USERS_DB = Path("users.json")
OPERATORS_DB = Path("operators.json")
GREETING_DB = Path("greeting.json")

def sb(text):
    out = []
    for c in str(text):
        if 'A' <= c <= 'Z':   out.append(chr(0x1D63C + ord(c) - 65))
        elif 'a' <= c <= 'z': out.append(chr(0x1D656 + ord(c) - 97))
        elif '0' <= c <= '9': out.append(chr(0x1D7EC + ord(c) - 48))
        else:                 out.append(c)
    return "".join(out)

# ══════════════════════════════════════════════════════════════════════════════
#   EMBEDDED USERBOT TEMPLATE
# ══════════════════════════════════════════════════════════════════════════════
USERBOT_TEMPLATE = r'''# ══════════════════════════════════════════════════════════════════════════════
#   s1n USERBOT
# ══════════════════════════════════════════════════════════════════════════════

import asyncio, io, json, os, random, re, time, base64, math, hashlib, shutil
import string, uuid, tempfile, urllib.parse, urllib.request
import json as _json
import contextvars, copy
from datetime import datetime
from pathlib import Path

from telethon import TelegramClient, events, functions, types, Button
from telethon.errors import (FloodWaitError, UserPrivacyRestrictedError,
    ChatAdminRequiredError, UserNotParticipantError, PeerFloodError,
    UserAlreadyParticipantError, PhoneCodeInvalidError, PhoneCodeExpiredError,
    PhoneNumberInvalidError, SessionPasswordNeededError, RPCError)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import InviteToChannelRequest, EditTitleRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.messages import GetHistoryRequest

try:
    from gtts import gTTS; TTS_OK = True
except ImportError: TTS_OK = False
try:
    import yt_dlp; YTDLP_OK = True
except ImportError: YTDLP_OK = False
try:
    import qrcode; QR_OK = True
except ImportError: QR_OK = False
try:
    from googletrans import Translator; TRANS_OK = True
except ImportError: TRANS_OK = False
try:
    from pytgcalls import PyTgCalls
    from pytgcalls.types import MediaStream
    PYTGCALLS_OK = True
except Exception: PYTGCALLS_OK = False

FFMPEG_OK = shutil.which("ffmpeg") is not None

API_ID = int(os.environ.get("USERBOT_API_ID", "0") or 0)
API_HASH = os.environ.get("USERBOT_API_HASH", "")
SESSION_STR = os.environ.get("USERBOT_SESSION", "")
if not (API_ID and API_HASH and SESSION_STR):
    raise SystemExit("Missing USERBOT env vars")

OWNER_ID = 0
UP = "!"
BP = "."
DB = "s1n_vault.json"

def sb(text):
    out = []
    for c in str(text):
        if 'A' <= c <= 'Z':   out.append(chr(0x1D63C + ord(c) - 65))
        elif 'a' <= c <= 'z': out.append(chr(0x1D656 + ord(c) - 97))
        elif '0' <= c <= '9': out.append(chr(0x1D7EC + ord(c) - 48))
        else:                 out.append(c)
    return "".join(out)

def style(text):
    s = str(text)
    if s.startswith("◈"): s = "🩷" + s[1:]
    return sb(s)

H1, H2, H3 = "🤍", "🩷", "🩵"

_real_state = {
    "texts": [
        "Baune trima cute RND he tri behen ko to slave banake rkha he mene itna attitude kese aara tujhme😂😂😂😂😂💔😂😂💔😂💔😂💔😂💔😂💔💔😂🥀🥀🥀",
        "Apki mom itni RND kese he bina pese lie chud jaati😏🥀💔",
        "Trima pe atomic bomb gir jae jo tre sarr pe pankha he na vo tut ke tre goto pe gire jo tre ghar pe cylinder he na tre ma jab uspe khana banari ho tb vi fatt jae jo tra nall he na vo leak hojae or tra ghar bhass jae mc",
        "ＴＲＩＭＡ　ＣＨＵＤＧＹＩ　ＲＥ😜💜        ほソがん       ˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊",
        "Beta lund chus bada ho pese duga 😏🥀",
        "sun aukat anusar chud tu",
        "chl mc apni mom ki kali chut ki mms send kr"
    ],
    "sticker": None, "traid": [], "tst": [], "muted": [], "btr": None,
    "bots": [], "bot_names": [], "main_bot": 0,
    "autodel": 10, "delay": 0.35, "count": 0,
    "afk": None, "notes": {}, "anim": True,
    "todos": [], "nicknames": {}, "bot_texts": [], "bot_notes": {},
    "filters": [], "greet": None, "greet_id": None,
    "antilink": False, "antispam": False, "warns": {},
    "blacklist": [], "saved": {}, "quotes": [],
    "stats_msgs": 0, "stats_cmds": 0, "stats_start": None,
    "bot_delay": 0.35, "bre_targets": [],
    "chudai_texts": [], "vchudai_file": None, "rrall": None,
}

CHUDAI_DEFAULT = (
    "{name} TERY MA CHUDGYI RE 🩷 🤍🤍~\n"
    "☘☘☘☘☘☘☘☆☆☆☆☆☆彡彡彡彡彡彡彡\n\n\n\n"
) * 7

def _default_state():
    d = copy.deepcopy(_real_state)
    d["stats_start"] = datetime.now().isoformat()
    d["chudai_texts"] = [CHUDAI_DEFAULT]
    return d

_active_client = contextvars.ContextVar("active_client", default=None)
_active_state  = contextvars.ContextVar("active_state",  default=None)
_active_owner  = contextvars.ContextVar("active_owner",  default=None)
_active_db     = contextvars.ContextVar("active_db",     default=DB)

class _UserProxy:
    def __getattr__(self, n): return getattr(_active_client.get() or _real_user, n)
    def __call__(self, *a, **kw): return (_active_client.get() or _real_user)(*a, **kw)

class _StateProxy:
    def _d(self): return _active_state.get() or _real_state
    def __getitem__(self, k): return self._d()[k]
    def __setitem__(self, k, v): self._d()[k] = v
    def __delitem__(self, k): del self._d()[k]
    def __contains__(self, k): return k in self._d()
    def __iter__(self): return iter(self._d())
    def __len__(self): return len(self._d())
    def get(self, k, default=None): return self._d().get(k, default)
    def update(self, d): self._d().update(d)
    def keys(self): return self._d().keys()
    def items(self): return self._d().items()

STATE = _StateProxy()

def load():
    if os.path.exists(DB):
        try:
            with open(DB, "r", encoding="utf-8") as f:
                _real_state.update(json.load(f))
        except Exception: pass
    if _real_state.get("stats_start") is None:
        _real_state["stats_start"] = datetime.now().isoformat()

def save():
    s = _active_state.get() or _real_state
    path = _active_db.get() or DB
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({k: v for k, v in s.items() if not k.startswith("_")},
                      f, indent=2, ensure_ascii=False)
    except Exception: pass

load()

_real_user = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)
user = _UserProxy()
TASKS, BOT_TASKS = {}, {}
BOTS = []
SENT, SENT_IDS = [], set()
CLUSTERS = {}
PENDING = {}

def _owner(): return _active_owner.get() or OWNER_ID
def _cluster_clients():
    c = CLUSTERS.get(_owner())
    if not c: return [_active_client.get() or _real_user]
    return [c["main"]] + list(c["workers"])
def _title_bot():
    if not BOTS: return None
    idx = _real_state.get("main_bot", 0)
    return BOTS[idx] if 0 <= idx < len(BOTS) else BOTS[0]

ANIM = {
    "load":   ["◐ ʟᴏᴀᴅɪɴɢ","◓ ʟᴏᴀᴅɪɴɢ","◑ ʟᴏᴀᴅɪɴɢ","◒ ʟᴏᴀᴅɪɴɢ"],
    "spin":   ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"],
    "pulse":  ["♡","♥","♡","♥"],
    "fire":   ["🩷","🩷🩷","🩷🩷🩷","🩷🩷🩷🩷"],
    "hearts": ["🤍","🩷","🩵","🤍","🩷","🩵"],
    "stars":  ["✦","✧","✦","✧","✩"],
    "hug":    ["(つ｡◕‿‿◕｡)つ","(づ￣ ³￣)づ","(っ´▽`)っ","🤍"],
    "slap":   ["( ˘ ³˘)","🤍","🩷","🩵","╰(°ㅂ°)╯"],
    "kiss":   ["😗","😙","😚","😘"],
    "cry":    ["😢","😭","😿","🩵🩵","🩵🩵🩵"],
    "dance":  ["┌(・。・)┘♪","└(・。・)┐♪","┌(・。・)┘♪","└(・。・)┐♪"],
    "punch":  ["🤜","🩷","🤛","🩵","💢"],
    "love":   ["🩷","🩵","🤍","🩷","🩵"],
    "hate":   ["🤍","🖤","💢"],
    "run":    ["🏃","🏃‍♂️","🏃","🏃‍♂️","💨"],
    "cute":   ["(◕‿◕)","(｡◕‿◕｡)","(◠‿◠)","(*^▽^*)","(づ｡◕‿‿◕｡)づ"],
    "blush":  ["😊","😳","☺️","😚"],
    "sparkle":["🩷","🩵","🤍","🩷","🩵"],
    "cat":    ["(=^･ω･^=)","(=^‥^=)","ᓚᘏᗢ"],
    "bunny":  ["🐰","🐇","(•ㅅ•)","ʕ•ᴥ•ʔ"],
    "flower": ["🩷","🤍","🩵","🩷"],
    "sleep":  ["😴","💤","🛏","🤍","🩷"],
    "magic":  ["🩷","🩵","🤍","🩷","🩵"],
    "party":  ["🩷","🤍","🩵","🩷"],
}

async def anim(chat, key, reply_to=None, delay=0.35, cycles=1, final=None):
    frames = ANIM.get(key)
    if not frames or not STATE.get("anim", True): return None
    try:
        m = await user.send_message(chat, frames[0], reply_to=reply_to)
        for _ in range(cycles):
            for f in frames:
                await asyncio.sleep(delay)
                try: await m.edit(f)
                except FloodWaitError: pass
                except Exception: break
        if final is not None:
            try: await m.edit(style(final))
            except Exception: pass
        return m
    except Exception: return None

async def loading(chat, label, reply_to=None, delay=0.25):
    try:
        m = await user.send_message(chat, f"{ANIM['spin'][0]}  {label}", reply_to=reply_to)
        for i in range(10):
            await asyncio.sleep(delay)
            try: await m.edit(f"{ANIM['spin'][i % len(ANIM['spin'])]}  {label}")
            except Exception: break
        return m
    except Exception: return None

ZAL = ''.join(chr(c) for c in range(0x0300, 0x036F))
EMO = ["🩷","🩵","🤍"]

def zalgo(t, lvl=2):
    return ''.join(ch + ''.join(random.choice(ZAL) for _ in range(random.randint(0, lvl))) for ch in t)
def wave(t, p=0):
    return ''.join(ch.upper() if (i+p)%2==0 else ch.lower() for i,ch in enumerate(t))
def rndcase(t):
    return ''.join(ch.upper() if random.random()>0.5 else ch.lower() for ch in t)
def small_caps(t):
    m = str.maketrans("abcdefghijklmnopqrstuvwxyz", "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ")
    return t.lower().translate(m)
def upside_down(t):
    m = str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz∀ᗺƆᗡƎℲ⅁HIſꓘ˥WNOԀΌᴚS⊥∩ΛMX⅄Z0ƖᄅƐㄣϛ9ㄥ86")
    return t.translate(m)[::-1]
def b64_encode(t): return base64.b64encode(t.encode()).decode()
def b64_decode(t):
    try: return base64.b64decode(t.encode()).decode()
    except Exception: return None
def hex_encode(t): return t.encode().hex()
def rot13(t):
    m = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm")
    return t.translate(m)
def stutter(t): return " ".join(f"{w[0]}-{w}" if w else w for w in t.split())

def remember(msg, client=None):
    try:
        cli = client or (_active_client.get() or _real_user)
        SENT.append((cli, msg.chat_id, msg.id))
        SENT_IDS.add((id(cli), msg.chat_id, msg.id))
    except Exception: pass

async def _autodel(client, chat, mid, sec):
    await asyncio.sleep(sec)
    try: await client.delete_messages(chat, mid)
    except Exception: pass

async def send(client, chat, text, reply_to=None, **kw):
    try:
        m = await asyncio.wait_for(client.send_message(chat, text, reply_to=reply_to, **kw), timeout=10.0)
    except (asyncio.TimeoutError, FloodWaitError) as e:
        wait = e.seconds + 2 if isinstance(e, FloodWaitError) else 2
        await asyncio.sleep(min(wait, 10))
        try:
            m = await asyncio.wait_for(client.send_message(chat, text, reply_to=reply_to, **kw), timeout=10.0)
        except Exception: return None
    except Exception: return None
    
    remember(m, client)
    d = STATE.get("autodel", 0)
    if d: asyncio.create_task(_autodel(client, m.chat_id, m.id, d))
    return m

async def notify(chat, text, client=None, reply_to=None):
    return await send(client or (_active_client.get() or _real_user),
                      chat, style(text), reply_to=reply_to)

def spawn(name, coro):
    old = TASKS.get(name)
    if old and not old.done(): old.cancel()
    cli = _active_client.get() or _real_user
    t = asyncio.create_task(_guard(name, coro)); t._nexus_client = cli
    TASKS[name] = t; return t

def spawn_bot(name, coro):
    old = BOT_TASKS.get(name)
    if old and not old.done(): old.cancel()
    cli = _active_client.get() or _real_user
    t = asyncio.create_task(_guard_bot(name, coro)); t._nexus_client = cli
    BOT_TASKS[name] = t; return t

async def _guard(n, c):
    try: await c
    except asyncio.CancelledError: pass
    except Exception as e: print(f"[task:{n}] {e}")
    finally: TASKS.pop(n, None)

async def _guard_bot(n, c):
    try: await c
    except asyncio.CancelledError: pass
    except Exception as e: print(f"[bottask:{n}] {e}")
    finally: BOT_TASKS.pop(n, None)

def kill_all():
    n = 0
    active = _active_client.get() or _real_user
    for name in list(TASKS.keys()):
        t = TASKS[name]
        if getattr(t, "_nexus_client", _real_user) is active and not t.done():
            t.cancel(); n += 1
        TASKS.pop(name, None)
    for name in list(BOT_TASKS.keys()):
        t = BOT_TASKS[name]
        if getattr(t, "_nexus_client", _real_user) is active and not t.done():
            t.cancel(); n += 1
        BOT_TASKS.pop(name, None)
    return n

async def wipe_sent():
    global SENT
    active = _active_client.get() or _real_user
    buckets, keep = {}, []
    for cli, cid, mid in SENT:
        if cli is active:
            buckets.setdefault((id(cli), cid), [cli, cid, []])[2].append(mid)
        else: keep.append((cli, cid, mid))
    SENT = keep
    for key in list(SENT_IDS):
        if key[0] == id(active): SENT_IDS.discard(key)
    removed = 0
    for cli, cid, ids in buckets.values():
        for i in range(0, len(ids), 100):
            chunk = ids[i:i+100]
            try: await cli.delete_messages(cid, chunk); removed += len(chunk)
            except Exception:
                for mid in chunk:
                    try: await cli.delete_messages(cid, mid); removed += 1
                    except Exception: pass
    return removed

# ─── ANTI-FREEZE RAID LOOP ───
async def raid_loop(client, chat, text, reply_to=None, delay=None, count=None):
    delay = STATE["delay"] if delay is None else delay
    count = STATE["count"] if count is None else count
    n = 0
    while True:
        if count and n >= count: return
        try:
            m = await asyncio.wait_for(client.send_message(chat, text, reply_to=reply_to), timeout=10.0)
            remember(m, client)
            d = STATE.get("autodel", 0)
            if d: asyncio.create_task(_autodel(client, m.chat_id, m.id, d))
        except asyncio.TimeoutError:
            print("[raid] timeout, sleeping 5s")
            await asyncio.sleep(5); continue
        except FloodWaitError as fw: 
            print(f"[raid] flood wait {fw.seconds}s")
            await asyncio.sleep(min(fw.seconds, 20) + 2); continue
        except PeerFloodError:
            print("[raid] peer flood, sleeping 15s")
            await asyncio.sleep(15); continue
        except Exception: 
            await asyncio.sleep(2.0)
        n += 1
        await asyncio.sleep(delay)

async def raid_sticker_loop(chat, reply_to, delay=None):
    delay = STATE["delay"] if delay is None else delay
    st = STATE.get("sticker")
    if not st: return
    while True:
        try:
            src = await user.get_messages(st["chat"], ids=st["id"])
            if src:
                m = await asyncio.wait_for(user.send_file(chat, src, reply_to=reply_to), timeout=10.0); remember(m)
        except asyncio.TimeoutError: await asyncio.sleep(5); continue
        except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
        except Exception: pass
        await asyncio.sleep(delay)

async def raid_voice_loop(chat, reply_to, delay=None):
    delay = STATE["delay"] if delay is None else delay
    if not TTS_OK: return
    while True:
        try:
            buf = io.BytesIO()
            gTTS(text=random.choice(STATE["texts"])[:200], lang="en").write_to_fp(buf)
            buf.seek(0); buf.name = "s1n_voice.mp3"
            m = await asyncio.wait_for(user.send_file(chat, buf, voice_note=True, reply_to=reply_to), timeout=10.0)
            remember(m)
        except asyncio.TimeoutError: await asyncio.sleep(5); continue
        except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
        except Exception: pass
        await asyncio.sleep(delay)

async def send_saved_sticker(chat, reply_to=None, client=None):
    st = STATE.get("sticker")
    if not st: return
    cli = client or (_active_client.get() or _real_user)
    try:
        src = await cli.get_messages(st["chat"], ids=st["id"])
        if not src: return
        try: m = await cli.send_file(chat, src, reply_to=reply_to)
        except Exception: m = await cli.send_file(chat, src.media, reply_to=reply_to)
        remember(m, cli)
    except Exception: pass

def is_owner(uid):
    oid = _owner()
    return oid == 0 or uid == oid

def fmt(seconds):
    seconds = int(seconds); h, r = divmod(seconds, 3600); m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

C = {}
def cmd(name):
    def d(fn): C[name] = fn; return fn
    return d
BOTC = {}
def botcmd(name):
    def d(fn): BOTC[name] = fn; return fn
    return d

# ═══════ RAID ═══════
@cmd("spm")
async def c_spm(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ꜱᴘᴍ <ᴛᴇxᴛ>", reply_to=e.message.id)
    spawn(f"spm:{c}", raid_loop(user, c, a))
    await anim(c, "fire", reply_to=e.message.id, final="◈ ᴅᴇᴘʟᴏʏᴇᴅ")

@cmd("mc")
async def c_mc(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    t = a or random.choice(STATE["texts"])
    spawn(f"mc:{c}:{r.sender_id}", raid_loop(user, c, t, reply_to=r.id))
    await anim(c, "pulse", reply_to=e.message.id, final="◈ ʟᴏᴄᴋᴇᴅ")

@cmd("raidtext")
async def c_raidtext(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ʀᴀɪᴅᴛᴇxᴛ <ᴛᴇxᴛ>", reply_to=e.message.id)
    spawn(f"raidtext:{c}", raid_loop(user, c, a))
    await notify(c, "◈ ʀᴀɪᴅ ʟᴏᴏᴘ ᴏɴ", reply_to=e.message.id)

@cmd("raidmention")
async def c_raidmention(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try: ent = await user.get_entity(r.sender_id)
    except: return await notify(c, "◈ ɴᴏᴛ ʀᴇꜱᴏʟᴠᴀʙʟᴇ", reply_to=e.message.id)
    name = ent.first_name or "?"
    mention = f"[{name}](tg://user?id={ent.id})"
    async def loop():
        while True:
            try:
                m = await asyncio.wait_for(user.send_message(c, mention + " " + random.choice(STATE["texts"])), timeout=10.0)
                remember(m)
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: pass
            await asyncio.sleep(STATE["delay"])
    spawn(f"raidmention:{c}:{r.sender_id}", loop())
    await notify(c, f"◈ ᴍᴇɴᴛɪᴏɴ ʀᴀɪᴅ · {name}", reply_to=e.message.id)

@cmd("raidnum")
async def c_raidnum(e, a, r, c):
    async def loop():
        n = 0
        while True:
            n += 1
            try:
                m = await asyncio.wait_for(user.send_message(c, str(n)), timeout=10.0); remember(m)
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: pass
            await asyncio.sleep(STATE["delay"])
    spawn(f"raidnum:{c}", loop())
    await notify(c, "◈ ɴᴜᴍʙᴇʀ ʀᴀɪᴅ ᴏɴ", reply_to=e.message.id)

@cmd("raidlist")
async def c_raidlist(e, a, r, c):
    heads = ("spm","mc","raidtext","raidmention","raidnum","sps","spl","spz","spf",
             "spr","spx","bomb","flood","chain","matrix","wavespam","rain","spamall",
             "capsbomb","lovebomb","stickerbomb","emojibomb","spo","spamslow","spamfast",
             "randspam","raidvoice","raidsticker","chudai")
    raids = [k for k in TASKS if k.split(":")[0] in heads]
    if not raids: return await notify(c, "◈ ɴᴏ ᴀᴄᴛɪᴠᴇ ʀᴀɪᴅꜱ", reply_to=e.message.id)
    body = "\n".join(f"  ▸ {k}" for k in raids[:40])
    await notify(c, f"◈ ᴀᴄᴛɪᴠᴇ ʀᴀɪᴅꜱ ({len(raids)})\n{body}", reply_to=e.message.id)

@cmd("stopraid")
async def c_stopraid(e, a, r, c):
    heads = ("spm","mc","raidtext","raidmention","raidnum","sps","spl","spz","spf",
             "spr","spx","bomb","flood","chain","matrix","wavespam","rain","spamall",
             "capsbomb","lovebomb","stickerbomb","emojibomb","spo","spamslow","spamfast",
             "randspam","raidvoice","raidsticker","chudai")
    n = 0
    for k in list(TASKS.keys()):
        if k.split(":")[0] in heads:
            t = TASKS.get(k)
            if t and not t.done(): t.cancel(); n += 1
            TASKS.pop(k, None)
    await notify(c, f"◈ ꜱᴛᴏᴘᴘᴇᴅ {n}", reply_to=e.message.id)

@cmd("traid")
async def c_traid(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    uid = r.sender_id
    if uid in STATE["traid"]:
        STATE["traid"].remove(uid); save()
        return await notify(c, "◈ ᴛʀᴀɪᴅ ᴏғғ", reply_to=e.message.id)
    STATE["traid"].append(uid); save()
    await notify(c, "◈ ᴛʀᴀɪᴅ ᴏɴ", reply_to=e.message.id)

@cmd("tsst")
async def c_tsst(e, a, r, c):
    if not r or not r.sticker: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ", reply_to=e.message.id)
    STATE["sticker"] = {"chat": r.chat_id, "id": r.id}; save()
    await notify(c, "◈ ꜱᴛɪᴄᴋᴇʀ ꜱᴀᴠᴇᴅ", reply_to=e.message.id)

@cmd("tst")
async def c_tst(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    uid = r.sender_id
    if uid in STATE["tst"]:
        STATE["tst"].remove(uid); save()
        return await notify(c, "◈ ᴛʀᴀᴄᴋᴇʀ ᴏғғ", reply_to=e.message.id)
    STATE["tst"].append(uid); save()
    await notify(c, "◈ ᴛʀᴀᴄᴋᴇʀ ᴏɴ", reply_to=e.message.id)

@cmd("dbrk")
async def c_dbrk(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    uid = r.sender_id
    if uid not in STATE["muted"]: STATE["muted"].append(uid); save()
    try: await r.delete()
    except Exception: pass
    await notify(c, "◈ ꜱɪʟᴇɴᴄᴇᴅ", reply_to=e.message.id)

@cmd("brk")
async def c_brk(e, a, r, c):
    if a.strip().lower() == "all":
        STATE["muted"] = []; save()
        return await notify(c, "◈ ᴀʟʟ ʀᴇʟᴇᴀꜱᴇᴅ", reply_to=e.message.id)
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    uid = r.sender_id
    if uid in STATE["muted"]: STATE["muted"].remove(uid); save()
    await notify(c, "◈ ʀᴇʟᴇᴀꜱᴇᴅ", reply_to=e.message.id)

@cmd("rpraid")
async def c_rpraid(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    if not BOTS: return await notify(c, "◈ ɴᴏ ʙᴏᴛꜱ → .ꜱᴇᴛʙᴏᴛꜱ", reply_to=e.message.id)
    t = a or random.choice(STATE["texts"])
    spawn_bot(f"rpraid:{c}", bot_raid_all(c, t, reply_to=r.id))
    await notify(c, f"◈ ʙᴏᴛ ʀᴀɪᴅ ×{len(BOTS)}", reply_to=e.message.id)

@cmd("ruk")
async def c_ruk(e, a, r, c):
    m = await anim(c, "spin", reply_to=e.message.id, final="◈ ᴘᴜʀɢɪɴɢ")
    n = kill_all(); removed = await wipe_sent()
    STATE["traid"] = []; STATE["tst"] = []; STATE["btr"] = None
    STATE["rrall"] = None; save()
    try: await m.edit(style(f"◈ ᴡɪᴘᴇᴅ {removed} · {n} ᴛᴀꜱᴋꜱ"))
    except Exception: pass

# ═══════ SPAM ═══════
@cmd("sps")
async def c_sps(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ꜱᴘꜱ <ᴛᴇxᴛ>", reply_to=e.message.id)
    async def loop():
        while True:
            try: m = await asyncio.wait_for(user.send_message(c, a + " " + random.choice(EMO)), timeout=10.0); remember(m)
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: pass
            await asyncio.sleep(STATE["delay"])
    spawn(f"sps:{c}", loop())
    await notify(c, "◈ ᴠᴀʀɪᴀᴛɪᴏɴ ꜱᴘᴀᴍ ᴏɴ", reply_to=e.message.id)

@cmd("spl")
async def c_spl(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ꜱᴘʟ <ᴡᴏʀᴅꜱ>", reply_to=e.message.id)
    words = a.split()
    async def loop():
        while True:
            for w in words:
                try: m = await asyncio.wait_for(user.send_message(c, w), timeout=10.0); remember(m)
                except asyncio.TimeoutError: await asyncio.sleep(5); continue
                except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
                except Exception: pass
                await asyncio.sleep(STATE["delay"])
    spawn(f"spl:{c}", loop())
    await notify(c, "◈ ʟɪɴᴇ ꜱᴘᴀᴍ ᴏɴ", reply_to=e.message.id)

@cmd("spz")
async def c_spz(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ꜱᴘᴢ <ᴛᴇxᴛ>", reply_to=e.message.id)
    spawn(f"spz:{c}", raid_loop(user, c, zalgo(a, 3)))
    await notify(c, "◈ ᴢᴀʟɢᴏ ᴏɴ", reply_to=e.message.id)

@cmd("spf")
async def c_spf(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍꜱɢ", reply_to=e.message.id)
    async def loop():
        while True:
            try: m = await asyncio.wait_for(r.forward_to(c), timeout=10.0); remember(m)
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: pass
            await asyncio.sleep(STATE["delay"])
    spawn(f"spf:{c}", loop())
    await notify(c, "◈ ꜰᴡᴅ ꜱᴛᴏʀᴍ ᴏɴ", reply_to=e.message.id)

@cmd("spr")
async def c_spr(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍꜱɢ", reply_to=e.message.id)
    t = a or random.choice(STATE["texts"])
    spawn(f"spr:{c}", raid_loop(user, c, t, reply_to=r.id))
    await notify(c, "◈ ʀᴇᴘʟʏ ʀᴀɪᴅ ᴏɴ", reply_to=e.message.id)

@cmd("spx")
async def c_spx(e, a, r, c):
    if not STATE["texts"]: return await notify(c, "◈ ᴠᴀᴜʟᴛ ᴇᴍᴘᴛʏ", reply_to=e.message.id)
    async def loop():
        while True:
            try: m = await asyncio.wait_for(user.send_message(c, random.choice(STATE["texts"])), timeout=10.0); remember(m)
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: pass
            await asyncio.sleep(STATE["delay"])
    spawn(f"spx:{c}", loop())
    await notify(c, "◈ ʀᴀɴᴅᴏᴍ ʀᴀɪᴅ ᴏɴ", reply_to=e.message.id)

@cmd("spo")
async def c_spo(e, a, r, c):
    p = a.split(maxsplit=1)
    if len(p) < 2: return await notify(c, "◈ ᴜꜱᴇ · !ꜱᴘᴏ <ɴ> <ᴛᴇxᴛ>", reply_to=e.message.id)
    try: n = int(p[0])
    except: return await notify(c, "◈ ɪɴᴠᴀʟɪᴅ", reply_to=e.message.id)
    text = p[1]
    async def loop():
        for i in range(1, n + 1):
            try:
                m = await asyncio.wait_for(user.send_message(c, f"{i}. {text}"), timeout=10.0); remember(m)
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: pass
            await asyncio.sleep(STATE["delay"])
    spawn(f"spo:{c}", loop())
    await notify(c, f"◈ ᴏʀᴅᴇʀᴇᴅ {n}", reply_to=e.message.id)

@cmd("spamslow")
async def c_spamslow(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ꜱᴘᴀᴍꜱʟᴏᴡ <ᴛᴇxᴛ>", reply_to=e.message.id)
    spawn(f"spamslow:{c}", raid_loop(user, c, a, delay=2.0))
    await notify(c, "◈ ꜱʟᴏᴡ ꜱᴘᴀᴍ ᴏɴ", reply_to=e.message.id)

@cmd("spamfast")
async def c_spamfast(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ꜱᴘᴀᴍꜰᴀꜱᴛ <ᴛᴇxᴛ>", reply_to=e.message.id)
    spawn(f"spamfast:{c}", raid_loop(user, c, a, delay=0.1))
    await notify(c, "◈ ꜰᴀꜱᴛ ꜱᴘᴀᴍ ᴏɴ", reply_to=e.message.id)

@cmd("randspam")
async def c_randspam(e, a, r, c):
    if not STATE["texts"]: return await notify(c, "◈ ᴠᴀᴜʟᴛ ᴇᴍᴘᴛʏ", reply_to=e.message.id)
    async def loop():
        while True:
            try: m = await asyncio.wait_for(user.send_message(c, random.choice(STATE["texts"])), timeout=10.0); remember(m)
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: pass
            await asyncio.sleep(STATE["delay"])
    spawn(f"randspam:{c}", loop())
    await notify(c, "◈ ʀᴀɴᴅ ꜱᴘᴀᴍ ᴏɴ", reply_to=e.message.id)

@cmd("raidvoice")
async def c_raidvoice(e, a, r, c):
    if not TTS_OK: return await notify(c, "◈ ᴛᴛꜱ ᴏғғʟɪɴᴇ", reply_to=e.message.id)
    spawn(f"raidvoice:{c}", raid_voice_loop(c, r.id if r else None))
    await notify(c, "◈ ᴠᴏɪᴄᴇ ʀᴀɪᴅ ᴏɴ", reply_to=e.message.id)

@cmd("raidsticker")
async def c_raidsticker(e, a, r, c):
    if not STATE.get("sticker"): return await notify(c, "◈ ɴᴏ ꜱᴛɪᴄᴋᴇʀ → !ᴛꜱꜱᴛ", reply_to=e.message.id)
    spawn(f"raidsticker:{c}", raid_sticker_loop(c, r.id if r else None))
    await notify(c, "◈ ꜱᴛɪᴄᴋᴇʀ ʀᴀɪᴅ ᴏɴ", reply_to=e.message.id)

@cmd("bomb")
async def c_bomb(e, a, r, c):
    p = a.split(maxsplit=1)
    if len(p) < 2: return await notify(c, "◈ ᴜꜱᴇ · !ʙᴏᴍʙ <ɴ> <ᴛᴇxᴛ>", reply_to=e.message.id)
    try: n = int(p[0])
    except: return await notify(c, "◈ ɪɴᴠᴀʟɪᴅ", reply_to=e.message.id)
    spawn(f"bomb:{c}", raid_loop(user, c, p[1], count=n))
    await notify(c, f"◈ ʙᴏᴍʙ {n}", reply_to=e.message.id)

@cmd("rain")
async def c_rain(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ʀᴀɪɴ <ᴛᴇxᴛ>", reply_to=e.message.id)
    art = "\n".join("　" * i + a for i in range(3))
    spawn(f"rain:{c}", raid_loop(user, c, art))
    await notify(c, "◈ ʀᴀɪɴ ᴏɴ", reply_to=e.message.id)

@cmd("wavespam")
async def c_wavespam(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ᴡᴀᴠᴇꜱᴘᴀᴍ <ᴛᴇxᴛ>", reply_to=e.message.id)
    async def loop():
        i = 0
        while True:
            try: m = await asyncio.wait_for(user.send_message(c, wave(a, i)), timeout=10.0); remember(m)
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: pass
            i += 1; await asyncio.sleep(STATE["delay"])
    spawn(f"wavespam:{c}", loop())
    await notify(c, "◈ ᴡᴀᴠᴇ ᴏɴ", reply_to=e.message.id)

@cmd("matrix")
async def c_matrix(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ᴍᴀᴛʀɪx <ᴛᴇxᴛ>", reply_to=e.message.id)
    async def loop():
        while True:
            try: m = await asyncio.wait_for(user.send_message(c, rndcase(a)), timeout=10.0); remember(m)
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: pass
            await asyncio.sleep(STATE["delay"])
    spawn(f"matrix:{c}", loop())
    await notify(c, "◈ ᴍᴀᴛʀɪx ᴏɴ", reply_to=e.message.id)

@cmd("lovebomb")
async def c_lovebomb(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    msgs = ["ɪ ʟᴏᴠᴇ ʏᴏᴜ 🩷","ᴄᴜᴛᴇ 🤍","♡ ♡ ♡","ᴋɪꜱꜱᴇꜱ 🩵","ꜱᴡᴇᴇᴛɪᴇ 🩷","ʜᴜɢꜱ 🤍"]
    async def loop():
        while True:
            try: m = await asyncio.wait_for(user.send_message(c, random.choice(msgs), reply_to=r.id), timeout=10.0); remember(m)
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: pass
            await asyncio.sleep(STATE["delay"])
    spawn(f"lovebomb:{c}", loop())
    await notify(c, "◈ ʟᴏᴠᴇ ʙᴏᴍʙ ᴏɴ", reply_to=e.message.id)

@cmd("capsbomb")
async def c_capsbomb(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ᴄᴀᴘꜱʙᴏᴍʙ <ᴛᴇxᴛ>", reply_to=e.message.id)
    spawn(f"capsbomb:{c}", raid_loop(user, c, a.upper() + " !!!"))
    await notify(c, "◈ ᴄᴀᴘꜱ ʙᴏᴍʙ ᴏɴ", reply_to=e.message.id)

@cmd("emojibomb")
async def c_emojibomb(e, a, r, c):
    try: n = int(a)
    except: n = 15
    txt = " ".join(random.choice(EMO) for _ in range(30))
    spawn(f"emojibomb:{c}", raid_loop(user, c, txt, count=n))
    await notify(c, f"◈ ᴇᴍᴏᴊɪ ʙᴏᴍʙ {n}", reply_to=e.message.id)

@cmd("stickerbomb")
async def c_stickerbomb(e, a, r, c):
    if not STATE.get("sticker"): return await notify(c, "◈ ɴᴏ ꜱᴛɪᴄᴋᴇʀ → !ᴛꜱꜱᴛ", reply_to=e.message.id)
    spawn(f"stickerbomb:{c}", raid_sticker_loop(c, None))
    await notify(c, "◈ ꜱᴛɪᴄᴋᴇʀ ʙᴏᴍʙ ᴏɴ", reply_to=e.message.id)

@cmd("flood")
async def c_flood(e, a, r, c):
    try: n = int(a)
    except: n = 50
    spawn(f"flood:{c}", raid_loop(user, c, "🩷", count=n))
    await notify(c, f"◈ ꜰʟᴏᴏᴅ {n}", reply_to=e.message.id)

@cmd("chain")
async def c_chain(e, a, r, c):
    if not a: return await notify(c, "◈ ꜱᴇᴘ ᴡɪᴛʜ |", reply_to=e.message.id)
    parts = [p.strip() for p in a.split("|") if p.strip()]
    async def loop():
        i = 0
        while True:
            try: m = await asyncio.wait_for(user.send_message(c, parts[i % len(parts)]), timeout=10.0); remember(m)
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: pass
            i += 1; await asyncio.sleep(STATE["delay"])
    spawn(f"chain:{c}", loop())
    await notify(c, f"◈ ᴄʜᴀɪɴ {len(parts)}", reply_to=e.message.id)

@cmd("stutter")
async def c_stutter(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ꜱᴛᴜᴛᴛᴇʀ <ᴛᴇxᴛ>", reply_to=e.message.id)
    spawn(f"stutter:{c}", raid_loop(user, c, stutter(a)))
    await notify(c, "◈ ꜱᴛᴜᴛᴛᴇʀ ᴏɴ", reply_to=e.message.id)

@cmd("upsidedown")
async def c_upsidedown(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ᴜᴘꜱɪᴅᴇᴅᴏᴡɴ <ᴛᴇxᴛ>", reply_to=e.message.id)
    spawn(f"upsidedown:{c}", raid_loop(user, c, upside_down(a)))
    await notify(c, "◈ ᴜᴘꜱɪᴅᴇ ᴅᴏᴡɴ ᴏɴ", reply_to=e.message.id)

@cmd("spamall")
async def c_spamall(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ꜱᴘᴀᴍᴀʟʟ <ᴛᴇxᴛ>", reply_to=e.message.id)
    spawn(f"spamall:{c}", raid_loop(user, c, a))
    await notify(c, "◈ ᴍᴀꜱꜱ ꜱᴘᴀᴍ ᴏɴ", reply_to=e.message.id)

# ═══════ GROUP ═══════
@cmd("gcreate")
async def c_gcreate(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ɢᴄʀᴇᴀᴛᴇ <ɴᴀᴍᴇ>", reply_to=e.message.id)
    try:
        await user(functions.messages.CreateChatRequest(users=[], title=a[:64]))
        await notify(c, f"◈ ɢʀᴏᴜᴘ · {a[:64]}", reply_to=e.message.id)
    except Exception as ex:
        await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("ginfo")
async def c_ginfo(e, a, r, c):
    try:
        ent = await user.get_entity(c)
        title = getattr(ent, "title", "—")
        n = getattr(ent, "participants_count", "?")
        is_channel = getattr(ent, "broadcast", False)
        is_megagroup = getattr(ent, "megagroup", False)
        txt = (f"◈ ᴄʜᴀᴛ ɪɴғᴏ\n"
               f"◈ ᴛɪᴛʟᴇ · {title}\n"
               f"◈ ᴛʏᴘᴇ · {'channel' if is_channel else 'megagroup' if is_megagroup else 'group'}\n"
               f"◈ ɪᴅ · {ent.id}\n◈ ᴍᴇᴍʙᴇʀꜱ · {n}")
        await notify(c, txt, reply_to=e.message.id)
    except Exception as ex:
        await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gmembers")
async def c_gmembers(e, a, r, c):
    try:
        ent = await user.get_entity(c)
        n = getattr(ent, "participants_count", None)
        if n is None:
            count = 0
            async for _ in user.iter_participants(c):
                count += 1
            n = count
        await notify(c, f"◈ ᴍᴇᴍʙᴇʀꜱ · {n}", reply_to=e.message.id)
    except Exception as ex:
        await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gid")
async def c_gid(e, a, r, c):
    await notify(c, f"◈ ᴄʜᴀᴛ ɪᴅ · {c}", reply_to=e.message.id)

@cmd("gunpin")
async def c_gunpin(e, a, r, c):
    try:
        await user.unpin_message(c)
        await notify(c, "◈ ᴀʟʟ ᴜɴᴘɪɴɴᴇᴅ", reply_to=e.message.id)
    except Exception as ex:
        await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("ginvite")
async def c_ginvite(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ɢɪɴᴠɪᴛᴇ @ᴜꜱᴇʀ", reply_to=e.message.id)
    try:
        ent = await user.get_entity(a.strip())
        chat = await user.get_input_entity(c)
        await user(InviteToChannelRequest(chat, [ent]))
        await notify(c, f"◈ ɪɴᴠɪᴛᴇᴅ · {a.strip()}", reply_to=e.message.id)
    except Exception as ex:
        await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gpromote")
async def c_gpromote(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try:
        await user.edit_admin(c, r.sender_id, change_info=True, delete_messages=True,
                              ban_users=True, invite_users=True, pin_messages=True)
        await notify(c, "◈ ᴘʀᴏᴍᴏᴛᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gdemote")
async def c_gdemote(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try:
        await user.edit_admin(c, r.sender_id, is_admin=False)
        await notify(c, "◈ ᴅᴇᴍᴏᴛᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gkick")
async def c_gkick(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try:
        await user.kick_participant(c, r.sender_id)
        await notify(c, "◈ ᴋɪᴄᴋᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gban")
async def c_gban(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try:
        await user.edit_permissions(c, r.sender_id, view_messages=False)
        await notify(c, "◈ ʙᴀɴɴᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gunban")
async def c_gunban(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try:
        await user.edit_permissions(c, r.sender_id, view_messages=True)
        await notify(c, "◈ ᴜɴʙᴀɴɴᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gmute")
async def c_gmute(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try:
        await user.edit_permissions(c, r.sender_id, send_messages=False)
        await notify(c, "◈ ᴍᴜᴛᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gunmute")
async def c_gunmute(e, a, r, c):
    if not r: return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try:
        await user.edit_permissions(c, r.sender_id, send_messages=True)
        await notify(c, "◈ ᴜɴᴍᴜᴛᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gtitle")
async def c_gtitle(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ɢᴛɪᴛʟᴇ <ᴛɪᴛʟᴇ>", reply_to=e.message.id)
    try:
        await user(functions.channels.EditTitleRequest(c, a))
        await notify(c, "◈ ɢʀᴏᴜᴘ ʀᴇɴᴀᴍᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gdesc")
async def c_gdesc(e, a, r, c):
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ɢᴅᴇꜱᴄ <ᴅᴇꜱᴄ>", reply_to=e.message.id)
    try:
        await user(functions.channels.EditAboutRequest(c, a))
        await notify(c, "◈ ᴅᴇꜱᴄ ꜱᴇᴛ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("gleave")
async def c_gleave(e, a, r, c):
    try:
        await user(functions.channels.LeaveChannelRequest(c))
    except Exception as ex: await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

# ═══════ VOICE ═══════
VC_CLIENTS = {}
async def _get_vc(cli):
    if not PYTGCALLS_OK: raise RuntimeError("py-tgcalls not installed")
    cid = id(cli)
    if cid in VC_CLIENTS: return VC_CLIENTS[cid]
    vc = PyTgCalls(cli); await vc.start()
    VC_CLIENTS[cid] = vc
    return vc

@cmd("kawai")
async def c_kawai(e, a, r, c):
    if not TTS_OK: return await notify(c, "◈ ᴛᴛꜱ ᴏғғʟɪɴᴇ", reply_to=e.message.id)
    if not a: return await notify(c, "◈ ᴜꜱᴇ · !ᴋᴀᴡᴀɪ <ᴛᴇxᴛ>", reply_to=e.message.id)
    await loading(c, "ꜱʏɴᴛʜᴇꜱɪᴢɪɴɢ", reply_to=e.message.id)
    try:
        buf = io.BytesIO(); gTTS(text=a, lang="en").write_to_fp(buf)
        buf.seek(0); buf.name = "s1n_voice.mp3"
        m = await user.send_file(c, buf, voice_note=True, reply_to=e.message.id)
        remember(m)
    except Exception as ex: await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("vjoin")
async def c_vjoin(e, a, r, c):
    if not PYTGCALLS_OK: return await notify(c, "◈ ᴘʏ-ᴛɢᴄᴀʟʟꜱ ᴏғғʟɪɴᴇ", reply_to=e.message.id)
    try:
        await _get_vc(user)
        await notify(c, "◈ ᴊᴏɪɴᴇᴅ ᴠᴄ", reply_to=e.message.id)
    except Exception as ex:
        await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("vleave")
async def c_vleave(e, a, r, c):
    if not PYTGCALLS_OK: return await notify(c, "◈ ᴘʏ-ᴛɢᴄᴀʟʟꜱ ᴏғғʟɪɴᴇ", reply_to=e.message.id)
    vc = VC_CLIENTS.get(id(user))
    if vc:
        try: await vc.leave_call(c)
        except Exception: pass
    await notify(c, "◈ ʟᴇғᴛ ᴠᴄ", reply_to=e.message.id)

@cmd("vstop")
async def c_vstop(e, a, r, c):
    if not PYTGCALLS_OK: return await notify(c, "◈ ᴘʏ-ᴛɢᴄᴀʟʟꜱ ᴏғғʟɪɴᴇ", reply_to=e.message.id)
    for cli in _cluster_clients():
        vc = VC_CLIENTS.get(id(cli))
        if vc:
            try: await vc.leave_call(c)
            except Exception: pass
    await notify(c, "◈ ᴀʟʟ ʟᴇғᴛ", reply_to=e.message.id)

@cmd("setvchudai")
async def c_setvchudai(e, a, r, c):
    if not r or not (getattr(r, "voice", None) or getattr(r, "audio", None)
                     or getattr(r, "video_note", None)):
        return await notify(c, "◈ ʀᴇᴘʟʏ ᴛᴏ ᴠᴏɪᴄᴇ/ᴀᴜᴅɪᴏ/ᴠɴ", reply_to=e.message.id)
    STATE["vchudai_file"] = {"chat": r.chat_id, "id": r.id}; save()
    await notify(c, "◈ ꜱᴀᴠᴇᴅ", reply_to=e.message.id)

@cmd("vchudai")
async def c_vchudai(e, a, r, c):
    if not PYTGCALLS_OK: return await notify(c, "◈ ᴘʏ-ᴛɢᴄᴀʟʟꜱ ᴏғғʟɪɴᴇ", reply_to=e.message.id)
    if e.is_private: return await notify(c, "◈ ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ", reply_to=e.message.id)
    src = STATE.get("vchudai_file")
    if not src: return await notify(c, "◈ ꜱᴇᴛ ᴠɪᴀ !ꜱᴇᴛᴠᴄʜᴜᴅᴀɪ", reply_to=e.message.id)
    tmp = tempfile.mkdtemp(prefix="vchudai_")
    try:
        msg = await user.get_messages(src["chat"], ids=src["id"])
        path = await msg.download_media(tmp)
        if not path: raise RuntimeError("download failed")
        ok, fail = 0, 0
        for cli in _cluster_clients():
            try:
                vc = await _get_vc(cli)
                await vc.play(c, MediaStream(path))
                ok += 1; await asyncio.sleep(1.2)
            except Exception as ex:
                print(f"[vchudai] {ex}"); fail += 1
        await notify(c, f"◈ ᴊᴏɪɴᴇᴅ {ok} · ғᴀɪʟ {fail}", reply_to=e.message.id)
    except Exception as ex:
        await notify(c, f"◈ ғᴀɪʟ · {ex}", reply_to=e.message.id)

# ═══════ SONG ═══════
async def _search_ytdlp(query, limit=5):
    if not YTDLP_OK: return []
    opts = {"quiet": True, "no_warnings": True, "extract_flat": True,
            "default_search": f"ytsearch{limit}", "skip_download": True}
    def _run():
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
            return info.get("entries", []) if info else []
    return await asyncio.to_thread(_run)

async def _download_song(video_url, out_dir):
    opts = {"format": "bestaudio/best",
            "outtmpl": f"{out_dir}/%(title)s.%(ext)s",
            "quiet": True, "no_warnings": True, "noplaylist": True,
            "postprocessors": [{"key": "FFmpegExtractAudio",
                                "preferredcodec": "mp3", "preferredquality": "192"}],
            "writethumbnail": True}
    def _run():
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            path = ydl.prepare_filename(info)
            mp3_path = os.path.splitext(path)[0] + ".mp3"
            thumb = None
            for ext in (".jpg", ".webp", ".png"):
                cand = os.path.splitext(path)[0] + ext
                if os.path.exists(cand): thumb = cand; break
            return mp3_path, thumb, info
    return await asyncio.to_thread(_run)

@cmd("s")
async def c_song(e, a, r, c):
    if not YTDLP_OK: return await notify(c, "🩷 ʏᴛ-ᴅʟᴘ ᴏғғʟɪɴᴇ", reply_to=e.message.id)
    if not FFMPEG_OK: return await notify(c, "🩷 ғғᴍᴘᴇɢ ᴍɪꜱꜱɪɴɢ", reply_to=e.message.id)
    if not a: return await notify(c, "🩷 ᴜꜱᴇ · !ꜱ <ꜱᴏɴɢ>", reply_to=e.message.id)
    status = await notify(c, "🩷 ꜱᴇᴀʀᴄʜɪɴɢ", reply_to=e.message.id)
    try: results = await _search_ytdlp(a, limit=5)
    except Exception as ex:
        try: await status.edit(style(f"🩷 ғᴀɪʟ · {ex}"))
        except: pass
        return
    if not results:
        try: await status.edit(style("🩷 ɴᴏᴛʜɪɴɢ ғᴏᴜɴᴅ"))
        except: pass
        return
    best = results[0]
    vid_url = best.get("url") or best.get("webpage_url")
    title = best.get("title", "unknown")
    tmp = tempfile.mkdtemp(prefix="s1n_song_")
    try:
        mp3_path, thumb, info = await _download_song(vid_url, tmp)
        if not os.path.exists(mp3_path):
            return await status.edit(style("🩷 ᴅᴏᴡɴʟᴏᴀᴅ ғᴀɪʟᴇᴅ"))
        send_kw = dict(file=mp3_path, title=title[:64],
                       performer=(info.get("uploader") or "—")[:64],
                       duration=int(info.get("duration") or 0),
                       reply_to=e.message.id)
        if thumb and os.path.exists(thumb): send_kw["thumb"] = thumb
        try: m = await user.send_file(c, **send_kw)
        except: m = await user.send_file(c, mp3_path, reply_to=e.message.id)
        remember(m)
        try: await status.delete()
        except: pass
    except Exception as ex:
        try: await status.edit(style(f"🩷 ғᴀɪʟ · {ex}"))
        except: pass
    finally:
        try: shutil.rmtree(tmp, ignore_errors=True)
        except: pass

@cmd("splay")
async def c_splay(e, a, r, c):
    if not YTDLP_OK or not FFMPEG_OK:
        return await notify(c, "🩷 ᴍᴏᴅᴜʟᴇ ᴏғғʟɪɴᴇ", reply_to=e.message.id)
    if not a: return await notify(c, "🩷 ᴜꜱᴇ · !ꜱᴘʟᴀʏ <ꜱᴏɴɢ>", reply_to=e.message.id)
    status = await notify(c, "🩷 ᴡᴏʀᴋɪɴɢ", reply_to=e.message.id)
    try:
        results = await _search_ytdlp(a, limit=3)
        if not results: return await status.edit(style("🩷 ɴᴏᴛʜɪɴɢ"))
        vid_url = results[0].get("url") or results[0].get("webpage_url")
        tmp = tempfile.mkdtemp(prefix="s1n_play_")
        mp3_path, _, _ = await _download_song(vid_url, tmp)
        if not os.path.exists(mp3_path):
            return await status.edit(style("🩷 ғᴀɪʟᴇᴅ"))
        m = await user.send_file(c, mp3_path, voice_note=True, reply_to=e.message.id)
        remember(m)
        try: await status.delete()
        except: pass
        shutil.rmtree(tmp, ignore_errors=True)
    except Exception as ex:
        try: await status.edit(style(f"🩷 ғᴀɪʟ · {ex}"))
        except: pass

@cmd("ssearch")
async def c_ssearch(e, a, r, c):
    if not YTDLP_OK: return await notify(c, "🩷 ᴏғғʟɪɴᴇ", reply_to=e.message.id)
    if not a: return await notify(c, "🩷 ᴜꜱᴇ · !ꜱꜱᴇᴀʀᴄʜ <q>", reply_to=e.message.id)
    try: results = await _search_ytdlp(a, limit=5)
    except Exception as ex: return await notify(c, f"🩷 ғᴀɪʟ · {ex}", reply_to=e.message.id)
    if not results: return await notify(c, "🩷 ɴᴏᴛʜɪɴɢ", reply_to=e.message.id)
    lines = [f"🩷 ᴛᴏᴘ ᴍᴀᴛᴄʜᴇꜱ", ""]
    for v in results:
        lines.append(f"  🤍 {(v.get('title') or '?')[:60]}")
        lines.append(f"     🩵 {v.get('duration') or '?'}")
    await notify(c, "\n".join(lines), reply_to=e.message.id)

@cmd("lyrics")
async def c_lyrics(e, a, r, c):
    if not a: return await notify(c, "🩷 ᴜꜱᴇ · !ʟʏʀɪᴄꜱ <ꜱᴏɴɢ>", reply_to=e.message.id)
    try:
        url = f"https://api.lyrics.ovh/v1/{urllib.parse.quote(a)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            lyr = _json.loads(resp.read().decode()).get("lyrics", "🩷 ɴᴏ ʟʏʀɪᴄꜱ")
        for i in range(0, len(lyr), 3800):
            await notify(c, lyr[i:i+3800], reply_to=e.message.id)
    except Exception as ex: await notify(c, f"🩷 ғᴀɪʟ · {ex}", reply_to=e.message.id)
# ═══════ UTILS ═══════
@cmd("ping")
async def c_ping(e, a, r, c):
    t0 = time.perf_counter()
    m = await notify(c, "🩷 ᴘɪɴɢɪɴɢ")
    dt = (time.perf_counter() - t0) * 1000
    try: await m.edit(style(f"🩷 ᴘᴏɴɢ · {dt:.0f} ᴍꜱ"))
    except: pass

@cmd("alive")
async def c_alive(e, a, r, c):
    me = await user.get_me()
    txt = (f"🩷 s1ɴ ᴏɴʟɪɴᴇ\n"
           f"🤍 ᴏᴘᴇʀᴀᴛᴏʀ · {me.first_name}\n"
           f"🩵 ᴛᴀꜱᴋꜱ · {len(TASKS)} · ʙᴏᴛꜱ · {len(BOTS)}\n"
           f"🩷 ᴅᴇʟᴀʏ · {STATE['delay']}ꜱ")
    await anim(c, "stars", reply_to=e.message.id, final=txt)

@cmd("id")
async def c_id(e, a, r, c):
    if r: txt = f"🩷 ᴜꜱᴇʀ {r.sender_id} · ᴄʜᴀᴛ {c} · ᴍꜱɢ {r.id}"
    else: txt = f"🩷 ᴄʜᴀᴛ {c}"
    await notify(c, txt, reply_to=e.message.id)

@cmd("stats")
async def c_stats(e, a, r, c):
    txt = (f"🩷 ᴛᴇʟᴇᴍᴇᴛʀʏ\n"
           f"🤍 ᴛᴀꜱᴋꜱ · {len([t for t in TASKS.values() if not t.done()])}\n"
           f"🩵 ʙᴏᴛ ᴛᴀꜱᴋꜱ · {len([t for t in BOT_TASKS.values() if not t.done()])}\n"
           f"🩷 ᴛʀᴀɪᴅ · {len(STATE['traid'])}\n🤍 ᴍᴜᴛᴇᴅ · {len(STATE['muted'])}")
    await notify(c, txt, reply_to=e.message.id)

@cmd("afk")
async def c_afk(e, a, r, c):
    STATE["afk"] = a or "🩷 ᴀꜰᴋ"; save()
    await notify(c, "🩷 ᴀꜰᴋ ᴏɴ", reply_to=e.message.id)

@cmd("unafk")
async def c_unafk(e, a, r, c):
    STATE["afk"] = None; save()
    await notify(c, "🩷 ᴀꜰᴋ ᴏғғ", reply_to=e.message.id)

@cmd("purge")
async def c_purge(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ꜱᴛᴀʀᴛ ᴍꜱɢ", reply_to=e.message.id)
    ids = list(range(r.id, e.message.id + 1))
    for i in range(0, len(ids), 100):
        try: await user.delete_messages(c, ids[i:i+100])
        except: pass

@cmd("del")
async def c_del(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍꜱɢ", reply_to=e.message.id)
    try: await r.delete()
    except: pass

@cmd("tagall")
async def c_tagall(e, a, r, c):
    try: users = await user.get_participants(c, limit=200)
    except: return await notify(c, "🩵 ᴄᴀɴ'ᴛ ʀᴇᴀᴅ", reply_to=e.message.id)
    m = " ".join(f"[{u.first_name or '?'}](tg://user?id={u.id})" for u in users if not u.bot)
    await notify(c, f"{a or '🩷 ᴀᴛᴛᴇɴᴛɪᴏɴ'}\n{m[:3800]}")

@cmd("uptime")
async def c_uptime(e, a, r, c):
    start = datetime.fromisoformat(STATE["stats_start"])
    delta = datetime.now() - start
    h, rem = divmod(int(delta.total_seconds()), 3600); m, s = divmod(rem, 60)
    await notify(c, f"🩷 ᴜᴘᴛɪᴍᴇ · {h}ʜ {m}ᴍ {s}ꜱ", reply_to=e.message.id)

@cmd("myid")
async def c_myid(e, a, r, c):
    me = await user.get_me()
    await notify(c, f"🩷 ɪᴅ · {me.id}", reply_to=e.message.id)

@cmd("time")
async def c_time(e, a, r, c):
    now = datetime.now()
    await notify(c, f"🩷 {now.strftime('%H:%M:%S')} · {now.strftime('%Y-%m-%d')}",
                 reply_to=e.message.id)

@cmd("note")
async def c_note(e, a, r, c):
    p = a.split(maxsplit=1)
    if len(p) < 2: return await notify(c, "🩵 ᴜꜱᴇ · !ɴᴏᴛᴇ <ᴋ> <ᴠ>", reply_to=e.message.id)
    STATE["notes"][p[0]] = p[1]; save()
    await notify(c, f"🩷 ɴᴏᴛᴇ '{p[0]}' ꜱᴀᴠᴇᴅ", reply_to=e.message.id)

@cmd("notes")
async def c_notes(e, a, r, c):
    if not STATE["notes"]: return await notify(c, "🩵 ɴᴏɴᴇ", reply_to=e.message.id)
    body = "\n".join(f"  🤍 {k}: {v[:60]}" for k, v in STATE["notes"].items())
    await notify(c, f"🩷 ɴᴏᴛᴇꜱ\n{body}", reply_to=e.message.id)

@cmd("calc")
async def c_calc(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ᴄᴀʟᴄ <ᴇxᴘʀ>", reply_to=e.message.id)
    try:
        if not re.fullmatch(r"[0-9\.\+\-\*\/\(\)\s%]+", a): raise ValueError
        await notify(c, f"🩷 {a} = {eval(a)}", reply_to=e.message.id)
    except: await notify(c, "🩵 ɪɴᴠᴀʟɪᴅ", reply_to=e.message.id)

@cmd("b64")
async def c_b64(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ʙ64 <ᴛ>", reply_to=e.message.id)
    try: await notify(c, f"🩷 {b64_encode(a)}", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"🩵 ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("unb64")
async def c_unb64(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ᴜɴʙ64 <ᴛ>", reply_to=e.message.id)
    d = b64_decode(a)
    await notify(c, f"🩷 {d}" if d else "🩵 ɪɴᴠᴀʟɪᴅ", reply_to=e.message.id)

@cmd("hash")
async def c_hash(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ʜᴀꜱʜ <ᴛ>", reply_to=e.message.id)
    await notify(c, f"🩷 ꜱʜᴀ256 · {hashlib.sha256(a.encode()).hexdigest()[:32]}",
                 reply_to=e.message.id)

@cmd("md5")
async def c_md5(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ᴍᴅ5 <ᴛ>", reply_to=e.message.id)
    await notify(c, f"🩷 ᴍᴅ5 · {hashlib.md5(a.encode()).hexdigest()}", reply_to=e.message.id)

@cmd("hex")
async def c_hex(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ʜᴇx <ᴛ>", reply_to=e.message.id)
    await notify(c, f"🩷 {hex_encode(a)}", reply_to=e.message.id)

@cmd("rot13")
async def c_rot13(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ʀᴏᴛ13 <ᴛ>", reply_to=e.message.id)
    await notify(c, f"🩷 {rot13(a)}", reply_to=e.message.id)

@cmd("zalgo")
async def c_zalgo(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ᴢᴀʟɢᴏ <ᴛ>", reply_to=e.message.id)
    await notify(c, f"🩷 {zalgo(a, 4)}", reply_to=e.message.id)

@cmd("smallcaps")
async def c_smallcaps(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ꜱᴍᴀʟʟᴄᴀᴘꜱ <ᴛ>", reply_to=e.message.id)
    await notify(c, f"🩷 {small_caps(a)}", reply_to=e.message.id)

@cmd("save")
async def c_save(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍꜱɢ", reply_to=e.message.id)
    key = a or f"msg_{r.id}"
    STATE["saved"][key] = r.raw_text or "[media]"; save()
    await notify(c, f"🩷 ꜱᴀᴠᴇᴅ '{key}'", reply_to=e.message.id)

@cmd("get")
async def c_get(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ɢᴇᴛ <ᴋ>", reply_to=e.message.id)
    v = STATE["saved"].get(a)
    if not v: return await notify(c, "🩵 ɴᴏᴛ ғᴏᴜɴᴅ", reply_to=e.message.id)
    await notify(c, f"🩷 {v}", reply_to=e.message.id)

@cmd("timer")
async def c_timer(e, a, r, c):
    try: sec = int(a)
    except: return await notify(c, "🩵 ᴜꜱᴇ · !ᴛɪᴍᴇʀ 30", reply_to=e.message.id)
    m = await notify(c, f"🩷 ᴛɪᴍᴇʀ · {fmt(sec)}")
    async def tick():
        left = sec
        while left > 0:
            await asyncio.sleep(1); left -= 1
            if left % 5 == 0 or left <= 5:
                try: await m.edit(style(f"🩷 ᴛɪᴍᴇʀ · {fmt(left)}"))
                except: pass
        try: await m.edit(style("🩷 ᴛɪᴍᴇʀ ᴅᴏɴᴇ"))
        except: pass
    spawn(f"timer:{c}:{int(time.time())}", tick())

@cmd("delays")
async def c_delays(e, a, r, c):
    if not a:
        return await notify(c,
            f"🩵 ᴜꜱᴇ · !ᴅᴇʟᴀʏꜱ <ꜱᴇᴄꜱ>\n"
            f"🤍 ᴜꜱᴇʀ ʙᴏᴛ · {STATE['delay']}ꜱ\n"
            f"🩷 ʙᴏᴛꜱ · {STATE['bot_delay']}ꜱ",
            reply_to=e.message.id)
    try:
        sec = max(0.05, min(60.0, float(a)))
        STATE["delay"] = sec; STATE["bot_delay"] = sec; save()
        await notify(c, f"🩷 ᴀʟʟ ᴅᴇʟᴀʏꜱ · {sec}ꜱ", reply_to=e.message.id)
    except Exception:
        await notify(c, "🩵 ᴜꜱᴇ · !ᴅᴇʟᴀʏꜱ 0.5", reply_to=e.message.id)

@cmd("delay")
async def c_delay(e, a, r, c):
    try:
        STATE["delay"] = max(0.05, float(a)); save()
        await notify(c, f"🩷 ᴅᴇʟᴀʏ · {STATE['delay']}ꜱ", reply_to=e.message.id)
    except: await notify(c, "🩵 ᴜꜱᴇ · !ᴅᴇʟᴀʏ 0.5", reply_to=e.message.id)

@cmd("count")
async def c_count(e, a, r, c):
    try:
        STATE["count"] = max(0, int(a)); save()
        await notify(c, f"🩷 ʙᴜʀꜱᴛ · {STATE['count'] or '∞'}", reply_to=e.message.id)
    except: await notify(c, "🩵 ᴜꜱᴇ · !ᴄᴏᴜɴᴛ 25", reply_to=e.message.id)

@cmd("autodel")
async def c_autodel(e, a, r, c):
    try:
        STATE["autodel"] = max(0, int(a)); save()
        await notify(c, f"🩷 ᴀᴜᴛᴏ-ᴅᴇʟ · {STATE['autodel']}ꜱ", reply_to=e.message.id)
    except: await notify(c, "🩵 ᴜꜱᴇ · !ᴀᴜᴛᴏᴅᴇʟ 10", reply_to=e.message.id)

@cmd("addtext")
async def c_addtext(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ᴀᴅᴅᴛᴇxᴛ <ᴛ>", reply_to=e.message.id)
    STATE["texts"].append(a); save()
    await notify(c, f"🩷 ᴀᴅᴅᴇᴅ · {len(STATE['texts'])}", reply_to=e.message.id)

@cmd("deltext")
async def c_deltext(e, a, r, c):
    try:
        i = int(a) - 1; t = STATE["texts"].pop(i); save()
        await notify(c, f"🩷 ʀᴇᴍᴏᴠᴇᴅ · {t[:40]}", reply_to=e.message.id)
    except: await notify(c, "🩵 ᴜꜱᴇ · !ᴅᴇʟᴛᴇxᴛ 2", reply_to=e.message.id)

@cmd("listtext")
async def c_listtext(e, a, r, c):
    if not STATE["texts"]: return await notify(c, "🩵 ᴠᴀᴜʟᴛ ᴇᴍᴘᴛʏ", reply_to=e.message.id)
    body = "\n".join(f"  {i+1:02d} · {t}" for i, t in enumerate(STATE["texts"]))
    await notify(c, f"🩷 ᴛᴀʀɢᴇᴛ ᴠᴀᴜʟᴛ\n{body}", reply_to=e.message.id)

@cmd("anim")
async def c_anim(e, a, r, c):
    STATE["anim"] = a.strip().lower() in ("on","1","true","yes"); save()
    await notify(c, f"🩷 ᴀɴɪᴍ · {'ᴏɴ' if STATE['anim'] else 'ᴏғғ'}", reply_to=e.message.id)

# ═══════ CUTE ═══════
@cmd("hug")
async def c_hug(e, a, r, c):
    tgt = (await user.get_entity(r.sender_id)).first_name if r else "ᴀɴʏᴏɴᴇ"
    await anim(c, "hug", reply_to=e.message.id, cycles=2, final=f"🩷 ʜᴜɢꜱ {tgt}")

@cmd("slap")
async def c_slap(e, a, r, c):
    tgt = (await user.get_entity(r.sender_id)).first_name if r else "ᴀɴʏᴏɴᴇ"
    await anim(c, "slap", reply_to=e.message.id, cycles=2, final=f"🩷 ꜱʟᴀᴘᴘᴇᴅ {tgt}")

@cmd("kiss")
async def c_kiss(e, a, r, c):
    tgt = (await user.get_entity(r.sender_id)).first_name if r else "ᴀɴʏᴏɴᴇ"
    await anim(c, "kiss", reply_to=e.message.id, cycles=2, final=f"🩷 ᴋɪꜱꜱᴇᴅ {tgt}")

@cmd("cry")
async def c_cry(e, a, r, c):
    await anim(c, "cry", reply_to=e.message.id, cycles=3, final="🩵 ᴄʀʏɪɴɢ")

@cmd("dance")
async def c_dance(e, a, r, c):
    await anim(c, "dance", reply_to=e.message.id, cycles=3, final="🩷 ᴅᴀɴᴄɪɴɢ")

@cmd("love")
async def c_love(e, a, r, c):
    await anim(c, "love", reply_to=e.message.id, cycles=3, final="🩷 ʟᴏᴠᴇ")

@cmd("hate")
async def c_hate(e, a, r, c):
    await anim(c, "hate", reply_to=e.message.id, cycles=2, final="🩵 ʜᴀᴛᴇ")

@cmd("punch")
async def c_punch(e, a, r, c):
    await anim(c, "punch", reply_to=e.message.id, cycles=2, final="🩷 ᴋɴᴏᴄᴋᴏᴜᴛ")

@cmd("run")
async def c_run(e, a, r, c):
    await anim(c, "run", reply_to=e.message.id, cycles=2, final="🩷 ɢᴏɴᴇ")

@cmd("spin")
async def c_spin(e, a, r, c):
    await anim(c, "spin", reply_to=e.message.id, cycles=2, final="🩵 ꜱᴛᴀʙɪʟɪᴢᴇᴅ")

@cmd("cuddle")
async def c_cuddle(e, a, r, c):
    tgt = (await user.get_entity(r.sender_id)).first_name if r else "ᴀɴʏᴏɴᴇ"
    await anim(c, "cute", reply_to=e.message.id, cycles=3, final=f"🩷 ᴄᴜᴅᴅʟᴇꜱ {tgt}")

@cmd("pat")
async def c_pat(e, a, r, c):
    tgt = (await user.get_entity(r.sender_id)).first_name if r else "ᴀɴʏᴏɴᴇ"
    await anim(c, "cute", reply_to=e.message.id, cycles=3, final=f"🩷 ᴘᴀᴛꜱ {tgt}")

@cmd("boop")
async def c_boop(e, a, r, c):
    tgt = (await user.get_entity(r.sender_id)).first_name if r else "ᴀɴʏᴏɴᴇ"
    await notify(c, f"🩷 ʙᴏᴏᴘ {tgt}", reply_to=e.message.id)

@cmd("lick")
async def c_lick(e, a, r, c):
    tgt = (await user.get_entity(r.sender_id)).first_name if r else "ᴀɴʏᴏɴᴇ"
    await anim(c, "kiss", reply_to=e.message.id, cycles=2, final=f"🩷 ʟɪᴄᴋꜱ {tgt}")

@cmd("bite")
async def c_bite(e, a, r, c):
    tgt = (await user.get_entity(r.sender_id)).first_name if r else "ᴀɴʏᴏɴᴇ"
    await notify(c, f"🩷 ʙɪᴛ {tgt}", reply_to=e.message.id)

@cmd("tickle")
async def c_tickle(e, a, r, c):
    tgt = (await user.get_entity(r.sender_id)).first_name if r else "ᴀɴʏᴏɴᴇ"
    await anim(c, "cute", reply_to=e.message.id, cycles=3, final=f"🩷 ᴛɪᴄᴋʟᴇꜱ {tgt}")

@cmd("blush")
async def c_blush(e, a, r, c):
    await anim(c, "blush", reply_to=e.message.id, cycles=3, final="🩵 ʙʟᴜꜱʜ")

@cmd("shy")
async def c_shy(e, a, r, c):
    await notify(c, "🩵 ꜱʜʏ", reply_to=e.message.id)

@cmd("pout")
async def c_pout(e, a, r, c):
    await notify(c, "🩵 ᴘᴏᴜᴛ", reply_to=e.message.id)

@cmd("uwu")
async def c_uwu(e, a, r, c):
    await notify(c, "🩷 uwu", reply_to=e.message.id)

@cmd("owo")
async def c_owo(e, a, r, c):
    await notify(c, "🩷 owo", reply_to=e.message.id)

@cmd("nya")
async def c_nya(e, a, r, c):
    await anim(c, "cat", reply_to=e.message.id, cycles=3, final="🩷 ɴʏᴀᴀᴀ")

@cmd("purr")
async def c_purr(e, a, r, c):
    await notify(c, "🩷 ᴘᴜʀʀʀʀʀ", reply_to=e.message.id)

@cmd("meow")
async def c_meow(e, a, r, c):
    await notify(c, "🩷 ᴍᴇᴏᴡ", reply_to=e.message.id)

@cmd("woof")
async def c_woof(e, a, r, c):
    await notify(c, "🩷 ᴡᴏᴏғ", reply_to=e.message.id)

@cmd("sparkle")
async def c_sparkle(e, a, r, c):
    await anim(c, "sparkle", reply_to=e.message.id, cycles=3, final="🩷 ꜱᴘᴀʀᴋʟᴇ")

@cmd("flower")
async def c_flower(e, a, r, c):
    tgt = (await user.get_entity(r.sender_id)).first_name if r else "ᴀɴʏᴏɴᴇ"
    await anim(c, "flower", reply_to=e.message.id, cycles=3, final=f"🩷 ғʟᴏᴡᴇʀ ғᴏʀ {tgt}")

@cmd("hearteyes")
async def c_hearteyes(e, a, r, c):
    tgt = (await user.get_entity(r.sender_id)).first_name if r else "ᴀɴʏᴏɴᴇ"
    await anim(c, "hearts", reply_to=e.message.id, cycles=3, final=f"🩷 {tgt} ɪꜱ ᴄᴜᴛᴇ")

# ═══════ MOD ═══════
@cmd("warn")
async def c_warn(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    uid = str(r.sender_id)
    STATE["warns"][uid] = STATE["warns"].get(uid, 0) + 1; save()
    n = STATE["warns"][uid]
    await notify(c, f"🩷 ᴡᴀʀɴ {n}/3", reply_to=e.message.id)
    if n >= 3:
        try: await user.kick_participant(c, r.sender_id)
        except: pass

@cmd("warns")
async def c_warns(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    await notify(c, f"🩷 ᴡᴀʀɴꜱ {STATE['warns'].get(str(r.sender_id), 0)}/3",
                 reply_to=e.message.id)

@cmd("unwarn")
async def c_unwarn(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    STATE["warns"].pop(str(r.sender_id), None); save()
    await notify(c, "🩷 ᴄʟᴇᴀʀᴇᴅ", reply_to=e.message.id)

@cmd("ban")
async def c_ban(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try:
        await user.edit_permissions(c, r.sender_id, view_messages=False)
        await notify(c, "🩷 ʙᴀɴɴᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"🩵 ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("unban")
async def c_unban(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try:
        await user.edit_permissions(c, r.sender_id, view_messages=True)
        await notify(c, "🩷 ᴜɴʙᴀɴɴᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"🩵 ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("mute")
async def c_mute(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try:
        await user.edit_permissions(c, r.sender_id, send_messages=False)
        await notify(c, "🩷 ᴍᴜᴛᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"🩵 ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("unmute")
async def c_unmute(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    try:
        await user.edit_permissions(c, r.sender_id, send_messages=True)
        await notify(c, "🩷 ᴜɴᴍᴜᴛᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"🩵 ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("pin")
async def c_pin(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴀ ᴍꜱɢ", reply_to=e.message.id)
    try:
        await user.pin_message(c, r.id)
        await notify(c, "🩷 ᴘɪɴɴᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"🩵 ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("unpin")
async def c_unpin(e, a, r, c):
    try:
        await user.unpin_message(c)
        await notify(c, "🩷 ᴜɴᴘɪɴɴᴇᴅ", reply_to=e.message.id)
    except Exception as ex: await notify(c, f"🩵 ғᴀɪʟ · {ex}", reply_to=e.message.id)

@cmd("blacklist")
async def c_blacklist(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    if r.sender_id not in STATE["blacklist"]:
        STATE["blacklist"].append(r.sender_id); save()
    await notify(c, f"🩷 ʙʟᴀᴄᴋʟɪꜱᴛ · {len(STATE['blacklist'])}", reply_to=e.message.id)

@cmd("unblacklist")
async def c_unblacklist(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    if r.sender_id in STATE["blacklist"]:
        STATE["blacklist"].remove(r.sender_id); save()
    await notify(c, "🩷 ʀᴇᴍᴏᴠᴇᴅ", reply_to=e.message.id)

@cmd("antilink")
async def c_antilink(e, a, r, c):
    STATE["antilink"] = a.strip().lower() in ("on","1","true","yes"); save()
    await notify(c, f"🩷 ᴀɴᴛɪʟɪɴᴋ · {'ᴏɴ' if STATE['antilink'] else 'ᴏғғ'}",
                 reply_to=e.message.id)

@cmd("antispam")
async def c_antispam(e, a, r, c):
    STATE["antispam"] = a.strip().lower() in ("on","1","true","yes"); save()
    await notify(c, f"🩷 ᴀɴᴛɪꜱᴘᴀᴍ · {'ᴏɴ' if STATE['antispam'] else 'ᴏғғ'}",
                 reply_to=e.message.id)

# ═══════ FILTERS ═══════
@cmd("filter")
async def c_filter(e, a, r, c):
    p = a.split(maxsplit=1)
    if len(p) < 2: return await notify(c, "🩵 ᴜꜱᴇ · !ꜰɪʟᴛᴇʀ <ᴋᴡ> <ʀᴇᴘʟʏ>", reply_to=e.message.id)
    STATE["filters"].append({"kw": p[0].lower(), "reply": p[1]}); save()
    await notify(c, f"🩷 ғɪʟᴛᴇʀ '{p[0]}'", reply_to=e.message.id)

@cmd("filters")
async def c_filters(e, a, r, c):
    if not STATE["filters"]: return await notify(c, "🩵 ɴᴏɴᴇ", reply_to=e.message.id)
    body = "\n".join(f"  🤍 {i+1:02d}. {f['kw']}" for i, f in enumerate(STATE["filters"]))
    await notify(c, f"🩷 ғɪʟᴛᴇʀꜱ\n{body}", reply_to=e.message.id)

@cmd("stopfilter")
async def c_stopfilter(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ꜱᴛᴏᴘꜰɪʟᴛᴇʀ <ᴋᴡ>", reply_to=e.message.id)
    before = len(STATE["filters"])
    STATE["filters"] = [f for f in STATE["filters"] if f["kw"] != a.lower()]; save()
    await notify(c, f"🩷 ʀᴇᴍᴏᴠᴇᴅ {before - len(STATE['filters'])}", reply_to=e.message.id)

@cmd("autoreply")
async def c_autoreply(e, a, r, c):
    p = a.split(maxsplit=1)
    if len(p) < 2: return await notify(c, "🩵 ᴜꜱᴇ · !ᴀᴜᴛᴏʀᴇᴘʟʏ <ᴋ> <ᴠ>", reply_to=e.message.id)
    STATE["bot_notes"][p[0].lower()] = p[1]; save()
    await notify(c, f"🩷 '{p[0]}'", reply_to=e.message.id)

@cmd("autoreplies")
async def c_autoreplies(e, a, r, c):
    if not STATE["bot_notes"]: return await notify(c, "🩵 ɴᴏɴᴇ", reply_to=e.message.id)
    body = "\n".join(f"  🤍 {k}: {v[:40]}" for k, v in STATE["bot_notes"].items())
    await notify(c, f"🩷 ᴀᴜᴛᴏʀᴇᴘʟɪᴇꜱ\n{body}", reply_to=e.message.id)

# ═══════ GAMES ═══════
@cmd("toss")
async def c_toss(e, a, r, c):
    await anim(c, "spin", reply_to=e.message.id, cycles=2,
               final=f"🩷 {random.choice(['ʜᴇᴀᴅꜱ','ᴛᴀɪʟꜱ']).upper()}")

@cmd("dice")
async def c_dice(e, a, r, c):
    await notify(c, f"🩷 ᴅɪᴄᴇ · {random.randint(1,6)}", reply_to=e.message.id)

@cmd("roll")
async def c_roll(e, a, r, c):
    try: hi = int(a) if a else 100
    except: hi = 100
    await notify(c, f"🩷 ʀᴏʟʟ · {random.randint(1,hi)}/{hi}", reply_to=e.message.id)

@cmd("8ball")
async def c_8ball(e, a, r, c):
    ans = ["ʏᴇꜱ","ɴᴏ","ᴍᴀʏʙᴇ","ᴀꜱᴋ ᴀɢᴀɪɴ","ᴄᴇʀᴛᴀɪɴ","ᴅᴏᴜʙᴛғᴜʟ"]
    await notify(c, f"🩷 {random.choice(ans)}", reply_to=e.message.id)

@cmd("coin")
async def c_coin(e, a, r, c):
    await anim(c, "spin", reply_to=e.message.id, cycles=2,
               final=f"🩷 {random.choice(['ʜᴇᴀᴅꜱ','ᴛᴀɪʟꜱ']).upper()}")

@cmd("flip")
async def c_flip(e, a, r, c):
    await anim(c, "spin", reply_to=e.message.id, cycles=2,
               final=f"🩷 {random.choice(['ʜᴇᴀᴅꜱ','ᴛᴀɪʟꜱ']).upper()}")

@cmd("ship")
async def c_ship(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    pct = random.randint(1, 100)
    bar = "▰" * (pct // 10) + "▱" * (10 - pct // 10)
    await notify(c, f"🩷 ꜱʜɪᴘ · {pct}%\n  {bar}", reply_to=e.message.id)

@cmd("rps")
async def c_rps(e, a, r, c):
    choices = ["rock", "paper", "scissors"]
    if a.lower() not in choices:
        return await notify(c, "🩵 ᴜꜱᴇ · !ʀᴘꜱ rock|paper|scissors", reply_to=e.message.id)
    bot = random.choice(choices)
    if a.lower() == bot: res = "ᴛɪᴇ!"
    elif (a.lower(), bot) in [("rock","scissors"),("paper","rock"),("scissors","paper")]:
        res = "ʏᴏᴜ ᴡɪɴ!"
    else: res = "ʏᴏᴜ ʟᴏꜱᴇ"
    await notify(c, f"🩷 {a.lower()} vs {bot} · {res}", reply_to=e.message.id)

@cmd("iq")
async def c_iq(e, a, r, c):
    if not r: return await notify(c, "🩵 ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ", reply_to=e.message.id)
    await anim(c, "spin", reply_to=e.message.id, cycles=2,
               final=f"🩷 ɪǫ · {random.randint(50,200)}")

@cmd("rate")
async def c_rate(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ʀᴀᴛᴇ <ᴛ>", reply_to=e.message.id)
    await notify(c, f"🩷 '{a[:30]}' · {random.randint(1,10)}/10", reply_to=e.message.id)

@cmd("percent")
async def c_percent(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ᴘᴇʀᴄᴇɴᴛ <ᴛ>", reply_to=e.message.id)
    n = random.randint(0, 100)
    bar = "▰" * (n // 10) + "▱" * (10 - n // 10)
    await notify(c, f"🩷 {n}% {bar}", reply_to=e.message.id)

@cmd("pick")
async def c_pick(e, a, r, c):
    if not a: return await notify(c, "🩵 ꜱᴇᴘ ᴡɪᴛʜ ,", reply_to=e.message.id)
    opts = [o.strip() for o in a.split(",") if o.strip()]
    if not opts: return await notify(c, "🩵 ɴᴏɴᴇ", reply_to=e.message.id)
    await anim(c, "spin", reply_to=e.message.id, cycles=2,
               final=f"🩷 ᴘɪᴄᴋ · {random.choice(opts)}")

@cmd("magic8")
async def c_magic8(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴀꜱᴋ ᴀ ǫᴜᴇꜱᴛɪᴏɴ", reply_to=e.message.id)
    ans = ["ᴀʙꜱᴏʟᴜᴛᴇʟʏ","ɴᴏ","ᴍᴀʏʙᴇ","ᴜɴᴄʟᴇᴀʀ","ᴛʀʏ ᴀɢᴀɪɴ",
           "ᴡɪᴛʜᴏᴜᴛ ᴀ ᴅᴏᴜʙᴛ","ᴜɴʟɪᴋᴇʟʏ","ꜱᴛᴀʀꜱ ꜱᴀʏ ʏᴇꜱ"]
    await anim(c, "magic", reply_to=e.message.id, cycles=2,
               final=f"🩷 {random.choice(ans)}")

# ═══════ CLUSTER ═══════
@cmd("adduser")
async def c_adduser(e, a, r, c):
    if not is_owner(e.sender_id): return
    oid = _owner()
    if not (e.is_private and e.chat_id == oid):
        return await notify(c, "🩵 ʀᴜɴ ɪɴ ꜱᴀᴠᴇᴅ ᴍꜱɢꜱ", reply_to=e.message.id)
    PENDING[(oid, c)] = {"kind": "adduser", "step": "api_id"}
    await notify(c,
        "🩷 ꜱᴛᴇᴘ 1/4\n🤍 ꜱᴇɴᴅ API_ID\n🩵 /ᴄᴀɴᴄᴇʟ ᴛᴏ ꜱᴛᴏᴘ",
        reply_to=e.message.id)

@cmd("leave")
async def c_leave_all(e, a, r, c):
    ok, fail = 0, 0
    for cli in _cluster_clients():
        try:
            await cli(functions.channels.LeaveChannelRequest(c))
            ok += 1; await asyncio.sleep(0.8)
        except: fail += 1
    await notify(c, f"🩷 ʟᴇꜰᴛ {ok} · ғᴀɪʟ {fail}", reply_to=e.message.id)

@cmd("addall")
async def c_addall(e, a, r, c):
    if e.is_private: return await notify(c, "🩵 ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ", reply_to=e.message.id)
    try:
        invite = await user(functions.messages.ExportChatInviteRequest(c))
        hash_ = invite.link.split("/")[-1]
    except Exception as ex: return await notify(c, f"🩵 ғᴀɪʟ · {ex}", reply_to=e.message.id)
    ok, fail = 0, 0
    for cli in _cluster_clients():
        try:
            await cli(functions.messages.ImportChatInviteRequest(hash_))
            ok += 1; await asyncio.sleep(1.5)
        except UserAlreadyParticipantError: ok += 1
        except: fail += 1
    await notify(c, f"🩷 ᴊᴏɪɴᴇᴅ {ok} · ғᴀɪʟ {fail}", reply_to=e.message.id)

@cmd("promoteall")
async def c_promoteall(e, a, r, c):
    if e.is_private: return await notify(c, "🩵 ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ", reply_to=e.message.id)
    ok, fail = 0, 0
    for cli in _cluster_clients():
        try:
            me = await cli.get_me()
            await user.edit_admin(c, me.id, change_info=True, delete_messages=True,
                                  ban_users=True, invite_users=True, pin_messages=True)
            ok += 1; await asyncio.sleep(0.8)
        except: fail += 1
    await notify(c, f"🩷 ᴘʀᴏᴍᴏᴛᴇᴅ {ok} · ғᴀɪʟ {fail}", reply_to=e.message.id)

@cmd("pall")
async def c_pall(e, a, r, c):
    if e.is_private: return await notify(c, "🩵 ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ", reply_to=e.message.id)
    ok, fail = 0, 0
    for cli in _cluster_clients():
        try:
            me = await cli.get_me()
            await user.edit_admin(c, me.id, change_info=True, delete_messages=True,
                                  ban_users=True, invite_users=True, pin_messages=True)
            ok += 1; await asyncio.sleep(0.6)
        except: fail += 1
    await notify(c, f"🩷 ᴀʟʟ-ᴀᴅᴍɪɴ {ok} · ғᴀɪʟ {fail}", reply_to=e.message.id)

@cmd("rrall")
async def c_rrall(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ʀʀᴀʟʟ <ᴛ>", reply_to=e.message.id)
    STATE["rrall"] = {"chat": c, "text": a}; save()
    n = len(_cluster_clients())
    await notify(c, f"🩷 ʀʀᴀʟʟ · {n} ᴄʟɪᴇɴᴛꜱ\n🤍 ꜱᴛᴏᴘ · !ʀʀꜱᴛᴏᴘ",
                 reply_to=e.message.id)

@cmd("rrstop")
async def c_rrstop(e, a, r, c):
    STATE["rrall"] = None; save()
    _rrall_seen.clear()
    await notify(c, "🩷 ꜱᴛᴏᴘᴘᴇᴅ", reply_to=e.message.id)

@cmd("purgeall")
async def c_purgeall(e, a, r, c):
    if a.strip().lower() != "yes":
        return await notify(c, "🩵 ᴄᴏɴꜰɪʀᴍ · !ᴘᴜʀɢᴇᴀʟʟ ʏᴇꜱ", reply_to=e.message.id)
    total = 0
    for cli in _cluster_clients():
        try:
            async for d in cli.iter_dialogs():
                if d.is_group or d.is_channel:
                    try:
                        await cli(functions.channels.LeaveChannelRequest(d.id))
                        total += 1; await asyncio.sleep(0.8)
                    except: pass
        except: pass
    await notify(c, f"🩷 ᴘᴜʀɢᴇᴅ {total}", reply_to=e.message.id)

# ═══════ CHUDAI ═══════
@cmd("chudai")
async def c_chudai(e, a, r, c):
    if not a: return await notify(c, "🩵 ᴜꜱᴇ · !ᴄʜᴜᴅᴀɪ <ɴᴀᴍᴇ>", reply_to=e.message.id)
    cluster = _cluster_clients()
    texts = STATE.get("chudai_texts") or [CHUDAI_DEFAULT]
    target = r.id if r else e.message.id
    for i, cli in enumerate(cluster):
        spawn(f"chudai:{c}:{i}", _chudai_loop(cli, c, a, target, texts))
    await notify(c, f"🩷 ᴄʜᴜᴅᴀɪ · {a}\n🤍 {len(cluster)} ᴄʟɪᴇɴᴛꜱ\n🩵 ꜱᴛᴏᴘ · !ʀᴜᴋ",
                 reply_to=e.message.id)

# ─── ANTI-FREEZE CHUDAI LOOP ───
async def _chudai_loop(cli, chat, name, reply_to, texts):
    idx = 0
    while True:
        tpl = texts[idx % len(texts)]; idx += 1
        text = tpl.replace("{name}", name)
        try:
            m = await asyncio.wait_for(cli.send_message(chat, text, reply_to=reply_to), timeout=10.0)
            remember(m, cli)
        except asyncio.TimeoutError:
            print("[chudai] timeout, sleeping 5s")
            await asyncio.sleep(5); continue
        except FloodWaitError as fw: 
            print(f"[chudai] flood wait {fw.seconds}s")
            await asyncio.sleep(min(fw.seconds, 20) + 2); continue
        except PeerFloodError:
            print("[chudai] peer flood, sleeping 15s")
            await asyncio.sleep(15); continue
        except Exception: 
            await asyncio.sleep(2.0)
        
        # Force min 0.8s delay for chudai to prevent rapid ban
        base_delay = max(0.8, STATE["delay"])
        await asyncio.sleep(base_delay + random.uniform(0.1, 0.5))

@cmd("addchudai")
async def c_addchudai(e, a, r, c):
    text = a or (r.raw_text if r else "")
    if not text: return await notify(c, "🩵 ᴜꜱᴇ · !ᴀᴅᴅᴄʜᴜᴅᴀɪ <ᴛ>", reply_to=e.message.id)
    STATE["chudai_texts"].append(text); save()
    await notify(c, f"🩷 ᴀᴅᴅᴇᴅ · {len(STATE['chudai_texts'])}", reply_to=e.message.id)

@cmd("listchudai")
async def c_listchudai(e, a, r, c):
    texts = STATE.get("chudai_texts") or []
    if not texts: return await notify(c, "🩵 ᴇᴍᴘᴛʏ", reply_to=e.message.id)
    lines = [f"🩷 ᴄʜᴜᴅᴀɪ · {len(texts)}", ""]
    for i, t in enumerate(texts):
        preview = t.replace("\n", " ⏎ ")[:60]
        lines.append(f"  🤍 {i+1:02d} · {preview}")
    await notify(c, "\n".join(lines), reply_to=e.message.id)

@cmd("delchudai")
async def c_delchudai(e, a, r, c):
    try:
        i = int(a) - 1; t = STATE["chudai_texts"].pop(i); save()
        await notify(c, f"🩷 ʀᴇᴍᴏᴠᴇᴅ · {t[:40]}", reply_to=e.message.id)
    except: await notify(c, "🩵 ᴜꜱᴇ · !ᴅᴇʟᴄʜᴜᴅᴀɪ 1", reply_to=e.message.id)

# ═══════ BOT POOL ═══════
MAIN_BOT_REPLY = "🩷 s1ɴ ᴏɴʟɪɴᴇ"

# ─── ANTI-FREEZE BOT RAID ALL ───
async def bot_raid_all(chat, text, reply_to=None):
    delay = STATE["delay"]; count = STATE["count"]
    async def w(bot):
        n = 0
        while True:
            if count and n >= count: return
            try:
                m = await asyncio.wait_for(bot.send_message(chat, text, reply_to=reply_to), timeout=10.0)
                remember(m, bot)
                d = STATE.get("autodel", 0)
                if d: asyncio.create_task(_autodel(bot, m.chat_id, m.id, d))
            except asyncio.TimeoutError: await asyncio.sleep(5); continue
            except FloodWaitError as fw: await asyncio.sleep(min(fw.seconds, 20) + 2); continue
            except Exception: await asyncio.sleep(2.0)
            n += 1
            await asyncio.sleep(delay)
    await asyncio.gather(*[w(b) for b in BOTS], return_exceptions=True)

async def boot_bots():
    global BOTS
    for c in BOTS:
        try: await c.disconnect()
        except: pass
    BOTS = []; names = []
    for i, tok in enumerate(_real_state["bots"]):
        try:
            cli = TelegramClient(f"s1n_bot_{i}", API_ID, API_HASH)
            await cli.start(bot_token=tok)
            me = await cli.get_me()
            names.append(me.username or me.first_name)
            BOTS.append(cli)
            if i == _real_state.get("main_bot", 0): _register_main(cli)
        except Exception as ex: print(f"[bot:{i}] {ex}")
    if names: _real_state["bot_names"] = names; save()
    print(f"[s1n] {len(BOTS)} bot(s) → {', '.join(names) or '—'}")

def _register_main(cli):
    @cli.on(events.NewMessage(incoming=True))
    async def _main(ev):
        if ev.is_private and not ev.out:
            try: await ev.reply(MAIN_BOT_REPLY)
            except: pass

@botcmd("setbots")
async def b_setbots(e, a, r, c):
    raw = a or (r.raw_text if r else "") or ""
    toks = [t.strip() for t in re.split(r"[\s,]+", raw) if ":" in t]
    if not toks: return await notify(c, "🩵 ᴜꜱᴇ · .ꜱᴇᴛʙᴏᴛꜱ <ᴛᴏᴋᴇɴꜱ>", reply_to=e.message.id)
    _real_state["bots"] = toks; save()
    await loading(c, f"ʙᴏᴏᴛɪɴɢ {len(toks)}", reply_to=e.message.id)
    await boot_bots()
    listing = "\n".join(f"  🤍 {i+1:02d} · @{n}" for i, n in enumerate(_real_state["bot_names"]))
    await notify(c, f"🩷 ɴᴇᴛᴡᴏʀᴋ\n{listing or '  —'}")

@botcmd("botlist")
async def b_botlist(e, a, r, c):
    if not _real_state.get("bot_names"): return await notify(c, "🩵 ᴇᴍᴘᴛʏ", reply_to=e.message.id)
    main = _real_state.get("main_bot", 0)
    lines = [f"  🤍 {i+1:02d} · @{n}{' ᴍᴀɪɴ' if i == main else ''}"
             for i, n in enumerate(_real_state["bot_names"])]
    await notify(c, "🩷 ɴᴇᴛᴡᴏʀᴋ\n" + "\n".join(lines), reply_to=e.message.id)

@botcmd("bstatus")
async def b_bstatus(e, a, r, c):
    lines = []
    for i, b in enumerate(BOTS):
        try:
            me = await b.get_me()
            tag = " ᴍᴀɪɴ" if i == _real_state.get("main_bot", 0) else ""
            lines.append(f"  🤍 {i+1:02d} · @{me.username} ✔{tag}")
        except: lines.append(f"  🤍 {i+1:02d} · ᴏғғʟɪɴᴇ")
    body = "\n".join(lines) or "  —"
    await notify(c, f"🩷 ʙᴏᴛꜱ\n{body}", reply_to=e.message.id)

@botcmd("braid")
async def b_braid(e, a, r, c):
    if not BOTS: return await notify(c, "🩵 ɴᴏ ʙᴏᴛꜱ", reply_to=e.message.id)
    t = a or random.choice(STATE["texts"])
    spawn_bot(f"braid:{c}", bot_raid_all(c, t))
    await anim(c, "fire", reply_to=e.message.id, final=f"🩷 ʙᴏᴛ ʀᴀɪᴅ ×{len(BOTS)}")

@botcmd("ball")
async def b_ball(e, a, r, c):
    if not BOTS: return await notify(c, "🩵 ɴᴏ ʙᴏᴛꜱ", reply_to=e.message.id)
    t = a or random.choice(STATE["texts"])
    ok = 0
    for b in BOTS:
        try:
            m = await b.send_message(c, t); remember(m, b); ok += 1
            await asyncio.sleep(0.6)
        except: pass
    await notify(c, f"🩷 ʙᴄᴀꜱᴛ {ok}/{len(BOTS)}", reply_to=e.message.id)

@botcmd("clearbots")
async def b_clearbots(e, a, r, c):
    global BOTS
    for x in BOTS:
        try: await x.disconnect()
        except: pass
    BOTS = []
    _real_state["bots"] = []; _real_state["bot_names"] = []
    _real_state["main_bot"] = 0; save()
    await notify(c, "🩷 ᴘᴜʀɢᴇᴅ", reply_to=e.message.id)

# ═══════ MENUS ═══════
@cmd("help")
async def c_help(e, a, r, c):
    txt = (
        "🩷 " + sb("S1N MENU") + "\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🩷 " + sb("RAID") + "\n"
        "  !spm  !mc  !raidtext  !raidmention  !raidnum\n"
        "  !raidvoice  !raidsticker  !traid  !tst  !dbrk  !brk\n"
        "  !rpraid  !ruk  !raidlist  !stopraid\n\n"
        "🤍 " + sb("SPAM") + "\n"
        "  !sps  !spl  !spz  !spf  !spr  !spx  !spo  !spamall\n"
        "  !spamslow  !spamfast  !randspam  !wavespam  !matrix\n"
        "  !bomb  !rain  !flood  !chain  !stutter  !upsidedown\n"
        "  !capsbomb  !emojibomb  !stickerbomb  !lovebomb\n\n"
        "🩵 " + sb("GROUP") + "\n"
        "  !gcreate  !ginfo  !gmembers  !gid  !ginvite  !gleave\n"
        "  !gtitle  !gdesc  !gunpin  !tagall\n"
        "  !gkick  !gban  !gunban  !gmute  !gunmute\n"
        "  !gpromote  !gdemote\n\n"
        "🩷 " + sb("VOICE") + "\n"
        "  !vjoin  !vleave  !vstop  !setvchudai  !vchudai\n\n"
        "🤍 " + sb("SONG") + "\n"
        "  !s  !splay  !ssearch  !lyrics  !kawai\n\n"
        "🩵 " + sb("MODERATION") + "\n"
        "  !warn  !warns  !unwarn  !ban  !unban  !mute  !unmute\n"
        "  !pin  !unpin  !purge  !del  !purgeall\n"
        "  !antilink  !antispam  !blacklist  !unblacklist\n\n"
        "🩷 " + sb("CUTE") + "\n"
        "  !hug  !slap  !kiss  !cuddle  !pat  !boop  !lick  !bite\n"
        "  !tickle  !blush  !shy  !pout  !uwu  !owo  !nya  !purr\n"
        "  !meow  !woof  !sparkle  !flower  !hearteyes\n"
        "  !cry  !dance  !love  !hate  !punch  !run  !spin\n\n"
        "🤍 " + sb("GAMES") + "\n"
        "  !toss  !dice  !roll  !8ball  !coin  !flip  !ship  !rps\n"
        "  !iq  !rate  !percent  !pick  !magic8\n\n"
        "🩵 " + sb("UTILS") + "\n"
        "  !ping  !alive  !id  !stats  !uptime  !myid  !time\n"
        "  !afk  !unafk  !save  !get  !note  !notes  !timer\n"
        "  !delays  !delay  !count  !autodel  !anim\n"
        "  !addtext  !deltext  !listtext\n"
        "  !calc  !b64  !unb64  !hash  !md5  !hex  !rot13  !zalgo\n"
        "  !smallcaps\n\n"
        "🩷 " + sb("FILTERS") + "\n"
        "  !filter  !filters  !stopfilter  !autoreply  !autoreplies\n\n"
        "🤍 " + sb("CLUSTER") + "\n"
        "  !adduser  !leave  !addall  !promoteall  !pall\n"
        "  !rrall  !rrstop  !chudai  !addchudai  !listchudai  !delchudai\n\n"
        "🩵 " + sb("BOTS") + "\n"
        "  .setbots  .botlist  .bstatus  .braid  .ball  .clearbots\n\n"
        "🩷 " + sb("!helpext") + " " + sb("for extended list.")
    )
    await anim(c, "load", reply_to=e.message.id, final=txt)

@cmd("helpext")
async def c_helpext(e, a, r, c):
    txt = (
        "🩷 " + sb("EXTENDED") + "\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🩷 " + sb("RAID EXTRAS") + "\n"
        "  !raidtext <t>     — text loop\n"
        "  !raidmention      — mention + spam\n"
        "  !raidnum          — count 1,2,3…\n"
        "  !raidvoice        — TTS voice raid\n"
        "  !raidsticker      — sticker raid\n"
        "  !raidlist         — list active\n"
        "  !stopraid         — stop all\n\n"
        "🤍 " + sb("SPAM EXTRAS") + "\n"
        "  !spo <n> <t>      — ordered spam\n"
        "  !spamslow <t>     — slow loop\n"
        "  !spamfast <t>     — fast loop\n"
        "  !randspam         — random text loop\n\n"
        "🩵 " + sb("GROUP EXTRAS") + "\n"
        "  !gcreate <n>      — create group\n"
        "  !ginfo            — group info\n"
        "  !gmembers         — member count\n"
        "  !gid              — chat id\n"
        "  !ginvite @u       — invite user\n"
        "  !gtitle <t>       — rename\n"
        "  !gdesc <t>        — set desc\n"
        "  !gunpin           — unpin all\n"
        "  !gkick !gban !gunban !gmute !gunmute\n"
        "  !gpromote !gdemote !gleave\n\n"
        "🩷 " + sb("VOICE EXTRAS") + "\n"
        "  !vjoin            — join vc\n"
        "  !vleave           — leave vc\n"
        "  !vstop            — all clients leave\n"
        "  !setvchudai       — save vc audio\n"
        "  !vchudai          — play saved audio\n\n"
        "🤍 " + sb("UTILS EXTRAS") + "\n"
        "  !delays <s>       — set every delay\n"
        "  !delay <s>        — userbot delay\n"
        "  !count <n>        — burst limit\n"
        "  !autodel <s>      — auto-delete\n"
        "  !anim on|off      — animation toggle\n"
        "  !addtext <t>      — add text\n"
        "  !deltext <i>      — remove text\n"
        "  !listtext         — show vault\n"
        "  !save (reply)     — save msg\n"
        "  !get <k>          — fetch saved\n"
        "  !note / !notes    — text notes\n"
        "  !timer <s>        — countdown\n\n"
        "🩵 " + sb("CLUSTER EXTRAS") + "\n"
        "  !adduser          — add worker (saved)\n"
        "  !addall           — join all to chat\n"
        "  !promoteall       — promote all\n"
        "  !pall             — full admin\n"
        "  !leave            — all leave\n"
        "  !purgeall yes     — leave all chats\n"
        "  !rrall <t>        — reply-all\n"
        "  !rrstop           — stop reply-all\n"
        "  !chudai <name>    — cluster chudai\n"
        "  !addchudai <t>    — add variant\n"
        "  !listchudai       — list variants\n"
        "  !delchudai <i>    — remove one\n\n"
        "🩷 " + sb("BOTS") + "\n"
        "  .setbots <t>      — load bot tokens\n"
        "  .botlist          — show pool\n"
        "  .bstatus          — health check\n"
        "  .braid <t>        — all bots spam\n"
        "  .ball <t>         — all bots send once\n"
        "  .clearbots        — purge tokens"
    )
    await anim(c, "load", reply_to=e.message.id, final=txt)

# ═══════ ROUTER + ENGINE ═══════
CMD_RE = re.compile(r"^!([a-zA-Z]\w*)(?:[\s\n]+([\s\S]*))?$")
BOT_RE = re.compile(r"^\.([a-zA-Z]\w*)(?:@\d+)?(?:[\s\n]+([\s\S]*))?$")
_last_msg = {}
_rrall_seen = set()

async def _dispatch(event, raw):
    chat = event.chat_id; msg = event.message
    try: reply = await event.get_reply_message() if msg.reply_to else None
    except Exception: reply = None
    if STATE.get("autodel"):
        asyncio.create_task(_autodel(user, msg.chat_id, msg.id, STATE["autodel"]))
    STATE["stats_cmds"] = STATE.get("stats_cmds", 0) + 1
    m = CMD_RE.match(raw)
    if m:
        fn = C.get(m.group(1).lower())
        if not fn: return
        try: await fn(event, (m.group(2) or "").strip(), reply, chat)
        except Exception as ex: await notify(chat, f"🩵 ᴇʀʀᴏʀ · {ex}")
        return
    m = BOT_RE.match(raw)
    if m:
        fn = BOTC.get(m.group(1).lower())
        if not fn: return
        try: await fn(event, (m.group(2) or "").strip(), reply, chat)
        except Exception as ex: await notify(chat, f"🩵 ᴇʀʀᴏʀ · {ex}")

async def _rrall_reply(cli, chat, msg_id, text):
    try:
        m = await cli.send_message(chat, text, reply_to=msg_id)
        remember(m, cli)
    except FloodWaitError as fw: await asyncio.sleep(fw.seconds + 1)
    except: pass

async def _run_engine(event):
    msg = event.message
    if not msg.sender_id: return
    uid = msg.sender_id; chat = event.chat_id
    STATE["stats_msgs"] = STATE.get("stats_msgs", 0) + 1
    rrall = STATE.get("rrall")
    if rrall and rrall.get("chat") == chat and msg.id not in _rrall_seen:
        _rrall_seen.add(msg.id)
        if len(_rrall_seen) > 3000: _rrall_seen.clear()
        for cli in _cluster_clients():
            spawn(f"rrall:{chat}:{msg.id}:{id(cli)}",
                  _rrall_reply(cli, chat, msg.id, rrall["text"]))
    if STATE.get("afk") and msg.is_private and not is_owner(uid):
        try: await event.reply(STATE["afk"])
        except: pass
        return
    if uid in STATE.get("blacklist", []):
        try: await msg.delete()
        except: pass
        return
    if uid in STATE["muted"]:
        try: await msg.delete()
        except: pass
        return
    if STATE.get("antilink") and msg.raw_text:
        if re.search(r"(https?://|t\.me/|@\w+bot)", msg.raw_text):
            try: await msg.delete()
            except: pass
            return
    if STATE.get("antispam"):
        now = time.time(); key = (chat, uid)
        bucket = [t for t in _last_msg.get(key, []) if now - t < 3]
        bucket.append(now); _last_msg[key] = bucket
        if len(bucket) > 5:
            try: await msg.delete()
            except: pass
            return
    if STATE.get("greet") and isinstance(msg.action, types.MessageActionChatAddUser):
        try: await user.send_message(chat, STATE["greet"])
        except: pass
    if msg.raw_text:
        low = msg.raw_text.lower()
        for f in STATE.get("filters", []):
            if f["kw"] in low:
                try:
                    m = await user.send_message(chat, f["reply"], reply_to=msg.id)
                    remember(m)
                except: pass
                break
        for k, v in STATE.get("bot_notes", {}).items():
            if k in low:
                try:
                    m = await user.send_message(chat, v, reply_to=msg.id)
                    remember(m)
                except: pass
                break
    if uid in STATE["traid"] and STATE["texts"]:
        try:
            m = await user.send_message(chat, random.choice(STATE["texts"]),
                                        reply_to=msg.id)
            remember(m)
        except: pass
    if uid in STATE["tst"]:
        await send_saved_sticker(chat, reply_to=msg.id)

async def _handle_pending(event, st, raw):
    if st.get("kind") != "adduser":
        PENDING.pop((_owner(), event.chat_id), None); return
    oid = _owner(); chat = event.chat_id
    if raw.strip().lower() in ("/cancel", "cancel"):
        PENDING.pop((oid, chat), None)
        return await event.reply(style("🩵 ᴄᴀɴᴄᴇʟʟᴇᴅ"))
    step = st["step"]
    if step == "api_id":
        if not raw.strip().isdigit():
            return await event.reply(style("🩵 ᴅɪɢɪᴛꜱ ᴏɴʟʏ"))
        st["api_id"] = int(raw.strip()); st["step"] = "api_hash"
        return await event.reply(style("🩷 ꜱᴛᴇᴘ 2/4\n🤍 ꜱᴇɴᴅ API_HASH"))
    if step == "api_hash":
        if len(raw.strip()) < 20:
            return await event.reply(style("🩵 ᴛᴏᴏ ꜱʜᴏʀᴛ"))
        st["api_hash"] = raw.strip(); st["step"] = "phone"
        return await event.reply(style("🩷 ꜱᴛᴇᴘ 3/4\n🤍 ꜱᴇɴᴅ ᴘʜᴏɴᴇ (+ᴄᴏᴅᴇ)"))
    if step == "phone":
        cli = TelegramClient(StringSession(), st["api_id"], st["api_hash"])
        await cli.connect()
        try: sent = await cli.send_code_request(raw.strip())
        except PhoneNumberInvalidError:
            await cli.disconnect()
            return await event.reply(style("🩵 ɪɴᴠᴀʟɪᴅ"))
        except FloodWaitError as fw:
            await cli.disconnect()
            return await event.reply(style(f"🩵 ғʟᴏᴏᴅ {fw.seconds}ꜱ"))
        except Exception as exc:
            await cli.disconnect()
            return await event.reply(style(f"🩵 ᴇʀʀ · {exc}"))
        st["_cli"] = cli; st["phone"] = raw.strip()
        st["code_hash"] = sent.phone_code_hash; st["step"] = "code"
        return await event.reply(style("🩷 ꜱᴛᴇᴘ 4/4\n🤍 ꜱᴇɴᴅ ᴄᴏᴅᴇ"))
    if step == "code":
        code = re.sub(r"\D", "", raw)
        try:
            await st["_cli"].sign_in(
                phone=st["phone"], code=code, phone_code_hash=st["code_hash"])
        except SessionPasswordNeededError:
            st["step"] = "password"
            return await event.reply(style("🩵 2ꜰᴀ · ꜱᴇɴᴅ ᴘᴀꜱꜱᴡᴏʀᴅ"))
        except PhoneCodeInvalidError:
            return await event.reply(style("🩵 ᴡʀᴏɴɢ ᴄᴏᴅᴇ"))
        except PhoneCodeExpiredError:
            st["step"] = "phone"
            return await event.reply(style("🩵 ᴄᴏᴅᴇ ᴇxᴘɪʀᴇᴅ · ʀᴇꜱᴇɴᴅ"))
        except Exception as exc:
            return await event.reply(style(f"🩵 ғᴀɪʟ · {exc}"))
        return await _finalize_adduser(event, oid, chat, st)
    if step == "password":
        try: await st["_cli"].sign_in(password=raw)
        except Exception as exc:
            return await event.reply(style(f"🩵 2ꜰᴀ ғᴀɪʟ · {exc}"))
        return await _finalize_adduser(event, oid, chat, st)

async def _finalize_adduser(event, oid, chat, st):
    cli = st["_cli"]
    try:
        me = await cli.get_me()
        session_str = cli.session.save()
    finally:
        try: await cli.disconnect()
        except: pass
    PENDING.pop((oid, chat), None)
    cluster = CLUSTERS.get(oid)
    if not cluster:
        return await event.reply(style("🩵 ɴᴏ ᴄʟᴜꜱᴛᴇʀ"))
    existing_ids = set()
    try: existing_ids.add((await cluster["main"].get_me()).id)
    except: pass
    for w in cluster["workers"]:
        try: existing_ids.add((await w.get_me()).id)
        except: pass
    if me.id in existing_ids:
        return await event.reply(style("🩵 ᴀʟʀᴇᴀᴅʏ ɪɴ ᴄʟᴜꜱᴛᴇʀ"))
    worker = TelegramClient(StringSession(session_str), st["api_id"], st["api_hash"])
    await worker.connect()
    if not await worker.is_user_authorized():
        await worker.disconnect()
        return await event.reply(style("🩵 ʟᴏꜱᴛ"))
    cluster["workers"].append(worker)
    attach_handlers(worker, cluster["state"], oid, DB)
    await event.reply(style(
        f"🩷 ᴡᴏʀᴋᴇʀ · @{me.username or me.first_name}\n"
        f"🤍 ᴛᴏᴛᴀʟ · {len(cluster['workers'])}"))

def attach_handlers(cli, state, owner_id, db_path):
    @cli.on(events.NewMessage(outgoing=True))
    async def _router(event):
        tc = _active_client.set(event.client); ts = _active_state.set(state)
        to = _active_owner.set(owner_id); td = _active_db.set(db_path)
        try:
            msg = event.message
            if (id(event.client), event.chat_id, msg.id) in SENT_IDS: return
            raw = (msg.raw_text or "").strip()
            pending_key = (owner_id, event.chat_id)
            pending = PENDING.get(pending_key)
            if pending and not (raw and raw[0] in ("!", ".")):
                try: await _handle_pending(event, pending, raw)
                except Exception as ex:
                    await notify(event.chat_id, f"🩵 ᴇʀʀᴏʀ · {ex}",
                                 reply_to=event.message.id)
                    PENDING.pop(pending_key, None)
                return
            if not raw or raw[0] not in ("!", "."): return
            await _dispatch(event, raw)
        finally:
            _active_client.reset(tc); _active_state.reset(ts)
            _active_owner.reset(to); _active_db.reset(td)

    @cli.on(events.NewMessage(incoming=True))
    async def _engine(event):
        tc = _active_client.set(event.client); ts = _active_state.set(state)
        to = _active_owner.set(owner_id); td = _active_db.set(db_path)
        try: await _run_engine(event)
        finally:
            _active_client.reset(tc); _active_state.reset(ts)
            _active_owner.reset(to); _active_db.reset(td)

async def main():
    print("🩷 s1ɴ ᴜꜱᴇʀʙᴏᴛ ʙᴏᴏᴛɪɴɢ")
    await _real_user.start()
    me = await _real_user.get_me()
    global OWNER_ID
    OWNER_ID = me.id
    print(f"🩷 ᴏᴘᴇʀᴀᴛᴏʀ · {me.first_name} ({me.id})")
    if _real_state["bots"]: await boot_bots()
    CLUSTERS[OWNER_ID] = {"main": _real_user, "workers": [], "state": _real_state}
    attach_handlers(_real_user, _real_state, OWNER_ID, DB)
    print(f"🩷 ʀᴇᴀᴅʏ · {len(C)} ᴄᴍᴅꜱ · {len(BOTC)} ʙᴏᴛ ᴄᴍᴅꜱ")
    await _real_user.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
'''
# ═══ END OF USERBOT_TEMPLATE ═══

# ══════════════════════════════════════════════════════════════════════════════
#   HOSTER BOT (aiogram)
# ══════════════════════════════════════════════════════════════════════════════

def write_userbot_template():
    try:
        USERBOT_SCRIPT.write_text(USERBOT_TEMPLATE, encoding="utf-8")
    except Exception as e:
        print(f"[s1n] write_userbot_template failed (read-only fs?): {e}")

class HostFlow(StatesGroup):
    api_id = State()
    api_hash = State()
    phone = State()
    otp = State()
    twofa = State()

class AdminFlow(StatesGroup):
    broadcast = State()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

pending: dict = {}
running: dict = {}

def load_users() -> dict:
    if USERS_DB.exists():
        try: return json.loads(USERS_DB.read_text(encoding="utf-8"))
        except Exception: return {}
    return {}

def save_users(users: dict):
    try:
        USERS_DB.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"[s1n] save_users failed (read-only fs?): {e}")

def upsert_user(user_id: int, username, first_name: str):
    users = load_users()
    key = str(user_id)
    if key not in users:
        users[key] = {"username": username, "first_name": first_name,
                      "first_seen": datetime.now(timezone.utc).isoformat(),
                      "hosted": False}
    else:
        users[key]["username"] = username
        users[key]["first_name"] = first_name
    save_users(users)

def set_hosted_status(user_id: int, hosted: bool):
    users = load_users()
    key = str(user_id)
    if key in users:
        users[key]["hosted"] = hosted
        save_users(users)

def user_has_bot(user_id: int) -> bool:
    return (HOSTED_DIR / str(user_id) / "meta.json").exists()

def load_operators() -> set:
    ops = {OWNER_ID}
    if OPERATORS_DB.exists():
        try:
            ops |= set(int(x) for x in json.loads(OPERATORS_DB.read_text(encoding="utf-8")))
        except Exception: pass
    return ops

def save_operators(ops: set):
    try:
        OPERATORS_DB.write_text(json.dumps(sorted(ops)), encoding="utf-8")
    except Exception as e:
        print(f"[s1n] save_operators failed: {e}")

OPERATORS = load_operators()

def load_greeting() -> dict:
    defaults = {
        "photo_file_id": None,
        "text": "𝐻𝑂𝑆𝑇 ♡ \n𝑂𝑊𝑁𝐸𝑅ღ\n𝐺𝑈𝐼𝐷𝐸☘",
        "owner_url": f"https://t.me/{OWNER_USERNAME.lstrip('@')}",
        "guide_text": None,
        "greet_on": True,
    }
    if GREETING_DB.exists():
        try:
            data = json.loads(GREETING_DB.read_text(encoding="utf-8"))
            defaults.update(data)
        except Exception: pass
    return defaults

def save_greeting(g: dict):
    try:
        GREETING_DB.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"[s1n] save_greeting failed: {e}")

def _pid_file(user_id: int) -> Path:
    return HOSTED_DIR / str(user_id) / "pid"

def _kill_pid(pid: int):
    try: os.kill(pid, signal.SIGTERM)
    except Exception: pass

def kill_orphans():
    if not HOSTED_DIR.exists(): return
    for user_dir in HOSTED_DIR.iterdir():
        if not user_dir.is_dir(): continue
        pf = user_dir / "pid"
        if not pf.exists(): continue
        try:
            pid = int(pf.read_text(encoding="utf-8").strip())
            _kill_pid(pid)
        except Exception: pass
        try: pf.unlink()
        except Exception: pass

def spawn_userbot(user_id: int, api_id: int, api_hash: str, session_str: str) -> subprocess.Popen:
    user_dir = HOSTED_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["USERBOT_API_ID"] = str(api_id)
    env["USERBOT_API_HASH"] = api_hash
    env["USERBOT_SESSION"] = session_str
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    log_file = open(user_dir / "logs.txt", "a", encoding="utf-8")
    log_file.write(f"\n=== Spawn @ {datetime.now(timezone.utc).isoformat()} ===\n")
    log_file.flush()

    proc = subprocess.Popen(
        [sys.executable, str(USERBOT_SCRIPT.resolve())],
        cwd=str(user_dir.absolute()), env=env,
        stdin=subprocess.DEVNULL, stdout=log_file, stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    try: proc._log_file = log_file
    except Exception: pass
    try: _pid_file(user_id).write_text(str(proc.pid), encoding="utf-8")
    except Exception: pass
    running[user_id] = proc
    return proc

def stop_userbot(user_id: int, delete_dir: bool = False):
    proc = running.pop(user_id, None)
    if proc is not None and proc.poll() is None:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            try: proc.kill()
            except Exception: pass
    if proc is not None:
        lf = getattr(proc, "_log_file", None)
        if lf:
            try: lf.close()
            except Exception: pass
    pf = _pid_file(user_id)
    if pf.exists():
        try:
            pid = int(pf.read_text(encoding="utf-8").strip())
            _kill_pid(pid)
        except Exception: pass
        try: pf.unlink()
        except Exception: pass
    if delete_dir:
        user_dir = HOSTED_DIR / str(user_id)
        if user_dir.exists(): shutil.rmtree(user_dir, ignore_errors=True)

async def respawn_all():
    if not HOSTED_DIR.exists(): return
    for user_dir in HOSTED_DIR.iterdir():
        if not user_dir.is_dir(): continue
        meta_path = user_dir / "meta.json"
        session_path = user_dir / "session.txt"
        if not (meta_path.exists() and session_path.exists()): continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            session_str = session_path.read_text(encoding="utf-8").strip()
            uid = int(user_dir.name)
            spawn_userbot(uid, int(meta["api_id"]), meta["api_hash"], session_str)
            print(f"[s1n] respawned {uid}")
        except Exception as e:
            print(f"[s1n] respawn {user_dir.name} failed: {e}")

async def sync_hosted_flags():
    users = load_users()
    changed = False
    for key in users:
        actual = (HOSTED_DIR / key / "meta.json").exists()
        if users[key].get("hosted") != actual:
            users[key]["hosted"] = actual
            changed = True
    if changed: save_users(users)

def greeting_keyboard(is_op: bool = False) -> InlineKeyboardMarkup:
    g = load_greeting()
    # Ensure URL is clean
    url = g["owner_url"]
    if url.startswith("https://t.me/@"):
        url = url.replace("https://t.me/@", "https://t.me/")
    
    rows = [[
        InlineKeyboardButton(text="𝐻𝑂𝑆𝑇 ♡",  callback_data="host"),
        InlineKeyboardButton(text="𝑂𝑊𝑁𝐸𝑅ღ",   url=url),
        InlineKeyboardButton(text="𝐺𝑈𝐼𝐷𝐸☘",  callback_data="guide"),
    ]]
    if is_op:
        rows.append([InlineKeyboardButton(
            text="🩷 " + sb("Panel"), callback_data="op_panel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🩵 " + sb("Cancel"), callback_data="host_cancel"),
    ]])

def logout_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🩷 " + sb("Logout"), callback_data="logout_prompt"),
    ]])

def op_panel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🩷 " + sb("Stats"), callback_data="op_stats")],
        [InlineKeyboardButton(text="🤍 " + sb("Operators"), callback_data="op_ops")],
        [InlineKeyboardButton(text="🩵 " + sb("Broadcast"), callback_data="op_broadcast")],
        [InlineKeyboardButton(text="🩷 " + sb("Close"), callback_data="op_close")],
    ])

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    try: upsert_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    except Exception: pass
    
    uid = message.from_user.id
    is_op = uid in OPERATORS
    g = load_greeting()
    kb = greeting_keyboard(is_op)
    if g["greet_on"]:
        try:
            if g["photo_file_id"]:
                await message.answer_photo(photo=g["photo_file_id"],
                                           caption=g["text"], reply_markup=kb)
            else:
                await message.answer(g["text"], reply_markup=kb)
            return
        except Exception as e:
            print(f"[start photo failed] {e}")
            
    try:
        await message.answer("🩷 " + sb("Welcome to s1n Hoster."), reply_markup=kb)
    except Exception as e:
        print(f"[start text failed] {e}")
        await message.answer("🩷 " + sb("Welcome to s1n Hoster."))

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    cur = await state.get_state()
    if cur is None:
        await message.answer("🩵 " + sb("Nothing to cancel.")); return
    await cleanup_pending(message.from_user.id)
    await state.clear()
    try: kb = greeting_keyboard(message.from_user.id in OPERATORS)
    except Exception: kb = None
    await message.answer("🩷 " + sb("Cancelled."), reply_markup=kb)

@router.message(Command("logs"))
async def cmd_logs(message: Message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) > 1 and user_id in OPERATORS:
        target_id = args[1]
    else:
        target_id = str(user_id)
    log_path = HOSTED_DIR / target_id / "logs.txt"
    if not log_path.exists():
        await message.answer(f"🩵 {sb('No logs')}"); return
    content = log_path.read_text(encoding="utf-8")
    if not content.strip():
        await message.answer("🩵 " + sb("Log empty.")); return
    content = content[-4000:] if len(content) > 4000 else content
    await message.answer(f"<pre>{html.escape(content)}</pre>", parse_mode="HTML")

async def cleanup_pending(user_id: int):
    p = pending.pop(user_id, None)
    if p:
        try: await p["client"].disconnect()
        except Exception: pass

@router.callback_query(F.data == "guide")
async def cb_guide(query: CallbackQuery):
    g = load_greeting()
    text = g.get("guide_text")
    if not text:
        text = (
            "🩷 " + sb("How to host:") + "\n\n"
            "1. Get API ID & API HASH from my.telegram.org\n"
            "2. Tap 𝐻𝑂𝑆𝑇 ♡\n"
            "3. Send API ID, then API HASH\n"
            "4. Send phone number (with country code)\n"
            "5. Enter the OTP Telegram sends you\n"
            "6. If 2FA is enabled, send your password\n"
            "7. Done — use !help in any chat"
        )
    await query.message.answer(text)
    await query.answer()

@router.callback_query(F.data == "op_panel")
async def cb_op_panel(query: CallbackQuery):
    if query.from_user.id not in OPERATORS:
        await query.answer("Not allowed.", show_alert=True); return
    await query.message.answer(
        "🩷 " + sb("Operator panel") + "\n🤍 " +
        sb("Use .rev to open master control."),
        reply_markup=op_panel_kb())
    await query.answer()

@router.callback_query(F.data == "op_stats")
async def cb_op_stats(query: CallbackQuery):
    if query.from_user.id not in OPERATORS: return
    users = load_users()
    hosted = sum(1 for u in users.values() if u.get("hosted"))
    running_count = sum(1 for p in running.values() if p.poll() is None)
    await query.message.answer(
        "🩷 " + sb("Stats") + "\n\n"
        f"🤍 {sb('Users')}: <b>{len(users)}</b>\n"
        f"🩵 {sb('Hosted')}: <b>{hosted}</b>\n"
        f"🩷 {sb('Running')}: <b>{running_count}</b>\n"
        f"🤍 {sb('Operators')}: <b>{len(OPERATORS)}</b>",
        parse_mode="HTML")
    await query.answer()

@router.callback_query(F.data == "op_ops")
async def cb_op_ops(query: CallbackQuery):
    if query.from_user.id not in OPERATORS: return
    lines = []
    for uid in sorted(OPERATORS):
        try:
            u = await bot.get_chat(uid)
            lines.append(f"🤍 {u.first_name or '?'} — <code>{uid}</code>")
        except Exception:
            lines.append(f"🤍 <code>{uid}</code>")
    await query.message.answer(
        "🩷 " + sb("Operators") + f" ({len(OPERATORS)})\n" + "\n".join(lines),
        parse_mode="HTML")
    await query.answer()

@router.callback_query(F.data == "op_broadcast")
async def cb_op_broadcast(query: CallbackQuery, state: FSMContext):
    if query.from_user.id not in OPERATORS: return
    await state.set_state(AdminFlow.broadcast)
    await query.message.answer("🩷 " + sb("Send broadcast message:"))
    await query.answer()

@router.callback_query(F.data == "op_close")
async def cb_op_close(query: CallbackQuery):
    try: await query.message.delete()
    except Exception: pass
    await query.answer()

@router.message(StateFilter(AdminFlow.broadcast), F.text)
async def do_broadcast(message: Message, state: FSMContext):
    if message.from_user.id not in OPERATORS: return
    await state.clear()
    users = load_users()
    sent, failed = 0, 0
    for uid in users:
        try:
            await bot.send_message(int(uid), message.text)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)
    await message.answer(
        f"🩷 {sb('Broadcast')}\n🤍 {sb('Sent')}: {sent}\n🩵 {sb('Failed')}: {failed}")

def _parse_rev(text: str):
    tokens = text.split(maxsplit=2)
    if not tokens: return None
    cmd = tokens[0].split("@")[0].lower()
    if cmd != ".rev": return None
    sub = tokens[1].lower() if len(tokens) > 1 else ""
    arg = tokens[2] if len(tokens) > 2 else ""
    return sub, arg

@router.message(F.text.regexp(r"^\.rev\b"))
async def cmd_rev(message: Message):
    if message.from_user.id not in OPERATORS: return
    parsed = _parse_rev(message.text)
    if not parsed: return
    sub, arg = parsed
    if not sub:
        return await show_panel(message)
    try:
        await dispatch_op(message, sub, arg)
    except Exception as e:
        await message.answer(f"🩵 {e}")

async def show_panel(message: Message):
    users = load_users()
    hosted = sum(1 for u in users.values() if u.get("hosted"))
    running_count = sum(1 for p in running.values() if p.poll() is None)
    text = (
        "🩷 <b>" + sb("s1n Operator Panel") + "</b>\n\n"
        f"🤍 {sb('Total users')}: <b>{len(users)}</b>\n"
        f"🩵 {sb('Hosted')}: <b>{hosted}</b>\n"
        f"🩷 {sb('Running')}: <b>{running_count}</b>\n"
        f"🤍 {sb('Operators')}: <b>{len(OPERATORS)}</b>\n\n"
        "🩷 " + sb("Subcommands") + "\n"
        f"<code>.rev@1 ops</code> — {sb('list operators')}\n"
        f"<code>.rev@1 opadd &lt;uid&gt;</code> — {sb('add operator')}\n"
        f"<code>.rev@1 opdel &lt;uid&gt;</code> — {sb('remove operator')}\n"
        f"<code>.rev@1 photo</code> — {sb('set greeting photo')}\n"
        f"<code>.rev@1 text &lt;t&gt;</code> — {sb('set greeting text')}\n"
        f"<code>.rev@1 owner &lt;url&gt;</code> — {sb('set OWNER url')}\n"
        f"<code>.rev@1 guide &lt;t&gt;</code> — {sb('set guide text')}\n"
        f"<code>.rev@1 greet on|off</code> — {sb('toggle greeting')}\n"
        f"<code>.rev@1 preview</code> — {sb('preview greeting')}\n"
        f"<code>.rev@1 kick &lt;uid&gt;</code> — {sb('stop hosted userbot')}\n"
        f"<code>.rev@1 bcast &lt;t&gt;</code> — {sb('broadcast to all users')}"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=op_panel_kb())

async def dispatch_op(message: Message, sub: str, arg: str):
    if sub == "ops":
        if not OPERATORS: return await message.answer("🩵 " + sb("No operators."))
        lines = []
        for uid in sorted(OPERATORS):
            try:
                u = await bot.get_chat(uid)
                lines.append(f"🤍 {u.first_name or '?'} — <code>{uid}</code>")
            except Exception:
                lines.append(f"🤍 <code>{uid}</code>")
        return await message.answer(
            "🩷 <b>" + sb("Operators") + f"</b> ({len(OPERATORS)})\n" + "\n".join(lines),
            parse_mode="HTML")

    if sub == "opadd":
        if not arg.strip().isdigit():
            return await message.answer("🩵 " + sb("Usage: .rev@1 opadd <uid>"))
        uid = int(arg.strip())
        if uid in OPERATORS: return await message.answer("🩵 " + sb("Already operator."))
        OPERATORS.add(uid); save_operators(OPERATORS)
        return await message.answer(f"🩷 {sb('Added')} — <code>{uid}</code>", parse_mode="HTML")

    if sub == "opdel":
        if not arg.strip().isdigit():
            return await message.answer("🩵 " + sb("Usage: .rev@1 opdel <uid>"))
        uid = int(arg.strip())
        if uid == OWNER_ID: return await message.answer("🩵 " + sb("Cannot remove root."))
        if uid not in OPERATORS: return await message.answer("🩵 " + sb("Not operator."))
        OPERATORS.discard(uid); save_operators(OPERATORS)
        return await message.answer(f"🩷 {sb('Removed')} — <code>{uid}</code>", parse_mode="HTML")

    if sub == "photo":
        if not message.reply_to_message or not message.reply_to_message.photo:
            return await message.answer("🩵 " + sb("Reply to a photo."))
        g = load_greeting()
        g["photo_file_id"] = message.reply_to_message.photo[-1].file_id
        save_greeting(g)
        return await message.answer("🩷 " + sb("Greeting photo set."))

    if sub == "text":
        if not arg.strip():
            return await message.answer("🩵 " + sb("Usage: .rev@1 text <text>"))
        g = load_greeting(); g["text"] = arg; save_greeting(g)
        return await message.answer("🩷 " + sb("Greeting text set."))

    if sub == "owner":
        if not arg.strip().startswith("http"):
            return await message.answer("🩵 " + sb("URL must start with http."))
        g = load_greeting(); g["owner_url"] = arg.strip(); save_greeting(g)
        return await message.answer("🩷 " + sb("OWNER url set."))

    if sub == "guide":
        if not arg.strip():
            return await message.answer("🩵 " + sb("Usage: .rev@1 guide <text>"))
        g = load_greeting(); g["guide_text"] = arg; save_greeting(g)
        return await message.answer("🩷 " + sb("Guide text set."))

    if sub == "greet":
        g = load_greeting()
        g["greet_on"] = arg.strip().lower() in ("on", "1", "true", "yes")
        save_greeting(g)
        state = "on" if g["greet_on"] else "off"
        return await message.answer(f"🩷 {sb('Greeting')}: {state}")

    if sub == "preview":
        g = load_greeting(); kb = greeting_keyboard(True)
        if g["photo_file_id"]:
            try:
                await bot.send_photo(message.chat.id, g["photo_file_id"],
                                     caption=g["text"], reply_markup=kb)
            except Exception:
                await message.answer(g["text"], reply_markup=kb)
        else:
            await message.answer(g["text"], reply_markup=kb)
        return

    if sub == "kick":
        if not arg.strip().isdigit():
            return await message.answer("🩵 " + sb("Usage: .rev@1 kick <uid>"))
        uid = int(arg.strip())
        was_running = uid in running
        stop_userbot(uid, delete_dir=True)
        set_hosted_status(uid, False)
        return await message.answer(
            f"🩷 {sb('Kicked')} <code>{uid}</code> " +
            ("(was running)" if was_running else "(was stopped)"),
            parse_mode="HTML")

    if sub == "bcast":
        if not arg.strip():
            return await message.answer("🩵 " + sb("Usage: .rev@1 bcast <text>"))
        users = load_users(); sent = failed = 0
        for uid in users:
            try:
                await bot.send_message(int(uid), arg); sent += 1
            except Exception:
                failed += 1
            await asyncio.sleep(0.05)
        return await message.answer(
            f"🩷 {sb('Done')}\n🤍 {sb('Sent')}: {sent}\n🩵 {sb('Failed')}: {failed}")

    return await show_panel(message)

@router.callback_query(F.data == "host")
async def cb_host(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    if user_has_bot(user_id):
        await query.message.answer(
            "🩵 " + sb("You already have a userbot deployed. Use Logout first."),
            reply_markup=logout_kb())
        await query.answer(); return
    await cleanup_pending(user_id)
    await state.clear()
    await state.set_state(HostFlow.api_id)
    await query.message.answer(
        "🩷 " + sb("Step 1/5 — Send your API ID:") + "\n\n" +
        "🤍 " + sb("(Get it from my.telegram.org)"),
        reply_markup=cancel_kb())
    await query.answer()

@router.message(StateFilter(HostFlow.api_id), F.text)
async def flow_api_id(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    if not text.isdigit():
        await message.answer("🩵 " + sb("Invalid API ID — digits only. Try again:"),
                             reply_markup=cancel_kb()); return
    await state.update_data(api_id=int(text))
    await state.set_state(HostFlow.api_hash)
    await message.answer("🩷 " + sb("Step 2/5 — Send your API HASH:"),
                         reply_markup=cancel_kb())

@router.message(StateFilter(HostFlow.api_hash), F.text)
async def flow_api_hash(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    if len(text) != 32:
        await message.answer("🩵 " + sb("Invalid API HASH — must be 32 chars."),
                             reply_markup=cancel_kb()); return
    await state.update_data(api_hash=text)
    await state.set_state(HostFlow.phone)
    await message.answer(
        "🩷 " + sb("Step 3/5 — Send phone number with country code (+91…):"),
        reply_markup=cancel_kb())

@router.message(StateFilter(HostFlow.phone), F.text)
async def flow_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = (message.text or "").strip().replace(" ", "")
    if not text.startswith("+") or not text[1:].isdigit():
        await message.answer("🩵 " + sb("Invalid phone — must start with + and digits."),
                             reply_markup=cancel_kb()); return
    data = await state.get_data()
    api_id = data["api_id"]; api_hash = data["api_hash"]
    status = await message.answer("🩷 " + sb("Sending OTP…"))
    temp = None
    try:
        temp = TelegramClient(StringSession(), api_id, api_hash)
        await temp.connect()
        sent = await temp.send_code_request(text)
    except PhoneNumberInvalidError:
        if temp:
            try: await temp.disconnect()
            except Exception: pass
        await status.edit_text("🩵 " + sb("Telegram rejected number. Try again:"),
                               reply_markup=cancel_kb()); return
    except Exception as e:
        if temp:
            try: await temp.disconnect()
            except Exception: pass
        await status.edit_text(f"🩵 {sb('Error')}: {e}\n\n{sb('Try again:')}",
                               reply_markup=cancel_kb()); return
    pending[user_id] = {"client": temp, "phone": text,
                        "api_id": api_id, "api_hash": api_hash,
                        "phone_code_hash": sent.phone_code_hash}
    await state.set_state(HostFlow.otp)
    await status.edit_text("🩷 " + sb("Step 4/5 — Send the OTP you received:"),
                           reply_markup=cancel_kb())

@router.message(StateFilter(HostFlow.otp), F.text)
async def flow_otp(message: Message, state: FSMContext):
    user_id = message.from_user.id
    p = pending.get(user_id)
    if not p:
        await state.clear()
        await message.answer("🩵 " + sb("Session expired. Tap HOST to restart.")); return
    code = (message.text or "").strip().replace(" ", "")
    if not code:
        await message.answer("🩵 " + sb("Invalid OTP."),
                             reply_markup=cancel_kb()); return
    temp = p["client"]
    try:
        await temp.sign_in(phone=p["phone"], code=code, phone_code_hash=p["phone_code_hash"])
    except SessionPasswordNeededError:
        await state.set_state(HostFlow.twofa)
        await message.answer("🩷 " + sb("Step 5/5 — Send your 2FA password:"),
                             reply_markup=cancel_kb()); return
    except PhoneCodeInvalidError:
        await message.answer("🩵 " + sb("Wrong OTP. Try again:"),
                             reply_markup=cancel_kb()); return
    except PhoneCodeExpiredError:
        await cleanup_pending(user_id)
        await state.clear()
        await message.answer("🩵 " + sb("OTP expired. Tap HOST to restart.")); return
    except Exception as e:
        await message.answer(f"🩵 {sb('Error')}: {e}\n\n{sb('Try again:')}",
                             reply_markup=cancel_kb()); return
    await finalize_deploy(message, state, user_id)

@router.message(StateFilter(HostFlow.twofa), F.text)
async def flow_twofa(message: Message, state: FSMContext):
    user_id = message.from_user.id
    p = pending.get(user_id)
    if not p:
        await state.clear()
        await message.answer("🩵 " + sb("Session expired. Tap HOST to restart.")); return
    pwd = (message.text or "").strip()
    if not pwd:
        await message.answer("🩵 " + sb("Invalid password."),
                             reply_markup=cancel_kb()); return
    temp = p["client"]
    try:
        await temp.sign_in(password=pwd)
    except PasswordHashInvalidError:
        await message.answer("🩵 " + sb("Wrong 2FA password."),
                             reply_markup=cancel_kb()); return
    except Exception as e:
        await message.answer(f"🩵 {sb('Error')}: {e}\n\n{sb('Try again:')}",
                             reply_markup=cancel_kb()); return
    await finalize_deploy(message, state, user_id)

async def finalize_deploy(message: Message, state: FSMContext, user_id: int):
    p = pending.pop(user_id, None)
    if not p:
        await state.clear(); return
    temp = p["client"]
    try:
        me = await temp.get_me()
        account_id = me.id
        account_username = me.username
        account_first_name = me.first_name or "Unknown"
        session_str = temp.session.save()
    except Exception as e:
        await message.answer(f"🩵 {sb('Failed to fetch account')}: {e}")
        try: await temp.disconnect()
        except Exception: pass
        await state.clear(); return
    try: await temp.disconnect()
    except Exception: pass
    user_dir = HOSTED_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    (user_dir / "session.txt").write_text(session_str, encoding="utf-8")
    meta = {"user_id": user_id, "api_id": p["api_id"], "api_hash": p["api_hash"],
            "account_id": account_id, "account_username": account_username,
            "account_first_name": account_first_name,
            "deployed_at": datetime.now(timezone.utc).isoformat()}
    (user_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                                        encoding="utf-8")
    try:
        spawn_userbot(user_id, p["api_id"], p["api_hash"], session_str)
    except Exception as e:
        await message.answer(f"🩵 {sb('Failed to spawn')}: {e}")
        await state.clear(); return
    set_hosted_status(user_id, True)
    await state.clear()
    await message.answer(
        "🩷 " + sb("Your userbot is deployed. Use !help in any chat for commands."),
        reply_markup=logout_kb())
    try:
        acct = f"@{account_username}" if account_username else account_first_name
        owner_text = (
            "🩷 <b>New Userbot Deployed</b>\n\n"
            f"🤍 Account: {acct}\n"
            f"🩵 Account ID: <code>{account_id}</code>\n"
            f"🩷 User ID: <code>{user_id}</code>\n"
            f"🤍 Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )
        for op in OPERATORS:
            try: await bot.send_message(op, owner_text, parse_mode="HTML")
            except Exception: pass
    except Exception: pass

@router.callback_query(F.data == "host_cancel")
async def cb_host_cancel(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    await cleanup_pending(user_id)
    await state.clear()
    await query.message.answer("🩵 " + sb("Hosting cancelled."))
    await query.answer()

@router.callback_query(F.data == "logout_prompt")
async def cb_logout_prompt(query: CallbackQuery):
    user_id = query.from_user.id
    if not user_has_bot(user_id):
        await query.answer("🩵 " + sb("No active userbot."), show_alert=True); return
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🩷 " + sb("Yes, Logout"), callback_data="logout_confirm"),
        InlineKeyboardButton(text="🩵 " + sb("Cancel"), callback_data="logout_cancel"),
    ]])
    await query.message.answer(
        "🩷 " + sb("Are you sure you want to logout?") + "\n" +
        "🤍 " + sb("This will permanently terminate your userbot."),
        reply_markup=kb)
    await query.answer()

@router.callback_query(F.data == "logout_confirm")
async def cb_logout_confirm(query: CallbackQuery):
    user_id = query.from_user.id
    if not user_has_bot(user_id):
        await query.answer("🩵 " + sb("No active userbot."), show_alert=True); return
    stop_userbot(user_id, delete_dir=True)
    set_hosted_status(user_id, False)
    await query.message.edit_text("🩷 " + sb("Logged out. Your userbot has been terminated."))
    await query.answer()

@router.callback_query(F.data == "logout_cancel")
async def cb_logout_cancel(query: CallbackQuery):
    await query.message.edit_text("🩵 " + sb("Logout cancelled."))
    await query.answer()

@dp.error()
async def global_error_handler(event, exception):
    print(f"[aiogram global error] {exception}")

async def main():
    if BOT_TOKEN.startswith("PASTE"):
        raise SystemExit("Set BOT_TOKEN at the top of s1n_hoster.py")
    if not OWNER_ID:
        raise SystemExit("Set OWNER_ID at the top of s1n_hoster.py")
    if OWNER_ID not in OPERATORS:
        OPERATORS.add(OWNER_ID); save_operators(OPERATORS)

    print("[s1n] writing s1n_userbot.py template…")
    write_userbot_template()
    print(f"[s1n] wrote {USERBOT_SCRIPT.resolve()}")
    HOSTED_DIR.mkdir(parents=True, exist_ok=True)
    print("[s1n] booting…")
    kill_orphans()
    await sync_hosted_flags()
    await respawn_all()
    me = await bot.get_me()
    print(f"[s1n] logged in as @{me.username} (ID: {me.id})")
    print(f"[s1n] hosted dir: {HOSTED_DIR.resolve()}")
    print(f"[s1n] operators: {sorted(OPERATORS)}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())