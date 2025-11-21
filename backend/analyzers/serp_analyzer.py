from utils.serp_scraper import SERPScraper
import re
from collections import Counter

class SERPAnalyzer:
    """Analyze content against SERP competitors"""
    
    def __init__(self):
        self.scraper = SERPScraper()
    
    def analyze(self, text, target_keyword, current_url=None):
        """
        Analyze content performance against SERP results
        Returns dict with: score, issues, recommendations, details
        """
        if not target_keyword:
            return self._no_keyword_response()
        
        issues = []
        recommendations = []
        
        # Get SERP results
        serp_results = self.scraper.search_google(target_keyword, num_results=10)
        
        # Analyze competitor content
        competitor_data = self._analyze_competitors(serp_results)
        
        # Analyze current content
        current_word_count = len(text.split())
        current_topics = self._extract_topics(text)
        current_elements = self._check_content_elements(text)
        
        # Compare word count
        avg_word_count = competitor_data['avg_word_count']
        word_count_diff = ((current_word_count - avg_word_count) / avg_word_count * 100) if avg_word_count > 0 else 0
        
        if word_count_diff < -20:
            issues.append(f"Content {abs(word_count_diff):.0f}% shorter than SERP average")
            recommendations.append(f"Expand to {int(avg_word_count * 0.9)}+ words covering missing subtopics")
        
        # Compare topic coverage
        missing_topics = competitor_data['common_topics'] - current_topics
        if len(missing_topics) > 2:
            issues.append(f"Missing {len(missing_topics)} key subtopics that top rankers cover")
            recommendations.append(f"Add sections about: {', '.join(list(missing_topics)[:3])}")
        
        # Compare content elements
        if competitor_data['with_comparisons'] > 70 and not current_elements['has_comparison']:
            issues.append(f"No comparisons found ({competitor_data['with_comparisons']}% of top 10 have them)")
            recommendations.append("Add 2-3 product/option comparisons with real examples")
        
        if competitor_data['avg_data_points'] > 3 and current_elements['data_points'] < 3:
            issues.append(f"Only {current_elements['data_points']} data point(s) (top rankers avg {competitor_data['avg_data_points']:.0f} stats)")
            recommendations.append("Include 5-7 data points/statistics to support claims")
        
        if competitor_data['with_lists'] > 60 and not current_elements['has_lists']:
            issues.append("No bullet/numbered lists (most top rankers use them)")
            recommendations.append("Add bullet lists for scannable content")
            
        # Analyze Backlink Potential
        backlink_potential = self._analyze_backlink_potential(text, current_elements)
        if backlink_potential['score'] < 50:
            issues.append("Low backlink potential (content lacks linkable assets)")
            recommendations.append("Add linkable assets: original data, unique definitions, or expert quotes")
        
        # Predict ranking position
        predicted_position = self._predict_ranking(
            current_word_count, avg_word_count,
            len(current_topics), len(competitor_data['common_topics']),
            current_elements, competitor_data, backlink_potential
        )
        
        # Calculate score
        score = self._calculate_serp_score(
            word_count_diff, missing_topics, current_elements, competitor_data, predicted_position, backlink_potential
        )
        
        return {
            'score': score,
            'target_keyword': target_keyword,
            'serp_analysis': {
                'avg_word_count': int(avg_word_count),
                'your_word_count': current_word_count,
                'avg_topics': len(competitor_data['common_topics']),
                'your_topics': len(current_topics),
                'top_rankers_include': {
                    'comparisons': f"{competitor_data['with_comparisons']}%",
                    'data_stats': f"{competitor_data['with_data']}%",
                    'lists': f"{competitor_data['with_lists']}%",
                    'images': f"{competitor_data['with_images']}%"
                }
            },
            'backlink_potential': backlink_potential,
            'predicted_position': predicted_position,
            'issues': issues,
            'recommendations': recommendations[:3],
            'missing_topics': list(missing_topics)[:5]
        }
    
    def _analyze_competitors(self, serp_results):
        """Analyze top 10 SERP results"""
        total_words = 0
        all_topics = []
        with_comparisons = 0
        with_data = 0
        with_lists = 0
        with_images = 0
        total_data_points = 0
        valid_results = 0
        
        for result in serp_results[:10]:
            try:
                content = self.scraper.extract_page_content(result['url'])
                
                if content['word_count'] > 100:  # Valid page
                    valid_results += 1
                    total_words += content['word_count']
                    all_topics.extend(self._extract_topics(content['text']))
                    
                    if content.get('has_tables', False):
                        with_comparisons += 1
                    
                    # Check for data points (numbers with context)
                    data_points = len(re.findall(r'\d+[%$]|\d+\s*(?:percent|dollars|years|months)', content['text']))
                    if data_points > 0:
                        with_data += 1
                        total_data_points += data_points
                    
                    if content.get('has_lists', False):
                        with_lists += 1
                    
                    if content.get('has_images', False):
                        with_images += 1
            
            except Exception as e:
                continue
        
        # Calculate averages
        avg_word_count = (total_words / valid_results) if valid_results > 0 else 1500
        avg_data_points = (total_data_points / valid_results) if valid_results > 0 else 3
        
        # Find common topics (topics appearing in multiple articles)
        topic_counter = Counter(all_topics)
        common_topics = {topic for topic, count in topic_counter.items() if count >= 2}
        
        return {
            'avg_word_count': avg_word_count,
            'common_topics': common_topics,
            'with_comparisons': int((with_comparisons / max(valid_results, 1)) * 100),
            'with_data': int((with_data / max(valid_results, 1)) * 100),
            'with_lists': int((with_lists / max(valid_results, 1)) * 100),
            'with_images': int((with_images / max(valid_results, 1)) * 100),
            'avg_data_points': avg_data_points
        }
    
    def _extract_topics(self, text):
        """Extract main topics/subtopics from text"""
        # Simple topic extraction based on noun phrases and key terms
        topics = set()
        
        # Common topic patterns
        patterns = [
            r'\b(?:how to|guide to|tips for|best|top|ways to)\s+(\w+(?:\s+\w+){0,3})',
            r'\b(\w+(?:\s+\w+){0,2})\s+(?:comparison|review|analysis|guide)',
            r'\b(?:what is|understanding|about)\s+(\w+(?:\s+\w+){0,2})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            topics.update(matches[:20])  # Limit topics
        
        return topics
    
    def _check_content_elements(self, text):
        """Check for specific content elements"""
        # Check for comparisons
        has_comparison = bool(re.search(r'\b(?:vs|versus|compared to|comparison|better than|versus)\b', text.lower()))
        
        # Count data points
        data_points = len(re.findall(r'\d+[%$]|\d+\s*(?:percent|dollars|years|months|times|hours)', text))
        
        # Check for lists
        has_lists = bool(re.search(r'(?:\n\s*[-•*]\s+|\n\s*\d+\.\s+)', text))
        
        # Check for quotes
        has_quotes = text.count('"') >= 2 or text.count('"') >= 2
        
        return {
            'has_comparison': has_comparison,
            'data_points': data_points,
            'has_lists': has_lists,
            'has_quotes': has_quotes
        }
    
    def _predict_ranking(self, current_wc, avg_wc, current_topics, avg_topics, current_elements, competitor_data, backlink_potential=None):
        """Predict ranking position based on content analysis"""
        score = 0
        
        # Word count comparison (25 points)
        wc_ratio = current_wc / avg_wc if avg_wc > 0 else 0
        if wc_ratio >= 0.9:
            score += 25
        elif wc_ratio >= 0.7:
            score += 15
        elif wc_ratio >= 0.5:
            score += 5
        
        # Topic coverage (25 points)
        topic_ratio = current_topics / avg_topics if avg_topics > 0 else 0
        if topic_ratio >= 0.8:
            score += 25
        elif topic_ratio >= 0.6:
            score += 15
        elif topic_ratio >= 0.4:
            score += 5
        
        # Content elements (30 points)
        if current_elements['has_comparison'] and competitor_data['with_comparisons'] > 50:
            score += 10
        if current_elements['data_points'] >= 5:
            score += 10
        if current_elements['has_lists']:
            score += 5
        if current_elements['has_quotes']:
            score += 5
            
        # Backlink Potential (20 points)
        if backlink_potential:
            if backlink_potential['score'] > 70:
                score += 20
            elif backlink_potential['score'] > 40:
                score += 10
        
        # Predict position range
        if score >= 80:
            return "Page 1 (positions 1-3)"
        elif score >= 60:
            return "Page 1 (positions 4-10)"
        elif score >= 40:
            return "Page 2 (positions 11-20)"
        else:
            return "Page 3+ (positions 21+)"
    
    def _calculate_serp_score(self, wc_diff, missing_topics, current_elements, competitor_data, predicted_position, backlink_potential=None):
        """Calculate SERP performance score (0-100)"""
        score = 100
        
        # Word count penalty
        if wc_diff < -50:
            score -= 25
        elif wc_diff < -30:
            score -= 15
        elif wc_diff < -15:
            score -= 5
        
        # Topic coverage penalty
        if len(missing_topics) > 5:
            score -= 20
        elif len(missing_topics) > 3:
            score -= 10
        elif len(missing_topics) > 1:
            score -= 5
        
        # Content elements penalty
        if competitor_data['with_comparisons'] > 70 and not current_elements['has_comparison']:
            score -= 10
        
        if current_elements['data_points'] < 3:
            score -= 5
        
        if not current_elements['has_lists']:
            score -= 5
            
        # Backlink potential penalty
        if backlink_potential and backlink_potential['score'] < 40:
            score -= 10
        
        return max(0, score)
    
    def _no_keyword_response(self):
        """Response when no target keyword is provided"""
        return {
            'score': 0,
            'target_keyword': None,
            'serp_analysis': None,
            'predicted_position': 'Unknown',
            'issues': ['No target keyword provided - cannot analyze SERP performance'],
            'recommendations': ['Provide a target keyword to analyze SERP competition'],
            'missing_topics': []
        }
    
    def _analyze_backlink_potential(self, text, current_elements):
        """Analyze potential for attracting backlinks"""
        score = 0
        assets = []
        
        # Check for original data/stats
        if current_elements['data_points'] >= 5:
            score += 30
            assets.append("Original Data/Stats")
        elif current_elements['data_points'] >= 3:
            score += 15
            
        # Check for definitions ("is defined as", "refers to")
        if re.search(r'\b(is defined as|refers to|means)\b', text.lower()):
            score += 20
            assets.append("Definitional Content")
            
        # Check for comparisons
        if current_elements['has_comparison']:
            score += 20
            assets.append("Comparison/Review")
            
        # Check for quotes
        if current_elements['has_quotes']:
            score += 15
            assets.append("Expert Quotes")
            
        # Check for length (long-form content gets more links)
        word_count = len(text.split())
        if word_count > 2000:
            score += 15
            assets.append("Long-form Guide")
        elif word_count > 1000:
            score += 10
            
        return {
            'score': min(100, score),
            'level': 'High' if score > 70 else 'Medium' if score > 40 else 'Low',
            'linkable_assets': assets
        }
