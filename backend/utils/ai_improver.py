import os
import requests
from groq import Groq

class AIContentImprover:
    """AI-powered content improvement suggestions using Groq (fast & free)"""
    
    def __init__(self):
        # Groq API (Fast inference with Llama models)
        self.groq_api_key = os.getenv('GROQ_API_KEY', '')
        self.groq_client = None
        
        if self.groq_api_key:
            try:
                self.groq_client = Groq(api_key=self.groq_api_key)
            except Exception as e:
                print(f"Failed to initialize Groq client: {str(e)}")
                self.groq_client = None
        
        # Gemini API (Backup)
        self.gemini_api_key = os.getenv('GEMINI_API_KEY', '')
    
    def analyze_and_suggest(self, content, analysis_results):
        """
        Analyze content and provide AI-powered improvement suggestions
        
        Args:
            content: The content text
            analysis_results: Full analysis results from audit
            
        Returns:
            Dict with suggestions for improvement
        """
        print("Generating AI-powered content suggestions...")
        
        # Identify weak areas
        weak_areas = self._identify_weak_areas(analysis_results)
        
        if not weak_areas:
            return {
                'status': 'excellent',
                'message': 'Your content is performing well across all dimensions!',
                'suggestions': []
            }
        
        # Generate suggestions for each weak area
        suggestions = []
        
        for area in weak_areas:
            suggestion = self._generate_suggestion(content, area, analysis_results)
            if suggestion:
                suggestions.append(suggestion)
        
        return {
            'status': 'improvements_available',
            'weak_areas': weak_areas,
            'suggestions': suggestions,
            'priority_actions': self._prioritize_suggestions(suggestions)
        }
    
    def _identify_weak_areas(self, results):
        """Identify areas scoring below 60"""
        weak = []
        
        scores = {
            'SEO': results.get('seo', {}).get('score', 100),
            'SERP Performance': results.get('serp_performance', {}).get('score', 100),
            'AEO': results.get('aeo', {}).get('score', 100),
            'Humanization': results.get('humanization', {}).get('score', 100),
            'Differentiation': results.get('differentiation', {}).get('score', 100)
        }
        
        for area, score in scores.items():
            if score < 60:
                weak.append({
                    'area': area,
                    'score': score,
                    'severity': 'critical' if score < 40 else 'moderate'
                })
        
        return sorted(weak, key=lambda x: x['score'])
    
    def _generate_suggestion(self, content, weak_area, results):
        """Generate specific improvement suggestion using AI"""
        area_name = weak_area['area']
        score = weak_area['score']
        
        # Get specific issues for this area
        area_key = self._get_area_key(area_name)
        area_data = results.get(area_key, {})
        issues = area_data.get('issues', [])
        recommendations = area_data.get('recommendations', [])
        
        # Create focused prompt
        prompt = self._create_improvement_prompt(content, area_name, score, issues, recommendations)
        
        # Get AI suggestions
        ai_response = self._call_ai_api(prompt)
        
        if ai_response:
            return {
                'area': area_name,
                'score': score,
                'issues': issues[:3],
                'ai_suggestions': ai_response,
                'priority': 'high' if score < 40 else 'medium'
            }
        
        return None
    
    def _get_area_key(self, area_name):
        """Map area name to results key"""
        mapping = {
            'SEO': 'seo',
            'SERP Performance': 'serp_performance',
            'AEO': 'aeo',
            'Humanization': 'humanization',
            'Differentiation': 'differentiation'
        }
        return mapping.get(area_name, 'seo')
    
    def _create_improvement_prompt(self, content, area, score, issues, recommendations):
        """Create focused prompt for AI"""
        
        # Truncate content if too long
        content_preview = content[:1500] + "..." if len(content) > 1500 else content
        
        prompt = f"""You are an expert content strategist. Analyze this content and provide specific, actionable improvements for {area}.

Current Score: {score}/100

Content Preview:
{content_preview}

Identified Issues:
{chr(10).join(f"- {issue}" for issue in issues[:5])}

Recommendations:
{chr(10).join(f"- {rec}" for rec in recommendations[:5])}

Provide 3-5 specific, actionable improvements with examples:
1. What to change
2. Why it matters
3. Specific example or rewrite suggestion

Keep suggestions concise and practical."""

        return prompt
    
    def _call_ai_api(self, prompt):
        """Call AI API (Groq preferred, Gemini fallback)"""
        
        # Try Groq first (faster, free)
        if self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.1-70b-versatile",  # Fast and high quality
                    messages=[
                        {"role": "system", "content": "You are an expert content strategist providing actionable improvement suggestions."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                
                suggestion_text = response.choices[0].message.content
                return self._parse_ai_suggestions(suggestion_text)
            
            except Exception as e:
                print(f"Groq API error: {str(e)}, trying Gemini...")
        
        # Fallback to Gemini
        if self.gemini_api_key:
            try:
                response = requests.post(
                    f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_api_key}',
                    json={
                        'contents': [{
                            'parts': [{'text': prompt}]
                        }]
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    suggestion_text = data['candidates'][0]['content']['parts'][0]['text']
                    return self._parse_ai_suggestions(suggestion_text)
            
            except Exception as e:
                print(f"Gemini API error: {str(e)}")
        
        # Fallback to rule-based suggestions
        return self._generate_fallback_suggestions()
    
    def _parse_ai_suggestions(self, text):
        """Parse AI response into structured suggestions"""
        # Split by numbered points
        suggestions = []
        lines = text.split('\n')
        
        current_suggestion = ""
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                if current_suggestion:
                    suggestions.append(current_suggestion.strip())
                current_suggestion = line
            elif current_suggestion:
                current_suggestion += " " + line
        
        if current_suggestion:
            suggestions.append(current_suggestion.strip())
        
        return suggestions[:5]
    
    def _generate_fallback_suggestions(self):
        """Generate rule-based suggestions when AI is unavailable"""
        return [
            "Expand content depth with more detailed explanations and examples",
            "Add structured data markup (schema.org) for better search visibility",
            "Include more visual elements like images, infographics, or videos",
            "Break long paragraphs into shorter, scannable sections with subheadings",
            "Add internal and external links to authoritative sources"
        ]
    
    def _prioritize_suggestions(self, suggestions):
        """Prioritize suggestions by impact"""
        priority = []
        
        # Critical issues first
        for sugg in suggestions:
            if sugg.get('priority') == 'high':
                priority.append({
                    'area': sugg['area'],
                    'action': sugg['ai_suggestions'][0] if sugg['ai_suggestions'] else 'Improve ' + sugg['area'],
                    'impact': 'High - Will significantly improve score',
                    'effort': 'Medium'
                })
        
        return priority[:3]
    
    def rewrite_section(self, original_text, improvement_goal, context=""):
        """Generate rewritten version of a section"""
        
        prompt = f"""Rewrite this content section to {improvement_goal}.

Original text:
{original_text}

{f"Context: {context}" if context else ""}

Provide an improved version that:
- Maintains the core message
- {improvement_goal}
- Is more engaging and readable
- Uses active voice and clear language

Improved version:"""

        # Try Groq first
        if self.groq_client:
            try:
                print(f"Calling Groq API for rewrite with goal: {improvement_goal}")
                response = self.groq_client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert content editor."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                rewritten = response.choices[0].message.content.strip()
                print(f"Groq rewrite successful, generated {len(rewritten)} chars")
                return rewritten
            
            except Exception as e:
                print(f"Groq rewrite error: {str(e)}")
        else:
            print("Groq client not initialized - API key missing or invalid")
        
        # Try Gemini fallback
        if self.gemini_api_key:
            try:
                print(f"Trying Gemini API for rewrite...")
                response = requests.post(
                    f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_api_key}',
                    json={
                        'contents': [{
                            'parts': [{'text': prompt}]
                        }]
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    rewritten = data['candidates'][0]['content']['parts'][0]['text'].strip()
                    print(f"Gemini rewrite successful, generated {len(rewritten)} chars")
                    return rewritten
                else:
                    print(f"Gemini API error: {response.status_code} - {response.text}")
            
            except Exception as e:
                print(f"Gemini rewrite error: {str(e)}")
        else:
            print("Gemini API key not configured")
        
        print("WARNING: All AI APIs failed, returning original text")
        return original_text  # Return original if AI fails
    
    def generate_missing_section(self, topic, context, target_keyword=""):
        """Generate content for a missing section"""
        
        prompt = f"""Generate a well-written content section about: {topic}

Context: {context}
{f"Target Keyword: {target_keyword}" if target_keyword else ""}

Write a comprehensive paragraph (150-200 words) that:
- Covers the topic thoroughly
- Is informative and engaging
- Uses clear, professional language
- Includes relevant examples if applicable
{f"- Naturally incorporates '{target_keyword}'" if target_keyword else ""}

Section:"""

        if self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert content writer."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300,
                    temperature=0.8
                )
                
                return response.choices[0].message.content.strip()
            
            except Exception as e:
                print(f"Generation error: {str(e)}")
        
        return f"[Content about {topic} would go here]"
