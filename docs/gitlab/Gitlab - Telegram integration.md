<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

- Create a Telegram bot with **BotFather**.
- Get your Telegram chat ID.
- Create a GitLab webhook that triggers on events.
- Build or use a middleware service that receives GitLab webhook and sends a message via Telegram bot API.

| Tool / Service | Purpose                                 | Notes                             |
| -------------- | --------------------------------------- | --------------------------------- |
| GitLab         | Source code management                  | Your existing GitLab instance     |
| Telegram Bot   | Send notifications                      | Create a bot via BotFather        |
| GitLab Webhook | Trigger Telegram notifications          | Configure webhook in GitLab repo  |
| Middleware     | Optional: relay webhook to Telegram API | Can be a simple script or service |
IF You're looking to configure **Telegram integration directly via GitLab’s built-in integration panel** (under **Settings → Integrations → Telegram**). 
Here's how to fill it out properly:

---
### ✅ 1. **Create a Telegram Bot**

- Open Telegram, search for `@BotFather`
- Run `/newbot` and follow prompts
- Copy the **bot token** → you'll use this in GitLab
---
### ✅ 2. **Get Your Chat ID or Channel ID**

- Add the bot to your Telegram group or channel
- Promote the bot as **Admin**
- To get the **channel ID**:
    - Use `https://api.telegram.org/bot<your_bot_token>/getUpdates`
    - Send a message to your channel after adding the bot
    - You'll get a response containing something like:
        ```
        "chat": { "id": -1001234567890, ... }
        ```
    - That `-1001234567890` is your **Channel Identifier**
---
### ✅ 3. **GitLab → Integrations → Telegram**

Fill in as below:

|Field|Value|
|---|---|
|**Active**|✅ Check it|
|**Hostname**|`https://api.telegram.org`|
|**Token**|Your Telegram Bot Token from BotFather|
|**Channel Identifier**|e.g. `-1001234567890`|
|**Message thread ID**|(Optional, for threads in forums/supergroups)|

---
### ✅ 4. Enable Events to Notify

Scroll down and check:
- Push events
- Merge request events
- Issue events  
    ... or any others you want.

Then **click "Save changes"**.
