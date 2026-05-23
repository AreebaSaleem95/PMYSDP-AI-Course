# Project File Structure & Purpose Guide

## 📁 Complete Project Structure

```
azure-content-moderator/
├── 📄 Core Application Files
│   ├── app.py                    (Main terminal application)
│   ├── flask_api.py              (Web API version)
│   ├── config.py                 (Configuration & credentials)
│   └── test_examples.py          (Test suite)
│
├── 📚 Documentation Files
│   ├── README.md                 (Main documentation)
│   ├── QUICK_START.md            (5-minute setup)
│   ├── SETUP_GUIDE.md            (OS-specific setup)
│   ├── API_DOCUMENTATION.md      (API reference)
│   ├── PROJECT_PRESENTATION.md   (University presentation)
│   └── CHANGELOG.md              (Version history)
│
├── ⚙️ Configuration Files
│   ├── requirements.txt          (Python dependencies)
│   ├── .env.example              (Environment template)
│   └── .gitignore                (Git ignore rules)
│
└── 📋 This File
    └── FILE_STRUCTURE.md         (This guide)
```

## 📄 File Descriptions

### 🚀 Application Files

#### `app.py` (400+ lines)
**Purpose:** Main content moderation application

**Key Components:**
- `ContentModerator` class - Core moderation logic
- `analyze_content()` - Send text to Azure API
- `extract_severity_scores()` - Parse API response
- `decide_content_status()` - Determine approval/blocking
- `display_results()` - Format and display results
- `run_interactive_mode()` - User interaction loop
- `main()` - Entry point

**Usage:**
```bash
python app.py
```

**User Interaction:**
- Terminal-based interface
- Interactive input loop
- Real-time analysis feedback
- Severity visualization

---

#### `flask_api.py` (300+ lines)
**Purpose:** Web API version for integration with other applications

**Key Components:**
- Flask application setup
- `/api/health` - Health check endpoint
- `/api/moderate` - Single text analysis
- `/api/moderate-batch` - Batch text analysis
- Error handlers
- JSON response formatting

**Usage:**
```bash
python flask_api.py
```

**API Access:**
```bash
curl -X POST http://localhost:5000/api/moderate \
  -H "Content-Type: application/json" \
  -d '{"text": "Text to analyze"}'
```

---

#### `config.py`
**Purpose:** Configuration file for storing API credentials

**Contents:**
```python
AZURE_API_KEY = "YOUR_API_KEY_HERE"
AZURE_ENDPOINT = "https://YOUR_RESOURCE.cognitiveservices.azure.com"
SEVERITY_THRESHOLD = 2
DEBUG_MODE = False
```

**Security Note:** 
- This is where you add your Azure credentials
- Never commit real credentials to version control
- Use .env file for production

---

#### `test_examples.py` (200+ lines)
**Purpose:** Test suite demonstrating application usage

**Features:**
- Pre-defined test cases
- Custom test mode
- Example harmful/clean content
- Expected vs actual results
- Error handling examples

**Usage:**
```bash
python test_examples.py              # Run predefined tests
python test_examples.py --custom     # Custom test mode
```

---

### 📚 Documentation Files

#### `README.md` (Comprehensive Guide)
**Sections:**
- Project Overview
- Installation & Setup
- Usage Instructions
- Configuration Guide
- Error Handling
- Architecture Explanation
- Security Best Practices
- References & Resources
- Troubleshooting Guide
- Submission Checklist

**Target Audience:** Everyone

---

#### `QUICK_START.md` (5-Minute Setup)
**Sections:**
- 5-minute installation
- API quick test
- Severity reference
- Troubleshooting
- Next steps

**Target Audience:** Users wanting quick start

---

#### `SETUP_GUIDE.md` (OS-Specific)
**Sections:**
- Windows setup
- macOS setup
- Linux setup
- Azure credentials guide
- Troubleshooting
- Verification checklist
- Advanced configuration

**Target Audience:** Technical users, different OS

---

