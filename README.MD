# SiteMirror - Web Extraction & Website Mirroring Tool

A modern, minimalist desktop application for extracting and mirroring websites, with support for both clearnet and TOR/onion sites.

## Features

✨ **Modern UI**
- Sleek, dark theme inspired by modern development tools
- Real-time extraction monitoring
- Live thread activity tracking
- Responsive, intuitive interface

🌐 **Website Extraction**
- Single page or recursive crawling
- Asset downloading (CSS, JS, images)
- Link extraction and mapping
- TOR/Onion site support

⚙️ **Advanced Options**
- Multi-threaded extraction
- Headless browser support for dynamic content
- Cookie/session management
- robots.txt respect
- Customizable extraction depth

📊 **Monitoring**
- Real-time logs with filtering and search
- Thread monitor showing active workers
- Progress tracking with statistics
- Download location management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SiteMirror.git
cd SiteMirror
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## Project Structure

```
SiteMirror/
├── backend/                 # Backend engine
│   ├── core/               # Crawler and proxy management
│   ├── threading/          # Worker pool for multi-threading
│   ├── storage/            # File download and storage
│   └── logs/               # Logging system
├── ui/                     # PyQt UI
│   ├── main_window.py      # Main application window
│   ├── panels/             # UI panels and components
│   ├── widgets/            # Custom PyQt widgets
│   └── styles/             # Theme and styling
├── config/                 # Configuration files
├── data/                   # Extracted data storage
└── main.py                 # Application entry point
```

## Usage

1. **Enter URL**: Input a website or onion URL in the extraction panel
2. **Configure Options**: Select extraction depth, assets to download, and advanced options
3. **Start Extraction**: Click "Start Extraction" to begin
4. **Monitor Progress**: Watch real-time logs and thread activity
5. **Access Downloads**: Files are saved in the configured directory

## Technology Stack

**Frontend:**
- PyQt6/PySide6 - Native desktop UI
- Custom theme system for consistent styling

**Backend:**
- aiohttp - Async HTTP requests
- BeautifulSoup - HTML parsing
- Playwright - Browser automation (optional)
- stem - TOR support
- asyncio - Async operations

## Theme Colors

| Purpose | Color |
|---------|-------|
| Background | #0B0F17 |
| Card | #151B2C |
| Primary Accent | #7C4DFF |
| Success | #22C55E |
| Warning | #F59E0B |
| Error | #EF4444 |

## Performance

- Multi-threaded extraction with configurable worker count
- Async I/O for optimal resource usage
- Memory-efficient log viewer with virtualization
- Optimized for both small and large scale extractions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and authorized use only. Always respect website terms of service and robots.txt. The authors are not responsible for misuse of this software.

---

**SiteMirror** - Professional Web Extraction Made Simple
