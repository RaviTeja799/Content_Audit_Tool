import re
from collections import Counter

class EntityAnalyzer:
    def __init__(self):
        # Common entity patterns (simplified NER without heavy dependencies)
        self.org_indicators = ['Inc', 'Corp', 'LLC', 'Ltd', 'Company', 'Corporation', 'Group']
        self.tech_brands = ['Google', 'Microsoft', 'Apple', 'Amazon', 'Facebook', 'Twitter', 
                           'LinkedIn', 'Netflix', 'Tesla', 'OpenAI', 'Meta', 'YouTube']
    
    def analyze(self, text):
        score = 50
        feedback = []
        issues = []
        
        # Extract capitalized words (potential entities)
        capitalized_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Remove common sentence starters
        sentence_starters = {'The', 'This', 'That', 'These', 'Those', 'A', 'An', 'In', 'On', 'At', 'For'}
        entities = [word for word in capitalized_words if word not in sentence_starters]
        
        # Count entity frequency
        entity_counts = Counter(entities)
        unique_entities = len(entity_counts)
        
        # Detect organizations
        organizations = []
        for entity in entities:
            if any(indicator in entity for indicator in self.org_indicators):
                organizations.append(entity)
        
        # Detect tech brands
        tech_mentions = [brand for brand in self.tech_brands if brand in text]
        
        # Scoring
        if unique_entities > 10:
            score += 20
            feedback.append(f'Excellent entity coverage with {unique_entities} unique entities mentioned')
        elif unique_entities > 5:
            score += 10
            feedback.append(f'Good entity mentions: {unique_entities} unique entities')
        else:
            score -= 10
            issues.append('Limited entity mentions - add more specific names and brands')
            feedback.append('Consider adding more specific entities (people, companies, products)')
        
        # Check for authoritative sources
        if any(name in text for name in ['Harvard', 'Stanford', 'MIT', 'Forbes', 'Reuters', 'Bloomberg']):
            score += 10
            feedback.append('Authoritative sources mentioned - adds credibility')
        
        # Organization mentions
        if len(organizations) > 0:
            score += 5
            feedback.append(f'{len(organizations)} organization(s) mentioned')
        
        # Tech brand mentions
        if len(tech_mentions) > 0:
            feedback.append(f'Tech brands mentioned: {", ".join(tech_mentions[:3])}')
        
        # Entity repetition analysis
        most_common = entity_counts.most_common(3)
        if most_common and most_common[0][1] > 5:
            issues.append(f'Entity "{most_common[0][0]}" mentioned {most_common[0][1]} times - consider varying references')
            score -= 5
        
        score = max(0, min(100, score))
        
        return {
            'score': round(score),
            'unique_entities': unique_entities,
            'total_mentions': len(entities),
            'top_entities': [{'name': name, 'count': count} for name, count in most_common],
            'organizations': list(set(organizations)),
            'tech_brands': tech_mentions,
            'feedback': feedback,
            'issues': issues
        }
