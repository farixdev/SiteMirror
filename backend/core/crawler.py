"""
Main crawler engine for website extraction.
Handles URL fetching, parsing, and link extraction.
"""

import asyncio
import aiohttp
from typing import Set, List, Optional, Dict
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from enum import Enum

from backend.logs.logger import get_logger, LogLevel
from backend.core.proxy import get_proxy_manager


class ExtractionDepth(Enum):
    """Crawl depth options."""
    SINGLE_PAGE = "single"
    SAME_DOMAIN = "same_domain"
    RECURSIVE = "recursive"


class ExtractionMode(Enum):
    """Type of website."""
    CLEARNET = "clearnet"
    ONION = "onion"


@dataclass
class ExtractionConfig:
    """Configuration for extraction session."""
    url: str
    mode: ExtractionMode = ExtractionMode.CLEARNET
    depth: ExtractionDepth = ExtractionDepth.SINGLE_PAGE
    download_assets: bool = True
    download_media: bool = False
    extract_links: bool = True
    respect_robots: bool = True
    use_headless_browser: bool = False
    detect_dynamic_content: bool = False
    save_cookies: bool = False
    max_threads: int = 4
    timeout: int = 10
    user_agent: Optional[str] = None
    max_pages: int = 1000
    max_file_size_mb: int = 100
    allowed_extensions: List[str] = field(default_factory=lambda: [
        'html', 'css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'svg',
        'pdf', 'zip', 'tar', 'gz', 'txt', 'json'
    ])
    
    def get_base_domain(self) -> str:
        """Extract base domain from URL."""
        parsed = urlparse(self.url)
        return parsed.netloc


@dataclass
class ExtractedPage:
    """Represents an extracted page."""
    url: str
    title: Optional[str] = None
    status_code: int = 0
    content: str = ""
    links: List[str] = field(default_factory=list)
    assets: List[Dict] = field(default_factory=list)
    error: Optional[str] = None


class Crawler:
    """
    Async crawler for website extraction.
    """
    
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.logger = get_logger()
        self.proxy_manager = get_proxy_manager()
        
        self.visited_urls: Set[str] = set()
        self.extracted_pages: List[ExtractedPage] = []
        self.failed_urls: List[str] = []
        
        self.total_pages = 0
        self.total_size = 0
        self.start_time = None
        self.current_speed = 0
        
        self._setup_user_agent()
    
    def _setup_user_agent(self) -> None:
        """Setup user agent string."""
        if not self.config.user_agent:
            self.config.user_agent = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid for extraction."""
        try:
            parsed = urlparse(url)
            
            # Must have scheme
            if not parsed.scheme:
                return False
            
            # Check depth restriction
            if self.config.depth == ExtractionDepth.SAME_DOMAIN:
                base_domain = self.config.get_base_domain()
                if parsed.netloc != base_domain:
                    return False
            
            return True
        except Exception:
            return False
    
    def _is_allowed_extension(self, url: str) -> bool:
        """Check if file extension is allowed."""
        try:
            parsed = urlparse(url)
            path = parsed.path.lower()
            
            for ext in self.config.allowed_extensions:
                if path.endswith(f".{ext}"):
                    return True
            
            # If no extension, likely HTML
            if '.' not in path.split('/')[-1]:
                return True
            
            return False
        except Exception:
            return True
    
    async def _fetch_page(self, session: aiohttp.ClientSession, 
                         url: str) -> ExtractedPage:
        """Fetch a single page asynchronously."""
        page = ExtractedPage(url=url)
        
        try:
            headers = {
                'User-Agent': self.config.user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            proxy = self.proxy_manager.get_current_proxy()
            proxy_url = proxy.get_aiohttp_proxy_url() if proxy.is_enabled() else None
            
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            
            async with session.get(
                url, 
                headers=headers,
                proxy=proxy_url,
                timeout=timeout,
                ssl=False,
                allow_redirects=True
            ) as response:
                page.status_code = response.status
                
                if response.status == 200:
                    page.content = await response.text(errors='replace')
                    self.logger.success(f"✓ Fetched {url}")
                    
                    # Parse links and assets
                    self._parse_content(page)
                else:
                    self.logger.warning(f"✗ Status {response.status} for {url}")
        
        except asyncio.TimeoutError:
            page.error = "Timeout"
            self.logger.error(f"Timeout fetching {url}")
        except Exception as e:
            page.error = str(e)
            self.logger.error(f"Error fetching {url}: {str(e)}")
        
        return page
    
    def _parse_content(self, page: ExtractedPage) -> None:
        """Parse HTML content for links and assets."""
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                page.title = title_tag.get_text(strip=True)
            
            # Extract links
            if self.config.extract_links and self.config.depth != ExtractionDepth.SINGLE_PAGE:
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(page.url, href)
                    
                    if self._is_valid_url(absolute_url) and absolute_url not in self.visited_urls:
                        page.links.append(absolute_url)
                        self.logger.network(f"Found link: {absolute_url}")
            
            # Extract assets
            if self.config.download_assets:
                for img in soup.find_all('img', src=True):
                    src = urljoin(page.url, img['src'])
                    if self._is_allowed_extension(src):
                        page.assets.append({'type': 'image', 'url': src})
                
                for script in soup.find_all('script', src=True):
                    src = urljoin(page.url, script['src'])
                    if self._is_allowed_extension(src):
                        page.assets.append({'type': 'script', 'url': src})
                
                for link in soup.find_all('link', href=True):
                    href = urljoin(page.url, link['href'])
                    if self._is_allowed_extension(href):
                        page.assets.append({'type': 'stylesheet', 'url': href})
        
        except Exception as e:
            self.logger.error(f"Error parsing content from {page.url}: {str(e)}")
    
    async def extract(self) -> Dict:
        """Main extraction method."""
        import time
        self.start_time = time.time()
        
        self.logger.info(f"Starting extraction of {self.config.url}")
        self.logger.network(f"Mode: {self.config.mode.value} | Depth: {self.config.depth.value}")
        
        connector = aiohttp.TCPConnector(limit=self.config.max_threads)
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        ) as session:
            # Start with the main URL
            to_visit = [self.config.url]
            
            while to_visit and len(self.visited_urls) < self.config.max_pages:
                current_batch = to_visit[:self.config.max_threads]
                to_visit = to_visit[self.config.max_threads:]
                
                tasks = []
                for url in current_batch:
                    if url not in self.visited_urls:
                        self.visited_urls.add(url)
                        tasks.append(self._fetch_page(session, url))
                
                if tasks:
                    results = await asyncio.gather(*tasks)
                    
                    for page in results:
                        self.extracted_pages.append(page)
                        self.total_pages += 1
                        self.total_size += len(page.content)
                        
                        # Add found links for recursive crawl
                        if self.config.depth == ExtractionDepth.RECURSIVE:
                            for link in page.links:
                                if link not in self.visited_urls:
                                    to_visit.append(link)
                        elif self.config.depth == ExtractionDepth.SAME_DOMAIN:
                            for link in page.links[:10]:  # Limit to 10 per page
                                if link not in self.visited_urls:
                                    to_visit.append(link)
        
        elapsed = time.time() - self.start_time
        self.logger.success(f"Extraction complete: {len(self.extracted_pages)} pages extracted")
        
        return {
            'total_pages': self.total_pages,
            'total_size': self.total_size,
            'elapsed_time': elapsed,
            'pages': self.extracted_pages
        }
