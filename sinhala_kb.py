# Singlish -> Sinhala global keyboard (Windows)
import ctypes, os, threading, winsound
from ctypes import wintypes
from pynput import keyboard, mouse

# ---------- 1. Converter ----------
HAL = '්'
ZWJ = '\u200d'
CONS = {
    'k':'ක','kh':'ඛ','g':'ග','gh':'ඝ','ng':'ඟ','ch':'ච','chh':'ඡ','j':'ජ','jh':'ඣ',
    'T':'ට','Th':'ඨ','D':'ඩ','Dh':'ඪ','N':'ණ',
    't':'ත','th':'ත','d':'ද','dh':'ද','n':'න','nd':'ඳ',
    'p':'ප','ph':'ඵ','b':'බ','bh':'භ','m':'ම','mb':'ඹ',
    'y':'ය','r':'ර','l':'ල','L':'ළ','w':'ව','v':'ව',
    's':'ස','sh':'ශ','S':'ෂ','h':'හ','f':'ෆ',
}
VSIGN = {'a':'','aa':'ා','ae':'ැ','aae':'ෑ','i':'ි','ii':'ී','u':'ු','uu':'ූ',
         'e':'ෙ','ee':'ේ','ai':'ෛ','o':'ො','oo':'ෝ','au':'ෞ'}
VIND  = {'a':'අ','aa':'ආ','ae':'ඇ','aae':'ඈ','i':'ඉ','ii':'ඊ','u':'උ','uu':'ඌ',
         'e':'එ','ee':'ඒ','ai':'ඓ','o':'ඔ','oo':'ඕ','au':'ඖ'}
SPECIAL = {'x':'ං','H':'ඃ'}

C_KEYS = sorted(CONS, key=len, reverse=True)
V_KEYS = sorted(VSIGN, key=len, reverse=True)

def _match(keys, s, i):
    for k in keys:
        if s.startswith(k, i):
            return k
    return None

def convert(s):
    out, i = [], 0
    while i < len(s):
        c = _match(C_KEYS, s, i)
        if c:
            i += len(c)
            base = CONS[c]
            # Rakaransaya ('r')
            if c != 'r' and i < len(s) and s[i].lower() == 'r':
                base += HAL + ZWJ + 'ර'
                i += 1
            # Yansaya ('y')
            if c != 'y' and i < len(s) and s[i].lower() == 'y':
                base += HAL + ZWJ + 'ය'
                i += 1

            v = _match(V_KEYS, s, i)
            if v:
                out.append(base + VSIGN[v]); i += len(v)
            else:
                out.append(base + HAL)
            continue
        v = _match(V_KEYS, s, i)
        if v:
            out.append(VIND[v]); i += len(v); continue
        out.append(SPECIAL.get(s[i], s[i])); i += 1
    return ''.join(out)

# ---------- 2. SendInput (unicode typing) ----------
user32 = ctypes.windll.user32
ULONG_PTR = ctypes.c_size_t

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG), ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", wintypes.WORD), ("wScan", wintypes.WORD), ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [("uMsg", wintypes.DWORD), ("wParamL", wintypes.WORD), ("wParamH", wintypes.WORD)]
class _U(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]
class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [("type", wintypes.DWORD), ("u", _U)]

KEYUP, UNICODE = 0x0002, 0x0004

def _ki(vk=0, scan=0, flags=0):
    i = INPUT(type=1)
    i.ki = KEYBDINPUT(vk, scan, flags, 0, 0)
    return i

def send(backspaces, text):
    ev = []
    for _ in range(backspaces):
        ev += [_ki(vk=0x08), _ki(vk=0x08, flags=KEYUP)]
    for ch in text:
        ev += [_ki(scan=ord(ch), flags=UNICODE), _ki(scan=ord(ch), flags=UNICODE | KEYUP)]
    if ev:
        arr = (INPUT * len(ev))(*ev)
        user32.SendInput(len(ev), arr, ctypes.sizeof(INPUT))

# ---------- 3. State ----------
enabled, buffer, shown = False, "", ""

def reset():
    global buffer, shown
    buffer = shown = ""

def refresh():
    """Screen eke thiyena text eka, aluth text ekata wenas karanawa (diff witharai)"""
    global shown
    new = convert(buffer)
    p = 0
    while p < min(len(shown), len(new)) and shown[p] == new[p]:
        p += 1
    send(len(shown) - p, new[p:])
    shown = new

def beep(freq):
    threading.Thread(target=winsound.Beep, args=(freq, 120), daemon=True).start()

def down(vk):
    return bool(user32.GetAsyncKeyState(vk) & 0x8000)

MODS = {0x10, 0x11, 0x12, 0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0x14, 0x5B, 0x5C}

# ---------- 4. Global keyboard hook ----------
def win_filter(msg, data):
    global enabled, buffer
    if data.flags & 0x10:            # apey own injected keys -> ignore
        return True
    vk = data.vkCode
    is_down = msg in (0x100, 0x104)
    ctrl, alt = down(0x11), down(0x12)
    win = down(0x5B) or down(0x5C)

    if is_down and ctrl and alt and vk == 0x51:        # Ctrl+Alt+Q = exit
        os._exit(0)
    if is_down and ctrl and not alt and vk == 0x20:    # Ctrl+Space = ON/OFF
        enabled = not enabled
        reset()
        beep(1200 if enabled else 500)
        listener.suppress_event()

    if not enabled or vk in MODS:
        return True
    if ctrl or alt or win:
        if is_down: reset()
        return True

    if 0x41 <= vk <= 0x5A:                              # A-Z
        if is_down:
            ch = chr(vk)
            if not (down(0x10) != bool(user32.GetKeyState(0x14) & 1)):
                ch = ch.lower()
            if ch.lower() in 'aeiou':
                ch = ch.lower()
            buffer += ch
            refresh()
        listener.suppress_event()

    if vk == 0x08 and is_down and buffer:              # Backspace
        buffer = buffer[:-1]
        refresh()
        listener.suppress_event()

    if is_down:                                         # space, enter, symbols...
        reset()
    return True

listener = keyboard.Listener(win32_event_filter=win_filter)
mouse.Listener(on_click=lambda *a: reset()).start()
beep(800)
listener.start()
listener.join()