#### `API_DOCUMENTATION.md` (Complete API Reference)
**Sections:**
- Overview & authentication
- Base URL
- All endpoints documented
- Request/response formats
- Error responses
- Usage examples (Python, JavaScript, Java, C#)
- Best practices
- Rate limiting
- Troubleshooting

**Target Audience:** Developers integrating the API

---

#### `PROJECT_PRESENTATION.md` (University Presentation)
**Sections:**
- 12 presentation slides with talking points
- Viva questions with answers
- System architecture diagrams
- Results & testing data
- Real-world applications
- Lessons learned
- Future enhancements
- Presentation tips
- Confidence builders

**Target Audience:** Students preparing for viva

---

#### `CHANGELOG.md` (Version History)
**Sections:**
- Version 1.0.0 release notes
- Features implemented
- Files created
- Known issues
- Planned features
- Testing results
- Completion status

**Target Audience:** Project tracking

---

### ⚙️ Configuration Files

#### `requirements.txt`
**Purpose:** Python package dependencies

**Contents:**
```
requests==2.31.0        # HTTP requests library
python-dotenv==1.0.0    # Environment variable loader
flask==3.0.0            # Web framework
```

**Usage:**
```bash
pip install -r requirements.txt
```

---

#### `.env.example`
**Purpose:** Template for environment variables

**Usage:**
1. Copy to `.env`
2. Fill in your actual credentials
3. Never commit `.env` to version control

**Contains:**
- AZURE_API_KEY
- AZURE_ENDPOINT
- SEVERITY_THRESHOLD
- DEBUG_MODE
- Flask settings

---

#### `.gitignore`
**Purpose:** Prevent accidental upload of sensitive files

**Ignores:**
- Virtual environment
- `.env` files
- `__pycache__` directories
- IDE settings
- Log files
- Credentials/keys
- OS files

---

## 🔄 File Dependencies

```
main entry points:
    └── app.py
        └── config.py              (import credentials)
        └── requirements.txt       (needs requests)

    └── flask_api.py
        └── app.py                 (import ContentModerator)
        └── config.py              (import credentials)
        └── requirements.txt       (needs flask, requests)

    └── test_examples.py
        └── app.py                 (import ContentModerator)
        └── config.py              (import credentials)
        └── requirements.txt       (needs requests)
```

## 📊 Line Count Summary

```
app.py                      ~400 lines (core application)
flask_api.py                ~300 lines (web API)
test_examples.py            ~200 lines (test suite)
config.py                   ~30 lines  (configuration)
────────────────────────────────────────────────
Total Code                  ~930 lines

README.md                   ~500 lines
SETUP_GUIDE.md              ~300 lines
API_DOCUMENTATION.md        ~400 lines
PROJECT_PRESENTATION.md     ~800 lines
QUICK_START.md              ~100 lines
CHANGELOG.md                ~200 lines
FILE_STRUCTURE.md           ~350 lines
────────────────────────────────────────────────
Total Documentation         ~2,650 lines

Total Project               ~3,580 lines
```

## 🎯 Quick Reference: Which File to Use

### "I want to get started quickly"
→ Read: `QUICK_START.md` (5 minutes)

### "I need complete setup instructions"
→ Read: `SETUP_GUIDE.md` (OS-specific)

### "I want to run the application"
→ Use: `app.py` (terminal) or `flask_api.py` (web)

### "I need to integrate this into my code"
→ Read: `API_DOCUMENTATION.md`

### "I need to configure Azure credentials"
→ Edit: `config.py` (development) or `.env` (production)

### "I want to test the application"
→ Run: `test_examples.py`

### "I'm preparing a university presentation"
→ Read: `PROJECT_PRESENTATION.md`

### "I want to understand the architecture"
→ Read: `README.md` → Architecture section

### "I encountered an error"
→ Check: `README.md` → Troubleshooting section

### "I want to see all API endpoints"
→ Read: `API_DOCUMENTATION.md` → Endpoints section

## 📋 Feature Mapping

| Feature | File | Section |
|---------|------|---------|
| Main App | app.py | - |
| Web API | flask_api.py | - |
| Setup | SETUP_GUIDE.md | OS-specific |
| Quick Start | QUICK_START.md | - |
| API Reference | API_DOCUMENTATION.md | Endpoints |
| Presentation | PROJECT_PRESENTATION.md | Slides 1-12 |
| Viva Prep | PROJECT_PRESENTATION.md | Q&A section |
| Tests | test_examples.py | - |
| Config | config.py | - |
| Dependencies | requirements.txt | - |

## ✅ Setup Checklist

Before running the project:

- [ ] Read QUICK_START.md or SETUP_GUIDE.md
- [ ] Install Python 3.8+
- [ ] Create virtual environment
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Get Azure API key and endpoint
- [ ] Update config.py with credentials
- [ ] Run test: `python test_examples.py`
- [ ] Run main app: `python app.py`

## 🔐 Security Checklist

- [ ] API key not in app.py
- [ ] Credentials in config.py or .env
- [ ] .gitignore includes .env
- [ ] No sensitive data in logs
- [ ] HTTPS used for all API calls
- [ ] Error messages don't expose secrets

## 🎓 University Submission

Files to include in submission:
- [x] All source code files (app.py, flask_api.py, etc.)
- [x] README.md (main documentation)
- [x] PROJECT_PRESENTATION.md (for viva)
- [x] requirements.txt (for reproducibility)
- [x] config.py (with placeholder credentials)
- [x] test_examples.py (demonstrate functionality)
- [x] .gitignore (best practices)
- [x] CHANGELOG.md (project history)

## 📞 Support Resources

| Issue | Resource |
|-------|----------|
| Setup problems | SETUP_GUIDE.md |
| Running errors | README.md → Troubleshooting |
| API questions | API_DOCUMENTATION.md |
| Viva questions | PROJECT_PRESENTATION.md |
| Code examples | test_examples.py |

---

**Project Status: Complete & Ready! ✅**

All files are created, documented, and ready for use.
