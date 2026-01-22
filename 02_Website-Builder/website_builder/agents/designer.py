"""Designer Agent - Creates design specifications for websites."""

from typing import Any, Dict
from .base import BaseAgent


class DesignerAgent(BaseAgent):
    """Agent responsible for creating design specifications."""

    @property
    def name(self) -> str:
        return "Designer Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert UI/UX designer specializing in modern web design.
Your task is to create beautiful, modern, and user-friendly design specifications.

You understand color theory, typography, spacing, and modern design trends like:
- Glassmorphism
- Gradients
- Dark/Light modes
- Micro-animations
- Responsive design

Always respond with valid JSON only, no additional text."""

    def run(self, description: str, content: Dict[str, Any], style: str = "modern") -> Dict[str, Any]:
        """Generate design specifications based on website description and content.
        
        Args:
            description: Description of the website
            content: Generated content from ContentAgent
            style: Design style preference
            
        Returns:
            Dictionary containing design specifications
        """
        human_template = """Create a stunning design specification for:

Website Description: {description}
Design Style: {style}
Content Preview: {content_preview}

Generate a comprehensive design spec in this exact JSON format:
{{
    "theme": {{
        "mode": "dark or light",
        "style": "minimal/bold/elegant/playful"
    }},
    "colors": {{
        "primary": "#hexcode",
        "secondary": "#hexcode",
        "accent": "#hexcode",
        "background": "#hexcode",
        "surface": "#hexcode",
        "text_primary": "#hexcode",
        "text_secondary": "#hexcode",
        "gradient": "linear-gradient(...)"
    }},
    "typography": {{
        "font_heading": "Google Font name",
        "font_body": "Google Font name",
        "heading_sizes": {{
            "h1": "4rem",
            "h2": "2.5rem",
            "h3": "1.75rem"
        }},
        "body_size": "1rem",
        "line_height": "1.6"
    }},
    "spacing": {{
        "section_padding": "6rem",
        "element_gap": "2rem",
        "container_max_width": "1200px"
    }},
    "effects": {{
        "border_radius": "12px",
        "box_shadow": "0 10px 40px rgba(0,0,0,0.1)",
        "glass_effect": true,
        "animations": ["fade-in", "slide-up", "hover-lift"]
    }},
    "layout": {{
        "hero_style": "centered/split/full-width",
        "navigation": "fixed/sticky",
        "sections_order": ["hero", "features", "about", "testimonials", "contact", "footer"]
    }}
}}"""

        # Create a summary of content for the designer
        content_preview = f"Hero: {content.get('hero', {}).get('headline', 'N/A')}"

        chain = self.create_chain(human_template)
        result = chain.invoke({
            "description": description,
            "style": style,
            "content_preview": content_preview
        })

        # Parse JSON result
        import json
        try:
            design = json.loads(result)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                design = json.loads(json_match.group())
            else:
                raise ValueError("Failed to parse design from AI response")

        return {"design": design, "raw_response": result}
