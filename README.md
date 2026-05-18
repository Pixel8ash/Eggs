# 🎵 Universal Media Player

A Material 3 adaptive design media player for music and audiobooks with a **SECRET MENU**.

## ✨ Features

✅ **Material 3 Adaptive Design** - Beautiful purple/lavender theme  
✅ **Music & Audiobook Support** - MP3, FLAC, WAV, OGG, M4B, AAC  
✅ **Password Protected Settings** - Top-right ⚙️ button  
✅ **🔐 SECRET MENU** - Type "purple bananas" in settings password  
✅ **Separate Folders** - 🎬 Movies and 🎮 Games (completely isolated)  
✅ **Full Playback Controls** - Play, Pause, Stop, Previous, Next  
✅ **Volume & Progress Controls** - Sliders for full control  
✅ **Playlist Management** - Load and manage multiple files  

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/Pixel8ash/Eggs.git
cd Eggs

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Usage

```bash
python media_player.py
```

### 🔐 Accessing the Secret Menu

1. Click **⚙️ Settings** button (top-right corner)
2. Type `purple bananas` in the password prompt
3. 🔓 Secret menu unlocks with:
   - 🎬 **Movies folder** (left side - SEPARATE)
   - 🎮 **Games folder** (right side - SEPARATE)

> **⚠️ IMPORTANT:** The secret menu ONLY appears when you type exactly "purple bananas" in the settings password prompt. This is completely hidden from normal users!

### 📂 Regular Usage

1. Click **+ Load Files** to add music/audiobooks
2. Double-click items to play them
3. Use controls to manage playback
4. Adjust volume with the slider

## 🎨 Material 3 Design Colors

| Element | Color | Hex |
|---------|-------|-----|
| Primary | Purple | `#6750A4` |
| Secondary | Gray | `#625B71` |
| Tertiary | Red-Pink | `#7D5260` |
| Background | Off-White | `#FFFBFE` |
| Error | Red | `#B3261E` |

## 📋 Supported Formats

- **Audio**: MP3, FLAC, WAV, OGG, AAC, M4B
- **Audiobooks**: M4B, FLAC, MP3

## 🔧 Requirements

- Python 3.8 or higher
- PyQt6
- PyQt6-Multimedia

## 📁 Project Structure

```
Eggs/
├── media_player.py       # Main application
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## 🎮 Controls

| Button | Function |
|--------|----------|
| ▶️ Play | Start playback |
| ⏸ Pause | Pause playback |
| ⏹ Stop | Stop and reset |
| ⏮ Previous | Play previous track |
| ⏭ Next | Play next track |
| ⚙️ Settings | Access settings (SECRET: "purple bananas") |

## 🔊 Audio

- Volume range: 0-100%
- Progress slider for seeking
- Time display (MM:SS format)

---

**Enjoy your music and audiobooks!** 🎧📚

*Secret menu is completely hidden. Only the correct password reveals it!* 🤫
