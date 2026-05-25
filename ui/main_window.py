"""
Main application window - matches reference layout.
"""

import time
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                              QStatusBar, QLabel, QStackedWidget)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from ui.styles.theme import THEME, get_stylesheet
from ui.widgets.sidebar import Sidebar
from ui.widgets.custom_widgets import Card
from ui.panels.extraction_panel import ExtractionPanel
from ui.panels.log_viewer import LogViewer
from ui.panels.status_panel import (ExtractionStatusPanel, BottomStatsBar,
                                     OverallProgressBar, SaveLocationBar)
from ui.panels.history_panel import HistoryPanel
from ui.panels.settings_panel import SettingsPanel
from ui.panels.about_panel import AboutPanel
from backend.logs.logger import get_logger
from backend.core.extractor import get_extraction_manager
from backend.core.crawler import ExtractionConfig, ExtractionMode, ExtractionDepth


class MainWindow(QMainWindow):
    """Main application window."""
    
    # Thread-safe signals
    log_received = Signal(object)
    progress_updated = Signal(int)
    status_changed = Signal(str)
    extraction_finished = Signal(dict)
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("SiteMirror - Web Extraction & Mirroring Tool")
        self.setMinimumSize(1280, 800)
        
        # Apply theme
        self.setStyleSheet(get_stylesheet())
        
        # Get backend managers
        self.logger = get_logger()
        self.extraction_manager = get_extraction_manager()
        
        # State tracking
        self._extraction_start_time = None
        self._is_extracting = False
        
        # Connect thread-safe signals
        self.log_received.connect(self._on_log_entry_gui)
        self.progress_updated.connect(self._on_progress_update_gui)
        self.status_changed.connect(self._on_status_change_gui)
        self.extraction_finished.connect(self._on_extraction_finished_gui)
        
        # Register for log events
        self.logger.add_listener(self._on_log_entry)
        
        # Build UI
        self._build_ui()
        
        # Connect manager signals
        self.extraction_manager.add_progress_callback(self._on_progress_update)
        self.extraction_manager.add_status_callback(self._on_status_change)
        self.extraction_manager.add_finish_callback(self._on_extraction_finished)
        
        # Timer for elapsed time updates
        self._elapsed_timer = QTimer()
        self._elapsed_timer.timeout.connect(self._update_elapsed_time)
        self._elapsed_timer.setInterval(1000)
    
    def _build_ui(self) -> None:
        """Build the main UI layout."""
        
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Content area (horizontal split)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.tab_changed.connect(self._on_tab_changed)
        content_layout.addWidget(self.sidebar)
        
        # Stacked widget for tab content
        self.content_stack = QStackedWidget()
        
        # Tab 0: Overview
        overview_widget = self._create_overview_tab()
        self.content_stack.addWidget(overview_widget)
        
        # Tab 1: Settings
        self.settings_panel = SettingsPanel()
        self.content_stack.addWidget(self.settings_panel)
        
        # Tab 2: Downloads
        downloads_widget = self._create_placeholder_tab("Downloads", "Download management coming soon...")
        self.content_stack.addWidget(downloads_widget)
        
        # Tab 3: History
        self.history_panel = HistoryPanel()
        self.content_stack.addWidget(self.history_panel)
        
        # Tab 4: Logs (full-screen)
        logs_widget = self._create_logs_tab()
        self.content_stack.addWidget(logs_widget)
        
        # Tab 5: About
        self.about_panel = AboutPanel()
        self.content_stack.addWidget(self.about_panel)
        
        content_layout.addWidget(self.content_stack)
        
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)
        
        # Bottom save location bar
        self.save_bar = SaveLocationBar()
        main_layout.addWidget(self.save_bar)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def _create_overview_tab(self) -> QWidget:
        """Create the overview/extraction tab matching the reference."""
        tab_widget = QWidget()
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(12, 12, 12, 12)
        tab_layout.setSpacing(10)
        
        # === Top: Extraction Panel ===
        self.extraction_panel = ExtractionPanel()
        self.extraction_panel.extraction_started.connect(self._on_extraction_started)
        self.extraction_panel.extraction_stopped.connect(self._on_extraction_stopped)
        tab_layout.addWidget(self.extraction_panel)
        
        # === Middle: Logs + Status side by side ===
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(10)
        
        # Log viewer (takes most space)
        self.log_viewer = LogViewer()
        middle_layout.addWidget(self.log_viewer, stretch=3)
        
        # Extraction status panel (right side)
        self.status_panel = ExtractionStatusPanel()
        self.status_panel.setMaximumWidth(280)
        self.status_panel.setMinimumWidth(240)
        middle_layout.addWidget(self.status_panel, stretch=0)
        
        tab_layout.addLayout(middle_layout, stretch=1)
        
        # === Bottom: Progress bar ===
        self.overall_progress = OverallProgressBar()
        tab_layout.addWidget(self.overall_progress)
        
        # === Bottom: Stats bar ===
        self.bottom_stats = BottomStatsBar()
        tab_layout.addWidget(self.bottom_stats)
        
        tab_widget.setLayout(tab_layout)
        return tab_widget
    
    def _create_logs_tab(self) -> QWidget:
        """Create the dedicated full-screen logs tab."""
        tab_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        
        self.full_log_viewer = LogViewer()
        layout.addWidget(self.full_log_viewer)
        
        tab_widget.setLayout(layout)
        return tab_widget
    
    def _create_placeholder_tab(self, title: str, message: str) -> QWidget:
        """Create a placeholder tab."""
        tab_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(THEME.padding_lg, THEME.padding_lg,
                                 THEME.padding_lg, THEME.padding_lg)
        
        card = Card(title)
        msg = QLabel(message)
        msg.setStyleSheet(f"color: {THEME.text_secondary}; background-color: transparent;")
        card.layout.addWidget(msg)
        card.layout.addStretch()
        
        layout.addWidget(card)
        layout.addStretch()
        
        tab_widget.setLayout(layout)
        return tab_widget
    
    # ============================================================
    # Tab Navigation
    # ============================================================
    
    def _on_tab_changed(self, tab_id: str) -> None:
        """Handle sidebar tab change."""
        tab_map = {
            "Overview": 0,
            "Settings": 1,
            "Downloads": 2,
            "History": 3,
            "Logs": 4,
            "About": 5,
        }
        
        if tab_id in tab_map:
            self.content_stack.setCurrentIndex(tab_map[tab_id])
            
            # Sync logs if switching to full logs tab
            if tab_id == "Logs":
                self.full_log_viewer.all_logs = self.log_viewer.all_logs.copy()
                self.full_log_viewer._needs_render = True
    
    # ============================================================
    # Extraction Control
    # ============================================================
    
    def _on_extraction_started(self, config: dict) -> None:
        """Handle extraction start from panel."""
        try:
            extraction_config = ExtractionConfig(
                url=config['url'],
                mode=ExtractionMode.ONION if config['mode'] == 'onion' else ExtractionMode.CLEARNET,
                depth=self._get_extraction_depth(config['depth']),
                download_assets=config['download_assets'],
                download_media=config.get('download_media', False),
                extract_links=config.get('extract_links', True),
                respect_robots=config.get('respect_robots', True),
                use_headless_browser=config.get('use_headless_browser', False),
                detect_dynamic_content=config.get('detect_dynamic_content', False),
                save_cookies=config.get('save_cookies', False),
            )
            
            self._extraction_start_time = time.time()
            self._is_extracting = True
            
            # Update UI state
            self.status_panel.update_progress(0, "Starting...")
            self.status_panel.set_extracting(True)
            self.save_bar.set_engine_status("Active")
            self.overall_progress.set_progress(0)
            
            # Start elapsed timer
            self._elapsed_timer.start()
            
            # Start extraction
            session = self.extraction_manager.start_extraction(extraction_config)
            
            if session:
                self.logger.info(f"Extraction session started: {session.session_id}")
                
                # Update save location
                domain = extraction_config.get_base_domain()
                save_path = f"{self.save_bar.current_path}/{domain}"
                self.save_bar.set_path(save_path)
        
        except Exception as e:
            self.logger.error(f"Failed to start extraction: {str(e)}")
            self._is_extracting = False
            self.extraction_panel.reset_form()
    
    def _on_extraction_stopped(self) -> None:
        """Handle extraction stop from panel."""
        self.extraction_manager.stop_extraction()
        self._is_extracting = False
        self._elapsed_timer.stop()
        self.status_panel.set_extracting(False)
        self.save_bar.set_engine_status("Idle")
        self.extraction_panel.reset_form()
    
    def _get_extraction_depth(self, depth_str: str) -> ExtractionDepth:
        """Convert depth string to ExtractionDepth."""
        depth_map = {
            'single': ExtractionDepth.SINGLE_PAGE,
            'same_domain': ExtractionDepth.SAME_DOMAIN,
            'recursive': ExtractionDepth.RECURSIVE,
        }
        return depth_map.get(depth_str, ExtractionDepth.SINGLE_PAGE)
    
    # ============================================================
    # Thread-safe event handlers
    # ============================================================
    
    def _on_log_entry(self, entry) -> None:
        """Handle new log entry (from any thread)."""
        self.log_received.emit(entry)
    
    def _on_log_entry_gui(self, entry) -> None:
        """Handle log entry in the GUI thread."""
        self.log_viewer.add_log_entry(entry)
        
        # Update sidebar stats
        if hasattr(self, '_last_stats'):
            pass  # Will be updated by progress
    
    def _on_progress_update(self, progress: int) -> None:
        """Handle progress update (from background thread)."""
        self.progress_updated.emit(progress)
    
    def _on_progress_update_gui(self, progress: int) -> None:
        """Handle progress update in GUI thread."""
        status = "In Progress" if progress < 100 else "Complete!"
        self.status_panel.update_progress(progress, status)
        self.overall_progress.set_progress(progress)
        
        # Update stats
        if self.extraction_manager.current_session:
            session = self.extraction_manager.current_session
            stats = self.extraction_manager.get_live_stats()
            
            self.status_panel.update_stats(stats)
            self.status_panel.update_current_page(stats.get('current_url', '—'))
            
            self.bottom_stats.update_stats(
                pages=stats.get('pages_crawled', 0),
                files=stats.get('files_downloaded', 0),
                speed=stats.get('speed', '0 B/s'),
                elapsed=stats.get('elapsed', '00:00:00')
            )
            
            self.sidebar.update_stats(
                pages=stats.get('pages_crawled', 0),
                files=stats.get('files_downloaded', 0),
                size_str=stats.get('total_size', '0 B'),
                time_str=stats.get('elapsed', '00:00:00')
            )
    
    def _on_status_change(self, status: str) -> None:
        """Handle status change (from background thread)."""
        self.status_changed.emit(status)
    
    def _on_status_change_gui(self, status: str) -> None:
        """Handle status change in GUI thread."""
        self.save_bar.set_engine_status(status.title())
    
    def _on_extraction_finished(self, result: dict) -> None:
        """Handle extraction finish (from background thread)."""
        self.extraction_finished.emit(result)
    
    def _on_extraction_finished_gui(self, result: dict) -> None:
        """Handle extraction finish in GUI thread."""
        self._is_extracting = False
        self._elapsed_timer.stop()
        
        self.status_panel.update_progress(100, "Complete!")
        self.status_panel.set_extracting(False)
        self.overall_progress.set_progress(100)
        self.save_bar.set_engine_status("Idle")
        self.extraction_panel.reset_form()
        
        # Final stats update
        pages = result.get('total_pages', 0)
        files = result.get('files_saved', 0)
        size = result.get('total_size_str', '0 B')
        elapsed = result.get('elapsed_str', '00:00:00')
        
        self.bottom_stats.update_stats(pages=pages, files=files, elapsed=elapsed)
        self.sidebar.update_stats(pages=pages, files=files, size_str=size, time_str=elapsed)
        
        # Add to history
        self.history_panel.add_session({
            'url': result.get('url', 'Unknown'),
            'date': result.get('timestamp', 'N/A'),
            'type': result.get('depth', 'Single Page'),
            'size': size,
            'status': 'completed' if not result.get('error') else 'failed'
        })
    
    def _update_elapsed_time(self) -> None:
        """Update elapsed time display every second."""
        if self._extraction_start_time and self._is_extracting:
            elapsed = time.time() - self._extraction_start_time
            h = int(elapsed // 3600)
            m = int((elapsed % 3600) // 60)
            s = int(elapsed % 60)
            time_str = f"{h:02d}:{m:02d}:{s:02d}"
            
            self.bottom_stats.stat_elapsed.set_value(time_str)
            self.sidebar.stat_time[1].setText(time_str)


def run_app():
    """Run the application."""
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
