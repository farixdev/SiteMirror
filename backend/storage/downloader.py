"""
File storage and download management.
Handles saving extracted content and assets.
"""

import os
import asyncio
import aiohttp
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
import mimetypes

from backend.logs.logger import get_logger


class StorageManager:
    """Manages file storage for extracted content."""
    
    def __init__(self, base_path: str = "./data/extractions"):
        self.base_path = Path(base_path)
        self.logger = get_logger()
        self.bytes_written = 0
        self.files_saved = 0
    
    def create_session_directory(self, domain: str) -> Path:
        """Create a directory for a new extraction session."""
        # Create domain-specific folder
        timestamp = __import__('datetime').datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        session_dir = self.base_path / domain / timestamp
        
        try:
            session_dir.mkdir(parents=True, exist_ok=True)
            self.logger.success(f"Created session directory: {session_dir}")
            return session_dir
        except Exception as e:
            self.logger.error(f"Failed to create directory {session_dir}: {str(e)}")
            return None
    
    def _get_safe_filename(self, url: str) -> str:
        """Convert URL to safe filename."""
        parsed = urlparse(url)
        path = parsed.path
        
        # Get filename from path
        filename = path.split('/')[-1]
        
        if not filename or filename == '':
            filename = 'index.html'
        
        # Remove unsafe characters
        filename = "".join(c for c in filename if c.isalnum() or c in '.-_')
        
        if not filename:
            filename = 'file.html'
        
        return filename
    
    async def download_file(self, url: str, save_dir: Path,
                           proxy_url: Optional[str] = None,
                           user_agent: str = None) -> bool:
        """Download a file asynchronously."""
        try:
            filename = self._get_safe_filename(url)
            file_path = save_dir / filename
            
            headers = {
                'User-Agent': user_agent or 'Mozilla/5.0'
            }
            
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(
                    url,
                    headers=headers,
                    proxy=proxy_url,
                    ssl=False,
                    allow_redirects=True
                ) as response:
                    if response.status == 200:
                        content = await response.read()
                        
                        with open(file_path, 'wb') as f:
                            f.write(content)
                        
                        self.files_saved += 1
                        self.bytes_written += len(content)
                        
                        self.logger.success(f"✓ Saved {filename} ({len(content)} bytes)")
                        return True
                    else:
                        self.logger.warning(f"Failed to download {url}: {response.status}")
                        return False
        
        except Exception as e:
            self.logger.error(f"Error downloading {url}: {str(e)}")
            return False
    
    def save_html_content(self, content: str, filename: str, 
                         save_dir: Path) -> bool:
        """Save HTML content to file."""
        try:
            file_path = save_dir / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.files_saved += 1
            self.bytes_written += len(content.encode('utf-8'))
            
            self.logger.success(f"✓ Saved {filename}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error saving {filename}: {str(e)}")
            return False
    
    def get_storage_stats(self) -> dict:
        """Get storage statistics."""
        return {
            'files_saved': self.files_saved,
            'bytes_written': self.bytes_written,
            'mb_written': round(self.bytes_written / (1024 * 1024), 2)
        }
    
    def get_directory_size(self, path: Path) -> int:
        """Calculate total size of directory."""
        total = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total += os.path.getsize(filepath)
        except Exception:
            pass
        
        return total


# Global storage manager instance
_global_storage_manager = None


def get_storage_manager(base_path: str = "./data/extractions") -> StorageManager:
    """Get or create the global storage manager."""
    global _global_storage_manager
    
    if _global_storage_manager is None:
        _global_storage_manager = StorageManager(base_path)
    
    return _global_storage_manager
