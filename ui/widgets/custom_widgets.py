"""
Custom PySide6 widgets for SiteMirror UI.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QPushButton, QRadioButton, QCheckBox,
                              QButtonGroup, QFrame, QProgressBar)
from PySide6.QtCore import Qt, Signal, QTimer, QRectF
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QConicalGradient

from ui.styles.theme import THEME, get_log_color


class Card(QFrame):
    """Custom card widget for content containers."""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(THEME.padding_lg, THEME.padding_lg,
                                       THEME.padding_lg, THEME.padding_lg)
        self.layout.setSpacing(THEME.padding_md)
        
        if title:
            title_label = QLabel(title)
            title_font = QFont(THEME.font_family)
            title_font.setPointSize(THEME.font_heading)
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_label.setStyleSheet(f"color: {THEME.text_primary};")
            self.layout.addWidget(title_label)
        
        self.setLayout(self.layout)


class LabeledInput(QWidget):
    """Input field with label."""
    
    def __init__(self, label: str, placeholder: str = "", parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        label_widget = QLabel(label)
        label_font = QFont(THEME.font_family)
        label_font.setPointSize(THEME.font_small)
        label_widget.setFont(label_font)
        label_widget.setStyleSheet(f"color: {THEME.text_secondary};")
        
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setMinimumHeight(38)
        
        layout.addWidget(label_widget)
        layout.addWidget(self.input)
        
        self.setLayout(layout)
    
    def get_text(self) -> str:
        """Get input value."""
        return self.input.text()
    
    def set_text(self, text: str) -> None:
        """Set input value."""
        self.input.setText(text)


class RadioGroup(QWidget):
    """Styled radio button group."""
    
    changed = Signal(str)
    
    def __init__(self, label: str, options: list, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        label_widget = QLabel(label)
        label_font = QFont(THEME.font_family)
        label_font.setPointSize(THEME.font_small)
        label_widget.setFont(label_font)
        label_widget.setStyleSheet(f"color: {THEME.text_secondary};")
        layout.addWidget(label_widget)
        
        self.button_group = QButtonGroup()
        self.buttons = {}
        
        options_layout = QVBoxLayout()
        options_layout.setContentsMargins(0, 0, 0, 0)
        options_layout.setSpacing(6)
        
        for i, option in enumerate(options):
            btn = QRadioButton(option)
            self.button_group.addButton(btn, i)
            self.buttons[option] = btn
            options_layout.addWidget(btn)
            
            btn.toggled.connect(lambda checked, opt=option: 
                              self.changed.emit(opt) if checked else None)
        
        layout.addLayout(options_layout)
        self.setLayout(layout)
        
        # Set first option as default
        if options:
            self.buttons[options[0]].setChecked(True)
    
    def get_selected(self) -> str:
        """Get selected option."""
        for text, btn in self.buttons.items():
            if btn.isChecked():
                return text
        return None
    
    def set_selected(self, text: str) -> None:
        """Set selected option."""
        if text in self.buttons:
            self.buttons[text].setChecked(True)


class CheckboxGroup(QWidget):
    """Styled checkbox group."""
    
    changed = Signal(str, bool)
    
    def __init__(self, label: str, options: list, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        if label:
            label_widget = QLabel(label)
            label_font = QFont(THEME.font_family)
            label_font.setPointSize(THEME.font_small)
            label_widget.setFont(label_font)
            label_widget.setStyleSheet(f"color: {THEME.text_secondary};")
            layout.addWidget(label_widget)
        
        self.checkboxes = {}
        
        options_layout = QVBoxLayout()
        options_layout.setContentsMargins(0, 0, 0, 0)
        options_layout.setSpacing(6)
        
        for option in options:
            cb = QCheckBox(option)
            self.checkboxes[option] = cb
            options_layout.addWidget(cb)
            
            cb.toggled.connect(lambda checked, opt=option: 
                              self.changed.emit(opt, checked))
        
        layout.addLayout(options_layout)
        self.setLayout(layout)
    
    def get_checked(self) -> list:
        """Get all checked options."""
        return [text for text, cb in self.checkboxes.items() if cb.isChecked()]
    
    def set_checked(self, items: list) -> None:
        """Set checked options."""
        for text, cb in self.checkboxes.items():
            cb.setChecked(text in items)


class CTAButton(QPushButton):
    """Large call-to-action button."""
    
    def __init__(self, text: str = "Start", parent=None):
        super().__init__(text, parent)
        self.setObjectName("cta-button")
        self.setMinimumSize(180, 42)
        self.setCursor(Qt.PointingHandCursor)
        
        font = QFont(THEME.font_family)
        font.setPointSize(THEME.font_body)
        font.setBold(True)
        self.setFont(font)


class StopButton(QPushButton):
    """Stop extraction button."""
    
    def __init__(self, text: str = "Stop Extraction", parent=None):
        super().__init__(text, parent)
        self.setObjectName("stop-button")
        self.setMinimumSize(180, 42)
        self.setCursor(Qt.PointingHandCursor)
        
        font = QFont(THEME.font_family)
        font.setPointSize(THEME.font_body)
        font.setBold(True)
        self.setFont(font)


class CircularProgress(QWidget):
    """Custom circular progress indicator with gradient arc."""
    
    def __init__(self, size: int = 160, parent=None):
        super().__init__(parent)
        self._size = size
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
        
        self.progress = 0
        self._status_text = "Idle"
        
        # Timer for smooth animation
        self._target_progress = 0
        self._anim_timer = QTimer()
        self._anim_timer.timeout.connect(self._animate)
        self._anim_timer.setInterval(16)
    
    def set_progress(self, value: int, status: str = "") -> None:
        """Update progress with smooth animation."""
        self._target_progress = max(0, min(100, value))
        if status:
            self._status_text = status
        if not self._anim_timer.isActive():
            self._anim_timer.start()
    
    def _animate(self):
        """Smoothly animate toward target."""
        diff = self._target_progress - self.progress
        if abs(diff) < 0.5:
            self.progress = self._target_progress
            self._anim_timer.stop()
        else:
            self.progress += diff * 0.15
        self.update()
    
    def paintEvent(self, event):
        """Paint the circular progress indicator."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        s = self._size
        margin = 12
        rect = QRectF(margin, margin, s - 2 * margin, s - 2 * margin)
        
        # Background track
        bg_pen = QPen(QColor(THEME.border_color), 4)
        bg_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(rect, 0, 360 * 16)
        
        # Progress arc with gradient
        if self.progress > 0:
            gradient = QConicalGradient(rect.center(), 90)
            gradient.setColorAt(0, QColor(THEME.primary_accent))
            gradient.setColorAt(0.5, QColor("#A78BFA"))
            gradient.setColorAt(1, QColor(THEME.primary_accent))
            
            arc_pen = QPen(QColor(THEME.primary_accent), 5)
            arc_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(arc_pen)
            
            start_angle = 90 * 16
            span_angle = int(-(self.progress / 100 * 360) * 16)
            painter.drawArc(rect, start_angle, span_angle)
        
        # Center text - percentage
        painter.setPen(QColor(THEME.text_primary))
        pct_font = QFont(THEME.font_family, 22, QFont.Bold)
        painter.setFont(pct_font)
        pct_rect = QRectF(0, s * 0.28, s, 30)
        painter.drawText(pct_rect, Qt.AlignCenter, f"{int(self.progress)}%")
        
        # Status text
        painter.setPen(QColor(THEME.text_secondary))
        status_font = QFont(THEME.font_family, 8)
        painter.setFont(status_font)
        status_rect = QRectF(0, s * 0.55, s, 20)
        painter.drawText(status_rect, Qt.AlignCenter, self._status_text)
        
        painter.end()


class StatItem(QWidget):
    """Single statistics item with icon."""
    
    def __init__(self, icon: str, label: str, value: str = "0", parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Icon
        icon_label = QLabel(icon)
        icon_font = QFont(THEME.font_family)
        icon_font.setPointSize(12)
        icon_label.setFont(icon_font)
        icon_label.setStyleSheet("background-color: transparent;")
        
        # Text column
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(0)
        
        self.value_label = QLabel(value)
        value_font = QFont(THEME.font_family)
        value_font.setPointSize(12)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet(f"color: {THEME.text_primary}; background-color: transparent;")
        
        self.label = QLabel(label)
        label_font = QFont(THEME.font_family)
        label_font.setPointSize(THEME.font_small)
        self.label.setFont(label_font)
        self.label.setStyleSheet(f"color: {THEME.text_secondary}; background-color: transparent;")
        
        text_layout.addWidget(self.value_label)
        text_layout.addWidget(self.label)
        
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def set_value(self, value: str) -> None:
        """Update value."""
        self.value_label.setText(value)
