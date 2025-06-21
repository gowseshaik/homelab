```bash
$ python3 -m venv handsondevops
$ source ./handsondevops/bin/activate
$ pip install mkdocs

$ pip install mkdocs-material

$ echo ".obsidian/" >> .gitignore
$ git add .
$ git commit -am "add comment"
$ git push -u origin main
$ mkdocs gh-deploy --clean
```

🧩 Popular Themes

|Theme|Use with|
|---|---|
|`mkdocs`|Default|
|`readthedocs`|Lightweight|
|`material`|`pip install mkdocs-material`|

📦 Common Commands

|Command|Description|
|---|---|
|`mkdocs new my-project`|Create new MkDocs project|
|`mkdocs serve`|Run dev server at [http://127.0.0.1:8000](http://127.0.0.1:8000)|
|`mkdocs build`|Build static site to `site/` dir|
|`mkdocs gh-deploy`|Deploy to GitHub Pages|
📁 Project Structure
```
my-project/
├── docs/
│   ├── index.md
│   ├── about.md
├── mkdocs.yml
```

📄 mkdocs.yml (basic)
```
site_name: My Docs
nav:
  - Home: index.md
  - About: about.md
theme: readthedocs
```

example :  mkdocs.yml 
```
site_name: Gouse Shaik  
site_url: https://github.com/username/repo  
repo_url: https://github.com/username/repo 
repo_name: RepoName  
  
theme:  
  name: material  
  logo: images/logo-design-4.png  
  favicon: images/favicon.ico  
  features:  
    - navigation.instant  
    - navigation.top  
    - navigation.sections  
    - navigation.expand  
    - content.code.copy  
    - content.tabs.link  
    - toc.integrate  
    - content.action.edit  
    - content.tooltips  
  palette:  
    - scheme: default  
      primary: cyan  
      accent: teal  
      toggle:  
        icon: material/weather-night  
        name: Switch to dark mode  
    - scheme: slate  
      primary: cyan  
      accent: teal  
      toggle:  
        icon: material/weather-sunny  
        name: Switch to light mode  
  font:  
    text: "Patrick Hand"  
    code: "JetBrains Mono"  
  icon:  
    repo: fontawesome/brands/github  
  extra_css:  
    - extra.css  
  
markdown_extensions:  
  - admonition  
  - toc:  
      permalink: true  
  - codehilite  
  - footnotes  
  - tables  
  - pymdownx.superfences  
  - pymdownx.tabbed  
  - pymdownx.details  
  - pymdownx.emoji:  
      emoji_generator: !!python/name:pymdownx.emoji.to_svg  
  
plugins:  
  - search  
  
nav:  
  - Home: index.md  
  - About: about.md

exclude:
  - .obsidian/*
```

# python script to generate before pushing to Github
```
import os  
from pathlib import Path  
  
docs_dir = "docs"  
output_file = "docs/index.md"  
  
  
def generate_index():  
    content = "# Knowledge Base\n\n"  
  
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
```