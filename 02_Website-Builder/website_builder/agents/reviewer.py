"""Reviewer Agent - Reviews and improves generated website code."""

from typing import Any, Dict
from .base import BaseAgent


class ReviewerAgent(BaseAgent):
    """Agent responsible for reviewing and improving website code."""

    def __init__(self):
        # Moderate temperature for balanced creativity and consistency
        super().__init__(temperature=0.4)

    @property
    def name(self) -> str:
        return "Reviewer Agent"

    @property
    def system_prompt(self) -> str:
        return """You are a senior frontend developer and code reviewer.
Your task is to review website code and improve it for:

1. Code Quality: Clean, well-organized, properly indented
2. Performance: Optimized CSS, efficient JavaScript
3. Accessibility: ARIA labels, proper contrast, keyboard navigation
4. SEO: Meta tags, semantic HTML, proper headings
5. Visual Polish: Enhanced animations, better spacing, refined colors
6. Responsiveness: Better mobile experience
7. Cross-browser: Vendor prefixes where needed

When you review code, output the IMPROVED, COMPLETE HTML file.
Make meaningful improvements while keeping the core design intact.
Do NOT remove any sections. Only enhance what exists."""

    def run(self, html_code: str, description: str) -> Dict[str, Any]:
        """Review and improve the generated website code.
        
        Args:
            html_code: The HTML code to review
            description: Original website description for context
            
        Returns:
            Dictionary containing improved HTML code
        """
        human_template = """Review and improve this website code:

ORIGINAL WEBSITE PURPOSE: {description}

CODE TO REVIEW:
{html_code}

Please improve the code by:
1. Adding proper meta tags (description, viewport, og tags)
2. Ensuring all accessibility requirements are met
3. Adding subtle micro-animations for better UX
4. Polishing the visual design
5. Optimizing performance
6. Fixing any potential issues

Output ONLY the complete, improved HTML code.
Start with <!DOCTYPE html> and end with </html>.
Do NOT include any markdown code blocks or explanations.
Do NOT remove any sections - only improve them."""

        chain = self.create_chain(human_template)
        result = chain.invoke({
            "description": description,
            "html_code": html_code
        })

        # Clean up the result
        improved_html = result.strip()
        if improved_html.startswith("```"):
            lines = improved_html.split("\n")
            improved_html = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

        return {"html": improved_html, "raw_response": result}
