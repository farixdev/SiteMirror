"""
TOR proxy and network configuration support.
Handles TOR connection setup and proxy management.
"""

import socket
from typing import Optional, Tuple
from enum import Enum


class ProxyType(Enum):
    """Proxy types supported."""
    NONE = "none"
    HTTP = "http"
    SOCKS5 = "socks5"
    TOR = "tor"


class ProxyConfig:
    """Configuration for proxy settings."""
    
    def __init__(self, proxy_type: ProxyType = ProxyType.NONE,
                 host: str = "127.0.0.1", port: int = 9050):
        self.proxy_type = proxy_type
        self.host = host
        self.port = port
        self.username: Optional[str] = None
        self.password: Optional[str] = None
    
    def is_enabled(self) -> bool:
        """Check if proxy is enabled."""
        return self.proxy_type != ProxyType.NONE
    
    def get_socks_proxy(self) -> Tuple[str, int]:
        """Get SOCKS proxy address."""
        return (self.host, self.port)
    
    def get_aiohttp_proxy_url(self) -> str:
        """Get proxy URL for aiohttp."""
        if not self.is_enabled():
            return None
        
        if self.proxy_type == ProxyType.HTTP:
            return f"http://{self.host}:{self.port}"
        elif self.proxy_type in (ProxyType.SOCKS5, ProxyType.TOR):
            return f"socks5://{self.host}:{self.port}"
        
        return None
    
    def get_requests_proxy(self) -> dict:
        """Get proxy dict for requests library."""
        if not self.is_enabled():
            return {}
        
        proxy_url = self.get_aiohttp_proxy_url()
        if proxy_url:
            return {
                'http': proxy_url,
                'https': proxy_url
            }
        
        return {}


class TORConfig(ProxyConfig):
    """TOR-specific proxy configuration."""
    
    def __init__(self, tor_host: str = "127.0.0.1", 
                 tor_port: int = 9050, control_port: int = 9051):
        super().__init__(proxy_type=ProxyType.TOR, 
                        host=tor_host, port=tor_port)
        self.control_port = control_port
        self.is_connected = False
    
    def test_connection(self) -> bool:
        """Test TOR connection."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.host, self.port))
            sock.close()
            self.is_connected = result == 0
            return self.is_connected
        except Exception:
            self.is_connected = False
            return False


class ProxyManager:
    """Manages proxy configuration for the extraction engine."""
    
    def __init__(self):
        self.current_proxy = ProxyConfig(ProxyType.NONE)
        self.tor_config: Optional[TORConfig] = None
    
    def set_no_proxy(self) -> None:
        """Disable proxy."""
        self.current_proxy = ProxyConfig(ProxyType.NONE)
    
    def set_http_proxy(self, host: str, port: int) -> None:
        """Set HTTP proxy."""
        self.current_proxy = ProxyConfig(ProxyType.HTTP, host, port)
    
    def set_socks5_proxy(self, host: str, port: int) -> None:
        """Set SOCKS5 proxy."""
        self.current_proxy = ProxyConfig(ProxyType.SOCKS5, host, port)
    
    def set_tor_proxy(self, host: str = "127.0.0.1", 
                     port: int = 9050, control_port: int = 9051) -> bool:
        """Set TOR proxy and test connection."""
        self.tor_config = TORConfig(host, port, control_port)
        
        if self.tor_config.test_connection():
            self.current_proxy = self.tor_config
            return True
        else:
            return False
    
    def is_using_tor(self) -> bool:
        """Check if currently using TOR."""
        return isinstance(self.current_proxy, TORConfig)
    
    def get_current_proxy(self) -> ProxyConfig:
        """Get current proxy configuration."""
        return self.current_proxy


# Global proxy manager instance
_global_proxy_manager = ProxyManager()


def get_proxy_manager() -> ProxyManager:
    """Get the global proxy manager."""
    return _global_proxy_manager
