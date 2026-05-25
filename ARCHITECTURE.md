# SiteMirror - Architecture Documentation

## Project Overview

SiteMirror is a modern desktop application for extracting and mirroring websites with support for both clearnet (HTTP/HTTPS) and TOR (onion) sites.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     PyQt6 User Interface                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Extraction  │  │ Real-time    │  │ Status/Progress  │   │
│  │  Panel       │  │ Logs Viewer  │  │ Monitor          │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  History     │  │ Settings     │  │ About Panel      │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└──────────────────┬──────────────────────────────────────────┘
                   │ Signals/Slots
┌──────────────────▼──────────────────────────────────────────┐
│              Backend Engine (Python Async)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Extraction Manager (Orchestration)                  │   │
│  │ ┌────────────────────────────────────────────────┐  │   │
│  │ │ • Session Management                           │  │   │
│  │ │ • Status Tracking                              │  │   │
│  │ │ • Progress Updates                             │  │   │
│  │ └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Core Extraction Engine                             │   │
│  │ ┌────────────────────────────────────────────────┐  │   │
│  │ │ Crawler                                        │  │   │
│  │ │ • URL fetching (aiohttp)                      │  │   │
│  │ │ • HTML parsing (BeautifulSoup)                │  │   │
│  │ │ • Link extraction                             │  │   │
│  │ │ • Asset discovery                             │  │   │
│  │ └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Support Systems                                      │   │
│  │ ┌────────────────────────────────────────────────┐  │   │
│  │ │ Worker Pool      │ Logger      │ Storage       │  │   │
│  │ │ (Multi-threading)│ (Real-time) │ (File saving) │  │   │
│  │ └────────────────────────────────────────────────┘  │   │
│  │ ┌────────────────────────────────────────────────┐  │   │
│  │ │ Proxy Manager    │ TOR Manager │ Config        │  │   │
│  │ │ (Network config) │ (TOR/Onion) │ (Settings)    │  │   │
│  │ └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                   │ Network Requests
┌──────────────────▼──────────────────────────────────────────┐
│                    External Systems                         │
│  • HTTP/HTTPS Websites                                      │
│  • TOR Network (Onion Sites)                                │
│  • Local File System (Storage)                              │
└──────────────────────────────────────────────────────────────┘
```

## Module Structure

### `/ui` - User Interface
**Framework**: PySide6 (PyQt6 bindings)

- **main_window.py**: Main application window with tab management
- **panels/**:
  - `extraction_panel.py`: Configuration and control inputs
  - `log_viewer.py`: Real-time log display with filtering
  - `status_panel.py`: Progress indicators and statistics
  - `history_panel.py`: Previous extraction sessions
  - `settings_panel.py`: Application configuration
  - `about_panel.py`: Application information
- **widgets/**:
  - `custom_widgets.py`: Reusable UI components (Card, Buttons, etc.)
  - `sidebar.py`: Navigation sidebar
- **styles/**:
  - `theme.py`: Color scheme, fonts, and stylesheet generation

### `/backend` - Business Logic

#### **core/** - Core Engine
- **crawler.py**: Main crawler with async fetching and parsing
- **extractor.py**: Extraction manager orchestrating the process
- **proxy.py**: Proxy configuration (HTTP, SOCKS5, TOR)
- **tor_manager.py**: TOR connection management
- **config.py**: Application configuration management

#### **threading/** - Concurrency
- **worker_pool.py**: Thread pool for parallel task execution

#### **storage/** - Data Management
- **downloader.py**: File downloading and storage

#### **logs/** - Logging System
- **logger.py**: Real-time logging with listener callbacks

## Data Flow

### Extraction Process

```
User Action (Start Extraction)
    ↓
UI: extraction_started signal → Main Window
    ↓
Main Window → Extraction Manager
    ↓
Extraction Manager:
  • Validates URL (auto-detect onion)
  • Creates session directory
  • Creates Crawler instance
    ↓
Crawler (Async):
  • Gets proxy configuration
  • Fetches first URL
  • Parses HTML → BeautifulSoup
  • Extracts links/assets
  • Queues new URLs
  • Repeats (based on depth)
    ↓
Downloads:
  • Files saved to session directory
  • Log events → Logger
    ↓
Logger:
  • Creates LogEntry
  • Notifies all listeners
    ↓
UI Components:
  • Log Viewer: displays entry
  • Status Panel: updates stats
  • Thread Monitor: shows activity
