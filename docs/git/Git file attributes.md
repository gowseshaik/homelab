<span style="color:#4caf50;"><b>Created:</b> 2025-07-08</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-08</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
## **1. Handling Line Endings (Windows vs. Unix)**
**Scenario**: Your team uses both Windows (CRLF) and Unix (LF) systems, leading to inconsistent line endings.  

### **Solution**: Use `.gitattributes` to enforce consistent line endings.  

#### **Steps**:
1. **Create/Edit `.gitattributes`**:
   ```bash
   touch .gitattributes
   ```
2. **Define rules**:
   ```gitattributes
   # Auto-detect line endings for text files
   * text=auto

   # Force LF for scripts (Unix-compatible)
   *.sh eol=lf

   # Force CRLF for Windows-specific files
   *.bat eol=crlf
   ```
3. **Apply changes**:
   ```bash
   git add .gitattributes
   git commit -m "Normalize line endings"
   ```
4. **Verify**:
   ```bash
   git ls-files --eol  # Shows line endings per file
   ```

---
## **2. Treating Files as Binary (Avoiding Merge Conflicts)**
**Scenario**: Your repo has PDFs, Word docs, or JAR files that should not be diffed/merged.  

### **Solution**: Mark them as `binary` in `.gitattributes`.  

#### **Steps**:
1. **Edit `.gitattributes`**:
   ```gitattributes
   *.pdf binary
   *.docx binary
   *.jar binary
   ```
2. **Commit changes**:
   ```bash
   git add .gitattributes
   git commit -m "Treat PDF/DOCX/JAR as binary"
   ```
3. **Test**:
   ```bash
   git diff  # Should skip binary files
   ```

---
## **3. Custom Diff for Specific Files (e.g., Java, CSV)**
**Scenario**: You want better `git diff` output for structured files (Java, CSV, JSON).  

### **Solution**: Use a custom diff driver.  

#### **Steps**:
1. **Define a diff driver in `.gitconfig`**:
   ```bash
   git config --global diff.java.textconv "java -jar /path/to/javaprettifier.jar"
   ```
2. **Map it in `.gitattributes`**:
   ```gitattributes
   *.java diff=java
   *.csv diff=csv
   ```
3. **Test**:
   ```bash
   git diff MyFile.java  # Should use the custom formatter
   ```

---
## **4. Git LFS (Handling Large Files)**
**Scenario**: Your repo has large files (videos, datasets, PSDs), bloating Git history.  

### **Solution**: Use **Git LFS (Large File Storage)**.  

#### **Steps**:
1. **Install Git LFS**:
   ```bash
   git lfs install
   ```
2. **Track large files** (in `.gitattributes`):
   ```gitattributes
   *.psd filter=lfs diff=lfs merge=lfs -text
   *.mp4 filter=lfs diff=lfs merge=lfs -text
   ```
3. **Commit & push**:
   ```bash
   git add .gitattributes
   git commit -m "Track PSD/MP4 with LFS"
   git push
   ```
4. **Verify**:
   ```bash
   git lfs ls-files  # Lists LFS-tracked files
   ```

---
## **5. Export-Ignore (Exclude Files from Archives)**
**Scenario**: You generate `git archive` releases but want to exclude test files.  

### **Solution**: Use `export-ignore`.  

#### **Steps**:
1. **Edit `.gitattributes`**:
   ```gitattributes
   /tests/ export-ignore
   *.tmp export-ignore
   ```
2. **Test**:
   ```bash
   git archive --format=zip -o release.zip HEAD
   unzip -l release.zip  # Should exclude /tests/ and *.tmp
   ```

---
## **6. Filter Drivers (Pre-Process Files on Commit/Checkout)**
**Scenario**: You want to strip debug logs before committing.  

### **Solution**: Use a **clean/smudge filter**.  

#### **Steps**:
1. **Define filter in `.gitconfig`**:
   ```bash
   git config --global filter.clean_logs.clean "sed '/DEBUG/d'"
   ```
2. **Map it in `.gitattributes`**:
   ```gitattributes
   *.log filter=clean_logs
   ```
3. **Test**:
   ```bash
   echo "INFO: OK" > test.log
   echo "DEBUG: Remove me" >> test.log
   git add test.log
   git commit -m "Test filter"
   git show :test.log  # Should exclude DEBUG lines
   ```

---
## **Summary Table: Key Scenarios & Fixes**
| Scenario | Solution | `.gitattributes` Example |
|----------|----------|--------------------------|
| **Line endings** | `text=auto`, `eol=lf/crlf` | `*.sh eol=lf` |
| **Binary files** | `binary`, `-diff -merge` | `*.pdf binary` |
| **Custom diffs** | `diff=driver` | `*.java diff=java` |
| **Large files** | `filter=lfs` | `*.mp4 filter=lfs` |
| **Exclude from zip** | `export-ignore` | `/tests/ export-ignore` |
| **Pre-process files** | `filter=clean/smudge` | `*.log filter=clean_logs` |
