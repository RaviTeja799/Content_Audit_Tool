from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analyzers.seo_analyzer import SEOAnalyzer
from analyzers.serp_analyzer import SERPAnalyzer
from analyzers.aeo_analyzer import AEOAnalyzer
from analyzers.humanization_analyzer import HumanizationAnalyzer
from analyzers.differentiation_analyzer import DifferentiationAnalyzer
from analyzers.keyword_researcher import KeywordResearcher
from analyzers.content_comparator import ContentComparator
from analyzers.sentiment_analyzer import SentimentAnalyzer
from analyzers.entity_analyzer import EntityAnalyzer
from analyzers.freshness_analyzer import FreshnessAnalyzer
from analyzers.plagiarism_checker import PlagiarismChecker
from analyzers.schema_generator import SchemaGenerator
from utils.text_extractor import TextExtractor
from utils.pdf_generator import PDFReportGenerator
from utils.serp_scraper import SERPScraper
from utils.history_tracker import HistoryTracker
from utils.ai_improver import AIContentImprover
from utils.share_link_manager import ShareLinkManager

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
        sentiment_analyzer = SentimentAnalyzer()
        entity_analyzer = EntityAnalyzer()
        freshness_analyzer = FreshnessAnalyzer()
        plagiarism_checker = PlagiarismChecker()
        schema_generator = SchemaGenerator()
        
        # Run all analyses
        seo_result = seo_analyzer.analyze(text, headers, meta_description, target_keyword)
        serp_result = serp_analyzer.analyze(text, target_keyword, url)
        aeo_result = aeo_analyzer.analyze(text, headers)
        humanization_result = humanization_analyzer.analyze(text)
        differentiation_result = differentiation_analyzer.analyze(text, target_keyword)
        sentiment_result = sentiment_analyzer.analyze(text)
        entity_result = entity_analyzer.analyze(text)
        freshness_result = freshness_analyzer.analyze(text)
        plagiarism_result = plagiarism_checker.analyze(text)
        schema_result = schema_generator.generate(text, url or '', target_keyword)
        
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
            "sentiment": sentiment_result,
            "entities": entity_result,
            "freshness": freshness_result,
            "plagiarism": plagiarism_result,
            "schema": schema_result,
            "overall_score": calculate_overall_score([
                seo_result['score'],
                serp_result['score'],
                aeo_result['score'],
                humanization_result['score'],
                differentiation_result['score'],
                sentiment_result['score'],
                entity_result['score'],
                freshness_result['score'],
                plagiarism_result['score']
            ])
        }
        
        # Save to history
        try:
            tracker = HistoryTracker()
            analysis_id = tracker.save_analysis(results)
            results['analysis_id'] = analysis_id
        except Exception as e:
            print(f"Warning: Could not save to history: {str(e)}")
        
        return jsonify(results)
    
    except Exception as e:
        print(f"Error in analyze_content: {str(e)}")
        return jsonify({"error": str(e)}), 500

def calculate_overall_score(scores):
    """Calculate weighted average of all scores"""
    weights = [0.25, 0.25, 0.15, 0.15, 0.20]  # SEO, SERP, AEO, Human, Diff
    weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
    return round(weighted_sum, 1)