```

### Logging System

```
Logger (Singleton)
  │
  ├─ Internal Storage (all_logs list)
  │
  ├─ Listener Callbacks (registered by UI)
  │  ├─ Log Viewer
  │  ├─ Status Bar
  │  └─ Console (optional)
  │
  └─ Thread-Safe Access (locks)
```

## Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| UI Framework | PySide6 | Desktop application interface |
| HTTP Requests | aiohttp | Async HTTP client |
| HTML Parsing | BeautifulSoup | DOM parsing and extraction |
| Async Runtime | asyncio | Concurrent URL fetching |
| Threading | Python threading | Worker pool management |
| Network Proxy | stem | TOR connection control |
| Configuration | JSON | Settings persistence |
| File I/O | pathlib | Cross-platform file handling |

## Threading Model

### Worker Pool Design
```
Main Thread (Qt Event Loop)
    │
    ├─ UI Thread (Responsive interface)
    │
    └─ Extraction Thread (Background work)
       │
       └─ Async Event Loop (asyncio)
          │
          ├─ HTTP Fetch Task 1
          ├─ HTTP Fetch Task 2
          ├─ HTTP Fetch Task 3
          ├─ HTTP Fetch Task 4
          └─ ... (up to max_threads)
```

**Features**:
- Main thread remains responsive
- Extraction runs in background
- Non-blocking UI updates
- Thread-safe logging
- Graceful shutdown support

## Signal Flow

### Qt Signals Used
```
ExtractionPanel.extraction_started 
    → MainWindow._on_extraction_started()
    → ExtractionManager.start_extraction()

Logger.log_entry_created
    → MainWindow._on_log_entry()
    → LogViewer.add_log_entry()

ExtractionManager.progress_updated
    → MainWindow._on_progress_update()
    → StatusPanel.update_progress()

Sidebar.tab_changed
    → MainWindow._on_tab_changed()
    → QStackedWidget.setCurrentIndex()
```

## Configuration Hierarchy

```
1. Default Values (in code)
   ↓
2. config/settings.json (persistent)
   ↓
3. UI Settings Panel (user modifications)
   ↓
4. Command-line Arguments (future)
```

## TOR Integration

### Onion Site Support
```
User enters .onion URL
    ↓
Auto-detect via URL parsing
    ↓
TOR Manager:
  1. Check if TOR running
  2. If not, attempt to start
  3. Test SOCKS5 connection
  4. Verify circuit
    ↓
Proxy Manager:
  1. Configure SOCKS5 proxy
  2. Pass to Crawler
    ↓
Crawler:
  1. Use proxy for all requests
  2. Fetch .onion pages
  3. Extract content normally
```

## Performance Characteristics

### Optimizations
- **Async I/O**: Non-blocking HTTP requests
- **Connection Pooling**: Reused TCP connections
- **Memory Management**: Log rotation (5000 entry limit)
- **Thread Pool**: Configurable worker count
- **Rate Limiting**: Respects robots.txt

### Scalability
- Horizontal: Increase worker threads (up to ~32)
- Vertical: Upgrade system resources
- Temporal: Queue-based processing handles bursts

## Error Handling

### Graceful Degradation
```
Network Error
    ↓
Log warning/error
    ↓
Mark URL as failed
    ↓
Continue with remaining URLs
    ↓
Report summary stats
```

### Recovery Mechanisms
- Automatic retry (configurable count)
- Timeout protection
- Exception isolation (one failure doesn't crash)
- Status persistence

## Future Enhancement Points

1. **Browser Automation**: Playwright integration for JavaScript rendering
2. **Dynamic Content**: Detect and handle AJAX/SPA websites
3. **Database Storage**: SQL backend for large extractions
4. **Distributed Processing**: Multi-machine extraction
5. **REST API**: Backend API for programmatic access
6. **Caching**: Request deduplication and caching
7. **Resume Support**: Continue interrupted extractions

## Development Workflow

### Adding a New Feature
1. Backend logic in appropriate `backend/` module
2. Logger calls for visibility
3. UI components in `ui/` module
4. Connect via Qt signals/slots
5. Update configuration if needed
6. Test with logs enabled

### Debugging
- Enable full logging: `Logger.set_level(DEBUG)`
- Check `data/logs/` for exported logs
- Inspect `config/settings.json` for current configuration
- Monitor thread activity in Thread Monitor panel

---

**Architecture Version**: 1.0  
**Last Updated**: May 2024
