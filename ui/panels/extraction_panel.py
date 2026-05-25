"""
Main extraction panel component - matches reference layout.
Top section: URL input, 3-column options row, Start button.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QScrollArea, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ui.styles.theme import THEME
from ui.widgets.custom_widgets import (LabeledInput, RadioGroup, CheckboxGroup,
                                       CTAButton, StopButton, Card)


class ExtractionPanel(QWidget):
    """Main extraction panel with all controls."""
    
    extraction_started = Signal(dict)
    extraction_stopped = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_extracting = False
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === Header ===
        header_card = Card()
        header_card.layout.setContentsMargins(THEME.padding_lg, THEME.padding_lg,
                                               THEME.padding_lg, THEME.padding_lg)
        header_card.layout.setSpacing(12)
        
        # Section title
        title_row = QHBoxLayout()
        title_icon = QLabel("⚡")
        title_icon.setStyleSheet("font-size: 14pt; background-color: transparent;")
        title_label = QLabel("Start New Extraction")
        title_font = QFont(THEME.font_family)
        title_font.setPointSize(13)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {THEME.text_primary}; background-color: transparent;")
        title_row.addWidget(title_icon)
        title_row.addWidget(title_label)
        title_row.addStretch()
        header_card.layout.addLayout(title_row)
        
        # URL input
        self.url_input = LabeledInput(
            "Website / Onion Link",
            "https://example.com"
        )
        self.url_input.input.textChanged.connect(self._on_url_changed)
        header_card.layout.addWidget(self.url_input)
        
        # === Three-column options row ===
        options_row = QHBoxLayout()
        options_row.setSpacing(THEME.padding_lg)
        
        # Column 1: Site Type
        self.site_type = RadioGroup(
            "Site Type",
            ["ClearNet (HTTP/HTTPS)", "Onion Site (TOR)"]
        )
        
        # Column 2: Extraction Depth
        self.depth_option = RadioGroup(
            "Extraction Depth",
            ["Single Page", "Same Domain", "All Links (Recursive)"]
        )
        
        # Column 3: Additional Options
        self.options = CheckboxGroup(
            "Additional Options",
            [
                "Download Assets (Images, CSS, JS)",
                "Download External Links",
                "Respect robots.txt",
                "Use TOR for Onion Sites"
            ]
        )
        # Pre-check some defaults
        self.options.set_checked([
            "Download Assets (Images, CSS, JS)",
            "Respect robots.txt"
        ])
        
        options_row.addWidget(self.site_type)
        options_row.addWidget(self.depth_option)
        options_row.addWidget(self.options)
        
        # Start button
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        
        self.start_btn = CTAButton("▶  Start Extracting")
        self.start_btn.clicked.connect(self._on_start_extraction)
        
        self.stop_btn = StopButton("⬜  Stop Extraction")
        self.stop_btn.clicked.connect(self._on_stop_extraction)
        self.stop_btn.setVisible(False)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addStretch()
        
        options_row.addLayout(btn_layout)
        
        header_card.layout.addLayout(options_row)
        
        main_layout.addWidget(header_card)
        
        self.setLayout(main_layout)
    
    def _on_url_changed(self, text: str) -> None:
        """Handle URL change for auto-detection."""
        if '.onion' in text:
            self.site_type.set_selected("Onion Site (TOR)")
        elif text.startswith('http://') or text.startswith('https://'):
            self.site_type.set_selected("ClearNet (HTTP/HTTPS)")
    
    def _on_start_extraction(self) -> None:
        """Handle extraction start."""
        url = self.url_input.get_text().strip()
        
        if not url:
            return
        
        # Auto-add scheme if missing
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
            self.url_input.set_text(url)
        
        config = {
            'url': url,
            'mode': 'onion' if self.site_type.get_selected() == "Onion Site (TOR)" else 'clearnet',
            'depth': self._get_depth_value(),
            'download_assets': 'Download Assets (Images, CSS, JS)' in self.options.get_checked(),
            'extract_links': 'Download External Links' in self.options.get_checked(),
            'download_media': False,
            'respect_robots': 'Respect robots.txt' in self.options.get_checked(),
            'use_headless_browser': False,
            'detect_dynamic_content': False,
            'save_cookies': False,
        }
        
        self.extraction_started.emit(config)
        self._set_extracting(True)
    
    def _on_stop_extraction(self) -> None:
        """Handle extraction stop."""
        self.extraction_stopped.emit()
        self._set_extracting(False)
    
    def _get_depth_value(self) -> str:
        """Convert depth selection to value."""
        selection = self.depth_option.get_selected()
        depth_map = {
            "Single Page": "single",
            "Same Domain": "same_domain",
            "All Links (Recursive)": "recursive"
        }
        return depth_map.get(selection, "single")
    
    def _set_extracting(self, is_extracting: bool) -> None:
        """Toggle between extracting and idle states."""
        self._is_extracting = is_extracting
        self.url_input.input.setEnabled(not is_extracting)
        self.site_type.setEnabled(not is_extracting)
        self.depth_option.setEnabled(not is_extracting)
        self.options.setEnabled(not is_extracting)
        self.start_btn.setVisible(not is_extracting)
        self.stop_btn.setVisible(is_extracting)
    
    def reset_form(self) -> None:
        """Reset form to initial state."""
        self._set_extracting(False)
