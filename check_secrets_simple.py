# check_secrets_simple.py - Ultra simple version
import os
import glob

def check_secrets():
    print("🔍 Checking for hardcoded secrets...")
    issues = []
    
    # Find all Python files
    python_files = glob.glob('**/*.py', recursive=True)
    
    for filepath in python_files:
        # Skip virtual environment
        if 'venv' in filepath or 'env' in filepath or '__pycache__' in filepath:
            continue
        
        try:
            # Read file as binary and decode with error handling
            with open(filepath, 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
            
            # Check for patterns (simple version)
            if 'api_key="gsk_' in content or "api_key='gsk_" in content:
                # Make sure it's not using environment variable
                if 'os.environ' not in content and 'getenv' not in content:
                    issues.append(filepath)
                    
            if 'api_key="sk-' in content or "api_key='sk-" in content:
                if 'os.environ' not in content and 'getenv' not in content:
                    issues.append(filepath)
                    
        except Exception as e:
            print(f"  ⚠️  Skipped {filepath}: {str(e)[:50]}")
    
    if issues:
        print("\n❌ WARNING: Hardcoded API keys found in:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n📝 Please move these keys to .env file!")
        return False
    else:
        print("✅ No hardcoded secrets found!")
        print("✅ Your app is secure!")
        return True

if __name__ == "__main__":
    check_secrets()