"""
Test script for Mistral API integration in BRD Generator
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import AIService
from config.settings import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mistral_integration():
    """Test Mistral API integration with sample BRD generation"""
    
    print("🧪 Testing Mistral API Integration")
    print("=" * 50)
    
    try:
        # Test 1: Configuration validation
        print("\n1. Testing configuration...")
        Config.validate_config()
        print("✅ Configuration validation passed")
        
        # Test 2: AI Service initialization
        print("\n2. Testing AI Service initialization...")
        ai_service = AIService()
        provider_info = ai_service.get_provider_info()
        print(f"✅ AI Service initialized with provider: {provider_info['provider']}")
        print(f"   Model: {provider_info['model']}")
        print(f"   Status: {provider_info['status']}")
        
        # Test 3: API connection validation
        print("\n3. Testing API connection...")
        connection_valid = ai_service.validate_api_connection()
        if connection_valid:
            print("✅ API connection validation passed")
        else:
            print("❌ API connection validation failed")
            return False
        
        # Test 4: Sample BRD generation
        print("\n4. Testing sample BRD generation...")
        
        sample_data = {
            "domain": "Pharma",
            "project_title": "Clinical Trial Management System",
            "project_description": "A comprehensive system for managing clinical trials, including patient recruitment, data collection, and adverse event reporting.",
            "business_objectives": "Streamline clinical trial processes, ensure regulatory compliance, improve data accuracy, and reduce time-to-market for new drugs.",
            "stakeholders": "Clinical Research Coordinator, Data Manager, Regulatory Affairs Officer, Principal Investigator, IT Department",
            "additional_requirements": "System must integrate with existing EHR systems and support FDA 21 CFR Part 11 compliance."
        }
        
        print(f"   Generating BRD for: {sample_data['project_title']}")
        print(f"   Domain: {sample_data['domain']}")
        
        brd_sections = ai_service.generate_brd_content(**sample_data)
        
        print("✅ BRD generation completed successfully")
        print(f"   Generated {len(brd_sections)} sections:")
        
        for section_name, content in brd_sections.items():
            content_preview = content[:100] + "..." if len(content) > 100 else content
            print(f"   - {section_name}: {len(content)} characters")
            print(f"     Preview: {content_preview}")
        
        # Test 5: Test with Finance domain
        print("\n5. Testing Finance domain BRD generation...")
        
        finance_data = {
            "domain": "Finance",
            "project_title": "Credit Risk Analytics Platform",
            "project_description": "An advanced analytics platform for assessing credit risk, calculating probability of default, and managing risk-weighted assets.",
            "business_objectives": "Improve credit risk assessment accuracy, ensure Basel III compliance, automate risk calculations, and provide real-time risk monitoring.",
            "stakeholders": "Risk Manager, Credit Analyst, Compliance Officer, IT Department, Senior Management",
            "additional_requirements": "System must support regulatory reporting and integrate with existing core banking systems."
        }
        
        finance_brd = ai_service.generate_brd_content(**finance_data)
        print("✅ Finance domain BRD generation completed successfully")
        print(f"   Generated {len(finance_brd)} sections")
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed successfully!")
        print("Mistral API integration is working correctly.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    print("🚀 Starting Mistral API Integration Tests")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check if Mistral API key is available
    if not os.getenv("MISTRAL_API_KEY"):
        print("❌ MISTRAL_API_KEY not found in environment variables")
        print("Please set MISTRAL_API_KEY in your .env file")
        sys.exit(1)
    
    # Run tests
    test_passed = test_mistral_integration()
    
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   Mistral Integration: {'✅ PASSED' if test_passed else '❌ FAILED'}")
    
    if test_passed:
        print("\n🎉 All tests passed! The implementation is ready for use.")
        sys.exit(0)
    else:
        print("\n❌ Tests failed. Please check the errors above.")
        sys.exit(1)