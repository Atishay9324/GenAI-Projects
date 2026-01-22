"""CLI interface for the Website Builder."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from pathlib import Path
import http.server
import socketserver
import webbrowser
import threading

from .orchestrator import AgentOrchestrator


console = Console()


def print_banner():
    """Print the application banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║      🌐  AI Website Builder  🤖                               ║
║                                                               ║
║      Build stunning websites with AI agents                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """AI-powered CLI Website Builder using LangChain agents."""
    pass


@cli.command()
@click.option(
    "--description", "-d",
    help="Description of the website to build",
    default=None
)
@click.option(
    "--type", "-t", "website_type",
    type=click.Choice(["business", "portfolio", "landing", "blog", "saas"]),
    default="business",
    help="Type of website to build"
)
@click.option(
    "--style", "-s",
    type=click.Choice(["modern", "minimal", "bold", "elegant", "playful"]),
    default="modern",
    help="Design style for the website"
)
@click.option(
    "--name", "-n", "output_name",
    help="Name for the output folder",
    default=None
)
@click.option(
    "--skip-review",
    is_flag=True,
    help="Skip the code review step"
)
@click.option(
    "--interactive", "-i",
    is_flag=True,
    help="Use interactive mode with prompts"
)
def build(description, website_type, style, output_name, skip_review, interactive):
    """Build a new website using AI agents."""
    print_banner()
    
    try:
        if interactive or not description:
            # Interactive mode
            console.print("\n[bold]Let's build your website! 🚀[/]\n")
            
            description = Prompt.ask(
                "[cyan]Describe your website[/]",
                default="A modern portfolio website for a creative professional"
            )
            
            website_type = Prompt.ask(
                "[cyan]Website type[/]",
                choices=["business", "portfolio", "landing", "blog", "saas"],
                default="business"
            )
            
            style = Prompt.ask(
                "[cyan]Design style[/]",
                choices=["modern", "minimal", "bold", "elegant", "playful"],
                default="modern"
            )
            
            output_name = Prompt.ask(
                "[cyan]Project name (optional)[/]",
                default=""
            ) or None
            
            skip_review = not Confirm.ask(
                "[cyan]Run code review for better quality?[/]",
                default=True
            )
            
            console.print()

        if not description:
            console.print("[red]Error: Please provide a website description.[/]")
            raise click.Abort()

        # Build the website
        console.print(Panel(
            f"[bold]Building:[/] {description}\n"
            f"[bold]Type:[/] {website_type}\n"
            f"[bold]Style:[/] {style}",
            title="🛠️ Configuration",
            border_style="blue"
        ))
        console.print()

        orchestrator = AgentOrchestrator()
        project_dir = orchestrator.build_website(
            description=description,
            website_type=website_type,
            style=style,
            output_name=output_name,
            skip_review=skip_review
        )

        # Ask if user wants to preview
        if Confirm.ask("\n[cyan]Would you like to preview the website?[/]", default=True):
            serve_website(project_dir)

    except ValueError as e:
        console.print(f"[red]Configuration Error:[/] {e}")
        console.print("\n[yellow]Make sure you have set your OPENAI_API_KEY in the .env file.[/]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")
        raise click.Abort()


@cli.command()
@click.argument("path", type=click.Path(exists=True), default="output")
@click.option("--port", "-p", default=8000, help="Port to serve on")
def preview(path, port):
    """Preview a generated website in the browser."""
    print_banner()
    project_path = Path(path)
    
    if project_path.is_file():
        project_path = project_path.parent
    
    serve_website(project_path, port)


def serve_website(directory: Path, port: int = 8000):
    """Serve the website locally and open in browser."""
    import os
    os.chdir(directory)
    
    handler = http.server.SimpleHTTPRequestHandler
    
    # Find an available port
    while True:
        try:
            with socketserver.TCPServer(("", port), handler) as httpd:
                url = f"http://localhost:{port}"
                console.print(f"\n[green]🌐 Serving website at:[/] [link={url}]{url}[/link]")
                console.print("[yellow]Press Ctrl+C to stop the server[/]\n")
                
                # Open browser in a separate thread
                threading.Timer(1, lambda: webbrowser.open(url)).start()
                
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    console.print("\n[yellow]Server stopped.[/]")
                    break
        except OSError:
            port += 1
            if port > 9000:
                console.print("[red]Could not find an available port.[/]")
                break


@cli.command()
def config():
    """Show current configuration."""
    print_banner()
    
    from .config import OPENAI_API_KEY, OPENAI_MODEL, OUTPUT_DIR
    
    api_key_display = f"{OPENAI_API_KEY[:8]}..." if OPENAI_API_KEY else "[red]Not set[/]"
    
    console.print(Panel(
        f"[bold]OpenAI API Key:[/] {api_key_display}\n"
        f"[bold]Model:[/] {OPENAI_MODEL}\n"
        f"[bold]Output Directory:[/] {OUTPUT_DIR}",
        title="⚙️ Configuration",
        border_style="blue"
    ))


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
