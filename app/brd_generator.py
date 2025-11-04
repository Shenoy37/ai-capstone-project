from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency during local development
    OpenAI = None  # type: ignore


logger = logging.getLogger(__name__)


@dataclass
class BRDGenerator:
    """Create Business Requirements Document outlines for supported domains."""

    model: str = "gpt-4o"
    temperature: float = 0.2

    def __post_init__(self) -> None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if OpenAI is None or not api_key:
            self.client = None
            if OpenAI is None:
                logger.info("openai package not available; falling back to template generator.")
            else:
                logger.info("OPENAI_API_KEY not set; falling back to template generator.")
            return

        self.client = OpenAI(api_key=api_key)

    def generate_brd(self, domain: str, project_description: str, additional_notes: str = "") -> Dict[str, Any]:
        domain = domain.lower()
        if domain not in {"pharma", "finance"}:
            logger.warning("Unsupported domain %s provided. Defaulting to Pharma template.", domain)
            domain = "pharma"

        ai_result = self._generate_with_gpt(domain, project_description, additional_notes)
        if ai_result:
            return ai_result

        return self._generate_template(domain, project_description, additional_notes)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _generate_with_gpt(
        self, domain: str, project_description: str, additional_notes: str
    ) -> Optional[Dict[str, Any]]:
        if self.client is None:
            return None

        domain_context = {
            "pharma": "Focus on clinical trials, regulatory compliance (FDA/EMA), pharmacovigilance, data integrity, and validation requirements.",
            "finance": "Focus on regulatory compliance (SEC, FINRA, Basel III), risk management, audit trails, security, and data privacy requirements.",
        }

        system_prompt = (
            "You are an expert business analyst. Generate a Business Requirements Document (BRD) "
            "tailored to the requested domain. Respond with valid JSON using the schema: "
            "{\"title\": str, \"executive_summary\": str, \"objectives\": [str], \"scope\": {\"in_scope\": [str], "
            "\"out_of_scope\": [str]}, \"stakeholders\": [str], \"functional_requirements\": [str], "
            "\"non_functional_requirements\": [str], \"data_requirements\": [str], \"regulatory_and_compliance\": [str], "
            "\"risks_and_mitigations\": [str], \"timeline\": [str], \"dependencies\": [str], \"open_questions\": [str]}"
        )

        user_prompt = (
            f"Domain: {domain}\n"
            f"Domain guidance: {domain_context[domain]}\n\n"
            "Project context:\n"
            f"{project_description.strip()}\n\n"
            "Additional notes:\n"
            f"{additional_notes.strip() or 'None provided.'}\n\n"
            "Only return JSON — do not include code fences or commentary."
        )

        try:
            response = self.client.responses.create(  # type: ignore[union-attr]
                model=self.model,
                temperature=self.temperature,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
        except Exception as exc:  # pragma: no cover - network interaction
            logger.error("OpenAI request failed: %s", exc)
            return None

        try:
            raw_text = response.output_text  # type: ignore[attr-defined]
        except AttributeError:  # pragma: no cover - safety for SDK changes
            logger.error("Unexpected OpenAI response structure: %s", response)
            return None

        if not raw_text:
            logger.error("Empty response from OpenAI.")
            return None

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse JSON response: %s\nPayload: %s", exc, raw_text)
            return None

        return data

    def _generate_template(
        self, domain: str, project_description: str, additional_notes: str
    ) -> Dict[str, Any]:
        """Fallback deterministic generator when the OpenAI client is unavailable."""

        domain_specifics: Dict[str, Dict[str, List[str]]] = {
            "pharma": {
                "objectives": [
                    "Ensure alignment with Good Clinical Practice (GCP) and regulatory standards.",
                    "Streamline trial operations with validated digital workflows.",
                    "Enhance pharmacovigilance monitoring and reporting speed.",
                ],
                "functional": [
                    "Capture and manage clinical study protocols with role-based approvals.",
                    "Track adverse events with automated signal detection and escalation rules.",
                    "Integrate with laboratory information systems for real-time data ingestion.",
                ],
                "non_functional": [
                    "21 CFR Part 11 compliant audit trails for all data changes.",
                    "Validated system with documented Installation/Operational Qualification (IQ/OQ).",
                    "High availability architecture supporting 99.9% uptime across study phases.",
                ],
                "regulatory": [
                    "FDA and EMA submission alignment, including eCTD document structures.",
                    "ICH E6 (R3) adherence for clinical quality management.",
                    "Pharmacovigilance reporting compliance with global safety regulations.",
                ],
            },
            "finance": {
                "objectives": [
                    "Improve transparency for regulatory reporting and internal audits.",
                    "Automate risk scoring to support credit and market risk decisions.",
                    "Provide customer-facing insights while preserving data privacy controls.",
                ],
                "functional": [
                    "Generate regulatory filings (e.g., 10-Q/10-K) with configurable workflows.",
                    "Provide real-time risk dashboards with drill-down analytics.",
                    "Support Know Your Customer (KYC) onboarding with rule-based verification.",
                ],
                "non_functional": [
                    "Encryption of data at rest and in transit aligned with FFIEC guidelines.",
                    "Support for disaster recovery with Recovery Time Objective (RTO) under 4 hours.",
                    "Role-based access controls integrated with enterprise identity providers.",
                ],
                "regulatory": [
                    "SOX-compliant controls and audit logging for financial transactions.",
                    "Basel III capital adequacy and stress testing documentation support.",
                    "Adherence to GDPR/CCPA data privacy requirements for customer information.",
                ],
            },
        }

        specifics = domain_specifics[domain]
        base_title = "Pharma BRD" if domain == "pharma" else "Finance BRD"

        return {
            "title": f"{base_title} Draft",
            "executive_summary": (
                "This Business Requirements Document was generated from the provided project context. "
                "It highlights priorities, constraints, and regulatory expectations specific to the "
                f"{domain.capitalize()} domain.\n\n"
                f"Project context summary: {project_description.strip()}\n\n"
                f"Additional notes: {additional_notes.strip() or 'None provided.'}"
            ),
            "objectives": specifics["objectives"],
            "scope": {
                "in_scope": [
                    "Core capabilities described in the project context.",
                    "Process digitization and stakeholder experiences outlined in discovery.",
                    "Regulatory and quality management features essential to the domain.",
                ],
                "out_of_scope": [
                    "Adjacent initiatives not referenced in the current business case.",
                    "Legacy platform decommissioning beyond agreed integration points.",
                ],
            },
            "stakeholders": [
                "Executive Sponsor",
                "Business Owner",
                "Domain Subject Matter Experts",
                "IT Delivery Lead",
                "Quality and Compliance Officer",
            ],
            "functional_requirements": specifics["functional"],
            "non_functional_requirements": specifics["non_functional"],
            "data_requirements": [
                "Authoritative data sources catalogued with ownership and refresh frequency.",
                "Data lineage tracking across ingestion, transformation, and reporting layers.",
                "Data quality rules with monitoring thresholds and stewardship workflows.",
            ],
            "regulatory_and_compliance": specifics["regulatory"],
            "risks_and_mitigations": [
                "Regulatory change impacting scope — maintain change-control governance.",
                "Data integration complexity — allocate technical spikes and sandbox testing.",
                "User adoption risk — schedule enablement sessions and champion network.",
            ],
            "timeline": [
                "Discovery & requirements validation: 4-6 weeks.",
                "Solution design & vendor alignment: 6-8 weeks.",
                "Implementation & testing: 12-16 weeks (iterative).",
                "Validation & launch readiness: 4 weeks.",
            ],
            "dependencies": [
                "Access to subject matter experts for validation reviews.",
                "Availability of source system APIs and sandbox environments.",
                "Budget approvals for technology or vendor procurements.",
            ],
            "open_questions": [
                "Clarify success metrics and KPIs for executive reporting.",
                "Confirm integration boundaries with existing enterprise platforms.",
                "Determine change management approach for impacted user groups.",
            ],
        }
