import re
from datetime import datetime

class FreshnessAnalyzer:
    def __init__(self):
        self.current_year = datetime.now().year
        self.months = ['january', 'february', 'march', 'april', 'may', 'june',
                      'july', 'august', 'september', 'october', 'november', 'december']
        self.time_indicators = ['today', 'yesterday', 'recent', 'latest', 'current', 
                               'now', 'currently', 'recently', 'new', 'updated']
    
    def analyze(self, text):
        score = 50
        feedback = []
        issues = []
        text_lower = text.lower()
        
        # Find year mentions
        years = re.findall(r'\b(19|20)\d{2}\b', text)
        years = [int(year) for year in years]
        
        latest_year = max(years) if years else 0
        year_count = len(years)
        
        # Scoring based on year mentions
        if latest_year >= self.current_year:
            score += 30
            feedback.append(f'Content references current year ({self.current_year}) - excellent freshness')
        elif latest_year >= self.current_year - 1:
            score += 20
            feedback.append(f'Content references recent year ({latest_year}) - good freshness')
        elif latest_year >= self.current_year - 2:
            score += 10
            feedback.append(f'Content includes {latest_year} - moderately fresh')
        elif latest_year > 0:
            score -= 20
            issues.append(f'Content references outdated year ({latest_year}) - needs updating')
            feedback.append('Update content with current year information')
        else:
            score -= 10
            issues.append('No year mentions found - readers cannot assess timeliness')
            feedback.append('Add current year references to establish freshness')
        
        # Time indicators
        time_indicator_count = sum(1 for indicator in self.time_indicators if indicator in text_lower)
        if time_indicator_count >= 3:
            score += 10
            feedback.append('Good use of temporal indicators (recent, latest, current)')
        elif time_indicator_count == 0:
            score -= 5
            issues.append('No time indicators found')
        
        # Month mentions (seasonal content)
        month_mentions = [month for month in self.months if month in text_lower]
        if month_mentions:
            feedback.append(f'Seasonal references detected: {", ".join(month_mentions[:3])}')
        
        # Date patterns (MM/DD/YYYY, DD-MM-YYYY, etc.)
        date_patterns = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
        if date_patterns:
            score += 5
            feedback.append('Specific dates mentioned - adds credibility')
        
        # Statistics and numbers (often time-sensitive)
        stats_pattern = r'\b\d+(?:,\d{3})*(?:\.\d+)?%?\b'
        stats = re.findall(stats_pattern, text)
        if len(stats) > 10:
            feedback.append('Rich in statistics - ensure they are current')
            if latest_year < self.current_year - 1:
                issues.append('Statistics may be outdated - verify data recency')
                score -= 10
        
        # Publication indicators
        if any(phrase in text_lower for phrase in ['published', 'updated', 'last updated', 'as of']):
            score += 5
            feedback.append('Publication/update dates indicated')
        
        score = max(0, min(100, score))
        
        return {
            'score': round(score),
            'latest_year': latest_year,
            'year_mentions': year_count,
            'time_indicators': time_indicator_count,
            'has_dates': len(date_patterns) > 0,
            'seasonal_content': len(month_mentions) > 0,
            'feedback': feedback,
            'issues': issues
        }
