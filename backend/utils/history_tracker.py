import sqlite3
import json
from datetime import datetime
import os

class HistoryTracker:
    """Track and manage analysis history in SQLite database"""
    
    def __init__(self, db_path='data/history.db'):
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Analysis history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                url TEXT,
                target_keyword TEXT,
                word_count INTEGER,
                overall_score REAL,
                seo_score REAL,
                serp_score REAL,
                aeo_score REAL,
                humanization_score REAL,
                differentiation_score REAL,
                full_results TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Batch analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS batch_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT NOT NULL,
                batch_name TEXT,
                total_urls INTEGER,
                completed_urls INTEGER,
                status TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            )
        ''')
        
        # Batch items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS batch_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id TEXT NOT NULL,
                url TEXT NOT NULL,
                status TEXT,
                overall_score REAL,
                error TEXT,
                analysis_id INTEGER,
                FOREIGN KEY (analysis_id) REFERENCES analysis_history(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_analysis(self, results):
        """Save analysis results to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analysis_history (
                timestamp, url, target_keyword, word_count,
                overall_score, seo_score, serp_score, aeo_score,
                humanization_score, differentiation_score, full_results
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            results.get('url'),
            results.get('target_keyword'),
            results.get('word_count'),
            results.get('overall_score'),
            results.get('seo', {}).get('score'),
            results.get('serp_performance', {}).get('score'),
            results.get('aeo', {}).get('score'),
            results.get('humanization', {}).get('score'),
            results.get('differentiation', {}).get('score'),
            json.dumps(results)
        ))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return analysis_id
    
    def get_history(self, limit=50, keyword=None, url=None):
        """Retrieve analysis history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM analysis_history WHERE 1=1'
        params = []
        
        if keyword:
            query += ' AND target_keyword LIKE ?'
            params.append(f'%{keyword}%')
        
        if url:
            query += ' AND url LIKE ?'
            params.append(f'%{url}%')
        
        query += ' ORDER BY created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_progress_data(self, keyword=None, url=None, days=30):
        """Get score progression over time"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                timestamp,
                overall_score,
                seo_score,
                serp_score,
                aeo_score,
                humanization_score,
                differentiation_score,
                target_keyword,
                url
            FROM analysis_history
            WHERE datetime(created_at) >= datetime('now', '-' || ? || ' days')
        '''
        params = [days]
        
        if keyword:
            query += ' AND target_keyword LIKE ?'
            params.append(f'%{keyword}%')
        
        if url:
            query += ' AND url LIKE ?'
            params.append(f'%{url}%')
        
        query += ' ORDER BY created_at ASC'
        
        cursor.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_statistics(self):
        """Get overall statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total analyses
        cursor.execute('SELECT COUNT(*) FROM analysis_history')
        stats['total_analyses'] = cursor.fetchone()[0]
        
        # Average scores
        cursor.execute('''
            SELECT 
                AVG(overall_score) as avg_overall,
                AVG(seo_score) as avg_seo,
                AVG(serp_score) as avg_serp,
                AVG(aeo_score) as avg_aeo,
                AVG(humanization_score) as avg_humanization,
                AVG(differentiation_score) as avg_differentiation
            FROM analysis_history
        ''')
        avg_scores = cursor.fetchone()
        stats['avg_scores'] = {
            'overall': round(avg_scores[0], 1) if avg_scores[0] else 0,
            'seo': round(avg_scores[1], 1) if avg_scores[1] else 0,
            'serp': round(avg_scores[2], 1) if avg_scores[2] else 0,
            'aeo': round(avg_scores[3], 1) if avg_scores[3] else 0,
            'humanization': round(avg_scores[4], 1) if avg_scores[4] else 0,
            'differentiation': round(avg_scores[5], 1) if avg_scores[5] else 0
        }
        
        # Top keywords
        cursor.execute('''
            SELECT target_keyword, COUNT(*) as count
            FROM analysis_history
            WHERE target_keyword IS NOT NULL AND target_keyword != ''
            GROUP BY target_keyword
            ORDER BY count DESC
            LIMIT 5
        ''')
        stats['top_keywords'] = [{'keyword': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        conn.close()
        return stats
    
    def create_batch(self, batch_name, urls):
        """Create a new batch analysis"""
        batch_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create batch record
        cursor.execute('''
            INSERT INTO batch_analysis (batch_id, batch_name, total_urls, completed_urls, status)
            VALUES (?, ?, ?, 0, 'pending')
        ''', (batch_id, batch_name, len(urls)))
        
        # Create batch items
        for url in urls:
            cursor.execute('''
                INSERT INTO batch_items (batch_id, url, status)
                VALUES (?, ?, 'pending')
            ''', (batch_id, url))
        
        conn.commit()
        conn.close()
        
        return batch_id
    
    def update_batch_item(self, batch_id, url, status, overall_score=None, error=None, analysis_id=None):
        """Update batch item status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE batch_items
            SET status = ?, overall_score = ?, error = ?, analysis_id = ?
            WHERE batch_id = ? AND url = ?
        ''', (status, overall_score, error, analysis_id, batch_id, url))
        
        # Update batch progress
        cursor.execute('''
            UPDATE batch_analysis
            SET completed_urls = (
                SELECT COUNT(*) FROM batch_items
                WHERE batch_id = ? AND status IN ('completed', 'failed')
            )
            WHERE batch_id = ?
        ''', (batch_id, batch_id))
        
        # Check if batch is complete
        cursor.execute('''
            SELECT total_urls, completed_urls FROM batch_analysis
            WHERE batch_id = ?
        ''', (batch_id,))
        total, completed = cursor.fetchone()
        
        if total == completed:
            cursor.execute('''
                UPDATE batch_analysis
                SET status = 'completed', completed_at = ?
                WHERE batch_id = ?
            ''', (datetime.now().isoformat(), batch_id))
        
        conn.commit()
        conn.close()
    
    def get_batch_status(self, batch_id):
        """Get batch analysis status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get batch info
        cursor.execute('SELECT * FROM batch_analysis WHERE batch_id = ?', (batch_id,))
        columns = [desc[0] for desc in cursor.description]
        batch = dict(zip(columns, cursor.fetchone()))
        
        # Get batch items
        cursor.execute('SELECT * FROM batch_items WHERE batch_id = ?', (batch_id,))
        columns = [desc[0] for desc in cursor.description]
        items = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        batch['items'] = items
        
        conn.close()
        return batch
