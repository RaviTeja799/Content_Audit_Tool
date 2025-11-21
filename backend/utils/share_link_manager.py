import secrets
import json
from datetime import datetime, timedelta
import os

class ShareLinkManager:
    def __init__(self):
        self.shares_file = 'data/shared_reports.json'
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(self.shares_file):
            with open(self.shares_file, 'w') as f:
                json.dump({}, f)
    
    def create_share_link(self, analysis_results, expiry_days=30):
        token = secrets.token_urlsafe(32)
        expiry_date = (datetime.now() + timedelta(days=expiry_days)).isoformat()
        
        shares = self._load_shares()
        shares[token] = {
            'results': analysis_results,
            'created_at': datetime.now().isoformat(),
            'expires_at': expiry_date,
            'view_count': 0
        }
        self._save_shares(shares)
        
        return {
            'token': token,
            'url': f'/share/{token}',
            'expires_at': expiry_date
        }
    
    def get_shared_report(self, token):
        shares = self._load_shares()
        
        if token not in shares:
            return None
        
        share_data = shares[token]
        
        # Check expiry
        expires_at = datetime.fromisoformat(share_data['expires_at'])
        if datetime.now() > expires_at:
            del shares[token]
            self._save_shares(shares)
            return None
        
        # Increment view count
        share_data['view_count'] += 1
        shares[token] = share_data
        self._save_shares(shares)
        
        return share_data['results']
    
    def delete_share_link(self, token):
        shares = self._load_shares()
        if token in shares:
            del shares[token]
            self._save_shares(shares)
            return True
        return False
    
    def cleanup_expired(self):
        shares = self._load_shares()
        now = datetime.now()
        
        expired_tokens = [
            token for token, data in shares.items()
            if datetime.fromisoformat(data['expires_at']) < now
        ]
        
        for token in expired_tokens:
            del shares[token]
        
        self._save_shares(shares)
        return len(expired_tokens)
    
    def _load_shares(self):
        try:
            with open(self.shares_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_shares(self, shares):
        with open(self.shares_file, 'w') as f:
            json.dump(shares, f, indent=2)
