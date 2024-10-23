from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class LeadData:
    """Data structure for lead information"""
    company_size: int
    industry: str
    has_email: bool = True
    has_phone: bool = True
    revenue: Optional[float] = None
    website: Optional[str] = None
    location: Optional[str] = None

class LeadScorer:
    """Modular lead scoring system"""
    
    # Industry weights (0-100) based on target market relevance
    INDUSTRY_WEIGHTS = {
        'technology': 100,
        'healthcare': 90,
        'finance': 85,
        'manufacturing': 80,
        'retail': 75,
        'education': 70,
        'other': 50
    }

    # Company size scoring brackets
    SIZE_BRACKETS = [
        (1000, 100),    # 1000+ employees: 100 points
        (500, 90),      # 500-999 employees: 90 points
        (200, 80),      # 200-499 employees: 80 points
        (100, 70),      # 100-199 employees: 70 points
        (50, 60),       # 50-99 employees: 60 points
        (20, 50),       # 20-49 employees: 50 points
        (0, 30)         # 0-19 employees: 30 points
    ]

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """Initialize with custom weights if provided"""
        self.weights = weights or {
            'size': 0.35,
            'industry': 0.35,
            'contact': 0.30
        }
        self._normalize_weights()

    def _normalize_weights(self) -> None:
        """Normalize weights to sum to 1.0"""
        total = sum(self.weights.values())
        self.weights = {k: v/total for k, v in self.weights.items()}

    def calculate_size_score(self, employee_count: int) -> int:
        """Calculate score based on company size"""
        for min_size, score in self.SIZE_BRACKETS:
            if employee_count >= min_size:
                return score
        return 0

    def calculate_industry_score(self, industry: str) -> int:
        """Calculate score based on industry relevance"""
        industry = industry.lower()
        return self.INDUSTRY_WEIGHTS.get(industry, self.INDUSTRY_WEIGHTS['other'])

    def calculate_contact_score(self, has_email: bool, has_phone: bool) -> int:
        """Calculate score based on contact information completeness"""
        score = 100
        if not has_email:
            score -= 50  # Email is crucial
        if not has_phone:
            score -= 30  # Phone is important but less critical
        return max(0, score)  # Ensure score doesn't go below 0

    def get_grade(self, score: int) -> str:
        """Convert numerical score to letter grade"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        return 'F'

    def score_lead(self, lead: LeadData) -> Dict[str, any]:
        """
        Calculate comprehensive lead score based on all available factors.
        Returns detailed scoring breakdown and final grade.
        """
        # Calculate component scores
        size_score = self.calculate_size_score(lead.company_size)
        industry_score = self.calculate_industry_score(lead.industry)
        contact_score = self.calculate_contact_score(lead.has_email, lead.has_phone)

        # Calculate weighted total score
        total_score = round(
            size_score * self.weights['size'] +
            industry_score * self.weights['industry'] +
            contact_score * self.weights['contact']
        )

        return {
            'total_score': total_score,
            'grade': self.get_grade(total_score),
            'components': {
                'size_score': size_score,
                'industry_score': industry_score,
                'contact_score': contact_score
            },
            'weights': self.weights
        }

# For backward compatibility
def calculate_lead_score(
    company_size: int,
    industry: str,
    has_valid_email: bool = True,
    has_phone: bool = True,
    custom_factors: Dict[str, float] = None
) -> Dict[str, any]:
    """Legacy function for backward compatibility"""
    scorer = LeadScorer(weights=custom_factors)
    lead = LeadData(
        company_size=company_size,
        industry=industry,
        has_email=has_valid_email,
        has_phone=has_phone
    )
    return scorer.score_lead(lead)