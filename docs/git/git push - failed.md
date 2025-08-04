```
Error:
$ git push -u origin main
error: src refspec main does not match any
error: failed to push some refs to 'http://100.175.149.160:3000/gouse/TrendyBot.git'
```

```bash
Solution:
$ git add . && git commit -m "initial commit" && git branch -M main && git push -u origin main

$ git add . && git commit -m "initial commit" && git branch -M main && git push -u origin main
warning: in the working copy of '.idea/inspectionProfiles/profiles_settings.xml', LF will be replaced by CRLF the next time Git touches it
[main (root-commit) 926f67a] initial commit
 12 files changed, 401 insertions(+)
 create mode 100644 .idea/.gitignore
 create mode 100644 .idea/TrendyBot.iml
 create mode 100644 .idea/inspectionProfiles/profiles_settings.xml
 create mode 100644 .idea/misc.xml
 create mode 100644 .idea/modules.xml
 create mode 100644 .idea/vcs.xml
 create mode 100644 Dockerfile
 create mode 100644 docker-compose.yml
 create mode 100644 requirements.txt
 create mode 100644 scraper.py
 create mode 100644 superstars.csv
 create mode 100644 superstars_20250803_152912.csv
warning: use of unencrypted HTTP remote URLs is not recommended; see https://aka.ms/gcm/unsaferemotes for more information.
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 12 threads
Compressing objects: 100% (12/12), done.
Writing objects: 100% (15/15), 10.20 KiB | 2.55 MiB/s, done.
Total 15 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
remote: . Processing 1 references
remote: Processed 1 references in total
To http://100.75.49.6:3000/gouse/TrendyBot.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

```bash
switch to available branch
then push it
$ git push -u origin main
remote: Failed to authenticate user
fatal: Authentication failed for 'http://100.175.149.160:3000/gouse/k8sGO.git/'

$ git remote set-url origin http://<username>@100.175.149.160:3000/gouse/k8sGO.git

$ git push -u origin main
warning: use of unencrypted HTTP remote URLs is not recommended; see https://aka.ms/gcm/unsaferemotes for more information.
Enumerating objects: 40, done.
Counting objects: 100% (40/40), done.
Delta compression using up to 12 threads
Compressing objects: 100% (34/34), done.
Writing objects: 100% (40/40), 64.34 KiB | 2.80 MiB/s, done.
Total 40 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
remote: . Processing 1 references
remote: Processed 1 references in total
To http://100.75.49.6:3000/gouse/k8sGO.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```