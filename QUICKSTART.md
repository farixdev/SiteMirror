# SiteMirror - Quick Start Guide

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Optional: Tor (for onion site support)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/SiteMirror.git
cd SiteMirror
```

2. **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```

## First Extraction

1. **Enter a URL**: Type any website URL in the "Website / Onion URL" field
   - Example: `https://example.com`
   - For onion sites: `https://example.onion`

2. **Configure Options**:
   - Select extraction depth (Single Page / Same Domain / Recursive)
   - Choose what to download (Assets, Links, Media)
   - Enable advanced options if needed

3. **Start Extraction**: Click the purple "Start Extraction" button

4. **Monitor Progress**:
   - Watch real-time logs for detailed activity
   - Check the status panel for progress and statistics
   - Thread monitor shows active workers

5. **Access Downloaded Files**: 
   - Extracted files are saved in the configured directory
   - Click "📁 Open Folder" to browse files

## Advanced Features

### TOR/Onion Support
To extract from .onion sites:
1. Install Tor: [https://www.torproject.org/download/](https://www.torproject.org/download/)
2. Ensure Tor is running (application will attempt to start it)
3. Enter .onion URL and select "Onion Site (TOR)" mode
4. Start extraction

### Custom Settings
Access Settings tab to configure:
- Number of worker threads
- Request timeout
- Maximum pages and crawl depth
- File size limits
- Browser automation options

### Extraction Modes

**Single Page**
- Downloads only the specified URL
- Fast, minimal bandwidth
- Best for simple pages

**Same Domain**  
- Crawls all pages on the same domain
- Respects domain boundaries
- Good for complete site mirrors

**Recursive**
- Deep crawl across all found links
- Most thorough extraction
- Requires more time and bandwidth

## Troubleshooting

### "Tor connection failed"
- Install Tor separately from https://www.torproject.org
- Ensure Tor is running on port 9050
- Check Settings for correct TOR configuration

### Extraction seems slow
- Try reducing Max Threads in Settings (network throttling)
- Ensure website allows rapid requests (check robots.txt)
- Some sites implement rate limiting

### OutOfMemory errors
- Reduce Max Pages in Settings
- Use Recursive mode sparingly
- Close other applications

### Logs not updating
- Check that extraction is actually running (status shows "running")
- Verify network connectivity
- Try extracting a simpler URL first

## Configuration Files

Settings are stored in `config/settings.json`:
```json
{
  "network": {
    "max_threads": 4,
    "timeout_seconds": 10
  },
  "tor": {
    "enabled": false,
    "socks_host": "127.0.0.1",
    "socks_port": 9050
  },
  "extraction": {
    "max_pages": 1000,
    "max_depth": 10
  }
}
```

Modify directly or through the Settings tab.

## Data Storage

Extracted files are organized by:
```
data/
└── extractions/
    └── [domain]/
        └── [YYYY-MM-DD_HH-MM-SS]/
            ├── index.html
            ├── assets/
            └── ...
```

## Performance Tips

1. **Use Single Page mode** for quick tests
2. **Limit threads to 4-8** for stable extractions
3. **Enable asset downloading** selectively
4. **Set reasonable timeout** (10-20 seconds typical)
5. **Monitor system resources** - watch CPU/RAM usage

## Legal Disclaimer

This tool is for:
- ✅ Educational purposes
- ✅ Your own websites
- ✅ Authorized research
- ❌ Unauthorized access or scraping
- ❌ Circumventing access controls
- ❌ Violating Terms of Service

**Always:**
- Respect robots.txt
- Check Terms of Service
- Honor rate limits
- Use responsibly

## Getting Help

- Check logs for detailed error messages
- Review README.md for architecture overview
- Open an issue on GitHub with:
  - Your OS and Python version
  - Extraction URL (redacted if sensitive)
  - Full error logs
  - Steps to reproduce

---

**Happy Extracting!** 🌐
