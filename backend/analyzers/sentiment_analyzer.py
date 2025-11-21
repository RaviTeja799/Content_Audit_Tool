import re
from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self):
        self.positive_words = ['best', 'great', 'excellent', 'amazing', 'perfect', 'outstanding', 
                               'fantastic', 'wonderful', 'superb', 'brilliant', 'exceptional']
        self.negative_words = ['worst', 'bad', 'terrible', 'awful', 'poor', 'horrible', 
                               'disappointing', 'useless', 'waste', 'avoid']
    
    def analyze(self, text):
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
        except:
            polarity = 0
            subjectivity = 0.5
        
        score = 50
        feedback = []
        issues = []
        
        # Tone classification
        if polarity > 0.1:
            tone = 'positive'
            tone_score = min(100, 50 + (polarity * 50))
        elif polarity < -0.1:
            tone = 'negative'
            tone_score = max(0, 50 + (polarity * 50))
        else:
            tone = 'neutral'
            tone_score = 50
        
        score = tone_score
        
        # Subjectivity analysis
        if subjectivity > 0.7:
            feedback.append('Content is highly subjective - consider adding more factual data')
            score -= 10
            issues.append('High subjectivity detected')
        elif subjectivity < 0.3:
            feedback.append('Content is very objective - good for informational content')
            score += 5
        
        # Emotional language detection
        text_lower = text.lower()
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        
        if positive_count > 5:
            feedback.append('Good use of positive language to engage readers')
            score += 5
        
        if negative_count > 3:
            feedback.append('Consider reducing negative language unless reviewing products')
            score -= 5
            issues.append('Excessive negative language')
        
        # Sentence variety (emotional range)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) > 5:
            exclamations = text.count('!')
            questions = text.count('?')
            
            if exclamations > len(sentences) * 0.2:
                feedback.append('Too many exclamations - reduce for professional tone')
                score -= 5
                issues.append('Overuse of exclamation marks')
            elif exclamations > 0:
                feedback.append('Good use of exclamations for emphasis')
                score += 3
            
            if questions > 0:
                feedback.append('Questions engage readers effectively')
                score += 5
        
        # Final score clamping
        score = max(0, min(100, score))
        
        return {
            'score': round(score),
            'tone': tone,
            'polarity': round(polarity, 2),
            'subjectivity': round(subjectivity, 2),
            'positive_words': positive_count,
            'negative_words': negative_count,
            'feedback': feedback,
            'issues': issues
        }
