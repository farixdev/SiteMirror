"""
TOR connection manager and utilities.
"""

import socket
import subprocess
import platform
from typing import Optional, Tuple
from pathlib import Path

from backend.logs.logger import get_logger
from backend.core.proxy import TORConfig, ProxyManager


class TORConnectionManager:
    """Manages TOR connection and connectivity."""
    
    def __init__(self):
        self.logger = get_logger()
        self.tor_config = TORConfig()
        self.is_connected = False
        self.tor_process = None
    
    def test_connection(self, host: str = "127.0.0.1", 
                       port: int = 9050, timeout: int = 2) -> Tuple[bool, str]:
        """Test TOR SOCKS proxy connection."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                self.is_connected = True
                message = f"Successfully connected to TOR at {host}:{port}"
                self.logger.success(message)
                return True, message
            else:
                self.is_connected = False
                message = f"Failed to connect to TOR at {host}:{port}"
                self.logger.error(message)
                return False, message
        
        except Exception as e:
            self.is_connected = False
            message = f"TOR connection error: {str(e)}"
            self.logger.error(message)
            return False, message
    
    def test_tor_circuit(self, proxy_url: str = "socks5://127.0.0.1:9050") -> Tuple[bool, Optional[str]]:
        """Test TOR circuit by fetching IP address."""
        try:
            import aiohttp
            import asyncio
            
            async def _test():
                try:
                    connector = aiohttp.TCPConnector()
                    timeout = aiohttp.ClientTimeout(total=10)
                    
                    async with aiohttp.ClientSession(
                        connector=connector,
                        timeout=timeout
                    ) as session:
                        async with session.get(
                            "https://api.ipify.org?format=json",
                            proxy=proxy_url,
                            ssl=False
                        ) as response:
                            data = await response.json()
                            return data.get('ip')
                except Exception as e:
                    self.logger.error(f"TOR circuit test failed: {str(e)}")
                    return None
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            ip = loop.run_until_complete(_test())
            loop.close()
            
            if ip:
                self.logger.success(f"TOR circuit active. Exit IP: {ip}")
                return True, ip
            else:
                self.logger.error("Failed to get TOR exit IP")
                return False, None
        
        except Exception as e:
            self.logger.error(f"TOR circuit test error: {str(e)}")
            return False, None
    
    def get_tor_executable(self) -> Optional[Path]:
        """Find Tor executable on system."""
        system = platform.system()
        
        possible_paths = []
        
        if system == "Windows":
            possible_paths = [
                Path("C:/Program Files/Tor/tor.exe"),
                Path("C:/Program Files (x86)/Tor/tor.exe"),
                Path(Path.home() / "AppData/Local/Tor/tor.exe"),
            ]
        elif system == "Darwin":  # macOS
            possible_paths = [
                Path("/usr/local/bin/tor"),
                Path("/opt/homebrew/bin/tor"),
            ]
        else:  # Linux
            possible_paths = [
                Path("/usr/bin/tor"),
                Path("/usr/local/bin/tor"),
            ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def start_tor(self) -> bool:
        """Attempt to start Tor service (if not running)."""
        try:
            # First check if already running
            connected, _ = self.test_connection()
            if connected:
                self.logger.info("Tor is already running")
                return True
            
            tor_path = self.get_tor_executable()
            
            if not tor_path:
                self.logger.warning("Tor executable not found. Install Tor to use onion sites.")
                return False
            
            self.logger.info(f"Starting Tor from {tor_path}...")
            
            # Start Tor process
            self.tor_process = subprocess.Popen(
                [str(tor_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a moment for Tor to start
            import time
            time.sleep(3)
            
            # Test connection
            connected, msg = self.test_connection()
            if connected:
                self.logger.success("Tor started successfully")
                return True
            else:
                self.logger.error(f"Tor failed to start: {msg}")
                return False
        
        except Exception as e:
            self.logger.error(f"Error starting Tor: {str(e)}")
            return False
    
    def stop_tor(self) -> None:
        """Stop Tor process if we started it."""
        if self.tor_process:
            try:
                self.tor_process.terminate()
                self.tor_process.wait(timeout=5)
                self.is_connected = False
                self.logger.info("Tor stopped")
            except Exception as e:
                self.logger.error(f"Error stopping Tor: {str(e)}")
    
    def is_tor_available(self) -> bool:
        """Check if Tor is available and running."""
        connected, _ = self.test_connection()
        return connected


# Global TOR manager
_global_tor_manager = None


def get_tor_manager() -> TORConnectionManager:
    """Get or create global TOR manager."""
    global _global_tor_manager
    
    if _global_tor_manager is None:
        _global_tor_manager = TORConnectionManager()
    
    return _global_tor_manager
