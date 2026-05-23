# Detailed Setup Guide - Windows, macOS, and Linux

## 🪟 Windows Setup

### Step 1: Install Python

1. Download Python 3.8+ from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"

**Verify Installation:**
```bash
python --version
```

### Step 2: Create Virtual Environment

```bash
# Open Command Prompt or PowerShell in project folder
cd C:\path\to\project

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) in your terminal
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Credentials

**Option 1: Edit config.py (Recommended for Development)**

```python
# config.py
AZURE_API_KEY = "your_api_key_from_azure_portal"
AZURE_ENDPOINT = "https://your_resource_name.cognitiveservices.azure.com"
```

**Option 2: Use Environment Variables (Recommended for Production)**

1. Create `.env` file in project root:
```
AZURE_API_KEY=your_api_key
AZURE_ENDPOINT=https://your_resource.cognitiveservices.azure.com
```

2. Install python-dotenv:
```bash
pip install python-dotenv
```

3. Update config.py:
```python
import os
from dotenv import load_dotenv

load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
```

### Step 5: Run the Application

```bash
# Activate virtual environment if not already activated
venv\Scripts\activate

# Run terminal mode
python app.py

# OR run web API
python flask_api.py

# OR run tests
python test_examples.py
```

### Common Windows Issues

**Issue: "Python is not recognized"**
- Solution: Add Python to PATH or use full path: `C:\Python310\python.exe app.py`

**Issue: "Module not found"**
- Solution: Make sure virtual environment is activated: `venv\Scripts\activate`

**Issue: Port 5000 already in use**
- Solution: Change port in flask_api.py line ~290: `app.run(port=5001)`

---

## 🍎 macOS Setup

### Step 1: Install Python

**Using Homebrew (Recommended):**
```bash
# Install Homebrew first if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Verify:**
```bash
python3 --version
```

### Step 2: Create Virtual Environment

```bash
cd /path/to/project

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your terminal
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Credentials

Same as Windows (see Step 4 above)

### Step 5: Run the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run application
python app.py
```

### Common macOS Issues

**Issue: "Command not found: python"**
- Solution: Use `python3` instead of `python`

**Issue: Permission denied**
- Solution: Use `sudo` or fix permissions with: `chmod +x app.py`

**Issue: Module not found**
- Solution: Make sure virtual environment is activated and reinstall: `pip install --upgrade -r requirements.txt`

---

## 🐧 Linux Setup

### Step 1: Install Python

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Fedora/CentOS:**
```bash
sudo dnf install python3 python3-pip
```

**Arch:**
```bash
sudo pacman -S python python-pip
```

**Verify:**
```bash
python3 --version
```

### Step 2: Create Virtual Environment

```bash
cd ~/path/to/project

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Credentials

Same as Windows/macOS

### Step 5: Run the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run application
python3 app.py
```

### Common Linux Issues

**Issue: "No module named 'pip'"**
- Solution: `sudo apt install python3-pip`

**Issue: Permission denied**
- Solution: `chmod +x app.py` or use `python3 app.py`

**Issue: Permission denied for virtual environment**
- Solution: `chmod +x venv/bin/activate`

---

## 🔧 Getting Azure Credentials

### Step-by-Step Instructions

1. **Go to Azure Portal**
   - Open https://portal.azure.com
   - Sign in with your Microsoft account

