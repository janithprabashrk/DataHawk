#!/usr/bin/env python3
"""
DataHawk Setup Script
Automated setup for the DataHawk AI-powered web scraping tool.
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages with better timeout handling"""
    print("📦 Installing required packages...")
    
    # First, upgrade pip
    print("🔄 Upgrading pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ Pip upgraded successfully!")
    except subprocess.CalledProcessError:
        print("⚠️ Could not upgrade pip, continuing with current version...")
    
    # Install packages one by one with increased timeout
    packages = [
        "streamlit",
        "google-generativeai", 
        "selenium",
        "beautifulsoup4",
        "lxml",
        "html5lib",
        "python-dotenv"
    ]
    
    failed_packages = []
    
    for package in packages:
        print(f"📦 Installing {package}...")
        try:
            # Install with increased timeout and retries
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                package, 
                "--timeout", "300",  # 5 minutes timeout
                "--retries", "3"
            ])
            print(f"✅ {package} installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️ Failed to install: {', '.join(failed_packages)}")
        print("You can try installing them manually:")
        for pkg in failed_packages:
            print(f"   pip install {pkg} --timeout 300")
        return len(failed_packages) == 0
    else:
        print("✅ All packages installed successfully!")
        return True

def check_env_file():
    """Check if .env file exists and is configured"""
    if not os.path.exists('.env'):
        print("⚠️  .env file not found!")
        print("📝 Creating .env file from template...")
        
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as example:
                content = example.read()
            with open('.env', 'w') as env_file:
                env_file.write(content)
            print("✅ .env file created from template.")
        else:
            # Create basic .env file
            env_content = """# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# BrightData SuperProxy Configuration (Optional)
BRIGHTDATA_USERNAME=your_brightdata_username
BRIGHTDATA_PASSWORD=your_brightdata_password
BRIGHTDATA_ENDPOINT=brd.superproxy.io:9515
"""
            with open('.env', 'w') as env_file:
                env_file.write(env_content)
            print("✅ Basic .env file created.")
        
        print("\n🔑 IMPORTANT: Please edit .env file and add your API keys:")
        print("1. Get Gemini API key from: https://makersuite.google.com/app/apikey")
        print("2. Replace 'your_gemini_api_key_here' with your actual API key")
        return False
    else:
        # Check if API key is configured
        with open('.env', 'r') as env_file:
            content = env_file.read()
        
        if 'your_gemini_api_key_here' in content:
            print("⚠️  Please configure your Gemini API key in .env file")
            return False
        
        print("✅ .env file exists and appears to be configured.")
        return True

def main():
    """Main setup function"""
    print("🦅 DataHawk Setup")
    print("=" * 30)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation.")
        return False
    
    # Check environment configuration
    env_configured = check_env_file()
    
    print("\n" + "=" * 30)
    if env_configured:
        print("✅ Setup completed successfully!")
        print("\n🚀 To start DataHawk, run:")
        print("   streamlit run main.py")
    else:
        print("⚠️  Setup completed with warnings.")
        print("Please configure your .env file before running DataHawk.")
    
    return True

if __name__ == "__main__":
    main()
