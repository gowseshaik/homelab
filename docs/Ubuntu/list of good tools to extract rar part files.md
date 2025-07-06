<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
Here's a list of good tools to extract `.part*.rar` files on Ubuntu:

|**Tool**|**Command to Install**|**Supports Multi-Part RAR**|**Notes**|
|---|---|---|---|
|**unrar**|`sudo apt install unrar`|✅ Yes|Official but non-free binary|
|**unar**|`sudo apt install unar`|✅ Yes|Free and easier syntax|
|**7z (p7zip-full)**|`sudo apt install p7zip-full`|✅ Yes|Supports many formats, flexible|
|**rar**|`sudo apt install rar`|✅ Yes|Non-free, but official RAR tool|

> 🔧 **Recommended**: Use `unar` for ease or `unrar` if you're okay with non-free software.

Yes — **just run `7z x filename.part1.rar`**, and it will:

- ✅ **Automatically detect and extract all parts** (`filename.part2.rar`, `part3.rar`, etc.)
- ❗ All parts must be in the **same directory**
- 🚫 Do **not** run it on `part2.rar` or later — only `part1.rar` contains the header
### Example:
```bash
7z x myarchive.part1.rar
```

Will extract the full content from:
```
myarchive.part1.rar
myarchive.part2.rar
myarchive.part3.rar
...
```
