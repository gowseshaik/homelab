<span style="color:#4caf50;"><b>Created:</b> 2025-07-06</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

```bash
(.venv) gouse@gouse:~/Documents/homelab$ git push -u origin main
To https://github.com/gowseshaik/homelab.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/gowseshaik/homelab.git'
hint: Updates were rejected because the tip of your current branch is behind                                                                                                                                               
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

You're getting this error because your local `main` branch is **behind** the remote `main` branch — probably due to new commits on GitHub that your local repo doesn't have.
### Run this to fix:
```bash
git pull --rebase origin main && git push -u origin main
```
### Explanation:
- `git pull --rebase origin main`: Fetches and applies remote changes before your local commits.
- `git push -u origin main`: Pushes your changes after syncing with remote.

> ⚠️ If you have uncommitted changes, **stash or commit** them before running this to avoid conflicts.

```bash
(.venv) gouse@gouse:~/Documents/homelab/docs$ git push -u origin main
To https://github.com/gowseshaik/homelab.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/gowseshaik/homelab.git'
hint: Updates were rejected because a pushed branch tip is behind its remote                                                                                                                                               
hint: counterpart. If you want to integrate the remote changes, use 'git pull'
hint: before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
(.venv) gouse@gouse:~/Documents/homelab/docs$ git branch
* (no branch, rebasing main)
  gh-pages
  main
(.venv) gouse@gouse:~/Documents/homelab/docs$ cd ..
(.venv) gouse@gouse:~/Documents/homelab$ git branch
* (no branch, rebasing main)
  gh-pages
  main
(.venv) gouse@gouse:~/Documents/homelab$ git checkout barnch main
error: pathspec 'barnch' did not match any file(s) known to git
error: pathspec 'main' did not match any file(s) known to git
(.venv) gouse@gouse:~/Documents/homelab$ git branch
* (no branch, rebasing main)
  gh-pages
  main
(.venv) gouse@gouse:~/Documents/homelab$ 
```

You're currently **stuck in a rebase state**, which is why:
- Your current branch is shown as `* (no branch, rebasing main)`
- You can’t switch branches or push.

### 🔧 Fix it step-by-step:

#### ✅ 1. **Abort the rebase**
```bash
git rebase --abort

(.venv) gouse@gouse:~/Documents/homelab$ git rebase --abort
(.venv) gouse@gouse:~/Documents/homelab$ git branch
  gh-pages
* main

(.venv) gouse@gouse:~/Documents/homelab$ git status
On branch main
Your branch and 'origin/main' have diverged,
and have 2 and 8 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

nothing to commit, working tree clean
```
#### ✅ 2. **Switch to `main` branch**
```bash
git checkout main

(.venv) gouse@gouse:~/Documents/homelab$ git checkout main
Already on 'main'
Your branch and 'origin/main' have diverged,
and have 2 and 8 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)
```
#### ✅ 3. **Pull remote changes and rebase**
```bash
git pull --rebase origin main

(.venv) gouse@gouse:~/Documents/homelab$ git pull --rebase origin main
error: cannot pull with rebase: You have unstaged changes.
error: Please commit or stash them.

#If you want to **merge** remote changes:
git pull --no-rebase

# If you want to **rebase** your local commits on top of remote:
git pull --rebase

If you want to make it permanent for this repo:
# For **merge (default)**:
git config pull.rebase false

# For **rebase (recommended for clean history)**:
git config pull.rebase true
```
#### ✅ 4. **Push your changes**
```bash
git push -u origin main
```

#### ✅ 5. **Pull from remote to sync local and Push your changes**
Run this single command to resolve it:
```bash
git add . && git stash && git pull --rebase origin main && git stash pop
```
### 🔍 What each does:

- `git add .` → stages all changes (to avoid stash errors on untracked files).
- `git stash` → saves local changes temporarily.
- `git pull --rebase origin main` → pulls remote changes cleanly.
- `git stash pop` → restores your local changes back on top.

#### ✅ 5. To **discard** all local unstaged changes and pull 
If you want to **discard** all local unstaged changes and pull with rebase, run:
```bash
git reset --hard && git clean -fd && git pull --rebase origin main
```
### 🔍 Explanation:

- `git reset --hard` → discards all tracked file changes.
- `git clean -fd` → removes untracked files and directories.
- `git pull --rebase origin main` → pulls latest changes with rebase.

⚠️ **Warning**: This will delete all your local changes permanently.

