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