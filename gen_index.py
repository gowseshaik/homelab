import os
from pathlib import Path

docs_dir = "docs"
output_file = "docs/index.md"

# Directories to exclude (add more if needed)
EXCLUDE_DIRS = {".obsidian", "assets"}


def generate_index():
    content = "# Knowledge Base\n\n"

    for topic in sorted(os.listdir(docs_dir)):
        topic_path = os.path.join(docs_dir, topic)

        # Skip excluded directories and non-directories
        if not os.path.isdir(topic_path) or topic in EXCLUDE_DIRS:
            continue

        content += f"## {topic.capitalize()}\n"
        for file in sorted(os.listdir(topic_path)):
            if file.endswith(".md"):
                file_name = file[:-3]  # Remove '.md'
                content += f"- [{file_name}]({topic}/{file})\n"
        content += "\n"

    # Ensure output directory exists
    Path(output_file).parent.mkdir(exist_ok=True)

    with open(output_file, "w") as f:
        f.write(content)


if __name__ == "__main__":
    generate_index()