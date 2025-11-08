"""
Application settings and configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "models/gemini-2.5-pro-preview-03-25"
    
    # Application Settings
    APP_TITLE = "Intelligent BRD Generator"
    APP_DESCRIPTION = "Domain-specific Business Requirement Document Generator for Pharma and Finance"
    
    # File Paths
    DATA_DIR = "data"
    TEMPLATES_DIR = os.path.join(DATA_DIR, "templates")
    GENERATED_DIR = os.path.join(DATA_DIR, "generated")
    COMPLIANCE_DIR = os.path.join(DATA_DIR, "compliance")
    
    # Domain Configuration
    SUPPORTED_DOMAINS = ["Pharma", "Finance"]
    
    # Document Settings
    MAX_TOKENS = 5000
    TEMPERATURE = 0.7
    
    # Validation Settings
    COMPLIANCE_KEYWORDS = {
        "Pharma": ["FDA", "21 CFR Part 11", "HIPAA", "GxP", "clinical trial", "adverse event"],
        "Finance": ["Basel III", "GDPR", "credit risk", "probability of default", "loss given default", "collateral"]
    }
    
    # Required BRD Sections
    BRD_SECTIONS = [
        "Project Overview",
        "Business Objectives", 
        "Functional Requirements",
        "Non-Functional Requirements",
        "Key Performance Indicators (KPIs)",
        "Compliance & Risk Assessment",
        "Stakeholder Analysis",
        "Project Scope"
    ]
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        
        # Create directories if they don't exist
        os.makedirs(cls.TEMPLATES_DIR, exist_ok=True)
        os.makedirs(cls.GENERATED_DIR, exist_ok=True)
        os.makedirs(cls.COMPLIANCE_DIR, exist_ok=True)
        
        return True