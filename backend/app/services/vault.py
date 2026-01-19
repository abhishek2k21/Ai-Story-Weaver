"""
Vault Agent: Ethical oversight and content safety.

This agent ensures therapeutic appropriateness, content safety, and ethical
AI practices throughout the storytelling process.
"""

from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel
import logging
import re
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class EthicalAssessment(BaseModel):
    """Represents an ethical assessment of content."""
    assessment_id: str
    content_type: str  # 'story', 'character', 'scene', 'interaction'
    content_hash: str
    ethical_score: float  # 0-1, higher is more ethical
    risk_factors: List[Dict[str, Any]]
    therapeutic_alignment: float  # 0-1
    safety_flags: List[str]
    recommendations: List[str]
    assessed_at: datetime

class ContentFilter(BaseModel):
    """Represents a content filtering rule."""
    filter_id: str
    category: str  # 'harmful_content', 'inappropriate_language', 'trigger_warnings'
    pattern: str  # regex pattern
    severity: str  # 'low', 'medium', 'high', 'critical'
    action: str  # 'block', 'flag', 'modify', 'allow_with_warning'
    therapeutic_context: Optional[str] = None

class TherapeuticGuideline(BaseModel):
    """Represents therapeutic guidelines for content."""
    guideline_id: str
    condition: str  # 'anxiety', 'depression', 'ptsd', 'trauma'
    content_restrictions: List[str]
    required_elements: List[str]
    intensity_limits: Dict[str, float]
    supervision_requirements: List[str]

class PrivacyAssessment(BaseModel):
    """Represents a privacy assessment."""
    assessment_id: str
    data_types: List[str]
    privacy_risks: List[Dict[str, Any]]
    compliance_score: float  # 0-1
    recommendations: List[str]
    gdpr_alignment: bool
    hipaa_alignment: bool