@app.route('/api/export-pdf', methods=['POST'])
def export_pdf():
    """Export analysis results as a professional PDF report"""
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No analysis data provided"}), 400
        
        # Generate PDF
        pdf_generator = PDFReportGenerator()
        pdf_buffer = pdf_generator.generate_report(data)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'content-audit-{timestamp}.pdf'
        
        # Return PDF file
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        print(f"Error in export_pdf: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/research-keywords', methods=['POST'])
def research_keywords():
    """Research related keywords with metrics"""
    try:
        data = request.json
        seed_keyword = data.get('keyword', '')
        max_results = data.get('max_results', 20)
        
        if not seed_keyword:
            return jsonify({"error": "No keyword provided"}), 400
        
        # Research keywords
        researcher = KeywordResearcher()
        results = researcher.research_keywords(seed_keyword, max_results)
        
        return jsonify(results)
    
    except Exception as e:
        print(f"Error in research_keywords: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/compare-content', methods=['POST'])
def compare_content():
    """Compare content with top competitor"""
    try:
        data = request.json
        your_content = data.get('content', '')
        target_keyword = data.get('keyword', '')
        your_metadata = data.get('metadata', {})
        
        if not your_content:
            return jsonify({"error": "No content provided"}), 400
        
        if not target_keyword:
            return jsonify({"error": "No target keyword provided for competitor analysis"}), 400
        
        # Get top competitor
        scraper = SERPScraper()
        serp_results = scraper.search_google(target_keyword, num_results=1)
        
        if not serp_results:
            return jsonify({"error": "Could not fetch competitor data"}), 500
        
        # Extract competitor content
        competitor_url = serp_results[0]['url']
        competitor_data = scraper.extract_page_content(competitor_url)
        competitor_data['url'] = competitor_url
        competitor_data['title'] = serp_results[0]['title']
        
        # Compare content
        comparator = ContentComparator()
        comparison = comparator.compare_with_competitor(
            your_content,
            competitor_data,
            your_metadata
        )
        
        # Add competitor URL to results
        comparison['competitor_url'] = competitor_url
        comparison['competitor_title'] = serp_results[0]['title']
        
        return jsonify(comparison)
    
    except Exception as e:
        print(f"Error in compare_content: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ========== NEW ENDPOINTS: HISTORY TRACKING ==========

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get analysis history"""
    try:
        tracker = HistoryTracker()
        limit = int(request.args.get('limit', 50))
        keyword = request.args.get('keyword')
        url = request.args.get('url')
        
        history = tracker.get_history(limit, keyword, url)
        return jsonify(history)
    
    except Exception as e:
        print(f"Error in get_history: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/progress', methods=['GET'])
def get_progress():
    """Get score progression over time"""
    try:
        tracker = HistoryTracker()
        keyword = request.args.get('keyword')
        url = request.args.get('url')
        days = int(request.args.get('days', 30))
        
        progress = tracker.get_progress_data(keyword, url, days)
        return jsonify(progress)
    
    except Exception as e:
        print(f"Error in get_progress: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/statistics', methods=['GET'])
def get_statistics():
    """Get overall statistics"""
    try:
        tracker = HistoryTracker()
        stats = tracker.get_statistics()
        return jsonify(stats)
    
    except Exception as e:
        print(f"Error in get_statistics: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ========== NEW ENDPOINTS: BATCH ANALYSIS ==========

@app.route('/api/batch/create', methods=['POST'])
def create_batch():
    """Create a new batch analysis"""
    try:
        data = request.json
        batch_name = data.get('name', f'Batch {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        urls = data.get('urls', [])
        
        if not urls or len(urls) == 0:
            return jsonify({"error": "No URLs provided"}), 400
        
        tracker = HistoryTracker()
        batch_id = tracker.create_batch(batch_name, urls)
        
        return jsonify({"batch_id": batch_id, "total_urls": len(urls)})
    
    except Exception as e:
        print(f"Error in create_batch: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/batch/analyze', methods=['POST'])
def analyze_batch():
    """Analyze a single URL from a batch"""
    try:
        data = request.json
        batch_id = data.get('batch_id')
        url = data.get('url')
        target_keyword = data.get('target_keyword', '')
        
        if not batch_id or not url:
            return jsonify({"error": "Missing batch_id or url"}), 400
        
        tracker = HistoryTracker()
        
        try:
            # Extract and analyze
            extractor = TextExtractor()
            content_data = extractor.extract(url)
            
            if not content_data['text']:
                tracker.update_batch_item(batch_id, url, 'failed', error='Could not extract content')
                return jsonify({"error": "Could not extract content"}), 400
            
            # Run analysis (same as main analyze endpoint)
            text = content_data['text']
            headers = content_data.get('headers', [])
            meta_description = content_data.get('meta_description', '')
            
            seo_analyzer = SEOAnalyzer()
            serp_analyzer = SERPAnalyzer()
            aeo_analyzer = AEOAnalyzer()
            humanization_analyzer = HumanizationAnalyzer()
            differentiation_analyzer = DifferentiationAnalyzer()
            
            seo_result = seo_analyzer.analyze(text, headers, meta_description, target_keyword)
            serp_result = serp_analyzer.analyze(text, target_keyword, url)
            aeo_result = aeo_analyzer.analyze(text, headers)
            humanization_result = humanization_analyzer.analyze(text)
            differentiation_result = differentiation_analyzer.analyze(text, target_keyword)
            
            results = {
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
            
            # Save to history and update batch
            analysis_id = tracker.save_analysis(results)
            tracker.update_batch_item(batch_id, url, 'completed', results['overall_score'], analysis_id=analysis_id)
            
            return jsonify(results)
        
        except Exception as e:
            tracker.update_batch_item(batch_id, url, 'failed', error=str(e))
            return jsonify({"error": str(e)}), 500
    
    except Exception as e:
        print(f"Error in analyze_batch: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/batch/status/<batch_id>', methods=['GET'])
def get_batch_status(batch_id):
    """Get batch analysis status"""
    try:
        tracker = HistoryTracker()
        status = tracker.get_batch_status(batch_id)
        return jsonify(status)
    
    except Exception as e:
        print(f"Error in get_batch_status: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ========== NEW ENDPOINTS: AI IMPROVEMENTS ==========

@app.route('/api/ai/suggestions', methods=['POST'])
def get_ai_suggestions():
    """Get AI-powered improvement suggestions"""
    try:
        data = request.json
        content = data.get('content', '')
        analysis_results = data.get('analysis_results', {})
        
        if not content or not analysis_results:
            return jsonify({"error": "Missing content or analysis results"}), 400
        
        improver = AIContentImprover()
        suggestions = improver.analyze_and_suggest(content, analysis_results)
        
        return jsonify(suggestions)
    
    except Exception as e:
        print(f"Error in get_ai_suggestions: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/rewrite', methods=['POST'])
def ai_rewrite():
    """AI-powered section rewrite"""
    try:
        data = request.json
        original_text = data.get('text', '')
        improvement_goal = data.get('goal', 'improve readability and engagement')
        context = data.get('context', '')
        
        if not original_text:
            return jsonify({"error": "No text provided"}), 400
        
        improver = AIContentImprover()
        rewritten = improver.rewrite_section(original_text, improvement_goal, context)
        
        return jsonify({"original": original_text, "rewritten": rewritten})
    
    except Exception as e:
        print(f"Error in ai_rewrite: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/generate', methods=['POST'])
def ai_generate():
    """Generate missing content section"""
    try:
        data = request.json
        topic = data.get('topic', '')
        context = data.get('context', '')
        target_keyword = data.get('keyword', '')
        
        if not topic:
            return jsonify({"error": "No topic provided"}), 400
        
        improver = AIContentImprover()
        generated = improver.generate_missing_section(topic, context, target_keyword)
        
        return jsonify({"topic": topic, "generated_content": generated})
    
    except Exception as e:
        print(f"Error in ai_generate: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/share/create', methods=['POST'])
def create_share_link():
    """Create shareable public link for report"""
    try:
        data = request.json
        results = data.get('results', {})
        expiry_days = data.get('expiry_days', 30)
        
        if not results:
            return jsonify({"error": "No results provided"}), 400
        
        share_manager = ShareLinkManager()
        share_data = share_manager.create_share_link(results, expiry_days)
        
        # Generate full URL
        base_url = request.host_url.rstrip('/')
        share_data['full_url'] = f"{base_url}{share_data['url']}"
        
        return jsonify(share_data)
    
    except Exception as e:
        print(f"Error in create_share_link: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/share/<token>', methods=['GET'])
def get_shared_report(token):
    """Retrieve shared report by token"""
    try:
        share_manager = ShareLinkManager()
        results = share_manager.get_shared_report(token)
        
        if not results:
            return jsonify({"error": "Share link not found or expired"}), 404
        
        return jsonify(results)
    
    except Exception as e:
        print(f"Error in get_shared_report: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/clear-data', methods=['POST', 'DELETE'])
def clear_all_data():
    """Clear all analysis history, progress, and batch data"""
    try:
        tracker = HistoryTracker()
        
        # Delete database file
        db_path = tracker.db_path
        if os.path.exists(db_path):
            os.remove(db_path)
        
        # Reinitialize empty database
        tracker._init_database()
        
        # Clear shared links if they exist
        try:
            from utils.share_link_manager import ShareLinkManager
            share_manager = ShareLinkManager()
            share_db = share_manager.db_path
            if os.path.exists(share_db):
                os.remove(share_db)
        except:
            pass
        
        return jsonify({
            "success": True,
            "message": "All analysis results, history, and batch data have been cleared successfully"
        })
    
    except Exception as e:
        print(f"Error in clear_all_data: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Content Audit API...")
    print("API will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
