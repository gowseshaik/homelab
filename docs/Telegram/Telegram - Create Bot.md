Babu Sk, [8/3/2025 12:45 PM]
/newbot

BotFather, [8/3/2025 12:45 PM]
Alright, a new bot. How are we going to call it? Please choose a name for your bot.

Babu Sk, [8/3/2025 12:47 PM]
gnatrading

BotFather, [8/3/2025 12:47 PM]
Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.

Babu Sk, [8/3/2025 12:47 PM]
gnatradebot

BotFather, [8/3/2025 12:47 PM]
Done! Congratulations on your new bot. You will find it at t.me/gnatradebot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
834352342336:AAH2fhJoE_ZNoprqE234341nTmDwM-ovyHxdFAERazwsVVQ0
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api

You're looking to configure **Telegram integration directly via GitLab’s built-in integration panel** (under **Settings → Integrations → Telegram**). Here's how to fill it out properly:

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

| Field                  | Value                                         |
| ---------------------- | --------------------------------------------- |
| **Active**             | ✅ Check it                                    |
| **Hostname**           | `https://api.telegram.org`                    |
| **Token**              | Your Telegram Bot Token from BotFather        |
| **Channel Identifier** | e.g. `-1001234567890`                         |
| **Message thread ID**  | (Optional, for threads in forums/supergroups) |

---

### ✅ 4. Enable Events to Notify

Scroll down and check:

- Push events
- Merge request events
- Issue events  
    ... or any others you want.

Then **click "Save changes"**.
