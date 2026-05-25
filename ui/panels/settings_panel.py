"""
Settings panel - application configuration.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QSpinBox, QCheckBox, QComboBox, QLineEdit,
                              QPushButton, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ui.styles.theme import THEME
from ui.widgets.custom_widgets import Card


class SettingsSection(Card):
    """A settings section with title."""
    
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent)


class SettingsPanel(QWidget):
    """Settings and configuration panel."""
    
    settings_changed = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """)
        
        scroll_content = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(THEME.padding_md, THEME.padding_md,
                                      THEME.padding_md, THEME.padding_md)
        main_layout.setSpacing(THEME.padding_lg)
        
        # Network Settings
        network_section = SettingsSection("Network Settings")
        network_layout = network_section.layout
        
        # Max threads
        threads_layout = QHBoxLayout()
        threads_label = QLabel("Max Threads:")
        threads_label.setStyleSheet(f"color: {THEME.text_primary};")
        threads_label.setMinimumWidth(150)
        self.threads_spin = QSpinBox()
        self.threads_spin.setMinimum(1)
        self.threads_spin.setMaximum(32)
        self.threads_spin.setValue(4)
        self.threads_spin.setStyleSheet(f"""
            QSpinBox {{
                background-color: {THEME.bg_card};
                border: 1px solid {THEME.border_color};
                padding: 6px;
                color: {THEME.text_primary};
            }}
        """)
        threads_layout.addWidget(threads_label)
        threads_layout.addWidget(self.threads_spin)
        threads_layout.addStretch()
        network_layout.addLayout(threads_layout)
        
        # Timeout setting
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("Request Timeout (s):")
        timeout_label.setStyleSheet(f"color: {THEME.text_primary};")
        timeout_label.setMinimumWidth(150)
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setMinimum(5)
        self.timeout_spin.setMaximum(300)
        self.timeout_spin.setValue(10)
        self.timeout_spin.setStyleSheet(self.threads_spin.styleSheet())
        timeout_layout.addWidget(timeout_label)
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        network_layout.addLayout(timeout_layout)
        
        # TOR settings
        tor_checkbox = QCheckBox("Enable TOR Support")
        tor_checkbox.setStyleSheet(f"color: {THEME.text_primary};")
        network_layout.addWidget(tor_checkbox)
        
        main_layout.addWidget(network_section)
        
        # Extraction Settings
        extraction_section = SettingsSection("Extraction Settings")
        extraction_layout = extraction_section.layout
        
        # Max pages
        pages_layout = QHBoxLayout()
        pages_label = QLabel("Max Pages per Session:")
        pages_label.setStyleSheet(f"color: {THEME.text_primary};")
        pages_label.setMinimumWidth(150)
        self.pages_spin = QSpinBox()
        self.pages_spin.setMinimum(1)
        self.pages_spin.setMaximum(10000)
        self.pages_spin.setValue(1000)
        self.pages_spin.setStyleSheet(self.threads_spin.styleSheet())
        pages_layout.addWidget(pages_label)
        pages_layout.addWidget(self.pages_spin)
        pages_layout.addStretch()
        extraction_layout.addLayout(pages_layout)
        
        # Max file size
        size_layout = QHBoxLayout()
        size_label = QLabel("Max File Size (MB):")
        size_label.setStyleSheet(f"color: {THEME.text_primary};")
        size_label.setMinimumWidth(150)
        self.size_spin = QSpinBox()
        self.size_spin.setMinimum(1)
        self.size_spin.setMaximum(10000)
        self.size_spin.setValue(100)
        self.size_spin.setStyleSheet(self.threads_spin.styleSheet())
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_spin)
        size_layout.addStretch()
        extraction_layout.addLayout(size_layout)
        
        # Crawl depth limit
        crawl_layout = QHBoxLayout()
        crawl_label = QLabel("Max Crawl Depth:")
        crawl_label.setStyleSheet(f"color: {THEME.text_primary};")
        crawl_label.setMinimumWidth(150)
        self.depth_spin = QSpinBox()
        self.depth_spin.setMinimum(1)
        self.depth_spin.setMaximum(100)
        self.depth_spin.setValue(10)
        self.depth_spin.setStyleSheet(self.threads_spin.styleSheet())
        crawl_layout.addWidget(crawl_label)
        crawl_layout.addWidget(self.depth_spin)
        crawl_layout.addStretch()
        extraction_layout.addLayout(crawl_layout)
        
        # Browser settings
        browser_checkbox = QCheckBox("Use Headless Browser for All Sites")
        browser_checkbox.setStyleSheet(f"color: {THEME.text_primary};")
        extraction_layout.addWidget(browser_checkbox)
        
        main_layout.addWidget(extraction_section)
        
        # UI Settings
        ui_section = SettingsSection("UI Settings")
        ui_layout = ui_section.layout
        
        # Theme selection
        theme_h_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet(f"color: {THEME.text_primary};")
        theme_label.setMinimumWidth(150)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light (Coming Soon)"])
        self.theme_combo.setEnabled(False)
        self.theme_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {THEME.bg_card};
                border: 1px solid {THEME.border_color};
                color: {THEME.text_primary};
                padding: 6px;
            }}
        """)
        theme_h_layout.addWidget(theme_label)
        theme_h_layout.addWidget(self.theme_combo)
        theme_h_layout.addStretch()
        ui_layout.addLayout(theme_h_layout)
        
        # Font scaling
        font_layout = QHBoxLayout()
        font_label = QLabel("Font Size:")
        font_label.setStyleSheet(f"color: {THEME.text_primary};")
        font_label.setMinimumWidth(150)
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Small", "Normal", "Large", "Extra Large"])
        self.font_combo.setCurrentIndex(1)
        self.font_combo.setStyleSheet(self.theme_combo.styleSheet())
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_combo)
        font_layout.addStretch()
        ui_layout.addLayout(font_layout)
        
        # Animation toggle
        animation_checkbox = QCheckBox("Enable UI Animations")
        animation_checkbox.setChecked(True)
        animation_checkbox.setStyleSheet(f"color: {THEME.text_primary};")
        ui_layout.addWidget(animation_checkbox)
        
        main_layout.addWidget(ui_section)
        
        # About section
        about_section = SettingsSection("About")
        about_layout = about_section.layout
        
        version_label = QLabel("Version: 1.0.0")
        version_label.setStyleSheet(f"color: {THEME.text_secondary};")
        about_layout.addWidget(version_label)
        
        author_label = QLabel("Made with ❤️ for web researchers")
        author_label.setStyleSheet(f"color: {THEME.text_secondary};")
        about_layout.addWidget(author_label)
        
        license_label = QLabel("Licensed under MIT License")
        license_label.setStyleSheet(f"color: {THEME.text_secondary};")
        about_layout.addWidget(license_label)
        
        main_layout.addWidget(about_section)
        main_layout.addStretch()
        
        # Save button
        save_btn = QPushButton("💾 Save Settings")
        save_btn.setMinimumHeight(44)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME.primary_accent};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {THEME.hover_accent};
            }}
        """)
        save_btn.clicked.connect(self._on_save_settings)
        main_layout.addWidget(save_btn)
        
        scroll_content.setLayout(main_layout)
        scroll.setWidget(scroll_content)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
    
    def _on_save_settings(self) -> None:
        """Save settings."""
        settings = {
            'max_threads': self.threads_spin.value(),
            'timeout': self.timeout_spin.value(),
            'max_pages': self.pages_spin.value(),
            'max_file_size_mb': self.size_spin.value(),
            'max_depth': self.depth_spin.value(),
        }
        
        self.settings_changed.emit(settings)
        print("Settings saved!")
