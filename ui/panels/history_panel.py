"""
History panel - shows previous extraction sessions.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
                              QLabel, QPushButton, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.styles.theme import THEME
from ui.widgets.custom_widgets import Card


class HistoryCard(QFrame):
    """Card showing a single extraction session."""
    
    def __init__(self, session_data: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(THEME.padding_lg, THEME.padding_lg,
                                 THEME.padding_lg, THEME.padding_lg)
        layout.setSpacing(THEME.padding_sm)
        
        # Header with URL and date
        header_layout = QHBoxLayout()
        
        url_label = QLabel(session_data.get('url', 'Unknown'))
        url_font = QFont(THEME.font_family)
        url_font.setPointSize(THEME.font_body)
        url_font.setBold(True)
        url_label.setFont(url_font)
        url_label.setStyleSheet(f"color: {THEME.primary_accent};")
        header_layout.addWidget(url_label)
        
        date_label = QLabel(session_data.get('date', 'N/A'))
        date_font = QFont(THEME.font_family)
        date_font.setPointSize(THEME.font_small)
        date_label.setFont(date_font)
        date_label.setStyleSheet(f"color: {THEME.text_secondary};")
        header_layout.addStretch()
        header_layout.addWidget(date_label)
        
        layout.addLayout(header_layout)
        
        # Stats row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(THEME.padding_lg)
        
        type_label = QLabel(f"Type: {session_data.get('type', 'Unknown')}")
        type_label.setStyleSheet(f"color: {THEME.text_secondary};")
        stats_layout.addWidget(type_label)
        
        size_label = QLabel(f"Size: {session_data.get('size', '0 MB')}")
        size_label.setStyleSheet(f"color: {THEME.text_secondary};")
        stats_layout.addWidget(size_label)
        
        status_label = QLabel(f"Status: {session_data.get('status', 'Unknown')}")
        status_color = THEME.success if session_data.get('status') == 'completed' else THEME.warning
        status_label.setStyleSheet(f"color: {status_color};")
        stats_layout.addWidget(status_label)
        
        layout.addLayout(stats_layout)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(THEME.padding_sm)
        
        open_btn = QPushButton("📁 Open")
        open_btn.setMaximumWidth(100)
        open_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME.bg_card};
                border: 1px solid {THEME.border_color};
                color: {THEME.text_primary};
                padding: 6px 12px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {THEME.hover_accent};
            }}
        """)
        
        reextract_btn = QPushButton("🔄 Re-extract")
        reextract_btn.setMaximumWidth(120)
        reextract_btn.setStyleSheet(open_btn.styleSheet())
        
        action_layout.addStretch()
        action_layout.addWidget(open_btn)
        action_layout.addWidget(reextract_btn)
        
        layout.addLayout(action_layout)
        
        self.setLayout(layout)


class HistoryPanel(QWidget):
    """Panel showing extraction history."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(THEME.padding_md, THEME.padding_md,
                                 THEME.padding_md, THEME.padding_md)
        layout.setSpacing(THEME.padding_md)
        
        # Title
        title = QLabel("Extraction History")
        title_font = QFont(THEME.font_family)
        title_font.setPointSize(THEME.font_heading)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Scrollable history list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {THEME.border_color};
                background-color: {THEME.bg_primary};
                border-radius: 8px;
            }}
        """)
        
        scroll_content = QWidget()
        self.history_layout = QVBoxLayout()
        self.history_layout.setSpacing(THEME.padding_md)
        scroll_content.setLayout(self.history_layout)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        
        # Sample history data
        self._populate_sample_history()
    
    def _populate_sample_history(self) -> None:
        """Populate with sample history."""
        sample_sessions = [
            {
                'url': 'https://example.com',
                'date': '2024-05-25 14:32',
                'type': 'Same Domain',
                'size': '145 MB',
                'status': 'completed'
            },
            {
                'url': 'https://github.com',
                'date': '2024-05-24 10:15',
                'type': 'Single Page',
                'size': '5.2 MB',
                'status': 'completed'
            },
            {
                'url': 'https://example.onion',
                'date': '2024-05-23 22:45',
                'type': 'Recursive',
                'size': '342 MB',
                'status': 'failed'
            },
        ]
        
        for session in sample_sessions:
            card = HistoryCard(session)
            self.history_layout.addWidget(card)
        
        self.history_layout.addStretch()
    
    def add_session(self, session_data: dict) -> None:
        """Add a session to history."""
        card = HistoryCard(session_data)
        self.history_layout.insertWidget(0, card)
