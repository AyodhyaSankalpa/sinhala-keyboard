# 🇱🇰 Sinhala Singlish Keyboard for Windows

A lightweight, high-performance, system-wide **Singlish to Sinhala converter** for Windows. Built using Python, low-level Win32 APIs, and dynamic keystroke injection.

---

## ✨ Features

- ⚡ **Zero-Lag System-Wide Typing:** Works seamlessly in any Windows app (browsers, Word, Notepad, chat apps, IDEs).
- 🔤 **Full Rakaransaya (ක්‍ර) & Yansaya (ක්‍ය) Support:** Built-in Zero-Width Joiner (ZWJ) handling for complex Sinhala conjuncts.
- 🎯 **Dynamic Buffer Diffing:** Intelligently replaces typed text in real time using minimal backspace sequences.
- 🔕 **Silent Background Execution:** Zero CPU overhead, runs silently without distracting windows.
- 📦 **Standalone Installer:** Portable executable and setup installer provided (no Python required on target PCs).

---

## ⌨️ Shortcuts & Controls

| Shortcut | Action | Description |
|---|---|---|
| <kbd>Ctrl</kbd> + <kbd>Space</kbd> | **Toggle ON / OFF** | Switches between Sinhala and English typing (with audio beep) |
| <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>Q</kbd> | **Exit** | Quits the keyboard application completely |

---

## 📖 Singlish Typing Guide

### 1. Rakaransaya (රකාරාංශය) & Yansaya (යන්සය)
| Singlish | Sinhala Output | Example Word |
|---|---|---|
| `kra` | **ක්‍ර** | `kramaya` -> ක්‍රමය |
| `kri` | **ක්‍රි** | `kriyaawa` -> ක්‍රියාව |
| `kree` | **ක්‍රේ** | `kreesha` -> ක්‍රේෂ |
| `pra` | **ප්‍ර** | `praarthanaa` -> ප්‍රාර්ථනා |
| `shree` | **ශ්‍රී** | `shree` -> ශ්‍රී |
| `kya` | **ක්‍ය** | `kya` -> ක්‍ය |
| `kyaa` | **ක්‍යා** | `vaakyaa` -> වාක්‍යා |
| `vya` | **ව්‍ය** | `vyaapaaraya` -> ව්‍යාපාරය |
| `sathya` | **සත්‍ය** | `sathya` -> සත්‍ය |
| `vidyaawa` | **විද්‍යාව** | `vidyaawa` -> විද්‍යාව |

### 2. Common Phonetic Consonants
- **k** -> ක් | **ka** -> ක | **kaa** -> කා | **ki** -> කි | **kee** -> කේ
- **g** -> ග් | **ga** -> ග | **gaa** -> ගා | **gi** -> ගි | **gee** -> ගේ
- **t** / **th** -> ත්, ත | **T** -> ට්, ට | **d** -> ද්, ද | **D** -> ඩ්, ඩ
- **n** -> න්, න | **N** -> ණ්, ණ | **m** -> ම්, ම | **p** -> ප්, ප
- **s** -> ස්, ස | **sh** -> ශ්, ශ | **S** -> ෂ්, ෂ

---

## 🚀 Running from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AyodhyaSankalpa/sinhala-keyboard.git
   cd sinhala-keyboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script:**
   ```bash
   python sinhala_kb.py
   ```

---

## 🛠️ Building the Standalone Executable & Installer

### Build .exe with PyInstaller
```bash
python -m PyInstaller --noconsole --onefile --name "SinhalaKeyboard" sinhala_kb.py
```

### Build Windows Setup with Inno Setup
1. Open `installer.iss` in **Inno Setup Compiler**.
2. Press <kbd>F9</kbd> to compile.
3. The setup installer will be generated inside the `output/` directory.

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
