import re
import hashlib
from collections import defaultdict

class PlagiarismChecker:
    def __init__(self):
        self.ngram_size = 8
    
    def analyze(self, text):
        score = 100
        feedback = []
        issues = []
        
        # Clean text
        text_clean = re.sub(r'[^\w\s]', '', text.lower())
        words = text_clean.split()
        
        if len(words) < 50:
            return {
                'score': 100,
                'uniqueness': 100,
                'duplicate_phrases': 0,
                'feedback': ['Text too short for plagiarism analysis'],
                'issues': []
            }
        
        # Generate n-grams (phrases)
        ngrams = []
        for i in range(len(words) - self.ngram_size + 1):
            ngram = ' '.join(words[i:i + self.ngram_size])
            ngrams.append(ngram)
        
        # Count phrase frequency (self-plagiarism detection)
        phrase_counts = defaultdict(int)
        for ngram in ngrams:
            phrase_counts[ngram] += 1
        
        # Find repeated phrases
        repeated_phrases = {phrase: count for phrase, count in phrase_counts.items() if count > 1}
        
        if len(repeated_phrases) > 0:
            duplicate_ratio = len(repeated_phrases) / len(phrase_counts) if len(phrase_counts) > 0 else 0
            
            if duplicate_ratio > 0.3:
                score -= 40
                issues.append('High content repetition detected')
                feedback.append('Significant phrase repetition - rewrite for originality')
            elif duplicate_ratio > 0.15:
                score -= 20
                issues.append('Moderate content repetition')
                feedback.append('Some phrases are repeated - consider varying language')
            
            feedback.append(f'{len(repeated_phrases)} repeated phrases detected')
        else:
            feedback.append('No significant phrase repetition detected')
        
        # Check for boilerplate content patterns
        boilerplate_patterns = [
            r'click here',
            r'subscribe to our newsletter',
            r'leave a comment below',
            r'follow us on',
            r'share this post',
            r'copyright \d{4}'
        ]
        
        boilerplate_count = sum(1 for pattern in boilerplate_patterns if re.search(pattern, text.lower()))
        if boilerplate_count > 2:
            score -= 5
            feedback.append('Contains standard boilerplate content')
        
        # Generic phrase detection
        generic_phrases = [
            'in conclusion', 'in summary', 'as we have seen', 'it is important to note',
            'it goes without saying', 'needless to say', 'at the end of the day'
        ]
        
        generic_count = sum(1 for phrase in generic_phrases if phrase in text.lower())
        if generic_count > 3:
            score -= 10
            issues.append('Overuse of generic phrases')
            feedback.append('Reduce generic filler phrases for more original content')
        
        # Calculate uniqueness score
        uniqueness = 100 - (len(repeated_phrases) / len(phrase_counts) * 100 if len(phrase_counts) > 0 else 0)
        uniqueness = max(0, min(100, uniqueness))
        
        score = max(0, min(100, score))
        
        return {
            'score': round(score),
            'uniqueness': round(uniqueness),
            'duplicate_phrases': len(repeated_phrases),
            'total_phrases': len(phrase_counts),
            'boilerplate_detected': boilerplate_count > 0,
            'feedback': feedback,
            'issues': issues
        }