class VaultAgent:
    """Vault Agent for ethical oversight and content safety."""

    def __init__(self):
        """Initialize the Vault Agent."""
        self.content_filters = self._load_content_filters()
        self.therapeutic_guidelines = self._load_therapeutic_guidelines()
        self.assessment_history = []
        self.blocked_content = set()

    def assess_content_ethics(self, content: Dict[str, Any], context: Dict[str, Any]) -> EthicalAssessment:
        """Assess the ethical implications of content.

        Args:
            content: Content to assess
            context: Therapeutic and user context

        Returns:
            EthicalAssessment: Assessment results
        """
        try:
            content_hash = self._generate_content_hash(content)
            assessment_id = f"assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Perform multiple assessment layers
            safety_assessment = self._assess_content_safety(content)
            therapeutic_assessment = self._assess_therapeutic_alignment(content, context)
            privacy_assessment = self._assess_privacy_implications(content, context)

            # Calculate overall ethical score
            ethical_score = self._calculate_ethical_score(
                safety_assessment, therapeutic_assessment, privacy_assessment
            )

            # Identify risk factors
            risk_factors = self._identify_risk_factors(
                content, safety_assessment, therapeutic_assessment
            )

            # Generate safety flags
            safety_flags = self._generate_safety_flags(safety_assessment, risk_factors)

            # Create recommendations
            recommendations = self._generate_ethical_recommendations(
                ethical_score, risk_factors, context
            )

            assessment = EthicalAssessment(
                assessment_id=assessment_id,
                content_type=content.get("type", "unknown"),
                content_hash=content_hash,
                ethical_score=ethical_score,
                risk_factors=risk_factors,
                therapeutic_alignment=therapeutic_assessment["alignment_score"],
                safety_flags=safety_flags,
                recommendations=recommendations,
                assessed_at=datetime.now()
            )

            # Store assessment
            self.assessment_history.append(assessment)

            logger.info(f"Completed ethical assessment: {assessment_id} (score: {ethical_score:.2f})")

            return assessment

        except Exception as e:
            logger.error(f"Error assessing content ethics: {str(e)}")
            raise

    def filter_content(self, content: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Filter content based on safety and ethical guidelines.

        Args:
            content: Content to filter
            user_context: User therapeutic context

        Returns:
            Filtered content with modifications and warnings
        """
        try:
            filtered_content = content.copy()
            modifications = []
            warnings = []

            # Apply content filters
            for filter_rule in self.content_filters:
                matches = self._apply_content_filter(content, filter_rule, user_context)
                if matches:
                    modification = self._apply_filter_action(
                        filtered_content, filter_rule, matches, user_context
                    )
                    if modification:
                        modifications.append(modification)
                        if filter_rule.action == "allow_with_warning":
                            warnings.append(self._generate_content_warning(filter_rule))

            # Apply therapeutic guidelines
            therapeutic_modifications = self._apply_therapeutic_guidelines(
                filtered_content, user_context
            )
            modifications.extend(therapeutic_modifications)

            result = {
                "filtered_content": filtered_content,
                "modifications": modifications,
                "warnings": warnings,
                "requires_supervision": self._requires_supervision(filtered_content, user_context)
            }

            logger.info(f"Filtered content with {len(modifications)} modifications")

            return result

        except Exception as e:
            logger.error(f"Error filtering content: {str(e)}")
            raise

    def monitor_user_interactions(self, interaction_data: Dict[str, Any],
                                user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor user interactions for ethical concerns.

        Args:
            interaction_data: User interaction details
            user_profile: User profile and therapeutic context

        Returns:
            Monitoring results and interventions if needed
        """
        try:
            monitoring_results = {
                "risk_level": "low",
                "concerns": [],
                "interventions": [],
                "supervision_needed": False
            }

            # Assess interaction patterns
            pattern_analysis = self._analyze_interaction_patterns(interaction_data, user_profile)

            # Check for concerning behaviors
            concerning_behaviors = self._identify_concerning_behaviors(
                interaction_data, pattern_analysis, user_profile
            )

            if concerning_behaviors:
                monitoring_results["concerns"] = concerning_behaviors
                monitoring_results["risk_level"] = self._calculate_risk_level(concerning_behaviors)

                # Generate interventions
                interventions = self._generate_interventions(
                    concerning_behaviors, user_profile
                )
                monitoring_results["interventions"] = interventions

                # Determine supervision needs
                monitoring_results["supervision_needed"] = self._assess_supervision_needs(
                    concerning_behaviors, user_profile
                )

            logger.info(f"Monitored interaction - risk level: {monitoring_results['risk_level']}")

            return monitoring_results

        except Exception as e:
            logger.error(f"Error monitoring interactions: {str(e)}")
            raise

    def ensure_privacy_compliance(self, data_handling: Dict[str, Any]) -> PrivacyAssessment:
        """Ensure data handling complies with privacy regulations.

        Args:
            data_handling: Data handling practices to assess

        Returns:
            PrivacyAssessment: Privacy compliance results
        """
        try:
            assessment_id = f"privacy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Identify data types
            data_types = self._identify_data_types(data_handling)

            # Assess privacy risks
            privacy_risks = self._assess_privacy_risks(data_handling, data_types)

            # Calculate compliance score
            compliance_score = self._calculate_compliance_score(data_handling, privacy_risks)

            # Check regulatory alignment
            gdpr_alignment = self._check_gdpr_alignment(data_handling)
            hipaa_alignment = self._check_hipaa_alignment(data_handling)

            # Generate recommendations
            recommendations = self._generate_privacy_recommendations(
                privacy_risks, compliance_score
            )

            assessment = PrivacyAssessment(
                assessment_id=assessment_id,
                data_types=data_types,
                privacy_risks=privacy_risks,
                compliance_score=compliance_score,
                recommendations=recommendations,
                gdpr_alignment=gdpr_alignment,
                hipaa_alignment=hipaa_alignment
            )

            logger.info(f"Completed privacy assessment: {assessment_id} (compliance: {compliance_score:.2f})")

            return assessment

        except Exception as e:
            logger.error(f"Error assessing privacy compliance: {str(e)}")
            raise

    def generate_ethical_report(self, time_period: str = "week") -> Dict[str, Any]:
        """Generate a comprehensive ethical oversight report.

        Args:
            time_period: Time period for the report

        Returns:
            Ethical report data
        """
        try:
            # Filter assessments by time period
            recent_assessments = self._filter_assessments_by_time(time_period)

            report = {
                "period": time_period,
                "total_assessments": len(recent_assessments),
                "ethical_score_distribution": self._calculate_score_distribution(recent_assessments),
                "common_risk_factors": self._identify_common_risks(recent_assessments),
                "blocked_content_count": len(self.blocked_content),
                "supervision_recommendations": self._generate_supervision_recommendations(recent_assessments),
                "improvement_suggestions": self._suggest_improvements(recent_assessments),
                "generated_at": datetime.now()
            }

            logger.info(f"Generated ethical report for {time_period}")

            return report

        except Exception as e:
            logger.error(f"Error generating ethical report: {str(e)}")
            raise

    def _load_content_filters(self) -> List[ContentFilter]:
        """Load content filtering rules."""
        return [
            ContentFilter(
                filter_id="harmful_content_1",
                category="harmful_content",
                pattern=r"(?i)(self-harm|suicide|violent)",
                severity="critical",
                action="block"
            ),
            ContentFilter(
                filter_id="inappropriate_1",
                category="inappropriate_language",
                pattern=r"(?i)(explicit|offensive)",
                severity="high",
                action="flag"
            ),
            ContentFilter(
                filter_id="trigger_1",
                category="trigger_warnings",
                pattern=r"(?i)(trauma|abuse|loss)",
                severity="medium",
                action="allow_with_warning"
            )
        ]

    def _load_therapeutic_guidelines(self) -> Dict[str, TherapeuticGuideline]:
        """Load therapeutic guidelines."""
        return {
            "anxiety": TherapeuticGuideline(
                guideline_id="anxiety_1",
                condition="anxiety",
                content_restrictions=["sudden_shocks", "overwhelming_scenarios"],
                required_elements=["gradual_exposure", "coping_strategies"],
                intensity_limits={"emotional_intensity": 0.7, "sensory_stimulation": 0.6},
                supervision_requirements=["initial_sessions", "crisis_protocol"]
            ),
            "ptsd": TherapeuticGuideline(
                guideline_id="ptsd_1",
                condition="ptsd",
                content_restrictions=["trigger_reminders", "graphic_violence"],
                required_elements=["safe_word", "grounding_techniques"],
                intensity_limits={"trauma_similarity": 0.3, "emotional_intensity": 0.5},
                supervision_requirements=["mandatory_supervision", "emergency_contact"]
            )
        }

    def _generate_content_hash(self, content: Dict[str, Any]) -> str:
        """Generate a hash for content identification."""
        content_str = str(sorted(content.items()))
        return hashlib.sha256(content_str.encode()).hexdigest()[:16]

    def _assess_content_safety(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Assess content safety."""
        safety_score = 1.0
        issues = []

        # Check for harmful content
        text_content = self._extract_text_content(content)
        if text_content:
            harmful_patterns = [
                r"(?i)self-harm|suicide",
                r"(?i)violent|abuse",
                r"(?i)graphic|disturbing"
            ]

            for pattern in harmful_patterns:
                if re.search(pattern, text_content):
                    safety_score -= 0.3
                    issues.append({"type": "harmful_content", "pattern": pattern})

        return {
            "safety_score": max(0.0, safety_score),
            "issues": issues,
            "requires_supervision": safety_score < 0.7
        }

    def _assess_therapeutic_alignment(self, content: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess therapeutic alignment."""
        therapeutic_needs = context.get("therapeutic_needs", [])
        content_type = content.get("type", "story")

        alignment_score = 0.5  # Base score

        # Check alignment with therapeutic goals
        for need in therapeutic_needs:
            guideline = self.therapeutic_guidelines.get(need)
            if guideline:
                alignment_score += self._calculate_guideline_alignment(content, guideline)

        alignment_score = min(1.0, max(0.0, alignment_score))

        return {
            "alignment_score": alignment_score,
            "matched_guidelines": therapeutic_needs,
            "misalignments": []
        }

    def _assess_privacy_implications(self, content: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess privacy implications."""
        privacy_score = 1.0
        risks = []

        # Check for personal data exposure
        if self._contains_personal_data(content):
            privacy_score -= 0.4
            risks.append({"type": "personal_data_exposure", "severity": "high"})

        # Check data retention practices
        if not context.get("data_minimization"):
            privacy_score -= 0.2
            risks.append({"type": "excessive_data_retention", "severity": "medium"})

        return {
            "privacy_score": privacy_score,
            "risks": risks
        }

    def _calculate_ethical_score(self, safety: Dict, therapeutic: Dict, privacy: Dict) -> float:
        """Calculate overall ethical score."""
        weights = {
            "safety": 0.5,
            "therapeutic": 0.3,
            "privacy": 0.2
        }

        score = (
            safety["safety_score"] * weights["safety"] +
            therapeutic["alignment_score"] * weights["therapeutic"] +
            privacy["privacy_score"] * weights["privacy"]
        )

        return round(score, 2)

    def _identify_risk_factors(self, content: Dict, safety: Dict, therapeutic: Dict) -> List[Dict[str, Any]]:
        """Identify risk factors in content."""
        risks = []

        # Safety risks
        for issue in safety.get("issues", []):
            risks.append({
                "factor": issue["type"],
                "severity": "high" if safety["safety_score"] < 0.5 else "medium",
                "description": f"Content contains {issue['type']}"
            })

        # Therapeutic risks
        if therapeutic["alignment_score"] < 0.6:
            risks.append({
                "factor": "therapeutic_misalignment",
                "severity": "medium",
                "description": "Content may not align with therapeutic goals"
            })

        return risks

    def _generate_safety_flags(self, safety_assessment: Dict, risk_factors: List) -> List[str]:
        """Generate safety flags."""
        flags = []

        if safety_assessment["safety_score"] < 0.7:
            flags.append("content_safety_concern")

        if safety_assessment.get("requires_supervision"):
            flags.append("supervision_required")

        for risk in risk_factors:
            if risk["severity"] == "high":
                flags.append(f"high_risk_{risk['factor']}")

        return flags

    def _generate_ethical_recommendations(self, ethical_score: float, risk_factors: List,
                                        context: Dict) -> List[str]:
        """Generate ethical recommendations."""
        recommendations = []

        if ethical_score < 0.7:
            recommendations.append("Consider content modification to improve ethical score")

        if any(r["severity"] == "high" for r in risk_factors):
            recommendations.append("Immediate review by therapeutic supervisor required")

        if ethical_score > 0.9:
            recommendations.append("Content approved for therapeutic use")

        return recommendations

    def _apply_content_filter(self, content: Dict, filter_rule: ContentFilter,
                            user_context: Dict) -> List[str]:
        """Apply a content filter."""
        text_content = self._extract_text_content(content)
        if not text_content:
            return []

        matches = re.findall(filter_rule.pattern, text_content)
        return matches

    def _apply_filter_action(self, content: Dict, filter_rule: ContentFilter,
                           matches: List, user_context: Dict) -> Optional[Dict]:
        """Apply filter action to content."""
        if filter_rule.action == "block":
            self.blocked_content.add(self._generate_content_hash(content))
            return {"action": "blocked", "reason": filter_rule.category}
        elif filter_rule.action == "modify":
            return self._modify_content(content, filter_rule, matches)
        elif filter_rule.action == "flag":
            return {"action": "flagged", "category": filter_rule.category}

        return None

    def _apply_therapeutic_guidelines(self, content: Dict, user_context: Dict) -> List[Dict]:
        """Apply therapeutic guidelines to content."""
        modifications = []
        therapeutic_needs = user_context.get("therapeutic_needs", [])

        for need in therapeutic_needs:
            guideline = self.therapeutic_guidelines.get(need)
            if guideline:
                mod = self._apply_guideline_modifications(content, guideline)
                if mod:
                    modifications.extend(mod)

        return modifications

    def _requires_supervision(self, content: Dict, user_context: Dict) -> bool:
        """Determine if content requires supervision."""
        high_risk_conditions = ["ptsd", "severe_anxiety", "suicidal_ideation"]
        user_conditions = user_context.get("therapeutic_needs", [])

        return any(condition in high_risk_conditions for condition in user_conditions)

    def _analyze_interaction_patterns(self, interaction_data: Dict, user_profile: Dict) -> Dict:
        """Analyze user interaction patterns."""
        return {
            "frequency": "normal",
            "intensity": "moderate",
            "patterns": ["engaged", "progressive"]
        }

    def _identify_concerning_behaviors(self, interaction_data: Dict, pattern_analysis: Dict,
                                     user_profile: Dict) -> List[Dict]:
        """Identify concerning behaviors."""
        return []  # Placeholder - would analyze for concerning patterns

    def _calculate_risk_level(self, concerning_behaviors: List) -> str:
        """Calculate risk level."""
        if len(concerning_behaviors) > 2:
            return "high"
        elif len(concerning_behaviors) > 0:
            return "medium"
        else:
            return "low"

    def _generate_interventions(self, concerning_behaviors: List, user_profile: Dict) -> List[Dict]:
        """Generate interventions for concerning behaviors."""
        interventions = []

        for behavior in concerning_behaviors:
            interventions.append({
                "type": "therapeutic_intervention",
                "target_behavior": behavior.get("type"),
                "action": "provide_support_resources"
            })

        return interventions

    def _assess_supervision_needs(self, concerning_behaviors: List, user_profile: Dict) -> bool:
        """Assess if supervision is needed."""
        return len(concerning_behaviors) > 0

    def _identify_data_types(self, data_handling: Dict) -> List[str]:
        """Identify types of data being handled."""
        return ["personal_health_data", "interaction_logs", "therapeutic_content"]

    def _assess_privacy_risks(self, data_handling: Dict, privacy_risks: List) -> List[Dict]:
        """Assess privacy risks."""
        risks = []

        if "personal_health_data" in data_types:
            risks.append({
                "risk": "health_data_exposure",
                "severity": "high",
                "mitigation": "encryption_required"
            })

        return risks

    def _calculate_compliance_score(self, data_handling: Dict, privacy_risks: List) -> float:
        """Calculate compliance score."""
        base_score = 1.0

        for risk in privacy_risks:
            if risk["severity"] == "high":
                base_score -= 0.3
            elif risk["severity"] == "medium":
                base_score -= 0.1

        return max(0.0, base_score)

    def _check_gdpr_alignment(self, data_handling: Dict) -> bool:
        """Check GDPR alignment."""
        return data_handling.get("consent_obtained", False) and data_handling.get("data_minimization", False)

    def _check_hipaa_alignment(self, data_handling: Dict) -> bool:
        """Check HIPAA alignment."""
        return data_handling.get("health_data_protected", False)

    def _generate_privacy_recommendations(self, privacy_risks: List, compliance_score: float) -> List[str]:
        """Generate privacy recommendations."""
        recommendations = []

        if compliance_score < 0.8:
            recommendations.append("Implement stronger data protection measures")

        for risk in privacy_risks:
            recommendations.append(f"Address {risk['risk']} with {risk['mitigation']}")

        return recommendations

    def _filter_assessments_by_time(self, time_period: str) -> List[EthicalAssessment]:
        """Filter assessments by time period."""
        # Simplified - would implement proper time filtering
        return self.assessment_history[-10:]  # Last 10 assessments

    def _calculate_score_distribution(self, assessments: List[EthicalAssessment]) -> Dict:
        """Calculate ethical score distribution."""
        scores = [a.ethical_score for a in assessments]

        return {
            "average": sum(scores) / len(scores) if scores else 0,
            "min": min(scores) if scores else 0,
            "max": max(scores) if scores else 0,
            "distribution": {
                "excellent": len([s for s in scores if s >= 0.9]),
                "good": len([s for s in scores if 0.7 <= s < 0.9]),
                "needs_improvement": len([s for s in scores if s < 0.7])
            }
        }

    def _identify_common_risks(self, assessments: List[EthicalAssessment]) -> List[Dict]:
        """Identify common risk factors."""
        all_risks = []
        for assessment in assessments:
            all_risks.extend(assessment.risk_factors)

        # Count occurrences
        risk_counts = {}
        for risk in all_risks:
            key = risk.get("factor", "unknown")
            risk_counts[key] = risk_counts.get(key, 0) + 1

        return [{"factor": k, "count": v} for k, v in risk_counts.items()]

    def _generate_supervision_recommendations(self, assessments: List[EthicalAssessment]) -> List[str]:
        """Generate supervision recommendations."""
        recommendations = []

        low_score_count = len([a for a in assessments if a.ethical_score < 0.7])
        if low_score_count > len(assessments) * 0.3:
            recommendations.append("Increase supervision for content generation")

        return recommendations

    def _suggest_improvements(self, assessments: List[EthicalAssessment]) -> List[str]:
        """Suggest improvements based on assessment history."""
        return [
            "Implement more rigorous content filtering",
            "Enhance therapeutic alignment checks",
            "Improve privacy protection measures"
        ]

    def _extract_text_content(self, content: Dict) -> str:
        """Extract text content from content dict."""
        text_parts = []

        for key, value in content.items():
            if isinstance(value, str) and len(value) > 10:  # Reasonable text content
                text_parts.append(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        text_parts.append(item)

        return " ".join(text_parts)

    def _calculate_guideline_alignment(self, content: Dict, guideline: TherapeuticGuideline) -> float:
        """Calculate alignment with therapeutic guideline."""
        alignment = 0.0

        # Check required elements
        content_text = self._extract_text_content(content).lower()
        for element in guideline.required_elements:
            if element.lower() in content_text:
                alignment += 0.2

        # Check restrictions
        for restriction in guideline.content_restrictions:
            if restriction.lower() in content_text:
                alignment -= 0.3

        return max(0.0, min(0.5, alignment))

    def _contains_personal_data(self, content: Dict) -> bool:
        """Check if content contains personal data."""
        text_content = self._extract_text_content(content)
        personal_patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
            r"\b\d{10}\b"  # Phone
        ]

        for pattern in personal_patterns:
            if re.search(pattern, text_content):
                return True

        return False

    def _modify_content(self, content: Dict, filter_rule: ContentFilter, matches: List) -> Dict:
        """Modify content based on filter rule."""
        # Simplified modification - would implement proper content modification
        return {"action": "modified", "modifications": len(matches)}

    def _generate_content_warning(self, filter_rule: ContentFilter) -> str:
        """Generate content warning."""
        return f"Warning: Content contains {filter_rule.category}"

    def _apply_guideline_modifications(self, content: Dict, guideline: TherapeuticGuideline) -> List[Dict]:
        """Apply guideline modifications."""
        modifications = []

        # Check intensity limits
        for limit_type, limit_value in guideline.intensity_limits.items():
            current_intensity = self._assess_content_intensity(content, limit_type)
            if current_intensity > limit_value:
                modifications.append({
                    "type": "intensity_reduction",
                    "limit_type": limit_type,
                    "reduction_needed": current_intensity - limit_value
                })

        return modifications

    def _assess_content_intensity(self, content: Dict, intensity_type: str) -> float:
        """Assess content intensity for a specific type."""
        # Placeholder - would implement proper intensity assessment
        return 0.5