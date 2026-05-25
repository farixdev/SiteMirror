"""
Extraction manager - orchestrates the entire extraction process.
"""

import asyncio
import threading
import time
from typing import Optional, Dict, List, Callable
from datetime import datetime
from pathlib import Path

from backend.logs.logger import get_logger, LogEntry
from backend.core.crawler import Crawler, ExtractionConfig
from backend.storage.downloader import get_storage_manager


class ExtractionSession:
    """Represents a single extraction session."""
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.status = "initialized"
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.result: Optional[Dict] = None
        self.error: Optional[str] = None
        self.progress = 0
        
        # Live tracking
        self.pages_crawled = 0
        self.files_downloaded = 0
        self.total_bytes = 0
        self.current_url = ""
        self.pages_found = 0
    
    def get_elapsed_str(self) -> str:
        """Get formatted elapsed time."""
        if not self.start_time:
            return "00:00:00"
        end = self.end_time or time.time()
        elapsed = end - self.start_time
        h = int(elapsed // 3600)
        m = int((elapsed % 3600) // 60)
        s = int(elapsed % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    
    def get_size_str(self) -> str:
        """Get formatted total size."""
        if self.total_bytes < 1024:
            return f"{self.total_bytes} B"
        elif self.total_bytes < 1024 * 1024:
            return f"{self.total_bytes / 1024:.1f} KB"
        else:
            return f"{self.total_bytes / (1024 * 1024):.1f} MB"
    
    def __repr__(self) -> str:
        return f"ExtractionSession({self.session_id}, {self.config.url})"


class ExtractionManager:
    """
    Manages extraction sessions and coordinates all components.
    """
    
    def __init__(self):
        self.logger = get_logger()
        self.storage = get_storage_manager()
        
        self.current_session: Optional[ExtractionSession] = None
        self.sessions_history: Dict[str, ExtractionSession] = {}
        self.is_extracting = False
        self._stop_requested = False
        
        self.progress_callbacks: List[Callable] = []
        self.status_callbacks: List[Callable] = []
        self.finish_callbacks: List[Callable] = []
    
    def add_progress_callback(self, callback) -> None:
        """Register callback for progress updates."""
        self.progress_callbacks.append(callback)
    
    def add_status_callback(self, callback) -> None:
        """Register callback for status changes."""
        self.status_callbacks.append(callback)
    
    def add_finish_callback(self, callback) -> None:
        """Register callback for extraction completion."""
        self.finish_callbacks.append(callback)
    
    def _notify_progress(self, progress: int) -> None:
        """Notify progress listeners."""
        for callback in self.progress_callbacks:
            try:
                callback(progress)
            except Exception:
                pass
    
    def _notify_status(self, status: str) -> None:
        """Notify status listeners."""
        for callback in self.status_callbacks:
            try:
                callback(status)
            except Exception:
                pass
    
    def _notify_finish(self, result: dict) -> None:
        """Notify finish listeners."""
        for callback in self.finish_callbacks:
            try:
                callback(result)
            except Exception:
                pass
    
    def get_live_stats(self) -> dict:
        """Get live stats for UI updates."""
        if not self.current_session:
            return {}
        
        session = self.current_session
        elapsed = 0
        speed = "0 B/s"
        
        if session.start_time:
            elapsed = time.time() - session.start_time
            if elapsed > 0:
                bps = session.total_bytes / elapsed
                if bps < 1024:
                    speed = f"{bps:.0f} B/s"
                elif bps < 1024 * 1024:
                    speed = f"{bps / 1024:.1f} KB/s"
                else:
                    speed = f"{bps / (1024 * 1024):.2f} MB/s"
        
        return {
            'pages_crawled': session.pages_crawled,
            'files_downloaded': session.files_downloaded,
            'total_pages': session.pages_found,
            'total_files': session.files_downloaded,
            'total_size': session.get_size_str(),
            'speed': speed,
            'elapsed': session.get_elapsed_str(),
            'current_url': session.current_url,
            'start_time': datetime.fromtimestamp(session.start_time).strftime("%H:%M:%S") if session.start_time else "—",
            'eta': "—",
        }
    
    def start_extraction(self, config: ExtractionConfig) -> Optional[ExtractionSession]:
        """Start a new extraction session."""
        if self.is_extracting:
            self.logger.warning("Extraction already in progress")
            return None
        
        self.is_extracting = True
        self._stop_requested = False
        session = ExtractionSession(config)
        self.current_session = session
        self.sessions_history[session.session_id] = session
        
        session.start_time = time.time()
        session.status = "running"
        
        self.logger.info(f"Starting extraction session: {session.session_id}")
        self._notify_status("active")
        
        # Run extraction in separate thread
        thread = threading.Thread(
            target=self._run_extraction,
            args=(session, config),
            daemon=True
        )
        thread.start()
        
        return session
    
    def _run_extraction(self, session: ExtractionSession,
                       config: ExtractionConfig) -> None:
        """Run extraction in background thread."""
        try:
            # Create storage directory
            domain = config.get_base_domain()
            session_dir = self.storage.create_session_directory(domain)
            
            if not session_dir:
                raise Exception("Failed to create session directory")
            
            # Run the crawler
            crawler = Crawler(config)
            
            # Set up progress callback on crawler
            def on_page_done(page_data):
                if self._stop_requested:
                    return
                    
                session.pages_crawled = crawler.total_pages
                session.pages_found = len(crawler.visited_urls) + len(getattr(crawler, '_to_visit', []))
                session.total_bytes = crawler.total_size
                session.current_url = page_data.get('url', '')
                session.files_downloaded = crawler.total_assets_downloaded
                
                # Calculate progress
                if config.depth.value == 'single':
                    progress = min(95, int(session.pages_crawled / 1 * 90))
                else:
                    total_expected = max(session.pages_found, session.pages_crawled, 1)
                    progress = min(95, int(session.pages_crawled / total_expected * 90))
                
                session.progress = progress
                self._notify_progress(progress)
            
            crawler.on_page_done = on_page_done
            
            # Run async crawler
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(crawler.extract())
            finally:
                loop.close()
            
            # Save extracted content
            if result and 'pages' in result:
                for page in result['pages']:
                    if page.content and not page.error:
                        filename = self.storage._get_safe_filename(page.url)
                        self.storage.save_html_content(page.content, filename, session_dir)
                        session.files_downloaded += 1
                
                # Download assets
                if config.download_assets and result.get('assets'):
                    asset_dir = session_dir / "assets"
                    asset_dir.mkdir(exist_ok=True)
                    
                    asset_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(asset_loop)
                    try:
                        for asset in result['assets'][:50]:  # Limit assets
                            if self._stop_requested:
                                break
                            try:
                                asset_loop.run_until_complete(
                                    self.storage.download_file(
                                        asset['url'], asset_dir,
                                        user_agent=config.user_agent
                                    )
                                )
                                session.files_downloaded += 1
                            except Exception:
                                pass
                    finally:
                        asset_loop.close()
            
            session.result = result
            session.status = "completed"
            session.progress = 100
            session.total_bytes = crawler.total_size + self.storage.bytes_written
            
            self.logger.success(f"Extraction completed: {session.pages_crawled} pages, {session.files_downloaded} files saved")
            self._notify_progress(100)
            
            # Build final result
            final_result = {
                'total_pages': session.pages_crawled,
                'files_saved': session.files_downloaded,
                'total_size_str': session.get_size_str(),
                'elapsed_str': session.get_elapsed_str(),
                'url': config.url,
                'depth': config.depth.value,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'error': None,
            }
            self._notify_finish(final_result)
        
        except Exception as e:
            session.status = "failed"
            session.error = str(e)
            self.logger.error(f"Extraction failed: {str(e)}")
            
            self._notify_finish({
                'total_pages': session.pages_crawled,
                'files_saved': session.files_downloaded,
                'total_size_str': session.get_size_str(),
                'elapsed_str': session.get_elapsed_str(),
                'url': config.url,
                'depth': config.depth.value,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'error': str(e),
            })
        
        finally:
            session.end_time = time.time()
            self.is_extracting = False
            self._notify_status("idle")
    
    def stop_extraction(self) -> None:
        """Stop current extraction."""
        self._stop_requested = True
        if self.current_session:
            self.current_session.status = "stopped"
            self.current_session.end_time = time.time()
            self.is_extracting = False
            self.logger.warning("Extraction stopped by user")
            self._notify_status("idle")
    
    def get_session_history(self) -> Dict[str, ExtractionSession]:
        """Get all extraction sessions."""
        return self.sessions_history


# Global extraction manager
_global_extraction_manager = None


def get_extraction_manager() -> ExtractionManager:
    """Get or create the global extraction manager."""
    global _global_extraction_manager
    
    if _global_extraction_manager is None:
        _global_extraction_manager = ExtractionManager()
    
    return _global_extraction_manager
