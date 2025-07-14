##### to get the list of commits and authors for the specific file:
```json
git log --pretty=format:"%h %an %ad %s" --date=short -- src/AmytodoApp/my_index.thml
```


##### To get **only the most recent commit** that modified the file, use:
```json
git log -1 --pretty=format:"%ae" -- src/AmytodoApp/my_index.thml

### Breakdown:
- `-1` → limits to **1 latest commit**
- `--pretty=format:"..."` → custom output with hash, name, email, date, and message
- `--date=short` → formats date as `YYYY-MM-DD`
- `-- <file>` → restricts to that file only
```

##### To extract only the **author email** from that latest commit, use:
```json
git log -1 --pretty=format:"%ae" -- src/AmytodoApp/my_index.thml
```
##### Output:
Just the email address, like:
```json
gowse_1232someemail@gmail.com
```

### Automated Script
```json
MODIFIED_FILES_CONTENT=""
EMAIL_LIST=""

while IFS= read -r file; do
    # Get latest author email for each file
    EMAIL=$(git log -1 --pretty=format:"%ae" -- "$file")
    MODIFIED_FILES_CONTENT+="${file} (by ${EMAIL})<br>"
done < modified_files

# Remove trailing <br>
MODIFIED_FILES_CONTENT="${MODIFIED_FILES_CONTENT%<br>}"

if [[ -n "$MODIFIED_FILES_CONTENT" ]]; then
    sed -i "s|>RepoChangesNA<|>${MODIFIED_FILES_CONTENT}<|" /home/gouse/Reports/report.html
else
    sed -i "s|>RepoChangesNA<|>No Changes<|" /home/gouse/Reports/report.html
fi
```


