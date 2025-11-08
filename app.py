"""
Main Streamlit Application for Intelligent BRD Generator
"""

import streamlit as st
import os
import sys
from datetime import datetime
from typing import Dict, Any
import logging

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import AIService
from services.document_service import DocumentService
from services.validation_service import ValidationService
from config.settings import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
@st.cache_resource
def initialize_services():
    """Initialize all services with caching"""
    try:
        ai_service = AIService()
        document_service = DocumentService()
        validation_service = ValidationService()
        return ai_service, document_service, validation_service
    except Exception as e:
        st.error(f"Failed to initialize services: {str(e)}")
        return None, None, None

def setup_page_config():
    """Setup Streamlit page configuration"""
    st.set_page_config(
        page_title="Intelligent BRD Generator",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def create_input_form():
    """Create the main input form for BRD generation"""
    
    st.header("📋 BRD Generation Form")
    
    with st.form("brd_form"):
        # Domain Selection
        col1, col2 = st.columns(2)
        
        with col1:
            domain = st.selectbox(
                "Select Business Domain *",
                options=Config.SUPPORTED_DOMAINS,
                help="Choose the industry domain for your BRD"
            )
            
            project_title = st.text_input(
                "Project Title *",
                placeholder="Enter your project title",
                help="A clear, descriptive title for your project"
            )
        
        with col2:
            stakeholders = st.text_area(
                "Key Stakeholders *",
                placeholder="List key stakeholders (e.g., Project Manager, Business Analyst, Compliance Officer)",
                help="Identify the main stakeholders involved in this project"
            )
            
            priority = st.selectbox(
                "Project Priority",
                options=["High", "Medium", "Low"],
                help="Select the priority level of this project"
            )
        
        # Project Details
        st.subheader("Project Details")
        
        project_description = st.text_area(
            "Project Description *",
            placeholder="Provide a detailed description of your project, including background and context",
            height=120,
            help="Describe what this project aims to accomplish and the problem it solves"
        )
        
        business_objectives = st.text_area(
            "Business Objectives *",
            placeholder="List the main business objectives and expected outcomes",
            height=100,
            help="What are the specific business goals this project will achieve?"
        )
        
        additional_requirements = st.text_area(
            "Additional Requirements (Optional)",
            placeholder="Any additional information, constraints, or special considerations",
            height=80,
            help="Include any other relevant information that should be considered"
        )
        
        # Customization Options
        st.subheader("Customization Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            include_kpis = st.checkbox("Include KPIs", value=True)
        
        with col2:
            include_compliance = st.checkbox("Include Compliance Section", value=True)
        
        with col3:
            include_risk = st.checkbox("Include Risk Assessment", value=True)
        
        # Submit button
        submit_button = st.form_submit_button(
            "🚀 Generate BRD",
            type="primary",
            use_container_width=True
        )
        
        # Return form data
        if submit_button:
            return {
                "domain": domain,
                "project_title": project_title,
                "project_description": project_description,
                "business_objectives": business_objectives,
                "stakeholders": stakeholders,
                "additional_requirements": additional_requirements,
                "priority": priority,
                "include_kpis": include_kpis,
                "include_compliance": include_compliance,
                "include_risk": include_risk
            }
        
        return None

def validate_form_data(form_data: Dict[str, Any]) -> bool:
    """Validate form data before processing"""
    
    # Check domain separately since it's a selectbox with short values
    if not form_data.get("domain"):
        st.error("Please select a business domain")
        return False
    
    # Check other required fields with minimum length validation
    text_fields = {
        "project_title": 5,
        "project_description": 20,
        "business_objectives": 15,
        "stakeholders": 10
    }
    
    for field, min_length in text_fields.items():
        field_value = form_data.get(field)
        if not field_value or len(field_value.strip()) < min_length:
            st.error(f"Please provide a valid {field.replace('_', ' ').title()} (minimum {min_length} characters)")
            return False
    
    return True

def display_brd_preview(brd_sections: Dict[str, str]):
    """Display a preview of the generated BRD"""
    
    st.subheader("📖 BRD Preview")
    
    # Create tabs for different sections
    tabs = st.tabs(list(brd_sections.keys()))
    
    for i, (section_name, section_content) in enumerate(brd_sections.items()):
        with tabs[i]:
            if section_content:
                st.markdown(f"### {section_name}")
                st.write(section_content)
            else:
                st.info(f"Content for {section_name} will be generated based on specific requirements")

def display_validation_results(validation_result, quality_metrics):
    """Display validation results and quality metrics"""
    
    st.subheader("🔍 Validation Results")
    
    # Overall score
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score_color = "🟢" if validation_result.overall_score >= 0.8 else "🟡" if validation_result.overall_score >= 0.6 else "🔴"
        st.metric(
            "Overall Score", 
            f"{validation_result.overall_score:.2f}/1.00",
            delta=score_color
        )
    
    with col2:
        st.metric(
            "Compliance Score", 
            f"{validation_result.compliance_score:.2f}/1.00"
        )
    
    with col3:
        st.metric(
            "Completeness Score", 
            f"{validation_result.completeness_score:.2f}/1.00"
        )
    
    # Detailed results
    if validation_result.recommendations:
        st.subheader("💡 Recommendations")
        for i, rec in enumerate(validation_result.recommendations, 1):
            st.write(f"{i}. {rec}")
    
    if validation_result.warnings:
        st.subheader("⚠️ Warnings")
        for warning in validation_result.warnings:
            st.warning(warning)
    
    # Quality metrics
    st.subheader("📊 Quality Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Word Count", quality_metrics["total_word_count"])
        st.metric("Readability Score", f"{quality_metrics['readability_score']:.2f}/1.00")
    
    with col2:
        st.metric("Structure Score", f"{quality_metrics['structure_score']:.2f}/1.00")
        st.metric("Sections with Content", len([s for s in quality_metrics['section_word_counts'].values() if s > 0]))

def main():
    """Main application function"""
    
    # Setup page
    setup_page_config()
    
    # Initialize services
    ai_service, document_service, validation_service = initialize_services()
    
    if not all([ai_service, document_service, validation_service]):
        st.error("❌ Failed to initialize application services. Please check your configuration.")
        return
    
    # Header
    st.title("🤖 Intelligent BRD Generator")
    st.markdown("*Domain-specific Business Requirement Document Generator for Pharma and Finance*")
    st.markdown("---")
    
    # Sidebar information
    with st.sidebar:
        st.header("ℹ️ About")
        st.info("""
        This AI-powered tool generates comprehensive Business Requirement Documents (BRDs) tailored for specific domains.
        
        **Features:**
        - Domain-specific content generation
        - Compliance-aware documentation
        - Quality validation
        - Export to Word format
        """)
        
        st.header("📋 Quick Guide")
        st.markdown("""
        1. Select your business domain
        2. Fill in project details
        3. Customize sections as needed
        4. Generate and review BRD
        5. Export final document
        """)
    
    # Main content area
    tab1, tab2 = st.tabs(["📝 Generate BRD", "📚 Sample Documents"])
    
    with tab1:
        # Input form
        form_data = create_input_form()
        
        if form_data:
            # Validate form data
            if not validate_form_data(form_data):
                st.stop()
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Generate BRD content
                status_text.text("🤖 Generating BRD content using AI...")
                progress_bar.progress(25)
                
                brd_sections = ai_service.generate_brd_content(
                    domain=form_data["domain"],
                    project_title=form_data["project_title"],
                    project_description=form_data["project_description"],
                    business_objectives=form_data["business_objectives"],
                    stakeholders=form_data["stakeholders"],
                    additional_requirements=form_data["additional_requirements"]
                )
                
                # Step 2: Validate content
                status_text.text("🔍 Validating content quality and compliance...")
                progress_bar.progress(50)
                
                validation_result = validation_service.validate_brd_content(
                    brd_sections, form_data["domain"]
                )
                
                quality_metrics = validation_service.check_document_quality(brd_sections)
                
                # Step 3: Display results
                status_text.text("✅ BRD generated successfully!")
                progress_bar.progress(100)
                
                # Success message
                st.success(f"🎉 BRD for '{form_data['project_title']}' has been generated successfully!")
                
                # Display preview
                display_brd_preview(brd_sections)
                
                # Display validation results
                display_validation_results(validation_result, quality_metrics)
                
                # Export options
                st.subheader("💾 Export Options")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📄 Download as Word Document", type="primary"):
                        try:
                            metadata = {
                                "Priority": form_data["priority"],
                                "Generated By": "Intelligent BRD Generator",
                                "Validation Score": f"{validation_result.overall_score:.2f}/1.00"
                            }
                            
                            filepath = document_service.create_brd_document(
                                brd_sections=brd_sections,
                                domain=form_data["domain"],
                                project_title=form_data["project_title"],
                                metadata=metadata
                            )
                            
                            st.success(f"✅ Document saved successfully: {filepath}")
                            
                            # Provide download link
                            with open(filepath, "rb") as file:
                                st.download_button(
                                    label="📥 Download BRD Document",
                                    data=file.read(),
                                    file_name=os.path.basename(filepath),
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                        
                        except Exception as e:
                            st.error(f"❌ Error generating document: {str(e)}")
                
                with col2:
                    if st.button("📋 Generate Validation Report"):
                        validation_report = validation_service.generate_validation_report(
                            validation_result, quality_metrics
                        )
                        
                        st.subheader("📊 Validation Report")
                        st.text(validation_report)
                
                # Clear progress
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                st.error(f"❌ Error generating BRD: {str(e)}")
                logger.error(f"BRD generation error: {str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    with tab2:
        st.header("📚 Sample BRD Documents")
        
        st.subheader("Pharma Domain Example")
        st.info("""
        **Sample Scenario**: Clinical Trial Management System
        
        A pharmaceutical company needs a BRD for an adverse event tracking system during clinical trials.
        
        **Key Requirements**:
        - FDA 21 CFR Part 11 compliance
        - HIPAA data protection
        - Integration with EHR systems
        - Real-time adverse event reporting
        """)
        
        st.subheader("Finance Domain Example")
        st.info("""
        **Sample Scenario**: Credit Risk Analytics Platform
        
        A financial institution needs a BRD for a credit risk assessment platform.
        
        **Key Requirements**:
        - Basel III compliance
        - Probability of Default (PD) modeling
        - Risk-weighted asset calculation
        - Regulatory reporting capabilities
        """)
        
        st.subheader("🚀 Getting Started")
        st.markdown("""
        To generate your own BRD:
        1. Navigate to the "Generate BRD" tab
        2. Select your domain (Pharma or Finance)
        3. Fill in your project details
        4. Click "Generate BRD" to create your document
        5. Review, validate, and export your BRD
        """)

if __name__ == "__main__":
    main()