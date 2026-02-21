"""
Web Generator - Generates HTML landing pages for App/Website ideas.
Features age-adaptive complexity in generated code.
"""

from utils.llm_client import get_llm_client


class WebGenerator:
    """Generates age-adaptive HTML landing pages."""
    
    AGE_PROFILES = {
        "junior": {  # Class 6-7
            "grades": [6, 7],
            "complexity": "very simple HTML, minimal CSS, no JavaScript",
            "design": "colorful, fun, uses emojis, large text, simple layout",
            "sections": "hero with big title, 3 simple features with emojis, footer",
            "code_style": "heavily commented to help them learn, under 100 lines"
        },
        "middle": {  # Class 8-9
            "grades": [8, 9],
            "complexity": "clean HTML/CSS, basic hover effects, simple structure",
            "design": "modern and clean, good colors, readable fonts",
            "sections": "hero, features, how it works, call-to-action, footer",
            "code_style": "well-commented, organized, under 150 lines"
        },
        "senior": {  # Class 10-12
            "grades": [10, 11, 12],
            "complexity": "professional HTML/CSS/JS, animations, responsive design",
            "design": "startup-quality, gradients, shadows, professional typography",
            "sections": "nav, hero with CTA, features, testimonials, pricing hint, CTA, footer",
            "code_style": "production-like code, proper structure, under 200 lines"
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
        """Generate age-adaptive HTML landing page."""
        profile = self._get_age_profile(student_class)
        
        system_prompt = f"""You are a web developer creating a landing page for a CLASS {student_class} student.

═══════════════════════════════════════════════════════════
AGE-ADAPTIVE CODE GENERATION
═══════════════════════════════════════════════════════════

CODE COMPLEXITY: {profile['complexity']}

DESIGN STYLE: {profile['design']}

SECTIONS TO INCLUDE: {profile['sections']}

CODE STYLE: {profile['code_style']}

═══════════════════════════════════════════════════════════
REQUIREMENTS
═══════════════════════════════════════════════════════════

1. Generate COMPLETE, RUNNABLE HTML file
2. Include ALL CSS inline in <style> tag
3. {"NO JavaScript - keep it simple!" if student_class <= 7 else "Include basic JavaScript for interactivity" if student_class <= 9 else "Include smooth JavaScript interactions"}
4. Must work when saved as .html and opened in browser
5. {"Use lots of emojis and fun colors!" if student_class <= 7 else "Use clean, modern design" if student_class <= 9 else "Use professional startup design"}

{"IMPORTANT FOR CLASS 6-7: Make the code VERY simple. Add lots of comments explaining what each part does. This is a learning experience!" if student_class <= 7 else ""}
{"IMPORTANT FOR CLASS 8-9: Keep code clean and organized. Add helpful comments. Good learning opportunity." if 8 <= student_class <= 9 else ""}
{"IMPORTANT FOR CLASS 10-12: Generate professional-quality code they could show to investors or use as a real landing page." if student_class >= 10 else ""}

OUTPUT: Return ONLY the HTML code. Start with <!DOCTYPE html>"""
        
        features_text = "\n".join(f"- {f}" for f in refined_idea.get("core_features", []))
        
        user_prompt = f"""Create a landing page for this Class {student_class} student's startup:

STARTUP DETAILS:
- Problem: {refined_idea.get('problem_statement', 'N/A')}
- Target User: {refined_idea.get('target_user', 'N/A')}
- Features:
{features_text}
- Revenue Model: {refined_idea.get('revenue_model', 'N/A')}

CONTEXT: {context}

Generate {profile['complexity']} code with {profile['design']} design.
Include: {profile['sections']}

Return complete HTML code only."""
        
        html_code = self.llm.generate_code(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4
        )
        
        html_code = self._clean_code(html_code)
        html_code = self._ensure_valid_html(html_code)
        
        return {"html": html_code}
    
    def _clean_code(self, code: str) -> str:
        """Remove markdown and thinking tags."""
        code = code.strip()
        
        if "<think>" in code:
            think_end = code.find("</think>")
            if think_end != -1:
                code = code[think_end + 8:].strip()
        
        if code.startswith("```html"):
            code = code[7:]
        elif code.startswith("```"):
            code = code[3:]
        
        if code.endswith("```"):
            code = code[:-3]
        
        return code.strip()
    
    def _ensure_valid_html(self, html: str) -> str:
        """Ensure HTML is valid."""
        html = html.strip()
        
        if not html.lower().startswith("<!doctype"):
            html = "<!DOCTYPE html>\n" + html
        
        if "<html" not in html.lower():
            html = html.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n<html lang=\"en\">") + "\n</html>"
        
        return html
