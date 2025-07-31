Yes, if you haven't added the remote repo yet, first link it using:

```bash
git remote add origin https://github.com/your-username/your-repo.git
```

Then push your new branch:

```bash
git checkout -b new-branch-name
git add .
git commit -m "your commit message"
git push -u origin new-branch-name
```
