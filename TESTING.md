"""
Development and Testing Guide for SiteMirror
"""

# Development Checklist

## Before Release

### Code Quality
- [ ] All Python files pass syntax check
- [ ] No import errors
- [ ] No circular dependencies
- [ ] Type hints for critical functions
- [ ] Docstrings for public methods

### Functionality Testing
- [ ] Single page extraction works
- [ ] Same domain extraction works
- [ ] Log viewer displays all log types
- [ ] Settings save and load correctly
- [ ] History panel populates after extraction
- [ ] UI responsive during extraction
- [ ] Tab switching works correctly

### TOR/Onion Testing
- [ ] TOR connection detection works
- [ ] Onion URL auto-detection works
- [ ] Fallback when TOR unavailable
- [ ] Circuit test successful when TOR running

### Error Handling
- [ ] Invalid URL handling
- [ ] Network error recovery
- [ ] Timeout handling
- [ ] Large file handling
- [ ] Memory pressure handling

### Performance
- [ ] Extraction completes in reasonable time
- [ ] Memory usage stays reasonable (< 500MB)
- [ ] UI remains responsive
- [ ] No thread leaks after extraction completes
- [ ] Log viewer handles 10000+ entries

## Testing Procedures

### Manual UI Testing
```bash
# 1. Run the application
python main.py

# 2. Test tab navigation
- Click each sidebar tab
- Verify correct panel displays
- Check responsive layout

# 3. Test extraction
- Enter: https://example.com
- Click "Start Extraction"
- Wait for completion
- Verify logs update in real-time
- Check status panel updates

# 4. Test settings
- Go to Settings tab
- Change values
- Click "Save Settings"
- Verify config file updated

# 5. Test TOR (if available)
- Go to Settings, enable TOR
- Enter an onion URL
- Verify auto-detection
- Start extraction
```

### Automated Testing
```python
# Test logger
from backend.logs.logger import get_logger, LogLevel

logger = get_logger()
logger.info("Test info")
logger.success("Test success")
logger.error("Test error")
logger.warning("Test warning")
logger.network("Test network")

# Test worker pool
from backend.threading.worker_pool import get_worker_pool

pool = get_worker_pool(4)
pool.start()

def test_func(x):
    return x * 2

task = pool.submit_task("task1", test_func, (5,))
print(task.result)

pool.stop()

# Test proxy configuration
from backend.core.proxy import ProxyConfig, ProxyType

config = ProxyConfig(ProxyType.HTTP, "127.0.0.1", 8080)
print(config.get_aiohttp_proxy_url())

# Test crawler (requires network)
import asyncio
from backend.core.crawler import Crawler, ExtractionConfig, ExtractionMode, ExtractionDepth

config = ExtractionConfig(
    url="https://example.com",
    mode=ExtractionMode.CLEARNET,
    depth=ExtractionDepth.SINGLE_PAGE
)

crawler = Crawler(config)
result = asyncio.run(crawler.extract())
print(result)
```

## Performance Profiling

### Memory Profiling
```bash
pip install memory-profiler

python -m memory_profiler main.py
```

### CPU Profiling
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Run extraction...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

### Thread Analysis
```python
import threading

def print_threads():
    for thread in threading.enumerate():
        print(f"Thread: {thread.name}, Daemon: {thread.daemon}, Alive: {thread.is_alive()}")
```

## CI/CD Considerations

### GitHub Actions Workflow
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - run: pip install -r requirements.txt
    - run: python -m pytest tests/
```

## Deployment

### Linux (AppImage)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed \
  --add-data "ui:ui" \
  --add-data "backend:backend" \
  main.py
```

### Windows (Executable)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico ^
  --add-data "ui;ui" ^
  --add-data "backend;backend" ^
  main.py
```

### macOS (Bundle)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --osx-bundle-identifier="com.sitemirror.app" ^
  --add-data "ui:ui" ^
  --add-data "backend:backend" ^
  main.py
```

## Known Limitations

1. **Network**: Requires active internet connection
2. **TOR**: Must be installed separately for onion sites
3. **JavaScript**: Requires headless browser option for JS-heavy sites
4. **Memory**: Very large sites may require more RAM
5. **Rate Limiting**: Fast crawling may trigger site rate limits
6. **Authentication**: No automatic login support

## Future Improvements

- [ ] Session persistence and resumption
- [ ] Compression and deduplication
- [ ] Database backend option
- [ ] REST API interface
- [ ] Distributed extraction support
- [ ] Advanced authentication (cookies, headers)
- [ ] JavaScript rendering support
- [ ] Content transformation/optimization

## Support

For issues, please provide:
1. OS and Python version
2. Application version (from About panel)
3. Extraction URL (if non-sensitive)
4. Full log output
5. Steps to reproduce

## Maintenance

### Regular Updates
- [ ] Update dependencies monthly
- [ ] Review security advisories
- [ ] Test with new Python versions
- [ ] Update documentation

### Monitoring
- [ ] Error rates from users
- [ ] Common issues and patterns
- [ ] Performance metrics
- [ ] User feedback

---

**SiteMirror Testing Guide v1.0**
