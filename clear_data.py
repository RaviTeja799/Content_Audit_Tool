#!/usr/bin/env python3
"""
Utility script to clear all analysis results, history, and progress data
Run this script from the project root to reset the database
"""

import os
import sys

def clear_all_data():
    """Clear all analysis history, progress, and batch data"""
    
    # Define database files to delete
    db_files = [
        'backend/data/history.db',
        'backend/data/shares.db'  # If it exists
    ]
    
    print("=" * 60)
    print("CLEARING ALL DATA")
    print("=" * 60)
    
    deleted_count = 0
    
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"✓ Deleted: {db_file}")
                deleted_count += 1
            except Exception as e:
                print(f"✗ Error deleting {db_file}: {e}")
        else:
            print(f"- File not found: {db_file} (nothing to delete)")
    
    print("\n" + "=" * 60)
    print(f"✓ Successfully cleared {deleted_count} database file(s)")
    print("✓ All analysis results, history, and batch data have been reset")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    try:
        success = clear_all_data()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)
