from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.serp_scraper import SERPScraper
import re
import numpy as np

class DifferentiationAnalyzer:
    """Analyze content uniqueness vs competitors"""
    
    def __init__(self):
        self.scraper = SERPScraper()
    
    def analyze(self, text, target_keyword):
        """
        Analyze content differentiation from competitors
        Returns dict with: score, issues, recommendations, details
        """
        if not target_keyword:
            return self._no_keyword_response()
        
        issues = []
        recommendations = []
        
        # Get competitor content
        serp_results = self.scraper.search_google(target_keyword, num_results=10)
        competitor_texts = self._gather_competitor_content(serp_results[:3])  # Top 3 for comparison
        
        if not competitor_texts:
            return self._no_competitor_data_response()
        
        # Calculate content overlap
        overlap_data = self._calculate_content_overlap(text, competitor_texts)
        
        # Analyze unique elements
        unique_elements = self._analyze_unique_elements(text, competitor_texts)
        
        # Analyze structural differentiation
        structure_data = self._analyze_structural_difference(text, competitor_texts)
        
        # Check for unique value additions
        value_adds = self._check_unique_value(text)
        
        # Generate issues and recommendations
        if overlap_data['avg_similarity'] > 70:
            issues.append(f"{overlap_data['avg_similarity']:.0f}% content overlap with top 3 SERP results")
            recommendations.append("Rewrite sections to add unique perspective and original insights")
        
        if not unique_elements['has_unique_data']:
            issues.append("No unique examples or data")
            recommendations.append("Add original data points, case studies, or product comparisons")
        
        if structure_data['structure_similarity'] > 80:
            issues.append("Same structure as competitors (all follow identical outline)")
            recommendations.append("Use unique angle (e.g., 'student perspective' vs generic advice)")
        
        if not value_adds['has_unique_angle']:
            issues.append("Generic content without unique perspective")
            recommendations.append("Add personal experience, expert insights, or unique methodology")
        
        if not unique_elements['has_multimedia']:
            issues.append("No unique visual elements")
            recommendations.append("Add original images, infographics, or video content")
        
        # Calculate score
        score = self._calculate_differentiation_score(overlap_data, unique_elements, structure_data, value_adds)
        
        return {
            'score': score,
            'overlap_analysis': {
                'avg_similarity': f"{overlap_data['avg_similarity']:.0f}%",
                'highest_similarity': f"{overlap_data['highest_similarity']:.0f}%",
                'unique_sentences': overlap_data['unique_sentence_ratio']
            },
            'issues': issues,
            'recommendations': recommendations[:3],
            'unique_elements_found': self._list_unique_elements(unique_elements, value_adds),
            'differentiation_opportunities': self._suggest_differentiation_strategies(text, target_keyword)
        }
    
    def _gather_competitor_content(self, serp_results):
        """Gather content from top competitors"""
        competitor_texts = []
        
        for result in serp_results:
            try:
                content = self.scraper.extract_page_content(result['url'])
                if content['text'] and len(content['text']) > 500:
                    competitor_texts.append(content['text'])
            except:
                continue
        
        return competitor_texts
    
    def _calculate_content_overlap(self, text, competitor_texts):
        """Calculate content similarity using TF-IDF"""
        if not competitor_texts:
            return {'avg_similarity': 0, 'highest_similarity': 0, 'unique_sentence_ratio': 100}
        
        try:
            # Prepare documents
            all_docs = [text] + competitor_texts
            
            # Calculate TF-IDF similarity
            vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(all_docs)
            
            # Calculate cosine similarity
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
            
            avg_similarity = np.mean(similarities) * 100
            highest_similarity = np.max(similarities) * 100
            
            # Analyze sentence-level uniqueness
            unique_sentence_ratio = self._calculate_unique_sentences(text, competitor_texts)
            
            return {
                'avg_similarity': avg_similarity,
                'highest_similarity': highest_similarity,
                'unique_sentence_ratio': unique_sentence_ratio
            }
        
        except Exception as e:
            print(f"Error calculating overlap: {str(e)}")
            return {'avg_similarity': 50, 'highest_similarity': 60, 'unique_sentence_ratio': 60}
    
    def _calculate_unique_sentences(self, text, competitor_texts):
        """Calculate percentage of unique sentences"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip().lower() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return 0
        
        # Combine all competitor text
        combined_competitor = ' '.join(competitor_texts).lower()
        
        # Count unique sentences
        unique_count = 0
        for sentence in sentences:
            # Check if sentence appears in competitors (with fuzzy matching)
            words = sentence.split()
            if len(words) > 5:
                # Check if most of the sentence is unique
                word_matches = sum(1 for word in words if word in combined_competitor)
                if word_matches / len(words) < 0.6:  # Less than 60% word overlap
                    unique_count += 1
        
        return (unique_count / len(sentences) * 100) if sentences else 0
    
    def _analyze_unique_elements(self, text, competitor_texts):
        """Analyze presence of unique elements"""
        combined_competitor = ' '.join(competitor_texts).lower()
        text_lower = text.lower()
        
        # Check for unique data/statistics
        numbers_in_text = set(re.findall(r'\b\d+[%$]?\b', text))
        numbers_in_competitors = set(re.findall(r'\b\d+[%$]?\b', combined_competitor))
        unique_numbers = numbers_in_text - numbers_in_competitors
        has_unique_data = len(unique_numbers) > 3
        
        # Check for personal experience markers
        experience_markers = [
            'in my experience', 'i found', 'i tested', 'i tried',
            'we discovered', 'our research', 'our analysis', 'our study'
        ]
        has_personal_experience = any(marker in text_lower for marker in experience_markers)
        
        # Check for unique case studies or examples
        case_markers = ['case study', 'example:', 'for instance', 'real-world example']
        case_count = sum(text_lower.count(marker) for marker in case_markers)
        has_case_studies = case_count > 0
        
        # Check for multimedia references
        multimedia_markers = ['image', 'infographic', 'chart', 'graph', 'video', 'screenshot']
        has_multimedia = any(marker in text_lower for marker in multimedia_markers)
        
        return {
            'has_unique_data': has_unique_data,
            'has_personal_experience': has_personal_experience,
            'has_case_studies': has_case_studies,
            'has_multimedia': has_multimedia,
            'unique_data_points': len(unique_numbers)
        }
    
    def _analyze_structural_difference(self, text, competitor_texts):
        """Analyze structural differentiation"""
        # Extract header-like patterns
        text_headers = re.findall(r'(?:^|\n)([A-Z][^\n]{10,80})(?:\n|$)', text)
        
        # Check structure similarity with competitors
        structure_matches = 0
        for comp_text in competitor_texts:
            comp_headers = re.findall(r'(?:^|\n)([A-Z][^\n]{10,80})(?:\n|$)', comp_text)
            
            # Compare header topics
            for header in text_headers[:5]:  # Check first 5 headers
                for comp_header in comp_headers[:5]:
                    # Simple similarity check
                    common_words = set(header.lower().split()) & set(comp_header.lower().split())
                    if len(common_words) >= 2:
                        structure_matches += 1
                        break
        
        total_comparisons = len(text_headers[:5]) * len(competitor_texts)
        structure_similarity = (structure_matches / total_comparisons * 100) if total_comparisons > 0 else 0
        
        return {
            'structure_similarity': structure_similarity,
            'total_sections': len(text_headers)
        }
    
    def _check_unique_value(self, text):
        """Check for unique value propositions"""
        text_lower = text.lower()
        
        # Check for unique angle indicators
        unique_angles = [
            'beginner', 'advanced', 'expert', 'student', 'professional',
            'budget', 'premium', 'enterprise', 'small business',
            'complete guide', 'ultimate guide', 'definitive guide'
        ]
        has_unique_angle = any(angle in text_lower for angle in unique_angles)
        
        # Check for original opinions/insights
        opinion_markers = [
            'i believe', 'i think', 'in our opinion', 'we recommend',
            'our take', 'my recommendation', 'controversial', 'unpopular opinion'
        ]
        has_opinions = any(marker in text_lower for marker in opinion_markers)
        
        # Check for expert quotes or interviews
        quote_markers = [
            'expert', 'specialist', 'according to', 'says', 'told us',
            'interview', 'spoke with', 'conversation with'
        ]
        has_expert_input = any(marker in text_lower for marker in quote_markers)
        
        return {
            'has_unique_angle': has_unique_angle,
            'has_opinions': has_opinions,
            'has_expert_input': has_expert_input
        }
    
    def _calculate_differentiation_score(self, overlap_data, unique_elements, structure_data, value_adds):
        """Calculate differentiation score (0-100)"""
        score = 100
        
        # Content overlap penalty (35 points)
        if overlap_data['avg_similarity'] > 80:
            score -= 35
        elif overlap_data['avg_similarity'] > 70:
            score -= 25
        elif overlap_data['avg_similarity'] > 60:
            score -= 15
        elif overlap_data['avg_similarity'] > 50:
            score -= 8
        
        # Unique elements (30 points)
        if not unique_elements['has_unique_data']:
            score -= 12
        if not unique_elements['has_personal_experience']:
            score -= 8
        if not unique_elements['has_case_studies']:
            score -= 5
        if not unique_elements['has_multimedia']:
            score -= 5
        
        # Structure differentiation (20 points)
        if structure_data['structure_similarity'] > 80:
            score -= 20
        elif structure_data['structure_similarity'] > 60:
            score -= 12
        elif structure_data['structure_similarity'] > 40:
            score -= 6
        
        # Unique value (15 points)
        if not value_adds['has_unique_angle']:
            score -= 8
        if not value_adds['has_opinions']:
            score -= 4
        if not value_adds['has_expert_input']:
            score -= 3
        
        return max(0, score)
    
    def _list_unique_elements(self, unique_elements, value_adds):
        """List unique elements found"""
        elements = []
        
        if unique_elements['has_unique_data']:
            elements.append(f"Unique data points ({unique_elements['unique_data_points']} found)")
        if unique_elements['has_personal_experience']:
            elements.append("Personal experience/insights")
        if unique_elements['has_case_studies']:
            elements.append("Case studies/examples")
        if value_adds['has_unique_angle']:
            elements.append("Unique target audience angle")
        if value_adds['has_opinions']:
            elements.append("Original opinions/recommendations")
        if value_adds['has_expert_input']:
            elements.append("Expert quotes/input")
        
        return elements if elements else ["No significant unique elements found"]
    
    def _suggest_differentiation_strategies(self, text, target_keyword):
        """Suggest specific differentiation strategies"""
        strategies = []
        
        # Suggest based on content gaps
        if 'example' not in text.lower():
            strategies.append("Add real-world examples or case studies")
        
        if not re.search(r'\d+%|\d+\s*dollars?', text):
            strategies.append("Include specific statistics or data")
        
        if 'we tested' not in text.lower() and 'i tested' not in text.lower():
            strategies.append("Add original research or product testing")
        
        # Suggest unique angles
        strategies.append(f"Create '{target_keyword} for [specific audience]' angle")
        strategies.append("Add contrarian viewpoint or myth-busting section")
        strategies.append("Include expert interview or quote")
        strategies.append("Create original infographic or visual")
        
        return strategies[:5]
    
    def _no_keyword_response(self):
        """Response when no target keyword is provided"""
        return {
            'score': 0,
            'overlap_analysis': None,
            'issues': ['No target keyword provided - cannot analyze differentiation'],
            'recommendations': ['Provide a target keyword to analyze competitor differentiation'],
            'unique_elements_found': [],
            'differentiation_opportunities': []
        }
    
    def _no_competitor_data_response(self):
        """Response when competitor data cannot be retrieved"""
        return {
            'score': 50,
            'overlap_analysis': {
                'avg_similarity': 'N/A',
                'highest_similarity': 'N/A',
                'unique_sentences': 'N/A'
            },
            'issues': ['Could not retrieve competitor data for comparison'],
            'recommendations': [
                'Add unique case studies or examples',
                'Include original data or research',
                'Use a distinctive voice or angle'
            ],
            'unique_elements_found': ['Unable to assess without competitor data'],
            'differentiation_opportunities': [
                'Add personal experience or insights',
                'Include expert interviews',
                'Create original visual content'
            ]
        }
