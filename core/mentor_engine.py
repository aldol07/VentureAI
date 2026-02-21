"""
Mentor Engine - Generates intelligent follow-up questions and provides feedback.
Features age-adaptive mentoring based on student class level.
"""

from typing import List, Dict
from utils.llm_client import get_llm_client


class MentorEngine:
    """Handles age-adaptive mentor Q&A sessions."""
    
    # Age-adaptive question styles
    AGE_PROFILES = {
        "junior": {  # Class 6-7
            "grades": [6, 7],
            "question_style": "simple, friendly, using everyday examples",
            "validation_focus": "asking friends and family, simple observations",
            "monetization_focus": "pocket money, small contributions, help from adults",
            "differentiation_focus": "what makes it special compared to what exists",
            "feedback_style": "very encouraging, use emojis, celebrate small wins",
            "examples": "school projects, helping classmates, family activities"
        },
        "middle": {  # Class 8-9
            "grades": [8, 9],
            "question_style": "clear and practical, introducing basic business thinking",
            "validation_focus": "surveys, talking to potential users, online research",
            "monetization_focus": "who benefits and might pay, basic pricing ideas",
            "differentiation_focus": "unique features, better solutions than competitors",
            "feedback_style": "encouraging with constructive suggestions",
            "examples": "apps they use, local businesses, online services"
        },
        "senior": {  # Class 10-12
            "grades": [10, 11, 12],
            "question_style": "professional, startup-focused, challenging assumptions",
            "validation_focus": "market validation experiments, landing page tests, pre-sales, customer interviews",
            "monetization_focus": "unit economics, willingness to pay, pricing strategies, revenue projections",
            "differentiation_focus": "competitive moats, unique value proposition, defensibility",
            "feedback_style": "professional mentorship with actionable insights",
            "examples": "successful startups, market dynamics, growth strategies"
        }
    }
    
    def __init__(self):
        self.llm = get_llm_client()
        self.conversation_history: List[Dict] = []
    
    def _get_age_profile(self, student_class: int) -> dict:
        """Get the appropriate age profile."""
        for profile_name, profile in self.AGE_PROFILES.items():
            if student_class in profile["grades"]:
                return profile
        return self.AGE_PROFILES["middle"]
    
    def generate_questions(self, refined_idea: dict, student_class: int) -> list:
        """
        Generate age-adaptive mentor questions.
        
        Returns:
            List of question dicts with 'question' and 'context' keys
        """
        profile = self._get_age_profile(student_class)
        
        system_prompt = f"""You are a friendly startup mentor with AGE-ADAPTIVE INTELLIGENCE.

You are mentoring a CLASS {student_class} student. Adapt your questions to their level.

═══════════════════════════════════════════════════════════
AGE-ADAPTIVE SETTINGS FOR CLASS {student_class}
═══════════════════════════════════════════════════════════

QUESTION STYLE: {profile['question_style']}

FOR DEMAND VALIDATION, FOCUS ON: {profile['validation_focus']}

FOR MONETIZATION, FOCUS ON: {profile['monetization_focus']}

FOR DIFFERENTIATION, FOCUS ON: {profile['differentiation_focus']}

USE EXAMPLES LIKE: {profile['examples']}

═══════════════════════════════════════════════════════════
YOUR TASK
═══════════════════════════════════════════════════════════

Personalize these THREE mentor questions for the student's specific idea:

1. DEMAND VALIDATION: How will they check if people actually want this?
2. MONETIZATION: Who will pay and why?
3. DIFFERENTIATION: What makes this different/special?

Make questions:
- Specific to their idea (mention their product/users)
- Age-appropriate in language and expectations
- Thought-provoking but not intimidating
- Include helpful context/hints

OUTPUT FORMAT (JSON):
{{
    "questions": [
        {{
            "question": "Age-appropriate personalized question about validation",
            "context": "Helpful hint with age-appropriate example"
        }},
        {{
            "question": "Age-appropriate personalized question about monetization",
            "context": "Helpful hint with age-appropriate example"
        }},
        {{
            "question": "Age-appropriate personalized question about differentiation",
            "context": "Helpful hint with age-appropriate example"
        }}
    ]
}}"""
        
        user_prompt = f"""Create mentor questions for this Class {student_class} student's idea:

IDEA DETAILS:
- Problem: {refined_idea.get('problem_statement', 'N/A')}
- Target User: {refined_idea.get('target_user', 'N/A')}
- Features: {', '.join(refined_idea.get('core_features', []))}
- Revenue: {refined_idea.get('revenue_model', 'N/A')}

Remember: Use {profile['question_style']} style.
Focus validation on: {profile['validation_focus']}
Focus monetization on: {profile['monetization_focus']}

Return valid JSON only."""
        
        result = self.llm.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7
        )
        
        return result.get("questions", [])
    
    def get_feedback(
        self,
        question: str,
        answer: str,
        refined_idea: dict,
        student_class: int
    ) -> str:
        """
        Generate age-adaptive mentor feedback.
        
        Returns:
            Encouraging, age-appropriate feedback string
        """
        profile = self._get_age_profile(student_class)
        
        # Add to conversation history
        self.conversation_history.append({
            "question": question,
            "answer": answer
        })
        
        # Build context from previous Q&A
        history_context = ""
        if len(self.conversation_history) > 1:
            history_context = "\nPREVIOUS Q&A:\n"
            for i, qa in enumerate(self.conversation_history[:-1], 1):
                history_context += f"Q{i}: {qa['question']}\nA{i}: {qa['answer']}\n"
        
        system_prompt = f"""You are a supportive startup mentor with AGE-ADAPTIVE INTELLIGENCE.

You are mentoring a CLASS {student_class} student. Adapt your feedback to their level.

═══════════════════════════════════════════════════════════
AGE-ADAPTIVE FEEDBACK SETTINGS
═══════════════════════════════════════════════════════════

FEEDBACK STYLE: {profile['feedback_style']}

USE EXAMPLES LIKE: {profile['examples']}

{"Use emojis and very encouraging language! 🌟" if student_class <= 7 else ""}
{"Be encouraging but also introduce business thinking." if 8 <= student_class <= 9 else ""}
{"Provide professional mentorship with actionable startup insights." if student_class >= 10 else ""}

═══════════════════════════════════════════════════════════
FEEDBACK RULES
═══════════════════════════════════════════════════════════

1. Be encouraging FIRST, then constructive
2. Keep it to 2-3 sentences
3. If answer is weak, gently guide them
4. If answer is strong, acknowledge and add ONE insight
5. Reference their previous answers if relevant
6. Match language complexity to Class {student_class}

{"For Class 6-7: Use simple words, be very positive, suggest small next steps" if student_class <= 7 else ""}
{"For Class 8-9: Balance encouragement with practical suggestions" if 8 <= student_class <= 9 else ""}
{"For Class 10-12: Provide startup-level insights, mention frameworks like lean startup, MVP testing" if student_class >= 10 else ""}"""
        
        user_prompt = f"""Give feedback on this Class {student_class} student's answer:

THEIR STARTUP:
- Problem: {refined_idea.get('problem_statement', 'N/A')}
- Target User: {refined_idea.get('target_user', 'N/A')}
{history_context}
CURRENT QUESTION: {question}

STUDENT'S ANSWER: {answer}

Provide {profile['feedback_style']} feedback (2-3 sentences)."""
        
        feedback = self.llm.generate_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7,
            max_tokens=200
        )
        
        return feedback.strip()
    
    def reset_conversation(self):
        """Reset conversation history for a new session."""
        self.conversation_history = []
