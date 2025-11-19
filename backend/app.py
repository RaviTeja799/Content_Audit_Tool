from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analyzers.seo_analyzer import SEOAnalyzer
from analyzers.serp_analyzer import SERPAnalyzer
from analyzers.aeo_analyzer import AEOAnalyzer
from analyzers.humanization_analyzer import HumanizationAnalyzer
from analyzers.differentiation_analyzer import DifferentiationAnalyzer
from utils.text_extractor import TextExtractor

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Content Audit API is running"})

@app.route('/api/analyze', methods=['POST'])
def analyze_content():
    try:
        data = request.json
        input_data = data.get('input', '')
        target_keyword = data.get('target_keyword', '')
        
        if not input_data:
            return jsonify({"error": "No input provided"}), 400
        
        # Extract text and metadata
        extractor = TextExtractor()
        content_data = extractor.extract(input_data)
        
        if not content_data['text']:
            return jsonify({"error": "Could not extract text from input"}), 400
        
        text = content_data['text']
        url = content_data.get('url')
        headers = content_data.get('headers', [])
        meta_description = content_data.get('meta_description', '')
        
        # Auto-detect target keyword if not provided
        if not target_keyword and headers:
            target_keyword = headers[0] if headers else ''
        
        # Initialize analyzers
        seo_analyzer = SEOAnalyzer()
        serp_analyzer = SERPAnalyzer()
        aeo_analyzer = AEOAnalyzer()
        humanization_analyzer = HumanizationAnalyzer()
        differentiation_analyzer = DifferentiationAnalyzer()
        
        # Run all analyses
        seo_result = seo_analyzer.analyze(text, headers, meta_description, target_keyword)
        serp_result = serp_analyzer.analyze(text, target_keyword, url)
        aeo_result = aeo_analyzer.analyze(text, headers)
        humanization_result = humanization_analyzer.analyze(text)
        differentiation_result = differentiation_analyzer.analyze(text, target_keyword)
        
        # Compile results
        results = {
            "input_type": "url" if content_data.get('is_url') else "text",
            "url": url,
            "word_count": len(text.split()),
            "target_keyword": target_keyword,
            "seo": seo_result,
            "serp_performance": serp_result,
            "aeo": aeo_result,
            "humanization": humanization_result,
            "differentiation": differentiation_result,
            "overall_score": calculate_overall_score([
                seo_result['score'],
                serp_result['score'],
                aeo_result['score'],
                humanization_result['score'],
                differentiation_result['score']
            ])
        }
        
        return jsonify(results)
    
    except Exception as e:
        print(f"Error in analyze_content: {str(e)}")
        return jsonify({"error": str(e)}), 500

def calculate_overall_score(scores):
    """Calculate weighted average of all scores"""
    weights = [0.25, 0.25, 0.15, 0.15, 0.20]  # SEO, SERP, AEO, Human, Diff
    weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
    return round(weighted_sum, 1)

if __name__ == '__main__':
    print("Starting Content Audit API...")
    print("API will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
