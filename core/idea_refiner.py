from utils.llm_client import get_llm_client
from core.scoring_engine import ScoringEngine


class IdeaRefiner:
    """Refines raw startup ideas with age-adaptive output and reality checks."""
    
    
    AGE_PROFILES = {
        "junior": {  # Class 6-7
            "grades": [6, 7],
            "language": "simple, friendly, encouraging",
            "concepts": "basic business ideas, helping others, solving everyday problems",
            "features": "simple, easy-to-explain features that friends and family can understand",
            "revenue": "simple models like donations, small fees, or asking parents/teachers for support",
            "action_plan": """
- Day 1: Draw your idea on paper and show 5 friends
- Day 2: Ask 10 people if they would use it
- Day 3: Make a simple poster or presentation
- Day 4: Present to your class or family
- Day 5: Write down what you learned and how to make it better""",
            "experiments": "Talk to friends, make drawings, do simple surveys in class",
            "complexity": "Keep everything very simple. Use examples from school and home life.",
            "timeline_style": "fun activities, small steps, family involvement"
        },
        "middle": {  # Class 8-9
            "grades": [8, 9],
            "language": "clear, motivating, slightly technical",
            "concepts": "basic market understanding, user needs, simple competition analysis",
            "features": "practical features with clear benefits, can include basic technology",
            "revenue": "subscriptions, freemium models, small transaction fees, partnerships with local businesses",
            "action_plan": """
- Day 1: Research similar apps/services online, list 3 competitors
- Day 2: Create a survey and collect 20+ responses
- Day 3: Design basic wireframes or mockups
- Day 4: Build a simple prototype or landing page
- Day 5: Test with 10 users and collect feedback""",
            "experiments": "Online surveys, competitor research, basic prototyping, user interviews",
            "complexity": "Moderate complexity. Can include basic technical concepts and market research.",
            "timeline_style": "structured research, prototyping, user testing"
        },
        "senior": {  # Class 10-12
            "grades": [10, 11, 12],
            "language": "professional, startup-focused, industry-standard terminology",
            "concepts": "market validation, unit economics, competitive moats, growth strategies",
            "features": "comprehensive features with technical depth, scalability considerations",
            "revenue": "sophisticated models: freemium with premium tiers, marketplace commissions, B2B licensing, subscription tiers, transaction fees with clear unit economics",
            "action_plan": """
- Day 1: Conduct market research, analyze 5 competitors, identify unique value proposition
- Day 2: Build landing page, set up analytics, create waitlist signup
- Day 3: Run validation experiments - ads, social posts, direct outreach to 50+ potential users
- Day 4: Develop MVP with core feature, implement basic metrics tracking
- Day 5: Launch beta to early adopters, collect NPS scores, iterate based on feedback""",
            "experiments": "A/B testing, landing page conversion tracking, customer interviews, smoke tests, pre-sales validation, cohort analysis",
            "complexity": "Advanced startup concepts. Include validation frameworks, growth metrics, and scalable architecture thinking.",
            "timeline_style": "startup methodology, metrics-driven, investor-ready milestones"
        }
    }
    
    def __init__(self):
        self.llm = get_llm_client()
        self.scorer = ScoringEngine()
    
    def _get_age_profile(self, student_class: int) -> dict:
        """Get the appropriate age profile based on student class."""
        for profile_name, profile in self.AGE_PROFILES.items():
            if student_class in profile["grades"]:
                return profile
        return self.AGE_PROFILES["middle"]
    
    def _check_reality(self, idea: str, student_class: int) -> dict:
        """
        REALITY SIMPLIFIER GUARDRAIL
        Checks if idea is realistic and suggests simplification if needed.
        """
        system_prompt = """You are a Reality Check AI that evaluates startup ideas from students.

Your job is to determine if an idea is REALISTIC for a student to build.

UNREALISTIC IDEAS include:
- Ideas requiring millions in funding ("Uber for helicopters")
- Ideas requiring advanced technology beyond student capability ("AI that replaces all teachers")
- Ideas requiring regulatory approval ("New cryptocurrency exchange")
- Ideas requiring massive infrastructure ("Global delivery network")
- Ideas that are too vague ("App that solves everything")

REALISTIC IDEAS include:
- Simple apps or websites a student can build
- Local services they can test with friends/family
- Tools that solve specific, small problems
- Projects achievable in days/weeks, not years

OUTPUT FORMAT (JSON):
{
    "is_realistic": true/false,
    "original_scope": "What they proposed",
    "concerns": ["List of concerns if unrealistic"],
    "simplified_idea": "A realistic, scoped-down version if unrealistic, or null if already realistic",
    "simplification_reason": "Why we simplified, or null if not needed"
}"""
        
        user_prompt = f"""Evaluate this startup idea from a Class {student_class} student:

IDEA: {idea}

Is this realistic for a Class {student_class} student to build?
If not, suggest a simplified, achievable version.

Return valid JSON only."""
        
        try:
            return self.llm.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.5
            )
        except Exception:
            return {"is_realistic": True, "simplified_idea": None}
    
    def _generate_pivot_suggestions(self, refined_idea: dict, student_class: int) -> list:
        """
        PIVOT SUGGESTION ENGINE
        Generates backup directions if the main idea fails.
        """
        profile = self._get_age_profile(student_class)
        
        system_prompt = f"""You are a Startup Pivot Advisor helping a Class {student_class} student.

If their main idea doesn't work out, suggest 2-3 PIVOT DIRECTIONS they could take.

PIVOT RULES:
- Each pivot should use similar skills/resources
- Pivots should be EASIER or target a different market
- Use {profile['language']} language
- Make pivots achievable for a Class {student_class} student

OUTPUT FORMAT (JSON):
{{
    "pivots": [
        {{
            "direction": "Brief pivot name",
            "description": "What to do instead",
            "why_it_might_work": "Why this pivot makes sense"
        }}
    ]
}}"""
        
        user_prompt = f"""The student's main idea is:
- Problem: {refined_idea.get('problem_statement', 'N/A')}
- Target: {refined_idea.get('target_user', 'N/A')}
- Features: {', '.join(refined_idea.get('core_features', []))}

Suggest 2-3 pivot directions if this idea fails. Return valid JSON only."""
        
        try:
            result = self.llm.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.7
            )
            return result.get("pivots", [])
        except Exception:
            return []
    
    def _generate_timeline(self, refined_idea: dict, student_class: int) -> list:
        """
        TIMELINE VISUALIZER
        Generates a detailed day-by-day journey from idea to demo.
        """
        profile = self._get_age_profile(student_class)
        
        system_prompt = f"""You are a Startup Timeline Planner for a Class {student_class} student.

Create a detailed 5-DAY TIMELINE from idea to working demo.

TIMELINE STYLE: {profile['timeline_style']}

Each day should have:
- A clear focus/theme
- 2-3 specific tasks
- Expected outcome
- {"Fun activities suitable for young students" if student_class <= 7 else "Practical milestones" if student_class <= 9 else "Startup methodology milestones"}

OUTPUT FORMAT (JSON):
{{
    "timeline": [
        {{
            "day": 1,
            "theme": "Problem Validation",
            "tasks": ["Task 1", "Task 2", "Task 3"],
            "outcome": "What you'll have by end of day",
            "tip": "Helpful tip for this day"
        }}
    ]
}}"""
        
        user_prompt = f"""Create a 5-day timeline for this Class {student_class} student's startup:

- Problem: {refined_idea.get('problem_statement', 'N/A')}
- Target: {refined_idea.get('target_user', 'N/A')}
- Features: {', '.join(refined_idea.get('core_features', []))}

Make it {profile['timeline_style']}. Return valid JSON only."""
        
        try:
            result = self.llm.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.6
            )
            return result.get("timeline", [])
        except Exception:
            return []
    
    def _build_system_prompt(self, student_class: int, idea_type: str) -> str:
        """Build age-adaptive system prompt for idea refinement."""
        profile = self._get_age_profile(student_class)
        
        return f"""You are VenturePilot, an AI startup mentor with AGE-ADAPTIVE INTELLIGENCE.

You are helping a CLASS {student_class} student. Adapt ALL outputs to their cognitive maturity level.

═══════════════════════════════════════════════════════════
AGE-ADAPTIVE SETTINGS FOR CLASS {student_class}
═══════════════════════════════════════════════════════════

LANGUAGE STYLE: {profile['language']}
CONCEPT DEPTH: {profile['concepts']}
FEATURE COMPLEXITY: {profile['features']}
REVENUE MODELS TO SUGGEST: {profile['revenue']}
VALIDATION EXPERIMENTS: {profile['experiments']}
OVERALL COMPLEXITY: {profile['complexity']}

═══════════════════════════════════════════════════════════
IDEA TYPE: {idea_type}
═══════════════════════════════════════════════════════════

Tailor features and action plan specifically for {idea_type} projects.

═══════════════════════════════════════════════════════════
OUTPUT FORMAT (JSON)
═══════════════════════════════════════════════════════════

{{
    "problem_statement": "Clear problem statement in age-appropriate language",
    "target_user": "Specific target user description",
    "core_features": ["Feature 1", "Feature 2", "Feature 3"],
    "revenue_model": "Age-appropriate revenue model",
    "five_day_action_plan": ["Day 1 task", "Day 2 task", "Day 3 task", "Day 4 task", "Day 5 task"],
    "realism_note": "Note if idea was simplified, or null if realistic"
}}

CRITICAL: Adapt EVERYTHING to Class {student_class} level."""
    
    def refine(self, idea: str, student_class: int, idea_type: str) -> dict:
        """
        Refine a raw idea with:
        - Reality check and simplification
        - Age-adaptive structuring
        - Pivot suggestions
        - Timeline visualization
        - Readiness scoring
        
        Returns:
            dict with refined_idea, scores, reality_check, pivots, timeline
        """
        # Step 1: Reality Check
        reality_check = self._check_reality(idea, student_class)
        
        # Use simplified idea if original was unrealistic
        working_idea = idea
        if not reality_check.get("is_realistic", True) and reality_check.get("simplified_idea"):
            working_idea = reality_check["simplified_idea"]
        
        # Step 2: Refine the idea
        system_prompt = self._build_system_prompt(student_class, idea_type)
        profile = self._get_age_profile(student_class)
        
        user_prompt = f"""Please refine this startup idea for a Class {student_class} student:

IDEA: {working_idea}

REMEMBER:
1. Use {profile['language']} language
2. Suggest {profile['features']}
3. Action plan should include: {profile['experiments']}
4. Revenue model should be: {profile['revenue']}
5. Keep complexity level: {profile['complexity']}

Output valid JSON only."""
        
        refined_idea = self.llm.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7
        )
        
        # Add realism note if we simplified
        if not reality_check.get("is_realistic", True):
            refined_idea["realism_note"] = reality_check.get("simplification_reason", 
                "We simplified this idea to make it achievable for a student project.")
        
        # Step 3: Generate pivot suggestions
        pivots = self._generate_pivot_suggestions(refined_idea, student_class)
        
        # Step 4: Generate timeline
        timeline = self._generate_timeline(refined_idea, student_class)
        
        # Step 5: Calculate scores
        scores = self.scorer.calculate_scores(
            refined_idea=refined_idea,
            original_idea=idea,
            student_class=student_class
        )
        
        return {
            "refined_idea": refined_idea,
            "scores": scores,
            "reality_check": reality_check,
            "pivots": pivots,
            "timeline": timeline
        }
