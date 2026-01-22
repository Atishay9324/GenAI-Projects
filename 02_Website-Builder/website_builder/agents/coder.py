"""Coder Agent - Generates HTML, CSS, and JavaScript code."""

from typing import Any, Dict
from .base import BaseAgent


class CoderAgent(BaseAgent):
    """Agent responsible for generating website code."""

    def __init__(self):
        # Lower temperature for more consistent code generation
        super().__init__(temperature=0.3)

    @property
    def name(self) -> str:
        return "Coder Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert frontend developer specializing in modern, responsive websites.
You write clean, semantic HTML5, modern CSS3, and vanilla JavaScript.

Your code follows best practices:
- Semantic HTML elements
- CSS custom properties (variables)
- Mobile-first responsive design
- Accessibility standards (ARIA, proper contrast)
- Smooth animations and transitions
- Cross-browser compatibility

Generate COMPLETE, production-ready code. Do not use placeholders or comments like "add more here".
Always output the complete HTML file with embedded CSS and JavaScript."""

    def run(self, content: Dict[str, Any], design: Dict[str, Any], description: str) -> Dict[str, Any]:
        """Generate complete website code.
        
        Args:
            content: Website content from ContentAgent
            design: Design specifications from DesignerAgent
            description: Original website description
            
        Returns:
            Dictionary containing HTML, CSS, and JS code
        """
        human_template = """Generate a complete, production-ready single-page website.

Website Description: {description}

CONTENT:
{content}

DESIGN SPECIFICATIONS:
{design}

Create a COMPLETE index.html file with:
1. Embedded CSS in <style> tags (use CSS custom properties)
2. Embedded JavaScript in <script> tags
3. All sections: hero, features, about, testimonials, contact, footer
4. Responsive navigation with mobile menu
5. Smooth scroll behavior
6. Hover animations and micro-interactions
7. Mobile-responsive design (use media queries)
8. Google Fonts import

Output ONLY the complete HTML code, starting with <!DOCTYPE html> and ending with </html>.
Do NOT include any markdown code blocks or explanations."""

        import json
        
        chain = self.create_chain(human_template)
        result = chain.invoke({
            "description": description,
            "content": json.dumps(content, indent=2),
            "design": json.dumps(design, indent=2)
        })

        # Clean up the result (remove any markdown formatting if present)
        html_code = result.strip()
        if html_code.startswith("```"):
            lines = html_code.split("\n")
            html_code = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

        return {"html": html_code, "raw_response": result}
