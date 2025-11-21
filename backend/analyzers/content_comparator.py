import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ContentComparator:
    """Compare content with top competitor to identify gaps"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    def compare_with_competitor(self, your_content, competitor_data, your_metadata=None):
        """
        Compare your content with top competitor
        
        Args:
            your_content: Your content text
            competitor_data: Dict with competitor content details
            your_metadata: Dict with your content metadata
            
        Returns:
            Comprehensive comparison analysis
        """
        print("Performing content gap analysis...")
        
        competitor_text = competitor_data.get('text', '')
        
        # Structural comparison
        structural_gaps = self._compare_structure(your_metadata or {}, competitor_data)
        
        # Topic coverage analysis
        topic_gaps = self._analyze_topic_coverage(your_content, competitor_text)
        
        # Content element comparison
        element_gaps = self._compare_elements(your_metadata or {}, competitor_data)
        
        # Readability comparison
        readability_comparison = self._compare_readability(your_content, competitor_text)
        
        # Generate actionable recommendations
        recommendations = self._generate_gap_recommendations(
            structural_gaps,
            topic_gaps,
            element_gaps,
            readability_comparison
        )
        
        # Calculate overall gap score (0-100, lower is better - meaning fewer gaps)
        gap_score = self._calculate_gap_score(structural_gaps, topic_gaps, element_gaps)
        
        return {
            'gap_score': gap_score,
            'interpretation': self._interpret_gap_score(gap_score),
            'structural_gaps': structural_gaps,
            'topic_gaps': topic_gaps,
            'element_gaps': element_gaps,
            'readability_comparison': readability_comparison,
            'recommendations': recommendations,
            'competitor_info': {
                'word_count': competitor_data.get('word_count', 0),
                'headers': competitor_data.get('num_headers', 0),
                'has_images': competitor_data.get('has_images', False),
                'has_videos': competitor_data.get('has_videos', False)
            }
        }
    
    def _compare_structure(self, your_data, competitor_data):
        """Compare structural elements"""
        your_words = your_data.get('word_count', len(your_data.get('text', '').split()))
        comp_words = competitor_data.get('word_count', 0)
        
        your_headers = len(your_data.get('headers', []))
        comp_headers = competitor_data.get('num_headers', 0)
        
        return {
            'word_count': {
                'yours': your_words,
                'competitor': comp_words,
                'gap': comp_words - your_words,
                'percentage': round((your_words / comp_words * 100) if comp_words > 0 else 0, 1)
            },
            'headers': {
                'yours': your_headers,
                'competitor': comp_headers,
                'gap': comp_headers - your_headers
            }
        }
    
    def _analyze_topic_coverage(self, your_content, competitor_content):
        """Analyze topic coverage using TF-IDF"""
        if not your_content or not competitor_content:
            return {
                'similarity': 0,
                'unique_to_competitor': [],
                'unique_to_you': [],
                'common_topics': []
            }
        
        try:
            # Fit TF-IDF on both documents
            texts = [your_content, competitor_content]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculate similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Get feature names (topics/keywords)
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get top terms for each document
            your_scores = tfidf_matrix[0].toarray()[0]
            comp_scores = tfidf_matrix[1].toarray()[0]
            
            # Find unique and common topics
            your_top_indices = np.argsort(your_scores)[-20:][::-1]
            comp_top_indices = np.argsort(comp_scores)[-20:][::-1]
            
            your_topics = set([feature_names[i] for i in your_top_indices if your_scores[i] > 0])
            comp_topics = set([feature_names[i] for i in comp_top_indices if comp_scores[i] > 0])
            
            unique_to_competitor = list(comp_topics - your_topics)[:10]
            unique_to_you = list(your_topics - comp_topics)[:10]
            common_topics = list(your_topics & comp_topics)[:10]
            
            return {
                'similarity': round(similarity * 100, 1),
                'unique_to_competitor': unique_to_competitor,
                'unique_to_you': unique_to_you,
                'common_topics': common_topics
            }
        
        except Exception as e:
            print(f"Error in topic analysis: {str(e)}")
            return {
                'similarity': 50,
                'unique_to_competitor': [],
                'unique_to_you': [],
                'common_topics': []
            }
    
    def _compare_elements(self, your_data, competitor_data):
        """Compare content elements (images, videos, lists, etc.)"""
        elements = {
            'images': {
                'yours': your_data.get('has_images', False),
                'competitor': competitor_data.get('has_images', False),
                'gap': competitor_data.get('has_images', False) and not your_data.get('has_images', False)
            },
            'videos': {
                'yours': your_data.get('has_videos', False),
                'competitor': competitor_data.get('has_videos', False),
                'gap': competitor_data.get('has_videos', False) and not your_data.get('has_videos', False)
            },
            'lists': {
                'yours': your_data.get('has_lists', False),
                'competitor': competitor_data.get('has_lists', False),
                'gap': competitor_data.get('has_lists', False) and not your_data.get('has_lists', False)
            },
            'tables': {
                'yours': your_data.get('has_tables', False),
                'competitor': competitor_data.get('has_tables', False),
                'gap': competitor_data.get('has_tables', False) and not your_data.get('has_tables', False)
            }
        }
        
        return elements
    
    def _compare_readability(self, your_content, competitor_content):
        """Compare readability metrics"""
        import textstat
        
        try:
            your_ease = textstat.flesch_reading_ease(your_content)
            comp_ease = textstat.flesch_reading_ease(competitor_content)
            
            your_grade = textstat.flesch_kincaid_grade(your_content)
            comp_grade = textstat.flesch_kincaid_grade(competitor_content)
            
            return {
                'your_readability': round(your_ease, 1),
                'competitor_readability': round(comp_ease, 1),
                'your_grade_level': round(your_grade, 1),
                'competitor_grade_level': round(comp_grade, 1),
                'comparison': 'easier' if your_ease > comp_ease else 'harder'
            }
        except:
            return {
                'your_readability': 0,
                'competitor_readability': 0,
                'your_grade_level': 0,
                'competitor_grade_level': 0,
                'comparison': 'unknown'
            }
    
    def _generate_gap_recommendations(self, structural, topics, elements, readability):
        """Generate actionable recommendations based on gaps"""
        recommendations = []
        
        # Word count recommendations
        word_gap = structural['word_count']['gap']
        if word_gap > 500:
            recommendations.append(f"Expand content by ~{word_gap} words to match competitor depth")
        elif word_gap < -500:
            recommendations.append("Your content is longer - ensure it's not repetitive")
        
        # Header recommendations
        header_gap = structural['headers']['gap']
        if header_gap > 2:
            recommendations.append(f"Add {header_gap} more section headers to improve structure")
        
        # Topic coverage
        if topics.get('unique_to_competitor'):
            missing_topics = ', '.join(topics['unique_to_competitor'][:3])
            recommendations.append(f"Cover these competitor topics: {missing_topics}")
        
        # Element gaps
        if elements['images']['gap']:
            recommendations.append("Add relevant images - competitor has visual content")
        
        if elements['videos']['gap']:
            recommendations.append("Consider adding video content for better engagement")
        
        if elements['lists']['gap']:
            recommendations.append("Add bullet points or numbered lists for scannability")
        
        if elements['tables']['gap']:
            recommendations.append("Include comparison tables or data visualizations")
        
        # Readability
        if readability['comparison'] == 'harder':
            recommendations.append("Simplify language - competitor content is easier to read")
        
        return recommendations[:8]  # Top 8 most important
    
    def _calculate_gap_score(self, structural, topics, elements):
        """
        Calculate overall gap score (0-100)
        Lower score = more gaps = more work needed
        Higher score = fewer gaps = competitive content
        """
        score = 100
        
        # Word count penalty (max -20)
        word_percentage = structural['word_count']['percentage']
        if word_percentage < 50:
            score -= 20
        elif word_percentage < 70:
            score -= 15
        elif word_percentage < 90:
            score -= 10
        
        # Topic coverage penalty (max -30)
        similarity = topics.get('similarity', 50)
        if similarity < 30:
            score -= 30
        elif similarity < 50:
            score -= 20
        elif similarity < 70:
            score -= 10
        
        # Element gaps penalty (max -20, 5 per element)
        for element_type, data in elements.items():
            if data['gap']:
                score -= 5
        
        # Header gap penalty (max -10)
        header_gap = structural['headers']['gap']
        if header_gap > 3:
            score -= 10
        elif header_gap > 1:
            score -= 5
        
        return max(0, min(100, score))
    
    def _interpret_gap_score(self, score):
        """Interpret the gap score"""
        if score >= 80:
            return "Excellent - Your content is highly competitive"
        elif score >= 60:
            return "Good - Minor improvements needed"
        elif score >= 40:
            return "Needs Work - Several gaps to address"
        else:
            return "Significant Gaps - Major improvements required"
