
from generators.web_generator import WebGenerator
from generators.ai_tool_generator import AIToolGenerator
from generators.marketplace_generator import MarketplaceGenerator


class PrototypeRouter:
    """Routes prototype generation to the appropriate generator."""
    
    def __init__(self):
        self.generators = {
            "App or Website": WebGenerator(),
            "AI Tool": AIToolGenerator(),
            "Marketplace": MarketplaceGenerator()
        }
    
    def generate(
        self,
        idea_type: str,
        refined_idea: dict,
        student_class: int,
        mentor_answers: dict
    ) -> dict:
        """
        Route to appropriate generator and return prototype.
        
        Args:
            idea_type: One of "App or Website", "AI Tool", "Marketplace"
            refined_idea: The structured idea from IdeaRefiner
            student_class: Student's class (6-12)
            mentor_answers: Dict of mentor Q&A responses
        
        Returns:
            dict: Generator-specific prototype output
        """
        generator = self.generators.get(idea_type)
        
        if generator is None:
            raise ValueError(f"Unknown idea type: {idea_type}")
        
        # Build context from mentor session
        context = self._build_context(refined_idea, mentor_answers)
        
        return generator.generate(
            refined_idea=refined_idea,
            student_class=student_class,
            context=context
        )
    
    def _build_context(self, refined_idea: dict, mentor_answers: dict) -> str:
        """Build additional context from mentor session."""
        context_parts = []
        
        # Add mentor insights if available
        if mentor_answers:
            context_parts.append("Insights from mentor session:")
            for idx, answer in mentor_answers.items():
                context_parts.append(f"- {answer}")
        
        return "\n".join(context_parts) if context_parts else ""
