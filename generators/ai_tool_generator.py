"""
AI Tool Generator - Generates prompt logic and Streamlit demo.
Features age-adaptive complexity in generated code and prompts.
"""

from utils.llm_client import get_llm_client


class AIToolGenerator:
    """Generates age-adaptive AI tool prototypes."""
    
    AGE_PROFILES = {
        "junior": {  # Class 6-7
            "grades": [6, 7],
            "prompt_complexity": "very simple prompts, friendly AI personality, safe outputs",
            "code_complexity": "minimal code, lots of comments explaining each line",
            "ui_style": "colorful, fun, big buttons, emojis everywhere",
            "features": "single input, simple output, very basic"
        },
        "middle": {  # Class 8-9
            "grades": [8, 9],
            "prompt_complexity": "clear prompts, helpful AI, structured outputs",
            "code_complexity": "clean code, good comments, organized structure",
            "ui_style": "modern, clean, user-friendly",
            "features": "2-3 inputs, formatted output, download option"
        },
        "senior": {  # Class 10-12
            "grades": [10, 11, 12],
            "prompt_complexity": "sophisticated prompts, professional AI behavior, detailed outputs",
            "code_complexity": "production-quality code, error handling, best practices",
            "ui_style": "professional startup UI, polished design",
            "features": "multiple inputs, rich output formatting, export options, error handling"
        }
    }
    
    def __init__(self):
        self.llm = get_llm_client()
    
    def _get_age_profile(self, student_class: int) -> dict:
        for profile_name, profile in self.AGE_PROFILES.items():
            if student_class in profile["grades"]:
                return profile
        return self.AGE_PROFILES["middle"]
    
    def generate(self, refined_idea: dict, student_class: int, context: str) -> dict:
        """Generate age-adaptive AI tool prototype."""
        profile = self._get_age_profile(student_class)
        
        prompts = self._generate_prompts(refined_idea, context, student_class, profile)
        demo_script = self._generate_demo_script(refined_idea, prompts, student_class, profile)
        
        return {
            "system_prompt": prompts.get("system_prompt", "You are a helpful AI assistant."),
            "user_prompt_template": prompts.get("user_prompt_template", "{user_input}"),
            "streamlit_demo": demo_script
        }
    
    def _generate_prompts(self, refined_idea: dict, context: str, student_class: int, profile: dict) -> dict:
        """Generate age-adaptive AI prompts."""
        system_prompt = f"""You are an AI prompt engineer creating prompts for a CLASS {student_class} student's AI tool.

═══════════════════════════════════════════════════════════
AGE-ADAPTIVE PROMPT GENERATION
═══════════════════════════════════════════════════════════

PROMPT COMPLEXITY: {profile['prompt_complexity']}

{"FOR CLASS 6-7: Create VERY simple prompts. The AI should be friendly, use simple words, and be encouraging. Like a helpful friend!" if student_class <= 7 else ""}
{"FOR CLASS 8-9: Create clear, practical prompts. The AI should be helpful and give structured responses." if 8 <= student_class <= 9 else ""}
{"FOR CLASS 10-12: Create sophisticated prompts. The AI should behave professionally and give detailed, actionable responses." if student_class >= 10 else ""}

═══════════════════════════════════════════════════════════
REQUIREMENTS
═══════════════════════════════════════════════════════════

Create:
1. System prompt - defines AI personality (age-appropriate)
2. User prompt template - with {{placeholder}} variables
3. Input field names - {"just 1 simple field" if student_class <= 7 else "2-3 clear fields" if student_class <= 9 else "appropriate fields for the tool"}

OUTPUT FORMAT (JSON):
{{
    "system_prompt": "Age-appropriate system prompt",
    "user_prompt_template": "Template with {{placeholders}}",
    "input_fields": ["field1", "field2"]
}}"""
        
        features_text = "\n".join(f"- {f}" for f in refined_idea.get("core_features", []))
        
        user_prompt = f"""Create AI prompts for this Class {student_class} student's tool:

TOOL PURPOSE: {refined_idea.get('problem_statement', 'N/A')}
TARGET USER: {refined_idea.get('target_user', 'N/A')}
FEATURES:
{features_text}

Generate {profile['prompt_complexity']} prompts. Return valid JSON only."""
        
        try:
            return self.llm.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.5
            )
        except Exception:
            return {
                "system_prompt": f"You are a helpful AI assistant that helps with: {refined_idea.get('problem_statement', 'various tasks')}.",
                "user_prompt_template": "Please help me with: {user_input}",
                "input_fields": ["user_input"]
            }
    
    def _generate_demo_script(self, refined_idea: dict, prompts: dict, student_class: int, profile: dict) -> str:
        """Generate age-adaptive Streamlit demo script."""
        
        system_prompt = prompts.get("system_prompt", "You are a helpful AI assistant.")
        user_template = prompts.get("user_prompt_template", "{user_input}")
        input_fields = prompts.get("input_fields", ["user_input"])
        
        # Escape for string embedding
        system_prompt_safe = system_prompt.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
        user_template_safe = user_template.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
        
        # Build input fields
        input_code_lines = []
        invoke_args = []
        validation_checks = []
        
        for field in input_fields:
            clean_field = field.replace(" ", "_").replace("-", "_").lower()
            label = field.replace("_", " ").replace("-", " ").title()
            input_code_lines.append(f'    {clean_field} = st.text_area("{label}", height=100, placeholder="Enter {label.lower()}...")')
            invoke_args.append(f'"{field}": {clean_field}')
            validation_checks.append(clean_field)
        
        input_code = "\n".join(input_code_lines)
        invoke_dict = ", ".join(invoke_args)
        validation = " and ".join(validation_checks)
        
        problem_desc = refined_idea.get('problem_statement', 'AI-powered assistant').replace('"', '\\"').replace("'", "\\'")
        
        # Age-adaptive UI elements
        if student_class <= 7:
            title_emoji = "🌟"
            button_text = "✨ Make Magic!"
            success_text = "🎉 Here's your answer!"
            footer_text = "Made with love 💖"
            extra_styling = """
    .stButton button {
        font-size: 20px !important;
        padding: 15px 30px !important;
    }"""
        elif student_class <= 9:
            title_emoji = "🤖"
            button_text = "🚀 Generate"
            success_text = "### ✨ Result"
            footer_text = "Built with VenturePilot"
            extra_styling = ""
        else:
            title_emoji = "🤖"
            button_text = "Generate Response"
            success_text = "### Generated Response"
            footer_text = "Built with VenturePilot | Powered by AI"
            extra_styling = ""
        
        # Generate script
        demo_script = f'''#!/usr/bin/env python3
"""
AI Tool Demo - Generated by VenturePilot
For Class {student_class} Student
{refined_idea.get('problem_statement', 'AI-powered tool')}

{"=" * 50}
HOW TO RUN THIS:
{"=" * 50}
1. Install packages: pip install streamlit langchain-openai python-dotenv
2. Create .env file with: OPENROUTER_API_KEY=your-key
3. Run: streamlit run ai_tool_demo.py
{"=" * 50}
"""

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Page setup
st.set_page_config(page_title="AI Tool Demo", page_icon="{title_emoji}", layout="centered")

# Custom styling
st.markdown("""
<style>
    .stTextArea textarea {{ font-size: 14px; }}{extra_styling}
</style>
""", unsafe_allow_html=True)

# Header
st.title("{title_emoji} AI Tool Demo")
st.markdown("*{problem_desc}*")
st.markdown("---")

# Check API key
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    st.error("⚠️ Please add OPENROUTER_API_KEY to your .env file!")
    st.stop()

# Setup AI
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    llm = ChatOpenAI(
        model="deepseek/deepseek-r1",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
        default_headers={{"HTTP-Referer": "https://venturepilot.app", "X-Title": "VenturePilot"}}
    )
except ImportError:
    st.error("Missing packages! Run: pip install langchain-openai")
    st.stop()

# AI Prompts
SYSTEM_PROMPT = "{system_prompt_safe}"
USER_TEMPLATE = "{user_template_safe}"

prompt = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("human", USER_TEMPLATE)])
chain = prompt | llm | StrOutputParser()

# Input section
st.markdown("### 📝 Your Input")
{input_code}

# Generate button
if st.button("{button_text}", type="primary", use_container_width=True):
    if not ({validation}):
        st.warning("Please fill in all fields!")
    else:
        with st.spinner("{"🪄 Working magic..." if student_class <= 7 else "🤔 AI is thinking..." if student_class <= 9 else "Processing..."}"):
            try:
                result = chain.invoke({{{invoke_dict}}})
                st.markdown("---")
                st.markdown("{success_text}")
                st.markdown(result)
            except Exception as e:
                st.error(f"Oops! Something went wrong: {{str(e)}}")

st.markdown("---")
st.caption("{footer_text}")
'''
        
        return demo_script
