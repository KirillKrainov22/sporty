# Sporty Web Interface

## 🚀 Quick Start

### Option 1: Docker (Recommended - Cross-platform)
\`\`\`bash
# From project root
docker-compose up web
\`\`\`

### Option 2: Local Development
\`\`\`bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate:
#    Mac/Linux: source venv/bin/activate
#    Windows:   venv\\Scripts\\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run app.py
\`\`\`

## 📁 Project Structure
\`\`\`
web/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── Dockerfile         # Container config
├── .streamlit/        # Streamlit config
├── pages/             # Multi-page app
├── modules/           # Business logic
└── assets/            # Static files
\`\`\`

## 🔧 Development
- All pages accessible via sidebar
- API integration through modules/api_client.py
- Responsive design for mobile/desktop
