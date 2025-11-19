import re
from urllib.parse import urlparse

class AEOAnalyzer:
    """Analyze content for Answer Engine Optimization (AEO)"""
    
    def analyze(self, text, headers):
        """
        Analyze AEO aspects of content
        Returns dict with: score, issues, recommendations, details
        """
        issues = []
        recommendations = []
        details = {}
        
        # 1. Citation Analysis
        citation_data = self._analyze_citations(text)
        details['citations'] = citation_data
        
        if citation_data['count'] == 0:
            issues.append("No citations or sources found")
            recommendations.append("Add 3-5 credible sources with links to authoritative sites")
        elif citation_data['count'] < 3:
            issues.append(f"Only {citation_data['count']} citation(s) found")
            recommendations.append("Add more citations to establish credibility (aim for 5+)")
        
        # 2. Structured Data/Formatting
        structured_data = self._analyze_structured_formatting(text, headers)
        details['structured_data'] = structured_data
        
        if not structured_data['has_faq']:
            issues.append("No FAQ section detected")
            recommendations.append("Add FAQ section with schema markup for featured snippets")
        
        if not structured_data['has_lists']:
            issues.append("No bullet points or numbered lists")
            recommendations.append("Use lists for better AI parsing and featured snippet potential")
        
        # 3. Answer-Style Content
        answer_data = self._analyze_answer_patterns(text)
        details['answer_patterns'] = answer_data
        
        if answer_data['direct_answers'] == 0:
            issues.append("No direct answer patterns found")
            recommendations.append("Start with direct answers to questions (e.g., 'The best way to...')")
        
        # 4. Question Coverage
        question_data = self._analyze_questions(text)
        details['questions'] = question_data
        
        if question_data['questions_answered'] < 3:
            issues.append(f"Only {question_data['questions_answered']} question(s) addressed")
            recommendations.append("Answer 5+ common questions for better AEO coverage")
        
        # 5. Semantic Richness
        semantic_data = self._analyze_semantic_richness(text)
        details['semantic'] = semantic_data
        
        # Calculate score
        score = self._calculate_aeo_score(citation_data, structured_data, answer_data, question_data, semantic_data)
        
        return {
            'score': score,
            'issues': issues,
            'recommendations': recommendations[:3],
            'details': details,
            'good_points': self._get_good_points(citation_data, structured_data, answer_data, question_data)
        }
    
    def _analyze_citations(self, text):
        """Analyze citations and source quality"""
        # Find URLs
        url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
        urls = re.findall(url_pattern, text)
        
        # Find reference patterns
        reference_patterns = [
            r'\[[\d]+\]',  # [1], [2]
            r'\([\d]+\)',  # (1), (2)
            r'according to\s+[\w\s]+',
            r'source:\s*[\w\s]+',
            r'via\s+[\w\s]+'
        ]
        
        reference_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in reference_patterns)
        
        # Check for authoritative domains
        authoritative_domains = ['gov', 'edu', 'org']
        authoritative_sources = sum(1 for url in urls if any(domain in url for domain in authoritative_domains))
        
        total_citations = len(urls) + reference_count
        
        return {
            'count': total_citations,
            'urls': len(urls),
            'authoritative_sources': authoritative_sources,
            'has_quality_sources': authoritative_sources > 0
        }
    
    def _analyze_structured_formatting(self, text, headers):
        """Analyze structured data and formatting"""
        # Check for FAQ patterns
        faq_patterns = [
            r'(?:^|\n)(?:Q:|Question:|\?)\s*.+',
            r'(?:Frequently Asked Questions|FAQ)',
            r'(?:^|\n)(?:A:|Answer:)\s*.+'
        ]
        has_faq = any(re.search(pattern, text, re.IGNORECASE | re.MULTILINE) for pattern in faq_patterns)
        
        # Check for lists
        has_lists = bool(re.search(r'(?:\n\s*[-•*]\s+|\n\s*\d+\.\s+)', text))
        list_count = len(re.findall(r'(?:\n\s*[-•*]\s+|\n\s*\d+\.\s+)', text))
        
        # Check for how-to patterns
        has_howto = bool(re.search(r'(?:how to|step \d+|steps?:)', text, re.IGNORECASE))
        
        # Check for tables/comparisons
        has_tables = bool(re.search(r'\|.+\|.+\|', text))  # Markdown table pattern
        
        # Header structure (important for AEO)
        has_proper_headers = len(headers) >= 3
        
        return {
            'has_faq': has_faq,
            'has_lists': has_lists,
            'list_count': list_count,
            'has_howto': has_howto,
            'has_tables': has_tables,
            'has_proper_headers': has_proper_headers
        }
    
    def _analyze_answer_patterns(self, text):
        """Analyze direct answer patterns"""
        # Patterns that indicate direct answers
        answer_patterns = [
            r'(?:^|\n)(?:The best|The top|The most|The main)',
            r'(?:^|\n)(?:In short|Simply put|To summarize)',
            r'(?:^|\n)(?:Yes|No),\s+\w+',
            r'\b(?:is|are)\s+(?:defined as|known as|called)',
            r'(?:The answer is|The result is|This means)'
        ]
        
        direct_answers = sum(len(re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)) for pattern in answer_patterns)
        
        # Check for definition patterns
        has_definition = bool(re.search(r'\b(?:is|are)\s+(?:defined as|known as|a type of)', text, re.IGNORECASE))
        
        # Check for concise summaries at start
        first_paragraph = text.split('\n\n')[0] if '\n\n' in text else text[:500]
        has_early_answer = len(first_paragraph.split()) < 100  # Concise intro
        
        return {
            'direct_answers': direct_answers,
            'has_definition': has_definition,
            'has_early_answer': has_early_answer
        }
    
    def _analyze_questions(self, text):
        """Analyze question coverage"""
        # Find questions
        questions = re.findall(r'[^.!?]*\?', text)
        
        # Common question words
        question_words = ['what', 'why', 'how', 'when', 'where', 'who', 'which']
        questions_with_keywords = [q for q in questions if any(word in q.lower() for word in question_words)]
        
        # Estimate answered questions (questions followed by content)
        questions_answered = len(questions_with_keywords)
        
        return {
            'total_questions': len(questions),
            'questions_answered': questions_answered
        }
    
    def _analyze_semantic_richness(self, text):
        """Analyze semantic richness for AI understanding"""
        # Entity density (proper nouns, brands, etc.)
        words = text.split()
        capitalized_words = [w for w in words if w and w[0].isupper() and len(w) > 2]
        entity_density = (len(capitalized_words) / len(words) * 100) if words else 0
        
        # Sentence completeness (sentences with subject-verb)
        sentences = re.split(r'[.!?]+', text)
        complete_sentences = [s for s in sentences if len(s.split()) >= 5]
        completeness_ratio = (len(complete_sentences) / len(sentences)) if sentences else 0
        
        return {
            'entity_density': entity_density,
            'completeness_ratio': completeness_ratio
        }
    
    def _calculate_aeo_score(self, citation_data, structured_data, answer_data, question_data, semantic_data):
        """Calculate AEO score (0-100)"""
        score = 100
        
        # Citations (25 points)
        if citation_data['count'] == 0:
            score -= 25
        elif citation_data['count'] < 3:
            score -= 15
        elif citation_data['count'] < 5:
            score -= 8
        
        if not citation_data['has_quality_sources']:
            score -= 5
        
        # Structured formatting (30 points)
        if not structured_data['has_faq']:
            score -= 12
        if not structured_data['has_lists']:
            score -= 10
        if not structured_data['has_proper_headers']:
            score -= 8
        
        # Answer patterns (25 points)
        if answer_data['direct_answers'] == 0:
            score -= 15
        elif answer_data['direct_answers'] < 3:
            score -= 8
        
        if not answer_data['has_definition']:
            score -= 5
        if not answer_data['has_early_answer']:
            score -= 5
        
        # Question coverage (20 points)
        if question_data['questions_answered'] == 0:
            score -= 20
        elif question_data['questions_answered'] < 3:
            score -= 12
        elif question_data['questions_answered'] < 5:
            score -= 6
        
        return max(0, score)
    
    def _get_good_points(self, citation_data, structured_data, answer_data, question_data):
        """Identify positive aspects"""
        good_points = []
        
        if citation_data['count'] >= 5:
            good_points.append(f"{citation_data['count']} citations with sources")
        
        if citation_data['has_quality_sources']:
            good_points.append("Authoritative sources present (.gov/.edu/.org)")
        
        if structured_data['has_faq']:
            good_points.append("FAQ section present")
        
        if structured_data['has_lists'] and structured_data['list_count'] >= 3:
            good_points.append("Well-formatted with lists for scannability")
        
        if answer_data['direct_answers'] >= 3:
            good_points.append("Direct answer patterns present")
        
        if question_data['questions_answered'] >= 5:
            good_points.append(f"Answers {question_data['questions_answered']} questions")
        
        return good_points
