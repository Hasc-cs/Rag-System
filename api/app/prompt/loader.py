
from pathlib import Path #-------.work with files and folders


PROMPTS_DIR = Path(__file__).parent #api/app/prompt


def get_prompt(name: str, version: str = "v1") -> str:
    return (PROMPTS_DIR / name / f"{version}.md").read_text(encoding="utf-8").strip()
