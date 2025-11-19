import re
import textstat
from collections import Counter

class SEOAnalyzer:
    """Analyze content for SEO optimization"""
    
    def analyze(self, text, headers, meta_description, target_keyword):
        """
        Analyze SEO aspects of content
        Returns dict with: score, issues, recommendations, details
        """
        issues = []
        recommendations = []
        details = {}
        
        # 1. Keyword Density Analysis
        keyword_data = self._analyze_keyword_density(text, target_keyword)
        details['keyword_density'] = keyword_data
        
        if keyword_data['density'] < 0.5:
            issues.append(f"Keyword '{target_keyword}' appears only {keyword_data['count']} times ({keyword_data['density']:.1f}% density)")
            recommendations.append(f"Increase keyword to {keyword_data['recommended_count']} mentions (1.0-1.5% density)")
        elif keyword_data['density'] > 3.0:
            issues.append(f"Keyword density too high ({keyword_data['density']:.1f}%) - risk of keyword stuffing")
            recommendations.append("Reduce keyword mentions to 1.0-2.5% density for natural flow")
        
        # 2. Readability Analysis
        readability_data = self._analyze_readability(text)
        details['readability'] = readability_data
        
        if readability_data['flesch_ease'] < 60:
            issues.append(f"Content is difficult to read (Flesch score: {readability_data['flesch_ease']:.1f})")
            recommendations.append("Simplify sentences and use shorter words for better readability")
        
        # 3. Header Structure Analysis
        header_data = self._analyze_headers(headers, target_keyword)
        details['headers'] = header_data
        
        if not header_data['has_h1']:
            issues.append("No H1 header found")
            recommendations.append("Add a clear H1 header with target keyword")
        
        if header_data['total_headers'] < 3:
            issues.append(f"Only {header_data['total_headers']} headers found - content lacks structure")
            recommendations.append("Add more H2/H3 headers to improve content structure (aim for 5-8 headers)")
        
        if target_keyword and header_data['keyword_in_headers'] == 0:
            issues.append("Target keyword not found in any headers")
            recommendations.append("Include target keyword in at least one H2 or H3 header")
        
        # 4. Meta Description
        meta_data = self._analyze_meta_description(meta_description, target_keyword)
        details['meta_description'] = meta_data
        
        if not meta_description:
            issues.append("No meta description detected")
            recommendations.append("Add meta description (150-160 characters with target keyword)")
        elif meta_data['length'] < 120:
            issues.append(f"Meta description too short ({meta_data['length']} characters)")
            recommendations.append("Expand meta description to 150-160 characters")
        elif meta_data['length'] > 160:
            issues.append(f"Meta description too long ({meta_data['length']} characters)")
            recommendations.append("Shorten meta description to 150-160 characters")
        
        # 5. Content Length
        word_count = len(text.split())
        details['word_count'] = word_count
        
        if word_count < 300:
            issues.append(f"Content too short ({word_count} words)")
            recommendations.append("Expand content to at least 800-1000 words for better SEO")
        
        # Calculate score
        score = self._calculate_seo_score(keyword_data, readability_data, header_data, meta_data, word_count)
        
        return {
            'score': score,
            'issues': issues,
            'recommendations': recommendations[:3],  # Top 3
            'details': details,
            'good_points': self._get_good_points(keyword_data, readability_data, header_data, meta_data, word_count)
        }
    
    def _analyze_keyword_density(self, text, keyword):
        """Calculate keyword density and stats"""
        if not keyword:
            return {
                'count': 0,
                'density': 0.0,
                'recommended_count': 0
            }
        
        text_lower = text.lower()
        keyword_lower = keyword.lower()
        
        # Count occurrences
        count = text_lower.count(keyword_lower)
        
        # Calculate density
        total_words = len(text.split())
        keyword_words = len(keyword.split())
        density = (count * keyword_words / total_words * 100) if total_words > 0 else 0
        
        # Recommended count (1.0-1.5% density)
        recommended_count = int((total_words * 0.012) / keyword_words) if keyword_words > 0 else 0
        
        return {
            'count': count,
            'density': density,
            'recommended_count': max(recommended_count, 3)
        }
    
    def _analyze_readability(self, text):
        """Analyze text readability"""
        flesch_ease = textstat.flesch_reading_ease(text)
        flesch_grade = textstat.flesch_kincaid_grade(text)
        
        # Interpret Flesch score
        if flesch_ease >= 80:
            level = "Very Easy"
        elif flesch_ease >= 60:
            level = "Easy"
        elif flesch_ease >= 50:
            level = "Fairly Difficult"
        else:
            level = "Difficult"
        
        return {
            'flesch_ease': flesch_ease,
            'flesch_grade': flesch_grade,
            'level': level
        }
    
    def _analyze_headers(self, headers, target_keyword):
        """Analyze header structure"""
        has_h1 = any('h1' in str(h).lower() for h in headers[:1]) if headers else False
        total_headers = len(headers)
        
        # Check keyword in headers
        keyword_in_headers = 0
        if target_keyword:
            keyword_lower = target_keyword.lower()
            keyword_in_headers = sum(1 for h in headers if keyword_lower in h.lower())
        
        return {
            'has_h1': has_h1,
            'total_headers': total_headers,
            'keyword_in_headers': keyword_in_headers
        }
    
    def _analyze_meta_description(self, meta_description, target_keyword):
        """Analyze meta description"""
        length = len(meta_description)
        has_keyword = target_keyword.lower() in meta_description.lower() if target_keyword and meta_description else False
        
        return {
            'length': length,
            'has_keyword': has_keyword,
            'exists': bool(meta_description)
        }
    
    def _calculate_seo_score(self, keyword_data, readability_data, header_data, meta_data, word_count):
        """Calculate overall SEO score (0-100)"""
        score = 100
        
        # Keyword density (25 points)
        if keyword_data['density'] < 0.5:
            score -= 15
        elif keyword_data['density'] > 3.0:
            score -= 10
        elif keyword_data['density'] < 1.0:
            score -= 5
        
        # Readability (20 points)
        if readability_data['flesch_ease'] < 40:
            score -= 20
        elif readability_data['flesch_ease'] < 60:
            score -= 10
        
        # Headers (25 points)
        if not header_data['has_h1']:
            score -= 15
        if header_data['total_headers'] < 3:
            score -= 10
        elif header_data['total_headers'] < 5:
            score -= 5
        if header_data['keyword_in_headers'] == 0:
            score -= 10
        
        # Meta description (15 points)
        if not meta_data['exists']:
            score -= 15
        elif meta_data['length'] < 120 or meta_data['length'] > 160:
            score -= 10
        elif not meta_data['has_keyword']:
            score -= 5
        
        # Content length (15 points)
        if word_count < 300:
            score -= 15
        elif word_count < 600:
            score -= 10
        elif word_count < 800:
            score -= 5
        
        return max(0, score)
    
    def _get_good_points(self, keyword_data, readability_data, header_data, meta_data, word_count):
        """Identify positive aspects"""
        good_points = []
        
        if 1.0 <= keyword_data['density'] <= 2.5:
            good_points.append("Good keyword density (optimal range)")
        
        if readability_data['flesch_ease'] >= 60:
            good_points.append(f"Good readability ({readability_data['level']})")
        
        if header_data['has_h1'] and header_data['total_headers'] >= 5:
            good_points.append("Well-structured with proper headers")
        
        if meta_data['exists'] and 120 <= meta_data['length'] <= 160:
            good_points.append("Meta description present and proper length")
        
        if word_count >= 1000:
            good_points.append(f"Comprehensive content ({word_count} words)")
        
        return good_points
