import json
import re
from datetime import datetime

class SchemaGenerator:
    def __init__(self):
        self.current_date = datetime.now().isoformat()
    
    def generate(self, text, url='', keyword='', content_type='Article'):
        # Extract first heading as potential title
        title = self._extract_title(text, keyword)
        
        # Extract author if mentioned
        author = self._extract_author(text)
        
        # Generate description from first paragraph
        description = self._extract_description(text)
        
        # Detect content type
        detected_type = self._detect_content_type(text)
        if detected_type:
            content_type = detected_type
        
        # Generate appropriate schema
        if content_type == 'Article':
            schema = self._generate_article_schema(title, description, author, url)
        elif content_type == 'HowTo':
            schema = self._generate_howto_schema(title, description, text, url)
        elif content_type == 'FAQ':
            schema = self._generate_faq_schema(text)
        elif content_type == 'Product':
            schema = self._generate_product_schema(title, description, text)
        else:
            schema = self._generate_article_schema(title, description, author, url)
        
        return {
            'schema': schema,
            'content_type': content_type,
            'json_ld': json.dumps(schema, indent=2)
        }
    
    def _extract_title(self, text, keyword):
        # Try to find a title in first line or use keyword
        lines = text.split('\n')
        first_line = lines[0].strip() if lines else ''
        
        if len(first_line) > 10 and len(first_line) < 100:
            return first_line
        elif keyword:
            return keyword.title()
        else:
            words = text.split()[:10]
            return ' '.join(words) + '...'
    
    def _extract_author(self, text):
        # Simple author extraction patterns
        author_patterns = [
            r'by ([A-Z][a-z]+ [A-Z][a-z]+)',
            r'[Aa]uthor: ([A-Z][a-z]+ [A-Z][a-z]+)',
            r'[Ww]ritten by ([A-Z][a-z]+ [A-Z][a-z]+)'
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return 'Content Team'
    
    def _extract_description(self, text):
        # Get first paragraph as description
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if paragraphs:
            desc = paragraphs[0]
            if len(desc) > 160:
                desc = desc[:157] + '...'
            return desc
        return text[:160]
    
    def _detect_content_type(self, text):
        text_lower = text.lower()
        
        # HowTo detection
        if any(phrase in text_lower for phrase in ['step 1', 'step 2', 'how to', 'steps:', 'instructions:']):
            return 'HowTo'
        
        # FAQ detection
        if text_lower.count('?') > 3 and any(phrase in text_lower for phrase in ['what is', 'how do', 'why does']):
            return 'FAQ'
        
        # Product detection
        if any(phrase in text_lower for phrase in ['price', 'buy now', 'add to cart', 'rating', 'reviews']):
            return 'Product'
        
        return 'Article'
    
    def _generate_article_schema(self, title, description, author, url):
        return {
            '@context': 'https://schema.org',
            '@type': 'Article',
            'headline': title,
            'description': description,
            'author': {
                '@type': 'Person',
                'name': author
            },
            'datePublished': self.current_date,
            'dateModified': self.current_date,
            'url': url
        }
    
    def _generate_howto_schema(self, title, description, text, url):
        # Extract steps
        steps = []
        step_pattern = r'(?:step|Step)\s*\d+[:\.]?\s*(.+?)(?=(?:step|Step)\s*\d+|$)'
        matches = re.finditer(step_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for i, match in enumerate(matches, 1):
            step_text = match.group(1).strip()[:200]
            steps.append({
                '@type': 'HowToStep',
                'name': f'Step {i}',
                'text': step_text,
                'position': i
            })
        
        return {
            '@context': 'https://schema.org',
            '@type': 'HowTo',
            'name': title,
            'description': description,
            'step': steps[:10] if steps else [{'@type': 'HowToStep', 'text': description}],
            'url': url
        }
    
    def _generate_faq_schema(self, text):
        # Extract Q&A pairs
        qa_pairs = []
        
        # Find questions (lines ending with ?)
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if '?' in line:
                question = line.strip()
                # Get next non-empty line as answer
                answer = ''
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j].strip() and '?' not in lines[j]:
                        answer = lines[j].strip()
                        break
                
                if answer:
                    qa_pairs.append({
                        '@type': 'Question',
                        'name': question,
                        'acceptedAnswer': {
                            '@type': 'Answer',
                            'text': answer
                        }
                    })
        
        return {
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': qa_pairs[:10]
        }
    
    def _generate_product_schema(self, title, description, text):
        # Extract price if present
        price_match = re.search(r'\$(\d+(?:\.\d{2})?)', text)
        price = price_match.group(1) if price_match else '0.00'
        
        return {
            '@context': 'https://schema.org',
            '@type': 'Product',
            'name': title,
            'description': description,
            'offers': {
                '@type': 'Offer',
                'price': price,
                'priceCurrency': 'USD'
            }
        }
