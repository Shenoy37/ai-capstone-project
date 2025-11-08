# Quick Setup Guide for Mistral AI Integration

## 🚀 Getting Started

This guide will help you set up BRD Generator with Mistral AI integration in just a few minutes.

## 📋 Prerequisites

- Python 3.8 or higher
- Mistral API key (get one at [console.mistral.ai](https://console.mistral.ai/))

## ⚡ Quick Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your settings
```

Edit `.env` file:
```env
# Set your Mistral API key
MISTRAL_API_KEY=your_mistral_api_key_here
```

### Step 3: Test Integration
```bash
python test_mistral_integration.py
```

### Step 4: Run Application
```bash
streamlit run app.py
```

## 🔧 Configuration

### Mistral AI Configuration
```env
MISTRAL_API_KEY=your_api_key_here
```

The application will automatically use Mistral AI with the `mistral-small-latest` model.

## 🧪 Testing

### Run Comprehensive Tests
```bash
python test_mistral_integration.py
```

### Test Import Only
```bash
python -c "from services.ai_service import AIService; print('Import successful')"
```

## 📚 Documentation

- **Full Integration Guide**: [MISTRAL_API_INTEGRATION.md](MISTRAL_API_INTEGRATION.md)
- **User Documentation**: [README.md](README.md)
- **API Configuration**: [config/settings.py](config/settings.py)

## 🐛 Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: No module named 'mistralai'
```bash
# Solution: Install missing dependencies
pip install mistralai>=0.4.0 tenacity>=8.2.0
```

#### 2. Invalid API Key
```bash
# Check your .env file
cat .env

# Ensure MISTRAL_API_KEY is set correctly
```

#### 3. Connection Issues
```bash
# Test internet connectivity
ping api.mistral.ai

# Check API key validity
python -c "
from services.ai_service import AIService
try:
    service = AIService()
    print('Connection successful')
except Exception as e:
    print(f'Connection failed: {e}')
"
```

## 📞 Support

If you encounter issues:

1. Check [troubleshooting section](MISTRAL_API_INTEGRATION.md#troubleshooting)
2. Run test script for diagnostics
3. Check application logs for detailed error messages

## 🎯 Next Steps

Once setup is complete:

1. Open the web application at `http://localhost:8501`
2. Select your domain (Pharma or Finance)
3. Fill in your project details
4. Generate your first BRD with Mistral AI!

---

**Happy BRD Generating with Mistral AI! 🎉**