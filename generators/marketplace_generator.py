"""
Marketplace Generator - Generates complete marketplace prototype.
Features age-adaptive complexity in all outputs.
"""

from utils.llm_client import get_llm_client


class MarketplaceGenerator:
    """Generates age-adaptive marketplace prototypes."""
    
    AGE_PROFILES = {
        "junior": {  # Class 6-7
            "grades": [6, 7],
            "roles_complexity": "2 simple roles (like buyer and seller), easy to understand",
            "flow_complexity": "4-5 very simple steps, like a story",
            "schema_complexity": "2-3 basic tables, simple fields, lots of comments",
            "html_complexity": "very simple HTML, colorful, fun design, emojis",
            "language": "simple words, friendly, like explaining to a friend"
        },
        "middle": {  # Class 8-9
            "grades": [8, 9],
            "roles_complexity": "2-3 roles with clear responsibilities",
            "flow_complexity": "5-6 logical steps covering main user journey",
            "schema_complexity": "3-4 tables with relationships, clear structure",
            "html_complexity": "clean HTML/CSS, modern design, organized layout",
            "language": "clear and practical, introducing business concepts"
        },
        "senior": {  # Class 10-12
            "grades": [10, 11, 12],
            "roles_complexity": "3-4 roles including admin, detailed permissions",
            "flow_complexity": "6-8 comprehensive steps with edge cases",
            "schema_complexity": "4-6 normalized tables, indexes, proper relationships",
            "html_complexity": "professional HTML/CSS/JS, startup-quality design",
            "language": "professional startup terminology, industry-standard"
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
        """Generate age-adaptive marketplace prototype."""
        profile = self._get_age_profile(student_class)
        
        architecture = self._generate_architecture(refined_idea, context, student_class, profile)
        schema = self._generate_schema(refined_idea, architecture, student_class, profile)
        html = self._generate_html_scaffold(refined_idea, architecture, student_class, profile)
        
        return {
            "user_roles": architecture.get("user_roles", []),
            "user_flow": architecture.get("user_flow", []),
            "database_schema": schema,
            "html_scaffold": html
        }
    
    def _generate_architecture(self, refined_idea: dict, context: str, student_class: int, profile: dict) -> dict:
        """Generate age-adaptive user roles and flow."""
        system_prompt = f"""You are a product architect designing a marketplace for a CLASS {student_class} student.

═══════════════════════════════════════════════════════════
AGE-ADAPTIVE ARCHITECTURE
═══════════════════════════════════════════════════════════

ROLES COMPLEXITY: {profile['roles_complexity']}
FLOW COMPLEXITY: {profile['flow_complexity']}
LANGUAGE STYLE: {profile['language']}

{"FOR CLASS 6-7: Keep it SUPER simple! Like explaining a lemonade stand. Use fun, friendly language." if student_class <= 7 else ""}
{"FOR CLASS 8-9: Clear and practical. Help them understand basic marketplace dynamics." if 8 <= student_class <= 9 else ""}
{"FOR CLASS 10-12: Professional marketplace design. Include edge cases and business logic." if student_class >= 10 else ""}

OUTPUT FORMAT (JSON):
{{
    "user_roles": [
        {{"name": "Role Name", "description": "What they do in simple terms"}}
    ],
    "user_flow": [
        "Step 1: ...",
        "Step 2: ..."
    ]
}}"""
        
        features_text = "\n".join(f"- {f}" for f in refined_idea.get("core_features", []))
        
        user_prompt = f"""Design marketplace architecture for Class {student_class} student:

PURPOSE: {refined_idea.get('problem_statement', 'N/A')}
TARGET USERS: {refined_idea.get('target_user', 'N/A')}
FEATURES:
{features_text}
REVENUE: {refined_idea.get('revenue_model', 'N/A')}

Use {profile['language']} language.
Create {profile['roles_complexity']}.
Design {profile['flow_complexity']}.

Return valid JSON only."""
        
        try:
            return self.llm.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.5
            )
        except Exception:
            return {
                "user_roles": [
                    {"name": "Buyer", "description": "People who want to buy"},
                    {"name": "Seller", "description": "People who want to sell"}
                ],
                "user_flow": [
                    "Sign up for an account",
                    "Browse or list items",
                    "Make a purchase",
                    "Complete the transaction"
                ]
            }
    
    def _generate_schema(self, refined_idea: dict, architecture: dict, student_class: int, profile: dict) -> str:
        """Generate age-adaptive database schema."""
        system_prompt = f"""You are a database architect creating a schema for a CLASS {student_class} student.

═══════════════════════════════════════════════════════════
AGE-ADAPTIVE DATABASE DESIGN
═══════════════════════════════════════════════════════════

SCHEMA COMPLEXITY: {profile['schema_complexity']}

{"FOR CLASS 6-7: Create VERY simple tables (2-3 max). Add LOTS of comments explaining what each thing does. Like teaching database basics!" if student_class <= 7 else ""}
{"FOR CLASS 8-9: Create clean, organized tables (3-4). Add helpful comments. Good learning structure." if 8 <= student_class <= 9 else ""}
{"FOR CLASS 10-12: Create proper normalized schema (4-6 tables). Include indexes, foreign keys, timestamps. Production-ready structure." if student_class >= 10 else ""}

REQUIREMENTS:
- SQLite-compatible syntax
- {"Simple PRIMARY KEY only" if student_class <= 7 else "Proper relationships" if student_class <= 9 else "Full normalization, indexes, constraints"}
- {"Lots of comments for learning!" if student_class <= 9 else "Professional comments"}

OUTPUT: Return ONLY SQL code starting with -- Database Schema"""
        
        roles = architecture.get("user_roles", [])
        roles_text = ""
        if roles and isinstance(roles[0], dict):
            roles_text = "\n".join(f"- {r['name']}: {r['description']}" for r in roles)
        else:
            roles_text = "- Buyer\n- Seller"
        
        user_prompt = f"""Create database schema for Class {student_class} student's marketplace:

PURPOSE: {refined_idea.get('problem_statement', 'N/A')}
USER ROLES:
{roles_text}
FEATURES: {', '.join(refined_idea.get('core_features', []))}

Generate {profile['schema_complexity']}.
Return only SQL code."""
        
        schema = self.llm.generate_code(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3
        )
        
        return self._clean_code(schema, "sql")
    
    def _generate_html_scaffold(self, refined_idea: dict, architecture: dict, student_class: int, profile: dict) -> str:
        """Generate age-adaptive HTML scaffold."""
        system_prompt = f"""You are a web developer creating HTML for a CLASS {student_class} student's marketplace.

═══════════════════════════════════════════════════════════
AGE-ADAPTIVE HTML GENERATION
═══════════════════════════════════════════════════════════

HTML COMPLEXITY: {profile['html_complexity']}

{"FOR CLASS 6-7: VERY simple HTML! Colorful, fun, use emojis! Add comments explaining the code. Under 80 lines. Like a fun school project!" if student_class <= 7 else ""}
{"FOR CLASS 8-9: Clean, modern HTML/CSS. Good structure, helpful comments. Under 120 lines." if 8 <= student_class <= 9 else ""}
{"FOR CLASS 10-12: Professional startup-quality HTML/CSS/JS. Polished design, proper structure. Under 180 lines." if student_class >= 10 else ""}

REQUIREMENTS:
1. Complete, runnable HTML file
2. All CSS inline in <style>
3. {"NO JavaScript - keep simple!" if student_class <= 7 else "Basic JS for interactivity" if student_class <= 9 else "Professional JS interactions"}
4. {"Fun colors and emojis!" if student_class <= 7 else "Modern, clean design" if student_class <= 9 else "Startup-quality professional design"}

OUTPUT: Return ONLY HTML code starting with <!DOCTYPE html>"""
        
        roles = architecture.get("user_roles", [])
        if roles and isinstance(roles[0], dict):
            roles_text = ", ".join(r['name'] for r in roles)
        else:
            roles_text = "Buyer, Seller"
        
        user_prompt = f"""Create HTML marketplace for Class {student_class} student:

NAME: Generate a {"fun, catchy" if student_class <= 7 else "catchy" if student_class <= 9 else "professional"} name
PURPOSE: {refined_idea.get('problem_statement', 'N/A')}
USER ROLES: {roles_text}
FEATURES: {', '.join(refined_idea.get('core_features', []))}

Generate {profile['html_complexity']} code.
Return only complete HTML."""
        
        html = self.llm.generate_code(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4
        )
        
        html = self._clean_code(html, "html")
        return self._ensure_valid_html(html)
    
    def _clean_code(self, code: str, code_type: str) -> str:
        """Remove markdown and thinking tags."""
        code = code.strip()
        
        if "<think>" in code:
            think_end = code.find("</think>")
            if think_end != -1:
                code = code[think_end + 8:].strip()
        
        markers = [f"```{code_type}", "```"]
        for marker in markers:
            if code.startswith(marker):
                code = code[len(marker):]
                break
        
        if code.endswith("```"):
            code = code[:-3]
        
        return code.strip()
    
    def _ensure_valid_html(self, html: str) -> str:
        """Ensure HTML is valid."""
        html = html.strip()
        
        if not html.lower().startswith("<!doctype"):
            html = "<!DOCTYPE html>\n" + html
        
        if "<html" not in html.lower():
            html = html.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n<html lang=\"en\">")
            if "</html>" not in html.lower():
                html += "\n</html>"
        
        return html
