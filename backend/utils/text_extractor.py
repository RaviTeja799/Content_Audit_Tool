import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

class TextExtractor:
    """Extract text and metadata from URL or raw text"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def extract(self, input_data):
        """
        Extract text and metadata from input (URL or text)
        Returns dict with: text, url, headers, meta_description, is_url
        """
        if self._is_url(input_data):
            return self._extract_from_url(input_data)
        else:
            return self._extract_from_text(input_data)
    
    def _is_url(self, text):
        """Check if input is a URL"""
        try:
            result = urlparse(text.strip())
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _extract_from_url(self, url):
        """Extract content from URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            
            # Extract text
            text = soup.get_text(separator=' ', strip=True)
            text = re.sub(r'\s+', ' ', text)  # Clean whitespace
            
            # Extract headers
            headers = []
            for tag in ['h1', 'h2', 'h3', 'h4']:
                headers.extend([h.get_text(strip=True) for h in soup.find_all(tag)])
            
            # Extract meta description
            meta_desc = ''
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag and meta_tag.get('content'):
                meta_desc = meta_tag['content']
            
            return {
                'text': text,
                'url': url,
                'headers': headers,
                'meta_description': meta_desc,
                'is_url': True
            }
        
        except Exception as e:
            print(f"Error extracting from URL: {str(e)}")
            raise Exception(f"Failed to extract content from URL: {str(e)}")
    
    def _extract_from_text(self, text):
        """Process raw text input"""
        # Try to extract headers from markdown-style headers
        headers = []
        lines = text.split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                header = re.sub(r'^#+\s*', '', line.strip())
                headers.append(header)
        
        return {
            'text': text.strip(),
            'url': None,
            'headers': headers,
            'meta_description': '',
            'is_url': False
        }
