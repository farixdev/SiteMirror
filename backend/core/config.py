"""
Configuration management for SiteMirror.
"""

import json
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass, asdict
import os


@dataclass
class NetworkConfig:
    """Network configuration settings."""
    max_threads: int = 4
    timeout_seconds: int = 10
    max_retries: int = 3
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


@dataclass
class TORConfig:
    """TOR configuration."""
    enabled: bool = False
    socks_host: str = "127.0.0.1"
    socks_port: int = 9050
    control_host: str = "127.0.0.1"
    control_port: int = 9051
    password: str = ""


@dataclass
class ExtractionConfig:
    """Extraction configuration."""
    max_pages: int = 1000
    max_depth: int = 10
    max_file_size_mb: int = 100
    download_assets: bool = True
    respect_robots: bool = True
    use_headless_browser: bool = False
    detect_dynamic_content: bool = False
    save_cookies: bool = False


@dataclass
class UIConfig:
    """UI configuration."""
    theme: str = "dark"
    font_size: str = "normal"
    enable_animations: bool = True
    window_width: int = 1400
    window_height: int = 900


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_dir: str = "./config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "settings.json"
        
        self.network_config = NetworkConfig()
        self.tor_config = TORConfig()
        self.extraction_config = ExtractionConfig()
        self.ui_config = UIConfig()
        
        self.load()
    
    def load(self) -> None:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                
                # Load each config section
                if 'network' in data:
                    self.network_config = NetworkConfig(**data['network'])
                if 'tor' in data:
                    self.tor_config = TORConfig(**data['tor'])
                if 'extraction' in data:
                    self.extraction_config = ExtractionConfig(**data['extraction'])
                if 'ui' in data:
                    self.ui_config = UIConfig(**data['ui'])
            
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            data = {
                'network': asdict(self.network_config),
                'tor': asdict(self.tor_config),
                'extraction': asdict(self.extraction_config),
                'ui': asdict(self.ui_config),
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_dict(self) -> Dict[str, Any]:
        """Get all configuration as dictionary."""
        return {
            'network': asdict(self.network_config),
            'tor': asdict(self.tor_config),
            'extraction': asdict(self.extraction_config),
            'ui': asdict(self.ui_config),
        }


# Global config manager instance
_global_config_manager = None


def get_config_manager() -> ConfigManager:
    """Get or create global config manager."""
    global _global_config_manager
    
    if _global_config_manager is None:
        _global_config_manager = ConfigManager()
    
    return _global_config_manager
