import requests
import os
from collections import defaultdict

class KeywordResearcher:
    """Research and suggest related keywords with metrics"""
    
    def __init__(self):
        # Using DataForSEO API for keyword data
        self.dataforseo_login = os.getenv('DATAFORSEO_LOGIN', 'demo@example.com')
        self.dataforseo_password = os.getenv('DATAFORSEO_PASSWORD', 'demo_password')
        
        # Fallback: Use Serper API for related searches
        self.serper_api_key = os.getenv('SERPER_API_KEY', 'f9028bc0510c22bdb4ccddfd7b6a5228d54d985c')
    
    def research_keywords(self, seed_keyword, max_results=20):
        """
        Get related keywords with metrics
        
        Args:
            seed_keyword: The main keyword to research
            max_results: Number of keyword suggestions to return
            
        Returns:
            dict with keyword suggestions and metrics
        """
        print(f"Researching keywords for: {seed_keyword}")
        
        # Try to get real keyword data
        keywords = self._get_keyword_suggestions(seed_keyword, max_results)
        
        # Calculate opportunity scores
        for kw in keywords:
            kw['opportunity_score'] = self._calculate_opportunity(
                kw.get('search_volume', 0),
                kw.get('difficulty', 50)
            )
        
        # Sort by opportunity score
        keywords.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        return {
            'seed_keyword': seed_keyword,
            'total_keywords': len(keywords),
            'keywords': keywords,
            'categories': self._categorize_keywords(keywords)
        }
    
    def _get_keyword_suggestions(self, seed_keyword, max_results):
        """Get keyword suggestions from APIs"""
        try:
            # Try Serper API for related searches
            response = requests.post(
                'https://google.serper.dev/search',
                headers={
                    'X-API-KEY': self.serper_api_key,
                    'Content-Type': 'application/json'
                },
                json={
                    'q': seed_keyword,
                    'num': 10,
                    'gl': 'us',
                    'hl': 'en'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                keywords = []
                
                # Extract "People Also Ask" questions as keywords
                people_also_ask = data.get('peopleAlsoAsk', [])
                for paa in people_also_ask[:5]:
                    question = paa.get('question', '')
                    if question:
                        keywords.append({
                            'keyword': question,
                            'search_volume': self._estimate_volume(question),
                            'difficulty': self._estimate_difficulty(question),
                            'type': 'question',
                            'intent': 'informational'
                        })
                
                # Extract "Related Searches"
                related_searches = data.get('relatedSearches', [])
                for rs in related_searches:
                    query = rs.get('query', '')
                    if query and query.lower() != seed_keyword.lower():
                        keywords.append({
                            'keyword': query,
                            'search_volume': self._estimate_volume(query),
                            'difficulty': self._estimate_difficulty(query),
                            'type': 'related',
                            'intent': self._detect_intent(query)
                        })
                
                # Generate semantic variations
                keywords.extend(self._generate_semantic_variations(seed_keyword))
                
                print(f"✓ Found {len(keywords)} keyword suggestions")
                return keywords[:max_results]
        
        except Exception as e:
            print(f"API error: {str(e)}, using algorithmic generation")
        
        # Fallback: Generate algorithmic suggestions
        return self._generate_keyword_variations(seed_keyword, max_results)
    
    def _generate_keyword_variations(self, seed_keyword, max_results):
        """Generate keyword variations algorithmically"""
        keywords = []
        
        # Modifiers for different intents
        how_to = ['how to', 'ways to', 'steps to', 'guide to', 'tutorial']
        best = ['best', 'top', 'leading', 'recommended', 'popular']
        comparisons = ['vs', 'versus', 'compared to', 'alternatives to', 'better than']
        questions = ['what is', 'why', 'when to use', 'should i', 'can i']
        tools = ['tools for', 'software for', 'platforms for', 'apps for']
        
        base = seed_keyword.lower()
        
        # How-to variations (high volume, medium difficulty)
        for modifier in how_to[:3]:
            keywords.append({
                'keyword': f"{modifier} {base}",
                'search_volume': 5000,
                'difficulty': 45,
                'type': 'how-to',
                'intent': 'informational'
            })
        
        # Best variations (medium volume, high difficulty)
        for modifier in best[:3]:
            keywords.append({
                'keyword': f"{modifier} {base}",
                'search_volume': 8000,
                'difficulty': 65,
                'type': 'best',
                'intent': 'commercial'
            })
        
        # Question variations (medium volume, low difficulty)
        for modifier in questions[:3]:
            keywords.append({
                'keyword': f"{modifier} {base}",
                'search_volume': 3000,
                'difficulty': 35,
                'type': 'question',
                'intent': 'informational'
            })
        
        # Long-tail variations (low volume, low difficulty)
        long_tail = [
            f"{base} for beginners",
            f"{base} explained",
            f"{base} guide 2025",
            f"{base} tips and tricks",
            f"{base} case study",
            f"{base} examples",
            f"{base} benefits",
            f"{base} challenges"
        ]
        
        for kw in long_tail:
            keywords.append({
                'keyword': kw,
                'search_volume': 1500,
                'difficulty': 30,
                'type': 'long-tail',
                'intent': 'informational'
            })
        
        return keywords[:max_results]
    
    def _generate_semantic_variations(self, seed_keyword):
        """Generate semantically related keywords"""
        variations = []
        base = seed_keyword.lower()
        
        # Add year for trending topics
        variations.append({
            'keyword': f"{base} 2025",
            'search_volume': 4000,
            'difficulty': 40,
            'type': 'trending',
            'intent': 'informational'
        })
        
        # Add common combinations
        combinations = [
            f"{base} guide",
            f"{base} tips",
            f"{base} examples",
            f"{base} tools",
            f"{base} best practices"
        ]
        
        for kw in combinations:
            variations.append({
                'keyword': kw,
                'search_volume': 2500,
                'difficulty': 38,
                'type': 'semantic',
                'intent': 'informational'
            })
        
        return variations
    
    def _estimate_volume(self, keyword):
        """Estimate search volume based on keyword characteristics"""
        length = len(keyword.split())
        
        # Shorter keywords = higher volume
        if length <= 2:
            return 10000
        elif length <= 3:
            return 5000
        elif length <= 5:
            return 2000
        else:
            return 800
    
    def _estimate_difficulty(self, keyword):
        """Estimate SEO difficulty (0-100)"""
        length = len(keyword.split())
        
        # Question keywords are usually easier
        if any(q in keyword.lower() for q in ['how', 'what', 'why', 'when', 'where']):
            return 30 + (length * 2)
        
        # "Best" keywords are competitive
        if 'best' in keyword.lower():
            return 70
        
        # Long-tail = easier
        if length >= 5:
            return 25 + (length * 3)
        
        # Short = harder
        return 50 + (10 / length)
    
    def _detect_intent(self, keyword):
        """Detect search intent"""
        kw_lower = keyword.lower()
        
        if any(w in kw_lower for w in ['buy', 'price', 'cost', 'cheap', 'deal']):
            return 'transactional'
        elif any(w in kw_lower for w in ['best', 'top', 'review', 'vs', 'compare']):
            return 'commercial'
        elif any(w in kw_lower for w in ['how', 'what', 'why', 'guide', 'tutorial']):
            return 'informational'
        else:
            return 'navigational'
    
    def _calculate_opportunity(self, volume, difficulty):
        """
        Calculate opportunity score (0-100)
        High volume + Low difficulty = High opportunity
        """
        if volume == 0:
            return 0
        
        # Normalize volume (log scale)
        import math
        volume_score = min(100, (math.log10(volume + 1) * 20))
        
        # Inverse difficulty (easier = better)
        ease_score = 100 - difficulty
        
        # Weighted average (60% ease, 40% volume)
        opportunity = (ease_score * 0.6) + (volume_score * 0.4)
        
        return round(opportunity, 1)
    
    def _categorize_keywords(self, keywords):
        """Group keywords by type and intent"""
        categories = defaultdict(list)
        
        for kw in keywords:
            intent = kw.get('intent', 'informational')
            categories[intent].append(kw['keyword'])
        
        return dict(categories)
