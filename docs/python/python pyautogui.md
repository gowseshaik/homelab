<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
```
You're hitting the **PEP 668** protection — Ubuntu is blocking system-wide `pip install` to avoid breaking Python.
```

```
python3 -m venv ~/pyauto-env
source ~/pyauto-env/bin/activate
pip install pyautogui

python3 -m venv pyauto-env
source ./pyauto-env/bin/activate
pip install pyautogui
```

```
import pyautogui
import time

# Give time to switch to desired app
time.sleep(3)

# Move to specific screen location and click (adjust x, y)
pyautogui.moveTo(500, 400)
pyautogui.click()

# Wait a bit
time.sleep(1)

# Close window (Alt+F4 for Windows/Linux)
pyautogui.hotkey('alt', 'f4')


python your_script.py
```

To run your PyAutoGUI script as a **Windows background package**, follow these steps:

---

### ✅ 1. Freeze the script as a standalone `.exe`

Install `pyinstaller`:

```bash
pip install pyinstaller
```

Create the `.exe`:

```bash
pyinstaller --noconsole --onefile demo.py
```

- `--noconsole`: hides terminal window (runs silently in background)
    
- `--onefile`: packs everything into a single `.exe`
    
- Output will be in `dist/demo.exe`
    

---

### ✅ 2. Auto-run in background (optional)

To run at startup silently:

- Copy `demo.exe` to:
    
    ```plaintext
    C:\Users\<YourUsername>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
    ```
    

---

### ✅ 3. Run minimized or background-safe (avoid popups)

Update your `demo.py` to avoid mouse jumps while idle:

```python
import pyautogui
import time

pyautogui.FAILSAFE = False  # prevent crash on screen corner
time.sleep(2)  # time to move mouse away if needed

pyautogui.moveTo(500, 500)
pyautogui.click()
pyautogui.hotkey('alt', 'f4')
```

---

Let me know if you want to:

- Add a tray icon to stop it
    
- Auto-close specific app by name
    
- Make a config file for coordinates