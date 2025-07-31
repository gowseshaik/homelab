To completely uninstall your current Node.js (v18.19.1) and prepare for installing a fresh Node.js v20+, follow the steps below based on how Node.js was installed.

## 🔍 Step 1: Check How Node.js Was Installed

Run:

```bash
which node
which npm
node -v
```

Typical outputs:

| Output Location        | Install Method             |
| ---------------------- | -------------------------- |
| `/usr/bin/node`        | Ubuntu APT                 |
| `/usr/local/bin/node`  | Manual or global binary    |
| `~/.nvm/versions/node` | NVM (Node Version Manager) |

## 🧹 Step 2: Uninstall Based on Install Method

### 🔸 A. If installed via **APT** (Ubuntu package manager):

```bash
sudo apt remove nodejs npm -y
sudo apt purge nodejs npm -y
sudo apt autoremove -y
```

Then check:

```bash
node -v
npm -v
```

They should return: `command not found`

### 🔸 B. If installed **manually or via curl (in /usr/local)**:

```bash
sudo rm -rf /usr/local/bin/node
sudo rm -rf /usr/local/bin/npm
sudo rm -rf /usr/local/lib/node_modules
```

### 🔸 C. If installed via **nvm (Node Version Manager)**:

```bash
nvm uninstall 18.19.1
nvm deactivate
nvm use system
```

Then:

```bash
nvm ls
```

Remove any extra versions if needed.

## ✅ Step 3: Clean Check

```bash
which node
node -v
```

You should now see either **nothing** or `command not found`.
