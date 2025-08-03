<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

Ubuntu 20.04 contains a version of Node.js in its default repositories that can be used to provide a consistent experience across multiple systems. At the time of writing, the version in the repositories is 10.19. This will not be the latest version, but it should be stable and sufficient for quick experimentation with the language.

**Warning:** the version of Node.js included with Ubuntu 20.04, version 10.19, is now unsupported and unmaintained. You should not use this version in production, and should refer to one of the other sections in this tutorial to install a more recent version of Node.

To get this version, you can use the `apt` package manager. Refresh your local package index first:

```
sudo apt update
```

Then install Node.js:

```
sudo apt install nodejs
```

Check that the install was successful by querying `node` for its version number:

```
node -v
```

```
Outputv10.19.0
```

If the package in the repositories suits your needs, this is all you need to do to get set up with Node.js. In most cases, you’ll also want to also install `npm`, the Node.js package manager. You can do this by installing the `npm` package with `apt`:

```
sudo apt install npm
```

This allows you to install modules and packages to use with Node.js.

At this point, you have successfully installed Node.js and `npm` using `apt` and the default Ubuntu software repositories. The next section will show how to use an alternate repository to install different versions of Node.js.

# Clean steps to install **Node.js v20 LTS** on Ubuntu:

## ✅ Method 1: Using **NodeSource (APT-based, recommended)**

### 🔧 Step-by-step:

```bash
# 1. Update packages
sudo apt update

# 2. Add Node.js 20.x repo
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# 3. Install Node.js
sudo apt install -y nodejs

# 4. Confirm installation
node -v   # should show v20.x
npm -v    # should show latest npm
```

---

## ✅ Method 2: Using **NVM (Node Version Manager)**

> Use this if you want to switch between versions easily.

### 🔧 Step-by-step:

```bash
# 1. Install NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# 2. Load nvm immediately (or restart terminal)
export NVM_DIR="$HOME/.nvm"
source "$NVM_DIR/nvm.sh"

# 3. Install Node.js 20
nvm install 20

# 4. Set it as default
nvm use 20
nvm alias default 20

# 5. Confirm
node -v
npm -v


# Download and install nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# in lieu of restarting the shell
\. "$HOME/.nvm/nvm.sh"

# Download and install Node.js:
nvm install 22

# Verify the Node.js version:
node -v # Should print "v22.17.1".
nvm current # Should print "v22.17.1".

# Verify npm version:
npm -v # Should print "10.9.2".

```

---

### 💡 Which to choose?

|Method|Use When|
|---|---|
|**APT (Method 1)**|You want system-wide setup|
|**NVM (Method 2)**|You want per-user versions / easier upgrades|

---

Let me know if you're on a different distro or need a minimal install (no npm).

# Claude Code overview
https://docs.anthropic.com/en/docs/claude-code/overview

Learn about Claude Code, Anthropic’s agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before.

https://docs.anthropic.com/en/docs/claude-code/overview#get-started-in-30-seconds

Get started in 30 seconds

Prerequisites: [Node.js 18 or newer](https://nodejs.org/en/download/)

```bash
# Install Claude Code
sudo npm install -g @anthropic-ai/claude-code
sudo npm i -g @anthropic-ai/claude-code

# Navigate to your project
cd your-awesome-project

# Start coding with Claude
claude
```

That’s it! You’re ready to start coding with Claude. [Continue with Quickstart (5 mins) →](https://docs.anthropic.com/en/docs/claude-code/quickstart)

(Got specific setup needs or hit issues? See [advanced setup](https://docs.anthropic.com/en/docs/claude-code/setup) or [troubleshooting](https://docs.anthropic.com/en/docs/claude-code/troubleshooting).)