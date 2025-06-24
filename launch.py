#!/usr/bin/env python3
"""
Simple launcher for the AI Accessibility Advocate Assistant
"""

import subprocess
import sys
import os

def main():
    print("🌟 AI-Powered Accessibility Advocate Assistant")
    print("=" * 50)
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ app.py not found. Please run this from the project directory.")
        return
    
    # Check if secrets are configured
    if os.path.exists(".streamlit/secrets.toml"):
        print("✅ Found secrets configuration")
        
        # Quick check if API key is configured
        try:
            with open(".streamlit/secrets.toml", "r") as f:
                content = f.read()
                if "your-google-ai-studio-api-key-here" in content:
                    print("⚠️  Please update your API key in .streamlit/secrets.toml")
                    print("   Get your key from: https://aistudio.google.com/app/apikey")
                else:
                    print("✅ API key appears to be configured")
        except:
            pass
    else:
        print("⚠️  No secrets.toml found. Creating sample configuration...")
        print("   Please edit .streamlit/secrets.toml with your Google AI API key")
    
    print("\n🚀 Starting Streamlit app...")
    print("📱 Features available:")
    print("   💬 AI Accessibility Chat Assistant")
    print("   🖼️ Image Accessibility Analyzer")
    print("   📚 WCAG Guidelines & Resources")
    print("\n" + "=" * 50)
    
    # Launch streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start app: {e}")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install with: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 