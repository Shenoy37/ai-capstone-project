"""
Validation Service for BRD Generator - Handles content validation and compliance checking
"""

import re
from typing import Dict, List, Tuple
import logging
from config.settings import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidationResult:
    """Class to hold validation results"""
    
    def __init__(self):
        self.is_valid = True
        self.compliance_score = 0.0
        self.terminology_score = 0.0
        self.completeness_score = 0.0
        self.overall_score = 0.0
        self.missing_keywords = []
        self.missing_sections = []
        self.recommendations = []
        self.warnings = []
    
    def calculate_overall_score(self):
        """Calculate overall validation score"""
        self.overall_score = (
            self.compliance_score * 0.4 +
            self.terminology_score * 0.3 +
            self.completeness_score * 0.3
        )
        
        # Set validity based on overall score
        self.is_valid = self.overall_score >= 0.7
        
        return self.overall_score
    
    def to_dict(self) -> Dict:
        """Convert validation result to dictionary"""
        return {
            "is_valid": self.is_valid,
            "compliance_score": self.compliance_score,
            "terminology_score": self.terminology_score,
            "completeness_score": self.completeness_score,
            "overall_score": self.overall_score,
            "missing_keywords": self.missing_keywords,
            "missing_sections": self.missing_sections,
            "recommendations": self.recommendations,
            "warnings": self.warnings
        }

