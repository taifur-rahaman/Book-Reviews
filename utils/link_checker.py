import os
import re
from pathlib import Path

WORKSPACE_DIR = r"e:\Notes\reviews\Book-Reviews"

titles = {
    "Harry Potter and the Chamber of Secrets": "harry_potter_and_the_chamber_of_secrets.md",
    "Harry Potter and the Philosopher's Stone": "harry_potter_and_the_philosophers_stone.md",
    "Harry Potter and the Prisoner of Azkaban": "harry_potter_and_the_prisoner_of_azkaban.md",
    "The Battle of the Labyrinth": "the_battle_of_the_labyrinth.md",
    "The Last Olympian": "the_last_olympian.md",
    "The Lightning Thief": "the_lightning_thief.md",
    "The Perks of Being a Wallflower": "the_perks_of_being_a_wallflower.md",
    "The Sea of Monsters": "the_sea_of_monsters.md",
    "The Titan's Curse": "the_titans_curse.md"
}

def is_linked(text, match_start, match_end):
    links = [m.span() for m in re.finditer(r'\[.*?\]\(.*?\)', text)]
    for start, end in links:
        if start <= match_start and match_end <= end:
            return True
            
    # Also ignore if it is right after `# ` or `| Original Title | `
    if text.strip().startswith('# '):
        return True
    if text.strip().startswith('| Original Title |'):
        return True
    if text.strip().startswith('| Alternative Title |'):
        return True
    return False

def check_files():
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        if '.git' in root or 'node_modules' in root:
            continue
        for file in files:
            if not file.endswith(".md"):
                continue
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines):
                # if line is a table definition with links, skip
                for title, filename in titles.items():
                    for match in re.finditer(re.escape(title), line, re.IGNORECASE):
                        if not is_linked(line, match.start(), match.end()):
                            rel_dir = os.path.relpath(os.path.join(WORKSPACE_DIR, 'titles'), root)
                            rel_path = os.path.join(rel_dir, filename).replace('\\', '/')
                            print(f"{filepath}:{i+1}:{title}:{rel_path}")

if __name__ == "__main__":
    check_files()
