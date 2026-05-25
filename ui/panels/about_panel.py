"""
About panel - application information.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap

from ui.styles.theme import THEME
from ui.widgets.custom_widgets import Card


class AboutPanel(QWidget):
    """About and information panel."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(THEME.padding_lg, THEME.padding_lg,
                                 THEME.padding_lg, THEME.padding_lg)
        layout.setSpacing(THEME.padding_lg)
        layout.setAlignment(Qt.AlignTop)
        
        # Logo and title section
        logo_card = Card()
        
        logo_layout = QVBoxLayout()
        logo_layout.setSpacing(THEME.padding_md)
        logo_layout.setAlignment(Qt.AlignCenter)
        
        # App title
        title = QLabel("🌐 SiteMirror")
        title_font = QFont(THEME.font_family)
        title_font.setPointSize(32)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {THEME.primary_accent};")
        logo_layout.addWidget(title)
        
        # Tagline
        tagline = QLabel("Web Extraction & Mirroring Tool")
        tagline_font = QFont(THEME.font_family)
        tagline_font.setPointSize(16)
        tagline.setFont(tagline_font)
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet(f"color: {THEME.text_secondary};")
        logo_layout.addWidget(tagline)
        
        logo_card.layout.addLayout(logo_layout)
        layout.addWidget(logo_card)
        
        # Information card
        info_card = Card("About")
        
        info_texts = [
            ("Version", "1.0.0"),
            ("Python", "3.8+"),
            ("Framework", "PySide6"),
            ("License", "MIT"),
            ("Status", "Active Development"),
        ]
        
        for label, value in info_texts:
            info_layout = QVBoxLayout()
            info_layout.setSpacing(4)
            
            label_widget = QLabel(label)
            label_font = QFont(THEME.font_family)
            label_font.setPointSize(THEME.font_small)
            label_widget.setFont(label_font)
            label_widget.setStyleSheet(f"color: {THEME.text_secondary};")
            
            value_widget = QLabel(value)
            value_font = QFont(THEME.font_family)
            value_font.setPointSize(THEME.font_body)
            value_font.setBold(True)
            value_widget.setFont(value_font)
            value_widget.setStyleSheet(f"color: {THEME.text_primary};")
            
            info_layout.addWidget(label_widget)
            info_layout.addWidget(value_widget)
            
            info_card.layout.addLayout(info_layout)
        
        layout.addWidget(info_card)
        
        # Features card
        features_card = Card("Features")
        
        features = [
            "🌐 Multi-protocol support (HTTP/HTTPS, TOR)",
            "📊 Real-time extraction monitoring",
            "⚙️ Multi-threaded async architecture",
            "🔒 Privacy-focused design",
            "💻 Modern, responsive UI",
            "📦 Efficient storage and compression",
        ]
        
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setStyleSheet(f"color: {THEME.text_primary};")
            feature_label.setWordWrap(True)
            features_card.layout.addWidget(feature_label)
        
        layout.addWidget(features_card)
        
        # Credits card
        credits_card = Card("Credits")
        
        credits_text = QLabel(
            "Built with:\n"
            "• PySide6 - Qt bindings\n"
            "• aiohttp - Async HTTP\n"
            "• BeautifulSoup - HTML parsing\n"
            "• Playwright - Browser automation\n"
            "• stem - TOR connectivity"
        )
        credits_text.setStyleSheet(f"color: {THEME.text_secondary};")
        credits_text.setWordWrap(True)
        credits_card.layout.addWidget(credits_text)
        
        layout.addWidget(credits_card)
        
        # Footer
        footer = QLabel(
            "SiteMirror is provided as-is for educational purposes.\n"
            "Always respect website terms of service and robots.txt."
        )
        footer_font = QFont(THEME.font_family)
        footer_font.setPointSize(THEME.font_small - 1)
        footer.setFont(footer_font)
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet(f"color: {THEME.text_muted};")
        footer.setWordWrap(True)
        layout.addWidget(footer)
        
        layout.addStretch()
        
        self.setLayout(layout)
