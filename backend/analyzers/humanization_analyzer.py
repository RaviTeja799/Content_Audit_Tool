import re
import statistics
from collections import Counter

class HumanizationAnalyzer:
    """Analyze content for human-like writing patterns"""
    
    def analyze(self, text):
        """
        Analyze humanization aspects of content
        Returns dict with: score, issues, recommendations, details
        """
        issues = []
        recommendations = []
        details = {}
        
        # 1. Sentence Variety Analysis
        sentence_data = self._analyze_sentence_variety(text)
        details['sentence_variety'] = sentence_data
        
        if sentence_data['starter_repetition'] > 30:
            issues.append(f"{sentence_data['starter_repetition']:.0f}% sentences start the same way")
            recommendations.append("Vary sentence starters (use transitions, questions, different subjects)")
        
        if sentence_data['length_std_dev'] < 5:
            issues.append(f"Low sentence length variation (std dev {sentence_data['length_std_dev']:.1f})")
            recommendations.append("Mix short punchy sentences with longer complex ones")
        
        # 2. AI Pattern Detection
        ai_patterns = self._detect_ai_patterns(text)
        details['ai_patterns'] = ai_patterns
        
        if ai_patterns['ai_phrases_count'] > 5:
            issues.append(f"Contains {ai_patterns['ai_phrases_count']} AI-typical phrases")
            recommendations.append("Replace formal/robotic phrases with natural conversational language")
        
        if ai_patterns['overused_transitions'] > 3:
            issues.append("Overuse of transition phrases")
            recommendations.append("Reduce transition phrases like 'moreover', 'furthermore', 'in conclusion'")
        
        # 3. Natural Flow Analysis
        flow_data = self._analyze_natural_flow(text)
        details['flow'] = flow_data
        
        if not flow_data['has_contractions']:
            issues.append("No contractions used (sounds too formal)")
            recommendations.append("Use contractions (it's, don't, we'll) for natural tone")
        
        if flow_data['passive_voice_ratio'] > 20:
            issues.append(f"High passive voice usage ({flow_data['passive_voice_ratio']:.0f}%)")
            recommendations.append("Use more active voice for engaging writing")
        
        # 4. Vocabulary Analysis
        vocab_data = self._analyze_vocabulary(text)
        details['vocabulary'] = vocab_data
        
        if vocab_data['unique_word_ratio'] < 40:
            issues.append("Low vocabulary diversity (repetitive wording)")
            recommendations.append("Use synonyms and varied expressions")
        
        # 5. Conversational Elements
        conversational_data = self._analyze_conversational_elements(text)
        details['conversational'] = conversational_data
        
        if conversational_data['personal_pronouns'] == 0:
            issues.append("No personal pronouns (lacks human connection)")
            recommendations.append("Use 'you', 'we', 'I' to connect with readers")
        
        # Calculate score
        score = self._calculate_humanization_score(sentence_data, ai_patterns, flow_data, vocab_data, conversational_data)
        
        return {
            'score': score,
            'issues': issues,
            'recommendations': recommendations[:3],
            'details': details,
            'good_points': self._get_good_points(sentence_data, ai_patterns, flow_data, conversational_data)
        }
    
    def _analyze_sentence_variety(self, text):
        """Analyze sentence structure variety"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if not sentences:
            return {'starter_repetition': 0, 'avg_length': 0, 'length_std_dev': 0}
        
        # Analyze sentence starters
        starters = []
        for sentence in sentences:
            words = sentence.split()
            if words:
                # Get first 1-2 words as starter
                starter = ' '.join(words[:2]).lower()
                starters.append(starter)
        
        # Calculate starter repetition
        if starters:
            starter_counts = Counter(starters)
            most_common_count = starter_counts.most_common(1)[0][1]
            starter_repetition = (most_common_count / len(starters) * 100)
        else:
            starter_repetition = 0
        
        # Analyze sentence lengths
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_length = statistics.mean(sentence_lengths) if sentence_lengths else 0
        length_std_dev = statistics.stdev(sentence_lengths) if len(sentence_lengths) > 1 else 0
        
        return {
            'starter_repetition': starter_repetition,
            'avg_length': avg_length,
            'length_std_dev': length_std_dev,
            'total_sentences': len(sentences)
        }
    
    def _detect_ai_patterns(self, text):
        """Detect common AI writing patterns"""
        text_lower = text.lower()
        
        # Common AI phrases
        ai_phrases = [
            'it is important to note',
            'it is worth noting',
            'in today\'s digital age',
            'in today\'s world',
            'in recent years',
            'increasingly important',
            'vast array of',
            'plethora of',
            'myriad of',
            'a wide range of',
            'it should be noted',
            'one must consider',
            'delve into',
            'dive deep into',
            'comprehensive guide',
            'in this article, we will',
            'in this blog post',
            'as technology continues to evolve',
            'revolutionary',
            'game-changing',
            'cutting-edge',
            'state-of-the-art'
        ]
        
        ai_phrases_count = sum(1 for phrase in ai_phrases if phrase in text_lower)
        
        # Overused transitions
        formal_transitions = [
            'moreover', 'furthermore', 'nevertheless', 'nonetheless',
            'consequently', 'therefore', 'thus', 'hence'
        ]
        
        overused_transitions = sum(text_lower.count(word) for word in formal_transitions)
        
        # Check for repetitive structure (every paragraph starts the same)
        paragraphs = text.split('\n\n')
        paragraph_starters = [p.split()[0].lower() for p in paragraphs if p.strip() and len(p.split()) > 0]
        starter_variety = len(set(paragraph_starters)) / len(paragraph_starters) if paragraph_starters else 1
        
        return {
            'ai_phrases_count': ai_phrases_count,
            'overused_transitions': overused_transitions,
            'paragraph_starter_variety': starter_variety
        }
    
    def _analyze_natural_flow(self, text):
        """Analyze natural flow and voice"""
        # Check for contractions
        contractions = ["n't", "'ll", "'ve", "'re", "'m", "'d", "'s"]
        has_contractions = any(contraction in text for contraction in contractions)
        contraction_count = sum(text.count(c) for c in contractions)
        
        # Detect passive voice (simplified)
        passive_patterns = [
            r'\b(?:was|were|is|are|been|be)\s+\w+ed\b',
            r'\b(?:was|were|is|are|been|be)\s+\w+en\b'
        ]
        passive_matches = sum(len(re.findall(pattern, text)) for pattern in passive_patterns)
        total_sentences = len(re.split(r'[.!?]+', text))
        passive_voice_ratio = (passive_matches / total_sentences * 100) if total_sentences > 0 else 0
        
        # Check for questions (engaging element)
        question_count = text.count('?')
        
        # Check for exclamations (emotion)
        exclamation_count = text.count('!')
        
        return {
            'has_contractions': has_contractions,
            'contraction_count': contraction_count,
            'passive_voice_ratio': passive_voice_ratio,
            'question_count': question_count,
            'exclamation_count': exclamation_count
        }
    
    def _analyze_vocabulary(self, text):
        """Analyze vocabulary diversity"""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        if not words:
            return {'unique_word_ratio': 0, 'total_words': 0, 'unique_words': 0}
        
        unique_words = set(words)
        unique_word_ratio = (len(unique_words) / len(words) * 100)
        
        # Check for repeated words (excluding common words)
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out', 'this', 'that', 'with'}
        content_words = [w for w in words if w not in common_words]
        
        if content_words:
            word_counts = Counter(content_words)
            most_repeated = word_counts.most_common(5)
        else:
            most_repeated = []
        
        return {
            'unique_word_ratio': unique_word_ratio,
            'total_words': len(words),
            'unique_words': len(unique_words),
            'most_repeated': most_repeated
        }
    
    def _analyze_conversational_elements(self, text):
        """Analyze conversational writing elements"""
        text_lower = text.lower()
        
        # Count personal pronouns
        personal_pronouns = ['i', 'we', 'you', 'my', 'our', 'your']
        personal_pronouns_count = sum(len(re.findall(r'\b' + pronoun + r'\b', text_lower)) for pronoun in personal_pronouns)
        
        # Check for direct address
        has_direct_address = bool(re.search(r'\byou\b', text_lower))
        
        # Check for storytelling elements
        storytelling_words = ['story', 'example', 'instance', 'case', 'experience', 'time when']
        has_storytelling = any(word in text_lower for word in storytelling_words)
        
        # Check for conversational phrases
        conversational_phrases = [
            'let\'s', 'here\'s', 'there\'s', 'what\'s', 'that\'s',
            'you know', 'think about', 'imagine', 'picture this',
            'by the way', 'in fact', 'actually', 'basically'
        ]
        conversational_count = sum(1 for phrase in conversational_phrases if phrase in text_lower)
        
        return {
            'personal_pronouns': personal_pronouns_count,
            'has_direct_address': has_direct_address,
            'has_storytelling': has_storytelling,
            'conversational_count': conversational_count
        }
    
    def _calculate_humanization_score(self, sentence_data, ai_patterns, flow_data, vocab_data, conversational_data):
        """Calculate humanization score (0-100)"""
        score = 100
        
        # Sentence variety (25 points)
        if sentence_data['starter_repetition'] > 40:
            score -= 15
        elif sentence_data['starter_repetition'] > 30:
            score -= 10
        elif sentence_data['starter_repetition'] > 20:
            score -= 5
        
        if sentence_data['length_std_dev'] < 3:
            score -= 15
        elif sentence_data['length_std_dev'] < 5:
            score -= 10
        
        # AI patterns (30 points)
        if ai_patterns['ai_phrases_count'] > 8:
            score -= 20
        elif ai_patterns['ai_phrases_count'] > 5:
            score -= 15
        elif ai_patterns['ai_phrases_count'] > 3:
            score -= 8
        
        if ai_patterns['overused_transitions'] > 5:
            score -= 10
        elif ai_patterns['overused_transitions'] > 3:
            score -= 5
        
        # Natural flow (25 points)
        if not flow_data['has_contractions']:
            score -= 10
        
        if flow_data['passive_voice_ratio'] > 25:
            score -= 10
        elif flow_data['passive_voice_ratio'] > 20:
            score -= 5
        
        if flow_data['question_count'] == 0:
            score -= 5
        
        # Vocabulary (10 points)
        if vocab_data['unique_word_ratio'] < 30:
            score -= 10
        elif vocab_data['unique_word_ratio'] < 40:
            score -= 5
        
        # Conversational elements (10 points)
        if conversational_data['personal_pronouns'] == 0:
            score -= 10
        elif conversational_data['conversational_count'] == 0:
            score -= 5
        
        return max(0, score)
    
    def _get_good_points(self, sentence_data, ai_patterns, flow_data, conversational_data):
        """Identify positive aspects"""
        good_points = []
        
        if sentence_data['length_std_dev'] >= 7:
            good_points.append("Excellent sentence variety")
        
        if sentence_data['starter_repetition'] < 20:
            good_points.append("Diverse sentence starters")
        
        if ai_patterns['ai_phrases_count'] <= 2:
            good_points.append("Minimal AI-typical phrases")
        
        if flow_data['has_contractions'] and flow_data['contraction_count'] >= 3:
            good_points.append("Natural use of contractions")
        
        if flow_data['passive_voice_ratio'] < 15:
            good_points.append("Strong active voice usage")
        
        if conversational_data['personal_pronouns'] > 10:
            good_points.append("Conversational and engaging tone")
        
        if flow_data['question_count'] >= 3:
            good_points.append("Engaging use of questions")
        
        return good_points