class ValidationService:
    """Service class for BRD content validation"""
    
    def __init__(self):
        """Initialize the validation service"""
        self.compliance_keywords = Config.COMPLIANCE_KEYWORDS
        self.required_sections = Config.BRD_SECTIONS
        logger.info("Validation Service initialized successfully")
    
    def validate_brd_content(self, 
                            brd_sections: Dict[str, str],
                            domain: str) -> ValidationResult:
        """
        Validate BRD content for compliance, terminology, and completeness
        
        Args:
            brd_sections: Dictionary containing BRD sections
            domain: Business domain (Pharma/Finance)
            
        Returns:
            ValidationResult object with validation details
        """
        
        result = ValidationResult()
        
        try:
            # Validate compliance keywords
            result.compliance_score = self._validate_compliance_keywords(brd_sections, domain)
            
            # Validate domain terminology
            result.terminology_score = self._validate_domain_terminology(brd_sections, domain)
            
            # Validate section completeness
            result.completeness_score = self._validate_section_completeness(brd_sections)
            
            # Generate recommendations
            self._generate_recommendations(result, brd_sections, domain)
            
            # Calculate overall score
            result.calculate_overall_score()
            
            logger.info(f"Validation completed with overall score: {result.overall_score:.2f}")
            
        except Exception as e:
            logger.error(f"Error during validation: {str(e)}")
            result.warnings.append(f"Validation error: {str(e)}")
            result.is_valid = False
        
        return result
    
    def _validate_compliance_keywords(self, brd_sections: Dict[str, str], domain: str) -> float:
        """Validate presence of compliance keywords"""
        
        if domain not in self.compliance_keywords:
            return 0.5  # Default score for unknown domains
        
        required_keywords = self.compliance_keywords[domain]
        all_content = " ".join(brd_sections.values()).lower()
        
        found_keywords = []
        missing_keywords = []
        
        for keyword in required_keywords:
            if keyword.lower() in all_content:
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        # Calculate score
        score = len(found_keywords) / len(required_keywords) if required_keywords else 0
        
        # Store missing keywords for recommendations
        if hasattr(self, '_current_result'):
            self._current_result.missing_keywords = missing_keywords
        
        logger.info(f"Compliance validation: {len(found_keywords)}/{len(required_keywords)} keywords found")
        
        return score
    
    def _validate_domain_terminology(self, brd_sections: Dict[str, str], domain: str) -> float:
        """Validate domain-specific terminology usage"""
        
        domain_terminology = self._get_domain_terminology(domain)
        all_content = " ".join(brd_sections.values()).lower()
        
        found_terms = []
        for term in domain_terminology:
            if term.lower() in all_content:
                found_terms.append(term)
        
        # Calculate score based on terminology coverage
        expected_terms = min(5, len(domain_terminology))  # Expect at least 5 domain terms
        score = min(len(found_terms) / expected_terms, 1.0)
        
        logger.info(f"Terminology validation: {len(found_terms)} domain terms found")
        
        return score
    
    def _validate_section_completeness(self, brd_sections: Dict[str, str]) -> float:
        """Validate that all required sections are present and have content"""
        
        present_sections = list(brd_sections.keys())
        missing_sections = []
        empty_sections = []
        
        for required_section in self.required_sections:
            if required_section not in present_sections:
                missing_sections.append(required_section)
            elif not brd_sections[required_section] or len(brd_sections[required_section].strip()) < 50:
                empty_sections.append(required_section)
        
        # Calculate completeness score
        total_sections = len(self.required_sections)
        complete_sections = total_sections - len(missing_sections) - len(empty_sections)
        score = complete_sections / total_sections
        
        # Store missing sections for recommendations
        if hasattr(self, '_current_result'):
            self._current_result.missing_sections = missing_sections + empty_sections
        
        logger.info(f"Completeness validation: {complete_sections}/{total_sections} sections complete")
        
        return score
    
    def _generate_recommendations(self, result: ValidationResult, brd_sections: Dict[str, str], domain: str):
        """Generate improvement recommendations based on validation results"""
        
        # Store reference to result for use in other methods
        self._current_result = result
        
        # Compliance recommendations
        if result.compliance_score < 0.8:
            result.recommendations.append(
                f"Consider adding more compliance references for {domain} domain"
            )
            if result.missing_keywords:
                result.recommendations.append(
                    f"Include these compliance keywords: {', '.join(result.missing_keywords[:3])}"
                )
        
        # Terminology recommendations
        if result.terminology_score < 0.7:
            result.recommendations.append(
                f"Include more {domain}-specific terminology for better domain alignment"
            )
        
        # Completeness recommendations
        if result.completeness_score < 0.8:
            if result.missing_sections:
                result.recommendations.append(
                    f"Add content for missing sections: {', '.join(result.missing_sections)}"
                )
            result.recommendations.append(
                "Ensure each section has comprehensive content (minimum 50 words)"
            )
        
        # Quality warnings
        for section_name, section_content in brd_sections.items():
            if section_content:
                word_count = len(section_content.split())
                if word_count < 30:
                    result.warnings.append(
                        f"Section '{section_name}' appears to be too brief ({word_count} words)"
                    )
        
        # Remove reference to avoid memory leaks
        delattr(self, '_current_result')
    
    def _get_domain_terminology(self, domain: str) -> List[str]:
        """Get domain-specific terminology for validation"""
        
        if domain.lower() == "pharma":
            return [
                "clinical trial", "adverse event", "fda", "hipaa", "gxp",
                "investigational", "pharmacovigilance", "regulatory", "validation",
                "protocol", "informed consent", "data integrity", "audit trail"
            ]
        
        elif domain.lower() == "finance":
            return [
                "credit risk", "basel iii", "probability of default", "loss given default",
                "collateral", "regulatory", "compliance", "risk assessment",
                "capital adequacy", "stress testing", "audit", "governance"
            ]
        
        else:
            return ["business", "requirements", "stakeholders", "compliance"]
    
    def check_document_quality(self, brd_sections: Dict[str, str]) -> Dict[str, any]:
        """
        Perform additional quality checks on the document
        
        Args:
            brd_sections: Dictionary containing BRD sections
            
        Returns:
            Dictionary with quality metrics
        """
        
        quality_metrics = {
            "total_word_count": 0,
            "section_word_counts": {},
            "readability_score": 0.0,
            "structure_score": 0.0,
            "content_quality_issues": []
        }
        
        total_words = 0
        
        for section_name, section_content in brd_sections.items():
            if section_content:
                word_count = len(section_content.split())
                quality_metrics["section_word_counts"][section_name] = word_count
                total_words += word_count
                
                # Check for quality issues
                if word_count < 20:
                    quality_metrics["content_quality_issues"].append(
                        f"Section '{section_name}' is too brief"
                    )
                
                # Check for repetitive content
                sentences = section_content.split('.')
                if len(sentences) > 0:
                    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
                    if avg_sentence_length > 30:
                        quality_metrics["content_quality_issues"].append(
                            f"Section '{section_name}' has very long sentences"
                        )
        
        quality_metrics["total_word_count"] = total_words
        
        # Calculate readability score (simplified)
        if total_words > 0:
            quality_metrics["readability_score"] = min(total_words / 500, 1.0)
        
        # Calculate structure score
        expected_sections = len(self.required_sections)
        actual_sections = len([s for s in brd_sections.values() if s and len(s.strip()) > 0])
        quality_metrics["structure_score"] = actual_sections / expected_sections
        
        return quality_metrics
    
    def generate_validation_report(self, result: ValidationResult, quality_metrics: Dict) -> str:
        """
        Generate a comprehensive validation report
        
        Args:
            result: ValidationResult object
            quality_metrics: Quality metrics dictionary
            
        Returns:
            Formatted validation report
        """
        
        report_lines = []
        report_lines.append("=== BRD VALIDATION REPORT ===\n")
        
        # Overall assessment
        status = "PASSED" if result.is_valid else "FAILED"
        report_lines.append(f"Overall Status: {status}")
        report_lines.append(f"Overall Score: {result.overall_score:.2f}/1.00")
        report_lines.append("")
        
        # Detailed scores
        report_lines.append("DETAILED SCORES:")
        report_lines.append(f"  Compliance Score: {result.compliance_score:.2f}/1.00")
        report_lines.append(f"  Terminology Score: {result.terminology_score:.2f}/1.00")
        report_lines.append(f"  Completeness Score: {result.completeness_score:.2f}/1.00")
        report_lines.append("")
        
        # Quality metrics
        report_lines.append("QUALITY METRICS:")
        report_lines.append(f"  Total Word Count: {quality_metrics['total_word_count']}")
        report_lines.append(f"  Readability Score: {quality_metrics['readability_score']:.2f}/1.00")
        report_lines.append(f"  Structure Score: {quality_metrics['structure_score']:.2f}/1.00")
        report_lines.append("")
        
        # Recommendations
        if result.recommendations:
            report_lines.append("RECOMMENDATIONS:")
            for i, rec in enumerate(result.recommendations, 1):
                report_lines.append(f"  {i}. {rec}")
            report_lines.append("")
        
        # Warnings
        if result.warnings:
            report_lines.append("WARNINGS:")
            for warning in result.warnings:
                report_lines.append(f"  • {warning}")
            report_lines.append("")
        
        # Quality issues
        if quality_metrics["content_quality_issues"]:
            report_lines.append("CONTENT QUALITY ISSUES:")
            for issue in quality_metrics["content_quality_issues"]:
                report_lines.append(f"  • {issue}")
        
        return "\n".join(report_lines)