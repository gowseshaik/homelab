import os
from pathlib import Path

docs_dir = "docs"
output_file = "docs/index.md"


def generate_index():
    content = "# My Knowledge Base\n\n"

    for topic in sorted(os.listdir(docs_dir)):
        topic_path = os.path.join(docs_dir, topic)
        if os.path.isdir(topic_path) and topic != "assets":
            content += f"## {topic.capitalize()}\n"
            for file in sorted(os.listdir(topic_path)):
                if file.endswith(".md"):
                    file_name = file[:-3]  # Remove '.md'
                    content += f"- [{file_name}]({topic}/{file})\n"
            content += "\n"

    with open(output_file, "w") as f:
        f.write(content)


if __name__ == "__main__":
    generate_index()