# Intelligent BRD Generator

A Generative AI-powered application that creates domain-specific Business Requirement Documents (BRDs) for Pharmaceutical and Financial sectors using Mistral AI.

## 🚀 Features

- **Domain-Specific Content Generation**: Tailored BRDs for Pharma and Finance domains
- **Compliance-Aware Documentation**: Automatic inclusion of regulatory requirements
- **AI-Powered Content**: Uses Mistral AI for intelligent content generation
- **Quality Validation**: Built-in validation for compliance, terminology, and completeness
- **Export Functionality**: Generate professional Word documents
- **User-Friendly Interface**: Intuitive Streamlit-based web interface

## 📋 Supported Domains

### Pharmaceutical Domain
- FDA 21 CFR Part 11 compliance
- HIPAA data protection
- GxP guidelines
- Clinical trial management
- Adverse event reporting

### Finance Domain
- Basel III regulatory framework
- GDPR compliance
- Credit risk assessment
- Financial reporting standards
- Risk management guidelines

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Mistral API key

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd brd-generator
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the project root:
```
MISTRAL_API_KEY=your_mistral_api_key_here
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will open in your web browser at `http://localhost:8501`

## 📁 Project Structure

```
brd-generator/
├── app.py                 # Main Streamlit application
├── config/
│   ├── __init__.py
│   └── settings.py        # Application configuration
├── services/
│   ├── __init__.py
│   ├── ai_service.py      # AI integration with Gemini
│   ├── document_service.py # Document generation
│   └── validation_service.py # Content validation
├── utils/
│   ├── __init__.py
│   └── helpers.py         # Utility functions
├── data/
│   ├── templates/         # Domain templates
│   ├── generated/         # Generated BRDs
│   └── compliance/        # Compliance reference data
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # Project documentation
```

## 🎯 How to Use

### 1. Select Domain
Choose between Pharmaceutical and Finance domains based on your project requirements.

### 2. Fill Project Details
- **Project Title**: Clear, descriptive title for your project
- **Project Description**: Detailed description of your project
- **Business Objectives**: Specific goals and expected outcomes
- **Key Stakeholders**: List of main stakeholders involved
- **Additional Requirements**: Any other relevant information

### 3. Customize Sections
Select which sections to include in your BRD:
- KPIs (Key Performance Indicators)
- Compliance Section
- Risk Assessment

### 4. Generate BRD
Click the "Generate BRD" button to create your document using AI.

### 5. Review and Validate
- Preview the generated content
- Review validation results and quality metrics
- Check compliance and completeness scores

### 6. Export Document
Download the final BRD as a Word document for further use.

## 🔧 Configuration

### Application Settings
Edit `config/settings.py` to modify:
- Mistral API configuration
- Supported domains
- Validation parameters
- Document formatting options

### Compliance Keywords
Add domain-specific compliance keywords in the configuration:
```python
COMPLIANCE_KEYWORDS = {
    "Pharma": ["FDA", "21 CFR Part 11", "HIPAA", "GxP"],
    "Finance": ["Basel III", "GDPR", "SOX", "credit risk"]
}
```

## 📊 Validation Metrics

The system validates generated BRDs based on:

### Compliance Score (40% weight)
- Presence of regulatory keywords
- Inclusion of compliance references
- Domain-specific regulatory adherence

### Terminology Score (30% weight)
- Domain-specific terminology usage
- Industry-standard vocabulary
- Technical accuracy

### Completeness Score (30% weight)
- All required sections present
- Adequate content length
- Structured organization

## 🚨 Error Handling

### Common Issues and Solutions

1. **API Connection Error**
   - Verify your Mistral API key is correct
   - Check internet connectivity
   - Ensure API quota is available

2. **Generation Timeout**
   - Reduce content complexity
   - Check API rate limits
   - Try again after a short delay

3. **Document Export Error**
   - Ensure sufficient disk space
   - Check file permissions
   - Verify document content is not corrupted

## 🧪 Testing

### Running Tests
```bash
# Test AI service integration
python -m services.test_ai_service

# Test document generation
python -m services.test_document_service

# Test validation service
python -m services.test_validation_service
```

### Sample Test Cases
- Pharma domain: Clinical trial management system
- Finance domain: Credit risk analytics platform

## 📈 Performance Metrics

- **Generation Time**: <30 seconds for standard BRDs
- **Validation Accuracy**: >85% domain alignment
- **Compliance Coverage**: >90% regulatory inclusion
- **User Satisfaction**: Target ≥8/10 rating

## 🔒 Security Considerations

- API keys stored securely in environment variables
- Input validation and sanitization
- Secure file handling and temporary file cleanup
- No sensitive data logging

## 🌐 Deployment

### Local Development
```bash
streamlit run app.py --server.port 8501
```

### Cloud Deployment (Google Cloud Run)
1. Build Docker image
2. Push to Google Container Registry
3. Deploy to Cloud Run
4. Configure environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the sample BRDs in the data directory

## 🔄 Version History

- **v1.1.0**: Mistral AI integration with enhanced error handling and retry logic
- **v1.0.0**: Initial release with Pharma and Finance domain support
- Basic BRD generation and validation
- Word document export functionality
- Streamlit web interface

---

**Generated by Intelligent BRD Generator** 🤖