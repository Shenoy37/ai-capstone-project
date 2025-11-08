"""
AI Service for BRD Generator - Integration with Mistral API
"""

from mistralai import Mistral
from typing import Dict, List, Optional
import logging
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config.settings import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    """Service class for Mistral AI model integration"""
    
    def __init__(self):
        """Initialize the AI service with Mistral API"""
        try:
            Config.validate_config()
            self.api_config = Config.get_api_config()
            
            self._init_mistral()
                
            logger.info("AI Service initialized successfully with Mistral provider")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI Service: {str(e)}")
            raise
    
    def _init_mistral(self):
        """Initialize Mistral API client"""
        self.mistral_client = Mistral(
            api_key=self.api_config["api_key"],
            server_url=self.api_config.get("base_url")
        )
        logger.info("Mistral API client initialized")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError, Exception))
    )
    def _make_mistral_request(self, messages: List[Dict], max_tokens: int = None, temperature: float = None) -> str:
        """
        Make a request to Mistral API with retry logic
        
        Args:
            messages: List of message dictionaries for the conversation
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If API request fails after retries
        """
        try:
            # Rate limiting - add small delay between requests
            time.sleep(0.5)
            
            logger.info(f"Making Mistral API request with model: {self.api_config['model']}")
            
            response = self.mistral_client.chat.complete(
                model=self.api_config["model"],
                messages=messages,
                max_tokens=max_tokens or Config.MAX_TOKENS,
                temperature=temperature or Config.TEMPERATURE
            )
            
            if not response or not response.choices:
                raise ValueError("Empty response from Mistral API")
                
            generated_text = response.choices[0].message.content
            logger.info(f"Mistral API request successful, generated {len(generated_text)} characters")
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Mistral API request failed: {str(e)}")
            raise
    
    def generate_brd_content(self, 
                            domain: str, 
                            project_title: str,
                            project_description: str,
                            business_objectives: str,
                            stakeholders: str,
                            additional_requirements: str = "") -> Dict[str, str]:
        """
        Generate BRD content using Mistral AI
        
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
            logger.info(f"Generating BRD content for {domain} domain using Mistral")
            
            # Construct Mistral messages
            messages = self._construct_mistral_messages(
                domain, project_title, project_description, 
                business_objectives, stakeholders, additional_requirements
            )
            
            response_text = self._make_mistral_request(messages)
            
            # Parse and structure the response
            brd_sections = self._parse_response(response_text, domain)
            
            logger.info("BRD content generated successfully")
            return brd_sections
            
        except Exception as e:
            logger.error(f"Error generating BRD content: {str(e)}")
            raise
    
    def _construct_mistral_messages(self, 
                                 domain: str, 
                                 project_title: str,
                                 project_description: str,
                                 business_objectives: str,
                                 stakeholders: str,
                                 additional_requirements: str) -> List[Dict]:
        """Construct Mistral-specific message format for BRD generation"""
        
        domain_context = self._get_domain_context(domain)
        
        system_message = f"""You are an expert Business Analyst specializing in {domain} domain. Generate comprehensive, professional Business Requirement Documents (BRDs) that are compliance-ready and aligned with industry best practices.

Domain Context: {domain_context}

Your responses must:
- Use industry-standard terminology
- Include relevant compliance requirements
- Provide practical implementation details
- Be well-structured and professional
- Address all specified sections comprehensively"""

        user_message = f"""Generate a detailed Business Requirement Document (BRD) with the following specifications:

**Domain**: {domain}
**Project Title**: {project_title}
**Project Description**: {project_description}
**Business Objectives**: {business_objectives}
**Key Stakeholders**: {stakeholders}
**Additional Requirements**: {additional_requirements}

Generate a comprehensive BRD with these exact sections:
1. Project Overview
2. Business Objectives
3. Functional Requirements
4. Non-Functional Requirements
5. Key Performance Indicators (KPIs)
6. Compliance & Risk Assessment
7. Stakeholder Analysis
8. Project Scope

For each section, provide detailed, domain-specific content. Format your response with clear section headings using the exact section names provided above."""

        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    
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
        """Validate connection to Mistral API"""
        try:
            # Test with a simple message
            test_messages = [
                {"role": "user", "content": "Test connection"}
            ]
            response = self._make_mistral_request(test_messages, max_tokens=10)
            return True
                
        except Exception as e:
            logger.error(f"API connection validation failed: {str(e)}")
            return False
    
    def get_provider_info(self) -> Dict[str, str]:
        """Get information about the Mistral AI provider"""
        return {
            "provider": "mistral",
            "model": self.api_config["model"],
            "status": "connected" if self.validate_api_connection() else "disconnected"
        }