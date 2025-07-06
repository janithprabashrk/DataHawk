# 🦅 DataHawk - AI-Powered Web Scraper

DataHawk is an intelligent web scraping tool that leverages AI to extract, parse, and organize data from any website—no matter how complex. Whether you need e-commerce prices, news articles, social media trends, or custom datasets, DataHawk delivers with precision and speed.

## ✨ Key Features

- ✅ **AI-Powered Extraction** – Handles dynamic content, JavaScript-heavy sites, and anti-scraping measures
- ✅ **No-Code Friendly** – Simple Streamlit interface with smart automation
- ✅ **Customizable & Scalable** – From one-time scrapes to large-scale data pipelines
- ✅ **Ethical & Stealthy** – Respects robots.txt and mimics human browsing patterns
- ✅ **Google Gemini AI** – Fast, accurate content parsing with natural language descriptions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free tier available)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd DataHawk
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Configure your API key:**
   - Get your free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Edit `.env` file and replace `your_gemini_api_key_here` with your actual API key

4. **Start DataHawk:**
   ```bash
   streamlit run main.py
   ```

### Manual Installation

If you prefer manual setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env

# Edit .env file with your API keys
# Then run:
streamlit run main.py
```

## 📖 How to Use

1. **Enter Website URL** - Input any website you want to scrape
2. **Fetch Data** - Click to scrape and extract the website content
3. **Describe What to Parse** - Tell the AI what specific data you want to extract
4. **Parse Content** - Let AI analyze and extract the requested information
5. **Download Results** - Save your extracted data as a text file

### Example Parsing Descriptions

- "Extract all product names and prices"
- "Get all email addresses and phone numbers"
- "Find all article titles and publication dates"
- "Extract company information and contact details"
- "Get all job listings with salaries and locations"

## 🛠️ Technical Architecture

### Core Components

- **`main.py`** - Streamlit web interface with modern UI
- **`scrape.py`** - Web scraping using Selenium + BrightData proxy
- **`parse.py`** - AI-powered content parsing using Google Gemini
- **`setup.py`** - Automated installation and configuration

### Technologies Used

- **Frontend:** Streamlit (modern web UI)
- **Web Scraping:** Selenium WebDriver + BeautifulSoup4
- **AI Processing:** Google Gemini 1.5 Flash via API
- **Proxy Service:** BrightData SuperProxy (optional, for premium scraping)

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Required: Google Gemini API Configuration
GEMINI_API_KEY=your_actual_api_key

# Optional: BrightData Proxy (for advanced scraping)
BRIGHTDATA_USERNAME=your_username
BRIGHTDATA_PASSWORD=your_password
BRIGHTDATA_ENDPOINT=brd.superproxy.io:9515
```

### API Limits (Gemini Free Tier)

- **Requests:** 15 per minute
- **Tokens:** 1 million per day
- **Models:** Gemini 1.5 Flash (fast and efficient)

## 🔒 Security & Privacy

- All API keys are stored in environment variables
- No credentials hardcoded in source code
- Proxy credentials configurable via environment
- Respects website robots.txt and rate limits

## 📁 Project Structure

```
DataHawk/
├── main.py              # Streamlit web interface
├── scrape.py            # Web scraping logic
├── parse.py             # AI parsing with Gemini
├── setup.py             # Automated setup script
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── .env                 # Your configuration (private)
├── README.md            # This file
└── .gitignore          # Git ignore rules
```

## 🤝 Contributing

DataHawk is designed for developers, researchers, marketers, and data analysts who need fast, reliable, and adaptable web scraping.

## 📄 License

This project is open source. Please use responsibly and respect website terms of service.

## 🆘 Troubleshooting

### Common Issues

1. **Import errors** - Run `python setup.py` to install dependencies
2. **API key errors** - Make sure your Gemini API key is correct in `.env`
3. **Scraping failures** - Some websites may block automated access
4. **Parsing issues** - Try more specific descriptions for better results

### Getting Help

- Check the sidebar help in the application
- Review parsing examples for better prompts
- Ensure your API key has sufficient quota

---

🚀 **Get the data you want—automagically with DataHawk!** 🦅
