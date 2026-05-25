"""
SiteMirror theme and styling system.
Defines colors, fonts, and stylesheet configuration.
"""

from dataclasses import dataclass


@dataclass
class Theme:
    """Application theme configuration."""
    
    # Background colors
    bg_primary: str = "#0D0F1A"
    bg_secondary: str = "#111428"
    bg_card: str = "#151933"
    bg_input: str = "#0B0D18"
    bg_terminal: str = "#050811"
    
    # Sidebar
    sidebar_bg: str = "#0E1128"
    sidebar_active: str = "rgba(124, 77, 255, 0.15)"
    
    # Border and accents
    border_color: str = "#1E2240"
    primary_accent: str = "#7C4DFF"
    hover_accent: str = "#9B6DFF"
    green_accent: str = "#00C853"
    
    # Status colors
    success: str = "#22C55E"
    warning: str = "#F59E0B"
    error: str = "#EF4444"
    info_blue: str = "#60A5FA"
    
    # Text colors
    text_primary: str = "#E8EAED"
    text_secondary: str = "#8B8FA3"
    text_muted: str = "#555873"
    text_accent: str = "#7C4DFF"
    
    # Log colors
    log_blue: str = "#60A5FA"
    log_green: str = "#22C55E"
    log_yellow: str = "#F59E0B"
    log_red: str = "#EF4444"
    log_cyan: str = "#22D3EE"
    
    # Dimensions
    sidebar_width: int = 200
    status_bar_height: int = 36
    padding_xl: int = 24
    padding_lg: int = 20
    padding_md: int = 14
    padding_sm: int = 8
    
    # Border radius
    radius_lg: int = 14
    radius_md: int = 10
    radius_sm: int = 6
    
    # Fonts
    font_family: str = "Segoe UI"
    font_mono: str = "Consolas"
    
    # Font sizes (pt)
    font_title: int = 20
    font_heading: int = 14
    font_body: int = 10
    font_logs: int = 9
    font_small: int = 9


# Global theme instance
THEME = Theme()


