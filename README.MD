<div align="center">

# 🪞 SiteMirror

**A modern desktop tool for extracting and mirroring websites — clearnet and TOR/onion supported.**

![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/UI-PyQt6-41CD52?style=flat-square&logo=qt&logoColor=white)
![Playwright](https://img.shields.io/badge/automation-Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![TOR](https://img.shields.io/badge/TOR-supported-7D4698?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

</div>

---

## 📖 Overview

SiteMirror is a minimalist, dark-themed desktop application for extracting and mirroring entire websites. Whether you're archiving a public site or crawling onion addresses over TOR, SiteMirror handles it with multi-threaded extraction, real-time monitoring, and a clean native UI.

---

## ✨ Features

### 🖥️ Modern Interface
- Sleek dark theme inspired by modern developer tooling
- Real-time extraction monitoring and live thread activity tracking
- Intuitive, responsive layout built with PyQt6

### 🌐 Website Extraction
- Single-page or deep recursive crawling
- Full asset downloading — CSS, JS, images, and more
- Link extraction and site mapping
- TOR/Onion site support via `stem`

### ⚙️ Advanced Options
- Multi-threaded extraction with configurable worker count
- Headless browser support for JavaScript-rendered content
- Cookie and session management
- `robots.txt` compliance toggle
- Customizable crawl depth

### 📊 Real-Time Monitoring
- Live logs with filtering and search
- Thread monitor showing active workers
- Progress tracking with download statistics
- Configurable output directory

---

## 🚀 Installation

### Prerequisites

- Python `3.9` or higher
- Internet connection (+ TOR for onion sites)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/SiteMirror.git
cd SiteMirror

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the app
python main.py
```

---

## 🖱️ Usage

1. **Enter URL** — Paste a website or `.onion` address into the extraction panel
2. **Configure Options** — Set crawl depth, choose assets to download, and toggle advanced settings
3. **Start Extraction** — Hit **Start Extraction** to begin
4. **Monitor Progress** — Watch real-time logs and active thread count
5. **Access Files** — All downloaded content is saved to your configured output directory

---

## 📁 Project Structure

```
SiteMirror/
├── backend/
│   ├── core/               # Crawler engine & proxy management
│   ├── threading/          # Worker pool for multi-threading
│   ├── storage/            # File download & storage handling
│   └── logs/               # Logging system
├── ui/
│   ├── main_window.py      # Main application window
│   ├── panels/             # UI panels and components
│   ├── widgets/            # Custom PyQt widgets
│   └── styles/             # Theme and styling
├── config/                 # Configuration files
├── data/                   # Extracted data output
└── main.py                 # Entry point
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | PyQt6 / PySide6 |
| HTTP | aiohttp (async) |
| Parsing | BeautifulSoup4 |
| Browser Automation | Playwright *(optional)* |
| TOR Support | stem |
| Async Runtime | asyncio |

---

## 🎨 Theme

| Element | Color |
|---------|-------|
| Background | `#0B0F17` |
| Card | `#151B2C` |
| Primary Accent | `#7C4DFF` |
| Success | `#22C55E` |
| Warning | `#F59E0B` |
| Error | `#EF4444` |

---

## ⚡ Performance

- Async I/O with `asyncio` and `aiohttp` for minimal blocking
- Configurable thread pool for large-scale extractions
- Memory-efficient virtualized log viewer
- Optimized for both quick single-page grabs and deep recursive crawls

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

SiteMirror is intended for **educational and authorized use only**. Always respect a website's Terms of Service and `robots.txt` rules. The author is not responsible for any misuse of this tool.

---

## 👤 Author

Made with 🖤 by **[Farisxdev](https://github.com/farixdev)**

---

<div align="center">

Found this useful? Drop a ⭐ on GitHub — it helps a lot!

</div>
