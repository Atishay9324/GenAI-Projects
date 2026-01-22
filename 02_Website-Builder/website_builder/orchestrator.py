"""Agent Orchestrator - Coordinates all AI agents to build websites."""

import json
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import OUTPUT_DIR, validate_config
from .agents import ContentAgent, DesignerAgent, CoderAgent, ReviewerAgent


console = Console()


class AgentOrchestrator:
    """Orchestrates the website building process using multiple AI agents."""

    def __init__(self):
        """Initialize the orchestrator with all agents."""
        validate_config()
        self.content_agent = ContentAgent()
        self.designer_agent = DesignerAgent()
        self.coder_agent = CoderAgent()
        self.reviewer_agent = ReviewerAgent()

    def build_website(
        self,
        description: str,
        website_type: str = "business",
        style: str = "modern",
        output_name: Optional[str] = None,
        skip_review: bool = False
    ) -> Path:
        """Build a complete website using the AI agent pipeline.
        
        Args:
            description: Description of the website to build
            website_type: Type of website (business, portfolio, landing, etc.)
            style: Design style (modern, minimal, bold, elegant)
            output_name: Name for the output folder
            skip_review: Whether to skip the review step
            
        Returns:
            Path to the generated website
        """
        # Create output directory
        if output_name:
            project_dir = OUTPUT_DIR / output_name
        else:
            # Generate name from description
            safe_name = "".join(c if c.isalnum() else "_" for c in description[:30])
            project_dir = OUTPUT_DIR / safe_name.strip("_").lower()
        
        project_dir.mkdir(parents=True, exist_ok=True)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Step 1: Generate Content
            task = progress.add_task("[cyan]📝 Generating content...", total=None)
            console.print(Panel(f"[bold cyan]{self.content_agent.name}[/] is writing compelling content..."))
            
            content_result = self.content_agent.run(
                description=description,
                website_type=website_type
            )
            content = content_result["content"]
            progress.remove_task(task)
            console.print("[green]✓[/] Content generated successfully!")

            # Save content for reference
            with open(project_dir / "content.json", "w") as f:
                json.dump(content, f, indent=2)

            # Step 2: Generate Design
            task = progress.add_task("[magenta]🎨 Creating design...", total=None)
            console.print(Panel(f"[bold magenta]{self.designer_agent.name}[/] is crafting the visual design..."))
            
            design_result = self.designer_agent.run(
                description=description,
                content=content,
                style=style
            )
            design = design_result["design"]
            progress.remove_task(task)
            console.print("[green]✓[/] Design specifications created!")

            # Save design for reference
            with open(project_dir / "design.json", "w") as f:
                json.dump(design, f, indent=2)

            # Step 3: Generate Code
            task = progress.add_task("[yellow]💻 Writing code...", total=None)
            console.print(Panel(f"[bold yellow]{self.coder_agent.name}[/] is building the website..."))
            
            code_result = self.coder_agent.run(
                content=content,
                design=design,
                description=description
            )
            html_code = code_result["html"]
            progress.remove_task(task)
            console.print("[green]✓[/] Website code generated!")

            # Step 4: Review and Improve (optional)
            if not skip_review:
                task = progress.add_task("[blue]🔍 Reviewing & polishing...", total=None)
                console.print(Panel(f"[bold blue]{self.reviewer_agent.name}[/] is polishing the final result..."))
                
                review_result = self.reviewer_agent.run(
                    html_code=html_code,
                    description=description
                )
                html_code = review_result["html"]
                progress.remove_task(task)
                console.print("[green]✓[/] Code reviewed and improved!")

            # Save the final website
            index_path = project_dir / "index.html"
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(html_code)

        console.print()
        console.print(Panel(
            f"[bold green]🎉 Website created successfully![/]\n\n"
            f"[white]Location:[/] {project_dir}\n"
            f"[white]Open:[/] {index_path}",
            title="✨ Complete",
            border_style="green"
        ))

        return project_dir
