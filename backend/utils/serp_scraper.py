import requests
from bs4 import BeautifulSoup
import re
import time

class SERPScraper:
    """Scrape and analyze SERP results"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    
    def search_google(self, query, num_results=10):
        """
        Search Google and return top results
        Returns list of dicts with: url, title, snippet
        """
        try:
            # Encode query for URL
            encoded_query = query.replace(' ', '+')
            search_url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            
            # Find search result divs
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results[:num_results]:
                try:
                    # Extract URL
                    link_tag = result.find('a')
                    if not link_tag or not link_tag.get('href'):
                        continue
                    
                    url = link_tag['href']
                    
                    # Extract title
                    title_tag = result.find('h3')
                    title = title_tag.get_text() if title_tag else ''
                    
                    # Extract snippet
                    snippet_div = result.find('div', class_=['VwiC3b', 'yXK7lf'])
                    snippet = snippet_div.get_text() if snippet_div else ''
                    
                    if url and title:
                        results.append({
                            'url': url,
                            'title': title,
                            'snippet': snippet
                        })
                
                except Exception as e:
                    continue
            
            return results
        
        except Exception as e:
            print(f"Error searching Google: {str(e)}")
            # Return mock data if scraping fails
            return self._get_mock_serp_results(query)
    
    def extract_page_content(self, url):
        """
        Extract content from a URL for analysis
        Returns dict with: text, word_count, headers, has_images, has_videos
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                tag.decompose()
            
            # Extract main content
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            
            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
                text = re.sub(r'\s+', ' ', text)
            else:
                text = ''
            
            # Count words
            word_count = len(text.split())
            
            # Extract headers
            headers = []
            for tag in ['h1', 'h2', 'h3']:
                headers.extend([h.get_text(strip=True) for h in soup.find_all(tag)])
            
            # Check for multimedia
            has_images = len(soup.find_all('img')) > 0
            has_videos = len(soup.find_all(['video', 'iframe'])) > 0
            
            # Check for lists
            has_lists = len(soup.find_all(['ul', 'ol'])) > 0
            
            # Check for tables/comparisons
            has_tables = len(soup.find_all('table')) > 0
            
            return {
                'text': text,
                'word_count': word_count,
                'headers': headers,
                'num_headers': len(headers),
                'has_images': has_images,
                'has_videos': has_videos,
                'has_lists': has_lists,
                'has_tables': has_tables
            }
        
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return {
                'text': '',
                'word_count': 0,
                'headers': [],
                'num_headers': 0,
                'has_images': False,
                'has_videos': False,
                'has_lists': False,
                'has_tables': False
            }
    
    def _get_mock_serp_results(self, query):
        """Return mock SERP results if scraping fails"""
        return [
            {
                'url': f'https://example{i}.com/article',
                'title': f'Top Article About {query} - Example {i}',
                'snippet': f'This is a comprehensive guide about {query} with detailed information...'
            }
            for i in range(1, 11)
        ]
