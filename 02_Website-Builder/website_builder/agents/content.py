"""Content Agent - Generates website content and copy."""

from typing import Any, Dict
from .base import BaseAgent


class ContentAgent(BaseAgent):
    """Agent responsible for generating website content."""

    @property
    def name(self) -> str:
        return "Content Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert website content writer and copywriter. 
Your task is to create compelling, engaging, and SEO-friendly content for websites.

You will generate content in a structured JSON format including:
- Hero section (headline, subheadline, CTA button text)
- About section
- Features/Services section (3-4 items)
- Testimonials (2-3 quotes)
- Contact section content
- Footer content

Make the content professional, engaging, and tailored to the specific business/purpose.
Always respond with valid JSON only, no additional text."""

    def run(self, description: str, website_type: str = "business") -> Dict[str, Any]:
        """Generate website content based on description.
        
        Args:
            description: Description of the website to build
            website_type: Type of website (business, portfolio, landing, etc.)
            
        Returns:
            Dictionary containing structured website content
        """
        human_template = """Create website content for the following:

Website Description: {description}
Website Type: {website_type}

Generate comprehensive content in this exact JSON format:
{{
    "hero": {{
        "headline": "Main attention-grabbing headline",
        "subheadline": "Supporting text that explains the value proposition",
        "cta_primary": "Primary button text",
        "cta_secondary": "Secondary button text"
    }},
    "about": {{
        "title": "About section title",
        "description": "2-3 paragraph about section content"
    }},
    "features": [
        {{
            "title": "Feature 1 title",
            "description": "Feature 1 description",
            "icon": "suggested icon name"
        }},
        {{
            "title": "Feature 2 title",
            "description": "Feature 2 description",
            "icon": "suggested icon name"
        }},
        {{
            "title": "Feature 3 title",
            "description": "Feature 3 description",
            "icon": "suggested icon name"
        }}
    ],
    "testimonials": [
        {{
            "quote": "Testimonial quote",
            "author": "Person Name",
            "role": "Job Title, Company"
        }}
    ],
    "contact": {{
        "title": "Contact section title",
        "description": "Invitation to get in touch"
    }},
    "footer": {{
        "tagline": "Short company tagline",
        "copyright": "Copyright text"
    }}
}}"""

        chain = self.create_chain(human_template)
        result = chain.invoke({
            "description": description,
            "website_type": website_type
        })

        # Parse JSON result
        import json
        try:
            content = json.loads(result)
        except json.JSONDecodeError:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                content = json.loads(json_match.group())
            else:
                raise ValueError("Failed to parse content from AI response")

        return {"content": content, "raw_response": result}