def get_stylesheet() -> str:
    """Generate complete stylesheet for the application."""
    return f"""
    /* === Global === */
    QMainWindow {{
        background-color: {THEME.bg_primary};
    }}
    
    QWidget {{
        background-color: {THEME.bg_primary};
        color: {THEME.text_primary};
        font-family: '{THEME.font_family}';
        font-size: {THEME.font_body}pt;
    }}
    
    /* === Sidebar === */
    #sidebar {{
        background-color: {THEME.sidebar_bg};
        border-right: 1px solid {THEME.border_color};
        min-width: {THEME.sidebar_width}px;
        max-width: {THEME.sidebar_width}px;
    }}
    
    /* === Cards === */
    #card {{
        background-color: {THEME.bg_card};
        border: 1px solid {THEME.border_color};
        border-radius: {THEME.radius_lg}px;
    }}
    
    /* === Input fields === */
    QLineEdit {{
        background-color: {THEME.bg_input};
        border: 1px solid {THEME.border_color};
        border-radius: {THEME.radius_sm}px;
        color: {THEME.text_primary};
        padding: 8px 12px;
        font-size: {THEME.font_body}pt;
        selection-background-color: {THEME.primary_accent};
    }}
    
    QLineEdit:focus {{
        border: 1px solid {THEME.primary_accent};
    }}
    
    QLineEdit::placeholder {{
        color: {THEME.text_muted};
    }}
    
    /* === Radio buttons === */
    QRadioButton {{
        color: {THEME.text_primary};
        spacing: 6px;
        font-size: {THEME.font_body}pt;
    }}
    
    QRadioButton::indicator {{
        width: 16px;
        height: 16px;
        border-radius: 8px;
        border: 2px solid {THEME.border_color};
        background-color: transparent;
    }}
    
    QRadioButton::indicator:hover {{
        border: 2px solid {THEME.primary_accent};
    }}
    
    QRadioButton::indicator:checked {{
        background-color: {THEME.primary_accent};
        border: 2px solid {THEME.primary_accent};
    }}
    
    /* === Checkboxes === */
    QCheckBox {{
        color: {THEME.text_primary};
        spacing: 6px;
        font-size: {THEME.font_body}pt;
    }}
    
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border-radius: 3px;
        border: 2px solid {THEME.border_color};
        background-color: transparent;
    }}
    
    QCheckBox::indicator:hover {{
        border: 2px solid {THEME.primary_accent};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {THEME.primary_accent};
        border: 2px solid {THEME.primary_accent};
    }}
    
    /* === Buttons === */
    QPushButton {{
        background-color: transparent;
        border: none;
        color: {THEME.text_secondary};
        padding: 8px 14px;
        text-align: left;
        border-radius: {THEME.radius_sm}px;
        font-size: {THEME.font_body}pt;
    }}
    
    QPushButton:hover {{
        background-color: rgba(124, 77, 255, 0.08);
        color: {THEME.text_primary};
    }}
    
    /* === CTA Button === */
    #cta-button {{
        background-color: {THEME.green_accent};
        color: white;
        border: none;
        border-radius: {THEME.radius_sm}px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: {THEME.font_body}pt;
    }}
    
    #cta-button:hover {{
        background-color: #00E676;
    }}
    
    #cta-button:disabled {{
        background-color: {THEME.text_muted};
        color: {THEME.bg_primary};
    }}
    
    /* === Stop Button === */
    #stop-button {{
        background-color: transparent;
        color: {THEME.error};
        border: 1px solid {THEME.error};
        border-radius: {THEME.radius_sm}px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: {THEME.font_body}pt;
    }}
    
    #stop-button:hover {{
        background-color: rgba(239, 68, 68, 0.15);
    }}
    
    /* === Status bar === */
    #statusBar {{
        background-color: {THEME.bg_secondary};
        border-top: 1px solid {THEME.border_color};
        padding: 4px 12px;
        min-height: {THEME.status_bar_height}px;
    }}
    
    #statusBar QLabel {{
        background-color: transparent;
        font-size: {THEME.font_small}pt;
    }}
    
    /* === Log viewer === */
    #logViewer {{
        background-color: {THEME.bg_terminal};
        color: {THEME.text_primary};
        font-family: '{THEME.font_mono}';
        font-size: {THEME.font_logs}pt;
        border: 1px solid {THEME.border_color};
        border-radius: {THEME.radius_sm}px;
        padding: 8px;
    }}
    
    /* === Scroll bars === */
    QScrollBar:vertical {{
        background-color: {THEME.bg_primary};
        width: 8px;
        border: none;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {THEME.border_color};
        border-radius: 4px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {THEME.text_muted};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        border: none;
        background: none;
        height: 0;
    }}
    
    QScrollBar:horizontal {{
        background-color: {THEME.bg_primary};
        height: 8px;
        border: none;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {THEME.border_color};
        border-radius: 4px;
        min-width: 20px;
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        border: none;
        background: none;
        width: 0;
    }}
    
    /* === Progress bar === */
    QProgressBar {{
        background-color: {THEME.bg_input};
        border: 1px solid {THEME.border_color};
        border-radius: 4px;
        text-align: center;
        color: {THEME.text_primary};
        height: 10px;
        font-size: 8pt;
    }}
    
    QProgressBar::chunk {{
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {THEME.primary_accent},
            stop:1 #A78BFA
        );
        border-radius: 3px;
    }}
    
    /* === Spinbox === */
    QSpinBox {{
        background-color: {THEME.bg_input};
        border: 1px solid {THEME.border_color};
        border-radius: {THEME.radius_sm}px;
        padding: 4px 8px;
        color: {THEME.text_primary};
        font-size: {THEME.font_body}pt;
    }}
    
    QSpinBox::up-button, QSpinBox::down-button {{
        background-color: transparent;
        border: none;
    }}
    
    /* === ComboBox === */
    QComboBox {{
        background-color: {THEME.bg_input};
        border: 1px solid {THEME.border_color};
        color: {THEME.text_primary};
        padding: 4px 8px;
        border-radius: {THEME.radius_sm}px;
        font-size: {THEME.font_body}pt;
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {THEME.bg_card};
        border: 1px solid {THEME.border_color};
        color: {THEME.text_primary};
        selection-background-color: {THEME.primary_accent};
    }}
    
    /* === Tooltip === */
    QToolTip {{
        background-color: {THEME.bg_card};
        color: {THEME.text_primary};
        border: 1px solid {THEME.border_color};
        padding: 4px 8px;
        border-radius: 4px;
        font-size: {THEME.font_small}pt;
    }}
    """


def get_log_color(log_level: str) -> str:
    """Get color for log level."""
    colors = {
        "INFO": THEME.text_primary,
        "SUCCESS": THEME.log_green,
        "WARNING": THEME.log_yellow,
        "ERROR": THEME.log_red,
        "NETWORK": THEME.log_cyan,
        "DEBUG": THEME.text_secondary,
    }
    return colors.get(log_level, THEME.text_primary)
