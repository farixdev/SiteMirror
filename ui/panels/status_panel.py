"""
Extraction status, progress, and download location panels.
"""

import os
import platform
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QProgressBar, QFrame, QScrollArea, QPushButton,
                              QFileDialog)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ui.styles.theme import THEME
from ui.widgets.custom_widgets import Card, CircularProgress, StatItem


class ExtractionStatusPanel(QWidget):
    """Right-side panel showing extraction progress and live stats."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # === Extraction Status Card ===
        status_card = Card("Extraction Status")
        
        # Circular progress
        self.progress_circle = CircularProgress(size=150)
        status_card.layout.addWidget(self.progress_circle, alignment=Qt.AlignCenter)
        status_card.layout.addSpacing(8)
        
        # Current page info
        self.current_page_label = QLabel("Current Page")
        self.current_page_label.setStyleSheet(f"color: {THEME.text_secondary}; font-size: 8pt; background-color: transparent;")
        status_card.layout.addWidget(self.current_page_label)
        
        self.current_page_url = QLabel("—")
        self.current_page_url.setStyleSheet(f"color: {THEME.primary_accent}; font-size: 8pt; background-color: transparent;")
        self.current_page_url.setWordWrap(True)
        status_card.layout.addWidget(self.current_page_url)
        
        status_card.layout.addSpacing(8)
        
        # Stats grid
        stats_data = [
            ("Total Pages Found", "total_pages"),
            ("Total Files", "total_files"),
            ("Total Size", "total_size"),
            ("Start Time", "start_time"),
            ("ETA", "eta"),
        ]
        
        self._stat_labels = {}
        for label_text, key in stats_data:
            row = QHBoxLayout()
            row.setSpacing(4)
            
            lbl = QLabel(label_text)
            lbl.setStyleSheet(f"color: {THEME.text_secondary}; font-size: 8pt; background-color: transparent;")
            
            val = QLabel("—")
            val.setAlignment(Qt.AlignRight)
            val.setStyleSheet(f"color: {THEME.text_primary}; font-size: 8pt; font-weight: bold; background-color: transparent;")
            
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(val)
            
            status_card.layout.addLayout(row)
            self._stat_labels[key] = val
        
        status_card.layout.addStretch()
        
        # Stop button placeholder
        self.stop_btn = QPushButton("⬜  Stop Extraction")
        self.stop_btn.setObjectName("stop-button")
        self.stop_btn.setMinimumHeight(38)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setVisible(False)
        status_card.layout.addWidget(self.stop_btn)
        
        layout.addWidget(status_card)
        self.setLayout(layout)
    
    def update_progress(self, percentage: int, status: str = "") -> None:
        """Update progress display."""
        self.progress_circle.set_progress(percentage, status)
    
    def update_current_page(self, url: str) -> None:
        """Update current page being extracted."""
        self.current_page_url.setText(url)
    
    def update_stats(self, stats: dict) -> None:
        """Update all stats."""
        for key, label in self._stat_labels.items():
            if key in stats:
                label.setText(str(stats[key]))
    
    def set_extracting(self, is_extracting: bool) -> None:
        """Toggle extracting state."""
        self.stop_btn.setVisible(is_extracting)


class BottomStatsBar(QWidget):
    """Bottom stats bar showing pages, files, speed, elapsed time."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {THEME.bg_card};
                border: 1px solid {THEME.border_color};
                border-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(32)
        
        self.stat_pages = StatItem("📄", "Pages Extracted", "0")
        self.stat_files = StatItem("📁", "Files Downloaded", "0")
        self.stat_speed = StatItem("⚡", "Current Speed", "0 B/s")
        self.stat_elapsed = StatItem("⏱️", "Elapsed Time", "00:00:00")
        
        layout.addWidget(self.stat_pages)
        layout.addWidget(self.stat_files)
        layout.addWidget(self.stat_speed)
        layout.addWidget(self.stat_elapsed)
        
        self.setLayout(layout)
    
    def update_stats(self, pages: int = 0, files: int = 0,
                    speed: str = "0 B/s", elapsed: str = "00:00:00"):
        """Update bottom stats."""
        self.stat_pages.set_value(str(pages))
        self.stat_files.set_value(str(files))
        self.stat_speed.set_value(speed)
        self.stat_elapsed.set_value(elapsed)


class OverallProgressBar(QWidget):
    """Overall progress bar with label."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        label = QLabel("Overall Progress")
        label.setStyleSheet(f"color: {THEME.text_secondary}; font-size: 8pt; background-color: transparent;")
        label.setMinimumWidth(100)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        
        self.pct_label = QLabel("0%")
        self.pct_label.setStyleSheet(f"color: {THEME.text_primary}; font-size: 8pt; background-color: transparent;")
        self.pct_label.setMinimumWidth(40)
        self.pct_label.setAlignment(Qt.AlignRight)
        
        layout.addWidget(label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.pct_label)
        
        self.setLayout(layout)
    
    def set_progress(self, value: int):
        """Update progress bar."""
        value = max(0, min(100, value))
        self.progress_bar.setValue(value)
        self.pct_label.setText(f"{value}%")


class SaveLocationBar(QWidget):
    """Bottom bar showing save location."""
    
    location_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {THEME.bg_secondary};
                border-top: 1px solid {THEME.border_color};
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(14, 6, 14, 6)
        layout.setSpacing(10)
        
        label = QLabel("Save Location:")
        label.setStyleSheet(f"color: {THEME.text_secondary}; font-size: 8pt; background-color: transparent;")
        
        self.path_label = QLabel("")
        self.path_label.setStyleSheet(f"color: {THEME.text_primary}; font-size: 8pt; background-color: transparent;")
        
        folder_btn = QPushButton("📂")
        folder_btn.setMaximumSize(28, 28)
        folder_btn.setCursor(Qt.PointingHandCursor)
        folder_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {THEME.border_color};
                border-radius: 4px;
                padding: 2px;
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: rgba(124, 77, 255, 0.1);
            }}
        """)
        folder_btn.clicked.connect(self._on_change_path)
        
        layout.addWidget(label)
        layout.addWidget(self.path_label, 1)
        layout.addWidget(folder_btn)
        
        # Right side: engine status, proxies
        layout.addSpacing(40)
        
        self.engine_label = QLabel("Engine:  Idle")
        self.engine_label.setStyleSheet(f"color: {THEME.text_secondary}; font-size: 8pt; background-color: transparent;")
        
        self.proxy_label = QLabel("Proxies: 0")
        self.proxy_label.setStyleSheet(f"color: {THEME.text_secondary}; font-size: 8pt; background-color: transparent;")
        
        layout.addWidget(self.engine_label)
        layout.addSpacing(20)
        layout.addWidget(self.proxy_label)
        
        self.setLayout(layout)
        
        # Set default path
        self.current_path = os.path.abspath("./data/extractions")
        self.path_label.setText(self.current_path)
    
    def set_path(self, path: str) -> None:
        """Set current save path."""
        self.current_path = path
        self.path_label.setText(path)
    
    def set_engine_status(self, status: str) -> None:
        """Update engine status display."""
        color = THEME.success if status.lower() == "active" else THEME.text_secondary
        self.engine_label.setText(f"Engine:  <span style='color:{color}'>{status}</span>")
    
    def _on_change_path(self) -> None:
        """Change save path."""
        path = QFileDialog.getExistingDirectory(
            self, "Select Save Location",
            self.current_path
        )
        
        if path:
            self.set_path(path)
            self.location_changed.emit(path)
