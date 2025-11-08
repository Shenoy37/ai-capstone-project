"""
AI Service for BRD Generator - Integration with Google Gemini API
"""

import google.generativeai as genai
from typing import Dict, List, Optional
import logging
from config.settings import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    """Service class for AI model integration"""
    
    def __init__(self):
        """Initialize the AI service with Gemini API"""
        try:
            Config.validate_config()
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            logger.info("AI Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI Service: {str(e)}")
            raise
    
    def generate_brd_content(self, 
                            domain: str, 
                            project_title: str,
                            project_description: str,
                            business_objectives: str,
                            stakeholders: str,
                            additional_requirements: str = "") -> Dict[str, str]:
        """
        Generate BRD content using Gemini AI
        
        Args:
            domain: Business domain (Pharma/Finance)
            project_title: Title of the project
            project_description: Description of the project
            business_objectives: Business objectives
            stakeholders: Key stakeholders
            additional_requirements: Any additional requirements
            
        Returns:
            Dictionary containing generated BRD sections
        """
        
        try:
            # Construct the prompt based on domain
            prompt = self._construct_prompt(
                domain, project_title, project_description, 
                business_objectives, stakeholders, additional_requirements
            )
            
            # Generate content
            logger.info(f"Generating BRD content for {domain} domain")
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=Config.MAX_TOKENS,
                    temperature=Config.TEMPERATURE,
                )
            )
            
            # Parse and structure the response
            brd_sections = self._parse_response(response.text, domain)
            
            logger.info("BRD content generated successfully")
            return brd_sections
            
        except Exception as e:
            logger.error(f"Error generating BRD content: {str(e)}")
            raise
    
    def _construct_prompt(self, 
                         domain: str, 
                         project_title: str,
                         project_description: str,
                         business_objectives: str,
                         stakeholders: str,
                         additional_requirements: str) -> str:
        """Construct domain-specific prompt for BRD generation"""
        
        domain_context = self._get_domain_context(domain)
        
        prompt = f"""
You are an expert Business Analyst specializing in {domain} domain. Generate a comprehensive Business Requirement Document (BRD) with the following details:

**Domain**: {domain}
**Project Title**: {project_title}
**Project Description**: {project_description}
**Business Objectives**: {business_objectives}
**Key Stakeholders**: {stakeholders}
**Additional Requirements**: {additional_requirements}

**Domain Context**: {domain_context}

Generate a detailed BRD with the following sections:
1. Project Overview
2. Business Objectives
3. Functional Requirements
4. Non-Functional Requirements
5. Key Performance Indicators (KPIs)
6. Compliance & Risk Assessment
7. Stakeholder Analysis
8. Project Scope

For each section, provide detailed, domain-specific content that addresses:
- Industry-standard terminology
- Relevant compliance requirements
- Domain-specific considerations
- Practical implementation details

Ensure the content is:
- Professional and well-structured
- Compliance-ready for {domain} regulations
- Comprehensive and actionable
- Aligned with industry best practices

Format your response as a structured document with clear section headings and detailed content for each section.
"""
        
        return prompt
    
    def _get_domain_context(self, domain: str) -> str:
        """Get domain-specific context and compliance requirements"""
        
        if domain.lower() == "pharma":
            return """
Pharmaceutical Domain Context:
- Regulatory Framework: FDA 21 CFR Part 11, HIPAA, GxP guidelines
- Key Processes: Clinical trials, adverse event reporting, drug safety monitoring
- Data Requirements: Patient data anonymization, electronic health record (EHR) integration
- Compliance Focus: Data integrity, audit trails, validation protocols
- Terminology: Clinical trial phases, investigational medicinal products, pharmacovigilance
"""
        
        elif domain.lower() == "finance":
            return """
Finance Domain Context:
- Regulatory Framework: Basel III, GDPR, SOX, financial reporting standards
- Key Processes: Credit risk assessment, loan default prediction, collateral management
- Data Requirements: Financial data security, customer data protection, audit readiness
- Compliance Focus: Risk management, capital adequacy, data privacy
- Terminology: Probability of Default (PD), Loss Given Default (LGD), credit scoring, risk-weighted assets
"""
        
        else:
            return "General business context with standard compliance requirements."
    
    def _parse_response(self, response_text: str, domain: str) -> Dict[str, str]:
        """Parse the AI response into structured BRD sections"""
        
        sections = {}
        current_section = None
        current_content = []
        
        lines = response_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Check if line is a section header
            if self._is_section_header(line):
                # Save previous section if exists
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = line.replace('#', '').strip()
                current_content = []
            
            elif line and current_section:
                current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # Ensure all required sections are present
        for required_section in Config.BRD_SECTIONS:
            if required_section not in sections:
                sections[required_section] = f"[Content for {required_section} will be generated based on specific requirements]"
        
        return sections
    
    def _is_section_header(self, line: str) -> bool:
        """Check if a line is a section header"""
        section_keywords = [
            "Project Overview", "Business Objectives", "Functional Requirements",
            "Non-Functional Requirements", "Key Performance Indicators", "KPIs",
            "Compliance", "Risk Assessment", "Stakeholder Analysis", "Project Scope"
        ]
        
        for keyword in section_keywords:
            if keyword.lower() in line.lower():
                return True
        
        return False
    
    def validate_api_connection(self) -> bool:
        """Validate connection to Gemini API"""
        try:
            test_response = self.model.generate_content("Test connection")
            return True
        except Exception as e:
            logger.error(f"API connection validation failed: {str(e)}")
            return False