# 🇱🇰 Sinhala Singlish Keyboard for Windows

A lightweight, high-performance, system-wide **Singlish to Sinhala converter** for Windows. Built using Python, low-level Win32 APIs, dynamic keystroke injection, and following the standard phonetic layout.

---

## ✨ Features

- ⚡ **Zero-Lag System-Wide Typing:** Works seamlessly in any Windows app (browsers, Word, Notepad, chat apps, IDEs).
- 🔤 **Complete Phonetic & UCSC Layout Support:** All vowels, consonants, aspirated letters, and pre-nasalized letters.
- 🎯 **Rakaransaya, Yansaya & Gayanukitta:** `kra` -> ක්‍ර, `kya` -> ක්‍ය, `kru` -> කෘ, `kruu` -> කෲ.
- 🔄 **Dynamic Buffer Diffing:** Intelligently replaces typed text in real time using minimal backspace sequences.
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

### 1. ස්වර අක්ෂර (Independent Vowels)
- **a** -> අ | **aa** -> ආ
- **A** -> ඇ | **Aa** / **AA** -> ඈ
- **i** -> ඉ | **ii** -> ඊ
- **u** -> උ | **uu** -> ඌ
- **R** -> ඍ | **Ru** -> ඎ
- **e** -> එ | **ee** -> ඒ
- **ai** -> ඓ
- **o** -> ඔ | **oo** -> ඕ
- **au** / **ou** -> ඖ

### 2. ව්‍යංජන අක්ෂර (Consonants)
- **k** -> ක | **g** -> ග | **ch** -> ච | **j** -> ජ
- **t** -> ට | **d** -> ඩ | **th** -> ත | **dh** / **q** -> ද
- **n** -> න | **N** -> ණ | **p** -> ප | **b** -> බ | **m** -> ම
- **y** -> ය | **r** -> ර | **l** -> ල | **L** -> ළ
- **w** / **v** -> ව | **s** -> ස | **sh** -> ශ | **S** / **Sh** -> ෂ
- **h** -> හ | **f** -> ෆ

### 3. මහප්‍රාණ අක්ෂර (Aspirated Consonants)
- **kh** -> ඛ | **gh** -> ඝ | **chh** -> ඡ
- **T** -> ඨ | **D** -> ඪ
- **thh** -> ථ | **dhh** / **qh** -> ධ
- **ph** -> ඵ | **bh** -> භ

### 4. සඤ්ඤක සහ විශේෂ අක්ෂර (Sannaka & Special)
- **zg** / **ng** -> ඟ
- **zj** -> ඦ
- **zd** -> ඬ
- **zdh** / **zq** -> ඳ
- **zk** -> ඤ | **zh** -> ඥ
- **B** -> ඹ | **Lu** -> ළු
- **x** / **zn** -> ං | **X** -> ඞ | **H** -> ඃ

### 5. රකාරාංශය, යන්සය සහ ගයනුකිත්ත (Conjuncts & Signs)
- **kra** -> **ක්‍ර** (`kramaya` -> ක්‍රමය, `kri` -> ක්‍රි, `kree` -> ක්‍රේ)
- **kya** -> **ක්‍ය** (`kyaa` -> ක්‍යා, `vyaapaaraya` -> ව්‍යාපාරය)
- **kru** -> **කෘ** | **kruu** -> **කෲ**
- **kA** -> **කැ** | **kAa** / **kAA** -> **කෑ**

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
