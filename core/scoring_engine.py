"""
Scoring Engine - Calculates startup readiness scores.
Features age-adaptive scoring criteria based on student class level.
"""

from utils.llm_client import get_llm_client


class ScoringEngine:
    """Calculates age-adaptive startup readiness scores."""
    
    # Age-adaptive scoring criteria
    AGE_PROFILES = {
        "junior": {  # Class 6-7
            "grades": [6, 7],
            "clarity_criteria": """
   - Can a 10-12 year old explain this to a friend?
   - Is the problem relatable to school/home life?
   - Are features simple enough to draw on paper?""",
            "feasibility_criteria": """
   - Can they build this with help from parents/teachers?
   - Does it need only free tools and basic skills?
   - Can they test it with classmates and family?""",
            "innovation_criteria": """
   - Is it a fresh idea for their age group?
   - Does it solve a real problem they face?
   - Would their friends find it interesting?""",
            "expectations": "Expect simpler ideas. Focus on creativity and learning, not business viability."
        },
        "middle": {  # Class 8-9
            "grades": [8, 9],
            "clarity_criteria": """
   - Is the problem clearly defined with specific users?
   - Are features practical and understandable?
   - Is there a logical connection between problem and solution?""",
            "feasibility_criteria": """
   - Can they build a basic version with online tutorials?
   - Are required resources accessible to a teenager?
   - Can they validate with surveys and simple prototypes?""",
            "innovation_criteria": """
   - Does it offer something different from existing solutions?
   - Is there a unique angle or approach?
   - Does it show creative problem-solving?""",
            "expectations": "Expect moderate complexity. Balance creativity with basic business thinking."
        },
        "senior": {  # Class 10-12
            "grades": [10, 11, 12],
            "clarity_criteria": """
   - Is there a clear value proposition?
   - Is the target market well-defined with size estimation?
   - Are features prioritized with clear MVP scope?""",
            "feasibility_criteria": """
   - Can they build an MVP with available tech skills?
   - Is the go-to-market strategy realistic?
   - Can they run proper validation experiments?""",
            "innovation_criteria": """
   - Is there a defensible competitive advantage?
   - Does it address a gap in the market?
   - Is the approach scalable and differentiated?""",
            "expectations": "Expect startup-level thinking. Evaluate like an early-stage investor would."
        }
    }
    
    def __init__(self):
        self.llm = get_llm_client()
    
    def _get_age_profile(self, student_class: int) -> dict:
        """Get the appropriate age profile."""
        for profile_name, profile in self.AGE_PROFILES.items():
            if student_class in profile["grades"]:
                return profile
        return self.AGE_PROFILES["middle"]
    
    def _build_scoring_prompt(self, student_class: int) -> str:
        """Build age-adaptive scoring prompt."""
        profile = self._get_age_profile(student_class)
        
        return f"""You are an expert startup evaluator with AGE-ADAPTIVE INTELLIGENCE.

You are evaluating an idea from a CLASS {student_class} student.

═══════════════════════════════════════════════════════════
CRITICAL: ADJUST EXPECTATIONS FOR CLASS {student_class}
═══════════════════════════════════════════════════════════

{profile['expectations']}

═══════════════════════════════════════════════════════════
AGE-ADAPTIVE SCORING CRITERIA
═══════════════════════════════════════════════════════════

1. CLARITY (1-10) - For Class {student_class}:
{profile['clarity_criteria']}
   
   Score Guide:
   - 1-3: Vague, hard to understand
   - 4-6: Somewhat clear but needs work
   - 7-9: Clear and well-articulated for their age
   - 10: Exceptionally clear and compelling

2. FEASIBILITY (1-10) - For Class {student_class}:
{profile['feasibility_criteria']}
   
   Score Guide:
   - 1-3: Not feasible for a Class {student_class} student
   - 4-6: Challenging but possible with guidance
   - 7-9: Achievable with reasonable effort
   - 10: Highly achievable for their level

3. INNOVATION (1-10) - For Class {student_class}:
{profile['innovation_criteria']}
   
   Score Guide:
   - 1-3: Very common/overdone idea
   - 4-6: Some unique elements
   - 7-9: Creative and differentiated
   - 10: Highly innovative for their age group

═══════════════════════════════════════════════════════════
IMPORTANT REMINDERS
═══════════════════════════════════════════════════════════

- A Class 6 student with a simple but clear idea should score HIGH on clarity
- A Class 12 student with the same simple idea should score LOWER (expect more depth)
- Be encouraging but honest
- Provide brief, age-appropriate explanations

OUTPUT FORMAT (JSON only):
{{
    "clarity": <score 1-10>,
    "clarity_reason": "Brief age-appropriate explanation",
    "feasibility": <score 1-10>,
    "feasibility_reason": "Brief age-appropriate explanation",
    "innovation": <score 1-10>,
    "innovation_reason": "Brief age-appropriate explanation"
}}"""
    
    def calculate_scores(
        self,
        refined_idea: dict,
        original_idea: str,
        student_class: int
    ) -> dict:
        """
        Calculate age-adaptive readiness scores.
        
        Returns:
            dict with clarity, feasibility, innovation, overall scores and reasons
        """
        system_prompt = self._build_scoring_prompt(student_class)
        profile = self._get_age_profile(student_class)
        
        user_prompt = f"""Score this startup idea from a Class {student_class} student:

ORIGINAL IDEA: {original_idea}

REFINED PLAN:
- Problem: {refined_idea.get('problem_statement', 'N/A')}
- Target User: {refined_idea.get('target_user', 'N/A')}
- Features: {', '.join(refined_idea.get('core_features', []))}
- Revenue: {refined_idea.get('revenue_model', 'N/A')}
- Action Plan: {', '.join(refined_idea.get('five_day_action_plan', [])[:2])}...

REMEMBER: {profile['expectations']}

Provide scores and brief explanations in JSON format."""
        
        result = self.llm.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.5
        )
        
        # Extract scores
        clarity = result.get("clarity", 5)
        feasibility = result.get("feasibility", 5)
        innovation = result.get("innovation", 5)
        
        # Weighted average (feasibility weighted higher for students)
        overall = round((clarity * 0.3 + feasibility * 0.4 + innovation * 0.3), 1)
        
        return {
            "clarity": clarity,
            "clarity_reason": result.get("clarity_reason", ""),
            "feasibility": feasibility,
            "feasibility_reason": result.get("feasibility_reason", ""),
            "innovation": innovation,
            "innovation_reason": result.get("innovation_reason", ""),
            "overall": overall
        }
