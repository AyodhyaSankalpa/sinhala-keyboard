import ctypes, os, threading, queue
import tkinter as tk
from ctypes import wintypes
from pynput import keyboard, mouse

# ---------- 1. Converter ----------
HAL = '්'
ZWJ = '\u200d'
CONS = {
    # 1. Standard Consonants
    'k': 'ක', 'kh': 'ඛ',
    'g': 'ග', 'gh': 'ඝ',
    'ch': 'ච', 'chh': 'ඡ',
    'j': 'ජ', 'jh': 'ඣ',
    't': 'ට', 'T': 'ඨ',
    'd': 'ඩ', 'D': 'ඪ',
    'th': 'ත', 'thh': 'ථ',
    'dh': 'ද', 'dhh': 'ධ',
    'q': 'ද', 'qh': 'ධ',
    'n': 'න', 'N': 'ණ',
    'p': 'ප', 'ph': 'ඵ',
    'b': 'බ', 'bh': 'භ',
    'B': 'ඹ',
    'm': 'ම',
    'y': 'ය',
    'r': 'ර',
    'l': 'ල', 'L': 'ළ',
    'w': 'ව', 'v': 'ව',
    's': 'ස', 'sh': 'ශ', 'Sha': 'ෂ', 'Sh': 'ෂ', 'S': 'ෂ',
    'h': 'හ',
    'f': 'ෆ',

    # 2. Sannaka & Nasals
    'zg': 'ඟ', 'ng': 'ඟ',
    'zj': 'ඦ',
    'zd': 'ඬ',
    'zdh': 'ඳ', 'zq': 'ඳ', 'nd': 'ඳ',
    'zk': 'ඤ',
    'zh': 'ඥ',
    'mb': 'ඹ',
}
VSIGN = {
    'ruu': 'ෲ', 'ru': 'ෘ',
    'Aa': 'ෑ', 'AA': 'ෑ', 'A': 'ැ',
    'aae': 'ෑ', 'ae': 'ැ',
    'aa': 'ා', 'a': '',
    'ii': 'ී', 'i': 'ි',
    'uu': 'ූ', 'u': 'ු',
    'ee': 'ේ', 'e': 'ෙ',
    'ai': 'ෛ',
    'oo': 'ෝ', 'o': 'ො',
    'au': 'ෞ', 'ou': 'ෞ',
}
VIND  = {
    'Aa': 'ඈ', 'AA': 'ඈ', 'A': 'ඇ',
    'aae': 'ඈ', 'ae': 'ඇ',
    'aa': 'ආ', 'a': 'අ',
    'ii': 'ඊ', 'i': 'ඉ',
    'uu': 'ඌ', 'u': 'උ',
    'Ru': 'ඎ', 'R': 'ඍ',
    'ee': 'ඒ', 'e': 'එ',
    'ai': 'ඓ',
    'oo': 'ඕ', 'o': 'ඔ',
    'au': 'ඖ', 'ou': 'ඖ',
}
SPECIAL = {
    'x': 'ං',
    'zn': 'ං',
    'X': 'ඞ',
    'H': 'ඃ',
}

C_KEYS = sorted(CONS, key=len, reverse=True)
V_KEYS = sorted(VSIGN, key=len, reverse=True)
S_KEYS = sorted(SPECIAL, key=len, reverse=True)

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

            # Gayanukitta (ru -> ෘ, ruu -> ෲ)
            if c != 'r' and s.startswith(('ruu', 'ru'), i):
                gv = 'ruu' if s.startswith('ruu', i) else 'ru'
                out.append(base + VSIGN[gv])
                i += len(gv)
                continue

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
        
        sp = _match(S_KEYS, s, i)
        if sp:
            out.append(SPECIAL[sp]); i += len(sp); continue

        out.append(s[i]); i += 1
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

# ---------- 4. Transparent OSD Popup Indicator ----------
class OSDPopup:
    def __init__(self):
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def show(self, is_sinhala):
        self.q.put(is_sinhala)

    def _run(self):
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes('-topmost', True)
        root.attributes('-alpha', 0.90)
        root.configure(bg='#181825')

        w, h = 200, 50
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = sw - w - 30
        y = sh - h - 60
        root.geometry(f"{w}x{h}+{x}+{y}")

        frame = tk.Frame(root, bg='#181825', highlightbackground='#313244', highlightthickness=1)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

        lbl_icon = tk.Label(frame, text="", font=("Segoe UI Emoji", 15), bg='#181825')
        lbl_icon.pack(side='left', padx=(12, 6))

        lbl_text = tk.Label(frame, text="", font=("Nirmala UI", 12, "bold"), bg='#181825')
        lbl_text.pack(side='left', padx=(0, 12))

        root.withdraw()

        # Non-activating floating tool window (never steals typing focus)
        hwnd = root.winfo_id()
        GWL_EXSTYLE = -20
        WS_EX_NOACTIVATE = 0x08000000
        WS_EX_TOOLWINDOW = 0x00000080
        for h_wnd in (hwnd, user32.GetParent(hwnd)):
            if h_wnd:
                ex = user32.GetWindowLongW(h_wnd, GWL_EXSTYLE)
                user32.SetWindowLongW(h_wnd, GWL_EXSTYLE, ex | WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW)

        hide_id = [None]

        def _hide():
            root.withdraw()

        def _poll():
            while not self.q.empty():
                is_sinhala = self.q.get_nowait()
                if hide_id[0]:
                    root.after_cancel(hide_id[0])
                    hide_id[0] = None

                if is_sinhala:
                    lbl_icon.config(text="🇱🇰")
                    lbl_text.config(text="සිංහල ON", fg="#00E5FF")
                    frame.config(highlightbackground="#00B4D8")
                else:
                    lbl_icon.config(text="🔤")
                    lbl_text.config(text="English", fg="#E2E8F0")
                    frame.config(highlightbackground="#64748B")

                root.deiconify()
                user32.ShowWindow(hwnd, 8)  # 8 = SW_SHOWNA (show without activating)
                hide_id[0] = root.after(1100, _hide)

            root.after(40, _poll)

        root.after(40, _poll)
        root.mainloop()

osd = OSDPopup()

def down(vk):
    return bool(user32.GetAsyncKeyState(vk) & 0x8000)

MODS = {0x10, 0x11, 0x12, 0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0x14, 0x5B, 0x5C}

# ---------- 5. Global keyboard hook ----------
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
        osd.show(enabled)
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
listener.start()
listener.join()