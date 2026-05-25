"""
Sidebar navigation component.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ui.styles.theme import THEME


class Sidebar(QWidget):
    """Application sidebar with navigation."""
    
    tab_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setMinimumWidth(THEME.sidebar_width)
        self.setMaximumWidth(THEME.sidebar_width)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(4)
        
        # Logo area
        logo_widget = QWidget()
        logo_widget.setStyleSheet("background-color: transparent;")
        logo_layout = QVBoxLayout()
        logo_layout.setSpacing(2)
        logo_layout.setContentsMargins(8, 0, 8, 12)
        
        # Logo icon + title
        logo_row = QHBoxLayout()
        logo_row.setSpacing(8)
        
        logo_icon = QLabel("🌐")
        logo_icon.setStyleSheet("background-color: transparent; font-size: 18pt;")
        
        logo_title = QLabel("SiteMirror")
        title_font = QFont(THEME.font_family)
        title_font.setPointSize(14)
        title_font.setBold(True)
        logo_title.setFont(title_font)
        logo_title.setStyleSheet(f"color: {THEME.text_primary}; background-color: transparent;")
        
        logo_row.addWidget(logo_icon)
        logo_row.addWidget(logo_title)
        logo_row.addStretch()
        
        logo_subtitle = QLabel("Web Extraction & Mirroring Tool")
        sub_font = QFont(THEME.font_family)
        sub_font.setPointSize(7)
        logo_subtitle.setFont(sub_font)
        logo_subtitle.setStyleSheet(f"color: {THEME.text_muted}; background-color: transparent;")
        
        logo_layout.addLayout(logo_row)
        logo_layout.addWidget(logo_subtitle)
        logo_widget.setLayout(logo_layout)
        
        layout.addWidget(logo_widget)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFixedHeight(1)
        separator.setStyleSheet(f"background-color: {THEME.border_color}; border: none;")
        layout.addWidget(separator)
        layout.addSpacing(8)
        
        # Navigation items
        self.nav_buttons = {}
        nav_items = [
            ("Overview", "📊"),
            ("Settings", "⚙️"),
            ("Downloads", "📥"),
            ("History", "📜"),
            ("Logs", "📋"),
            ("About", "ℹ️"),
        ]
        
        for name, icon in nav_items:
            btn = self._create_nav_button(f" {icon}  {name}", name)
            self.nav_buttons[name] = btn
            layout.addWidget(btn)
        
        # Spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Quick Stats Section
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(124, 77, 255, 0.06);
                border: 1px solid {THEME.border_color};
                border-radius: 8px;
            }}
        """)
        stats_layout = QVBoxLayout()
        stats_layout.setContentsMargins(10, 10, 10, 10)
        stats_layout.setSpacing(6)
        
        stats_title = QLabel("Quick Stats")
        stats_title.setStyleSheet(f"color: {THEME.primary_accent}; font-weight: bold; background-color: transparent; font-size: 9pt;")
        stats_layout.addWidget(stats_title)
        
        self.stat_pages = self._create_stat_row("Pages Extracted", "0")
        self.stat_files = self._create_stat_row("Files Downloaded", "0")
        self.stat_size = self._create_stat_row("Total Size", "0 B")
        self.stat_time = self._create_stat_row("Current Session", "00:00:00")
        
        stats_layout.addLayout(self.stat_pages[0])
        stats_layout.addLayout(self.stat_files[0])
        stats_layout.addLayout(self.stat_size[0])
        stats_layout.addLayout(self.stat_time[0])
        
        stats_frame.setLayout(stats_layout)
        layout.addWidget(stats_frame)
        
        layout.addSpacing(8)
        
        # Bottom icons row
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(12)
        bottom_row.setContentsMargins(8, 0, 8, 0)
        
        for icon_text in ["🔗", "❓", "🌙"]:
            icon_btn = QPushButton(icon_text)
            icon_btn.setMaximumSize(32, 32)
            icon_btn.setCursor(Qt.PointingHandCursor)
            icon_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: none;
                    font-size: 12pt;
                    padding: 2px;
                }}
                QPushButton:hover {{
                    background-color: rgba(124, 77, 255, 0.1);
                    border-radius: 4px;
                }}
            """)
            bottom_row.addWidget(icon_btn)
        
        bottom_row.addStretch()
        layout.addLayout(bottom_row)
        
        self.setLayout(layout)
        
        # Set first item as active
        self.set_active_tab("Overview")
    
    def _create_stat_row(self, label: str, value: str):
        """Create a stats label-value row."""
        row = QHBoxLayout()
        row.setSpacing(4)
        
        lbl = QLabel(label)
        lbl.setStyleSheet(f"color: {THEME.text_muted}; background-color: transparent; font-size: 8pt;")
        
        val = QLabel(value)
        val.setAlignment(Qt.AlignRight)
        val.setStyleSheet(f"color: {THEME.text_primary}; background-color: transparent; font-size: 8pt; font-weight: bold;")
        
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(val)
        
        return (row, val)
    
    def update_stats(self, pages: int = 0, files: int = 0, size_str: str = "0 B", time_str: str = "00:00:00"):
        """Update sidebar quick stats."""
        self.stat_pages[1].setText(str(pages))
        self.stat_files[1].setText(str(files))
        self.stat_size[1].setText(size_str)
        self.stat_time[1].setText(time_str)
    
    def _create_nav_button(self, text: str, tab_id: str) -> QPushButton:
        """Create styled navigation button."""
        btn = QPushButton(text)
        btn.setMinimumHeight(36)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda: self._on_button_clicked(tab_id))
        return btn
    
    def _on_button_clicked(self, tab_id: str) -> None:
        """Handle button click."""
        self.set_active_tab(tab_id)
        self.tab_changed.emit(tab_id)
    
    def set_active_tab(self, tab_id: str) -> None:
        """Set active navigation tab."""
        for name, btn in self.nav_buttons.items():
            if name == tab_id:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: rgba(124, 77, 255, 0.18);
                        border-left: 3px solid {THEME.primary_accent};
                        color: {THEME.primary_accent};
                        border-radius: 6px;
                        padding: 8px 12px;
                        text-align: left;
                        font-weight: bold;
                        font-size: {THEME.font_body}pt;
                    }}
                    QPushButton:hover {{
                        background-color: rgba(124, 77, 255, 0.25);
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        border: none;
                        color: {THEME.text_secondary};
                        padding: 8px 12px;
                        text-align: left;
                        border-radius: 6px;
                        font-size: {THEME.font_body}pt;
                    }}
                    QPushButton:hover {{
                        background-color: rgba(124, 77, 255, 0.08);
                        color: {THEME.text_primary};
                    }}
                """)
