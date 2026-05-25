"""
Real-time log viewer component - terminal-style.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                              QPushButton, QComboBox, QLineEdit, QLabel)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QTextCursor, QColor, QTextCharFormat

from ui.styles.theme import THEME, get_log_color
from backend.logs.logger import LogEntry, LogLevel


class LogViewer(QWidget):
    """Real-time log viewer with filtering and search."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        # Title bar
        title_bar = QHBoxLayout()
        title_bar.setSpacing(8)
        
        title = QLabel("Live Activity / Logs")
        title_font = QFont(THEME.font_family)
        title_font.setPointSize(THEME.font_heading)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {THEME.text_primary}; background-color: transparent;")
        title_bar.addWidget(title)
        
        title_bar.addStretch()
        
        # Filter dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "All Logs", "Info", "Success", "Warning", "Error", "Network"
        ])
        self.filter_combo.currentTextChanged.connect(self._on_filter_changed)
        self.filter_combo.setMaximumWidth(120)
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search logs...")
        self.search_input.textChanged.connect(self._on_search_changed)
        self.search_input.setMaximumWidth(180)
        
        # Clear button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self._on_clear_logs)
        self.clear_btn.setMaximumWidth(60)
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME.bg_card};
                color: {THEME.text_secondary};
                border: 1px solid {THEME.border_color};
                padding: 4px 10px;
                border-radius: 4px;
                font-size: 8pt;
            }}
            QPushButton:hover {{
                background-color: rgba(124, 77, 255, 0.1);
                color: {THEME.text_primary};
            }}
        """)
        
        title_bar.addWidget(self.filter_combo)
        title_bar.addWidget(self.search_input)
        title_bar.addWidget(self.clear_btn)
        
        layout.addLayout(title_bar)
        
        # Log display - terminal style
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setObjectName("logViewer")
        font = QFont(THEME.font_mono)
        font.setPointSize(THEME.font_logs)
        self.log_text.setFont(font)
        
        layout.addWidget(self.log_text)
        
        self.setLayout(layout)
        
        # Storage
        self.all_logs = []
        self.current_filter = "All Logs"
        self.current_search = ""
        self._needs_render = False
        
        # Batch render timer (avoid re-rendering every single log)
        self._render_timer = QTimer()
        self._render_timer.timeout.connect(self._do_render)
        self._render_timer.setInterval(200)
        self._render_timer.start()
    
    def add_log_entry(self, entry: LogEntry) -> None:
        """Add a log entry."""
        self.all_logs.append(entry)
        
        # Keep only recent logs
        if len(self.all_logs) > 5000:
            self.all_logs = self.all_logs[-4000:]
        
        self._needs_render = True
    
    def _do_render(self):
        """Periodic render check."""
        if self._needs_render:
            self._needs_render = False
            self._render_logs()
    
    def _get_filtered_logs(self):
        """Get logs after applying filters."""
        logs = self.all_logs
        
        if self.current_filter != "All Logs":
            logs = [l for l in logs if l.level.value == self.current_filter.upper()]
        
        if self.current_search:
            search_lower = self.current_search.lower()
            logs = [l for l in logs if search_lower in l.message.lower()]
        
        return logs
    
    def _render_logs(self) -> None:
        """Render logs to text display."""
        logs = self._get_filtered_logs()
        
        self.log_text.clear()
        cursor = self.log_text.textCursor()
        
        for entry in logs[-500:]:  # Show last 500 for performance
            # Prefix with timestamp
            ts_format = QTextCharFormat()
            ts_format.setForeground(QColor(THEME.text_muted))
            cursor.insertText(f"[{entry.timestamp}]  ", ts_format)
            
            # Message with color
            msg_format = QTextCharFormat()
            color_hex = get_log_color(entry.level.value)
            msg_format.setForeground(QColor(color_hex))
            
            # Add check/cross marks for success/error
            prefix = ""
            if entry.level == LogLevel.SUCCESS:
                prefix = "✓ "
            elif entry.level == LogLevel.ERROR:
                prefix = "✗ "
            elif entry.level == LogLevel.WARNING:
                prefix = "⚠ "
            
            cursor.insertText(f"{prefix}{entry.message}\n", msg_format)
        
        # Scroll to bottom
        self.log_text.setTextCursor(cursor)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def _on_filter_changed(self, filter_text: str) -> None:
        """Handle filter change."""
        self.current_filter = filter_text
        self._needs_render = True
    
    def _on_search_changed(self, search_text: str) -> None:
        """Handle search change."""
        self.current_search = search_text
        self._needs_render = True
    
    def _on_clear_logs(self) -> None:
        """Clear all logs."""
        self.all_logs.clear()
        self.log_text.clear()
    
    def get_log_count(self) -> int:
        """Get total log count."""
        return len(self.all_logs)