2. **Create Resource** (if you don't have one)
   - Click "Create a resource"
   - Search for "Content Safety"
   - Click "Create"
   - Fill in details:
     - Name: `mycontentsafety`
     - Resource Group: Create new
     - Region: East US (or closest to you)
     - Pricing: Free tier (F0) for testing
   - Click "Review + Create" then "Create"

3. **Get Your Credentials**
   - Go to your new resource
   - Click "Keys and Endpoint" in left menu
   - Copy **Key1** (or Key2)
   - Copy **Endpoint URL**

4. **Add to config.py**
   ```python
   AZURE_API_KEY = "paste_your_key_here"
   AZURE_ENDPOINT = "https://mycontentsafety.cognitiveservices.azure.com"
   ```

### Example Credentials (Format Only, Not Real)
```
API Key: 8a7f3e2d1c9b4a5f6e7d8c9b0a1f2e3d
Endpoint: https://mycontentsafety-west.cognitiveservices.azure.com
```

---

## ✅ Verification Checklist

After setup, verify everything is working:

```bash
# 1. Check Python version
python --version          # Should be 3.8+

# 2. Check virtual environment is active
which python              # Should show path inside venv/

# 3. Check required packages
pip list                  # Should show requests, flask, python-dotenv

# 4. Test imports
python -c "import requests; print('✓ requests works')"
python -c "import flask; print('✓ flask works')"

# 5. Test app startup
python app.py            # Should start without errors

# 6. Check credentials
grep -v "HERE" config.py  # Should show actual values, not placeholders
```

---

## 🚀 Running for the First Time

### Quick Test

1. Make sure virtual environment is activated
2. Run: `python app.py`
3. You should see:
   ```
   ==================================================
   🛡️  AZURE AI CONTENT SAFETY MODERATOR
   ==================================================
   ```

4. Type a test message: `Hello, how are you?`
5. Should show analysis results

### If It Fails

**Error: "Invalid API key"**
→ Check credentials in config.py

**Error: "ModuleNotFoundError"**
→ Install dependencies: `pip install -r requirements.txt`

**Error: "Connection timed out"**
→ Check internet connection and endpoint URL

---

## 🔄 Deactivating Virtual Environment

When you're done working:

```bash
# Windows
deactivate

# macOS/Linux
deactivate

# Or just close the terminal
```

---

## 📦 Updating Dependencies

```bash
# Update all packages to latest versions
pip install --upgrade -r requirements.txt

# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade requests
```

---

## 🐛 Troubleshooting Installation

### Issue: Virtual Environment Won't Activate

```bash
# Windows
python -m venv venv
venv\Scripts\activate.bat

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Issue: pip Commands Don't Work

```bash
# Try using python -m pip instead
python -m pip install -r requirements.txt

# Or upgrade pip first
python -m pip install --upgrade pip
```

### Issue: Dependency Installation Fails

```bash
# Clear pip cache
pip cache purge

# Try installing again
pip install -r requirements.txt

# If still fails, install individually
pip install requests==2.31.0
pip install flask==3.0.0
pip install python-dotenv==1.0.0
```

### Issue: Certificate Error on macOS

```bash
# macOS may need certificate installation
/Applications/Python\ 3.x/Install\ Certificates.command

# Then try pip install again
```

---

## 🌐 Network & Firewall Issues

### Behind Corporate Proxy

```bash
pip install --proxy [user:passwd@]proxy.server:port -r requirements.txt
```

### Firewall Blocking Azure

- Check if port 443 (HTTPS) is open
- Check if your network firewall allows requests to:
  - `*.cognitiveservices.azure.com`

---

## 💾 Backup & Recovery

### Backup Your Configuration

```bash
# Copy these files to safe location
- config.py
- .env (if using)
```

### Restore Project

```bash
# If something goes wrong
rm -rf venv/
python -m venv venv

# Activate and reinstall
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## ⚙️ Advanced Configuration

### Custom Severity Threshold

Edit `app.py` in main():
```python
moderator = ContentModerator(
    api_key=AZURE_API_KEY,
    endpoint=AZURE_ENDPOINT,
    severity_threshold=3  # Change from 2 to 3
)
```

### Enable Debug Mode

Edit `config.py`:
```python
DEBUG_MODE = True
```

### Change Flask Port

Edit `flask_api.py` at the bottom:
```python
app.run(port=5001)  # Change from 5000 to 5001
```

---

## ✨ Next Steps

After successful setup:
1. Run `python test_examples.py` to see demo analysis
2. Read [README.md](README.md) for full documentation
3. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
4. Check [PROJECT_PRESENTATION.md](PROJECT_PRESENTATION.md) for viva prep

---

**Setup Complete! 🎉**

For issues, refer to the Troubleshooting section or check README.md
