
Use the following command to view your configured Git for your username:
```bash
git config user.name
```
### 🔍 Additional:
- To check global username:
    ```bash
    git config --global user.name
    ```
- To see all Git config values:
    ```bash
    git config --list
    ```

| **Command**                                        | **Purpose**                                                 |
| -------------------------------------------------- | ----------------------------------------------------------- |
| `git config --list`                                | Show all Git config values (from all levels)                |
| `git config --global user.name "Your Name"`        | Set global username                                         |
| `git config --global user.email "you@example.com"` | Set global user email                                       |
| `git config user.name "Your Name"`                 | Set local (repo-level) username                             |
| `git config user.email "you@example.com"`          | Set local (repo-level) user email                           |
| `git config --global core.editor nano`             | Set default global text editor                              |
| `git config core.editor code`                      | Set default local text editor                               |
| `git config --global merge.tool vimdiff`           | Set merge tool globally                                     |
| `git config --global diff.tool vimdiff`            | Set diff tool globally                                      |
| `git config --global color.ui auto`                | Enable colored output globally                              |
| `git config --system core.autocrlf input`          | Set line ending handling (system-wide)                      |
| `git config --global alias.co checkout`            | Create a shortcut alias (e.g., `git co` for `git checkout`) |
| `git config --unset user.name`                     | Remove local user.name setting                              |
| `git config --unset --global user.email`           | Remove global user.email setting                            |
| `git config --edit`                                | Edit local Git config file in editor                        |
| `git config --global --edit`                       | Edit global Git config file in editor                       |
| `git config --system --edit`                       | Edit system-level Git config file                           |

|Command|Description|
|---|---|
|`git config --global user.name "Your Name"`|Set global Git username|
|`git config --global user.email "you@example.com"`|Set global Git email|
|`git config --local core.editor "vim"`|Set editor for Git commit messages in current repo|
|`git config --global core.autocrlf true`|Handle line endings automatically (Windows)|
|`git config --global credential.helper cache`|Cache credentials temporarily|
|`git config --global alias.co checkout`|Create alias `co` for `checkout` command|
|`git config --global push.default simple`|Set default push behavior|
|`git config --list`|List all current Git configurations|
|`git config --local merge.tool vimdiff`|Set merge tool for the local repo|
|`git config --global color.ui auto`|Enable colored output in Git commands|
|`git config --global core.excludesfile ~/.gitignore_global`|Set global ignore file|
|`git config --local diff.algorithm patience`|Use "patience" diff algorithm locally|
|`git config --global init.defaultBranch main`|Set default branch name for new repos|
|`git config --global pull.rebase true`|Enable rebase on git pull globally|
