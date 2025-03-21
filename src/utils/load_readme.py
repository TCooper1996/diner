from pathlib import Path

def load_readme() -> str:
    # Dynamically locate the project root (two levels up from this file)
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    # Define README path
    readme_path = PROJECT_ROOT / "README.md"

    # Load the README content
    return readme_path.read_text(encoding='utf-8')