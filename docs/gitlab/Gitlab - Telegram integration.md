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
    - Chat ID or Topic ID Correctness : Confirm the `chat_id` or `message_thread_id` (for topics) is **valid and matches** the bot's chat.
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

---
### ✅ Step-by-step Root Cause Diagnosis (First Principles)

|Step|Check|One-liner Explanation|
|---|---|---|
|1|**Bot Token Validity**|Ensure the Telegram bot token is **correct**, not expired or revoked.|
|2|**Chat ID or Topic ID Correctness**|Confirm the `chat_id` or `message_thread_id` (for topics) is **valid and matches** the bot's chat.|
|3|**Bot Added to Group/Channel**|Make sure the bot is **added to the group/channel** and has **admin rights** to send messages.|
|4|**Bot Privacy Mode**|If group is a supergroup and Privacy Mode is ON, **disable it** via [BotFather > /setprivacy].|
|5|**Test Message API Call**|Manually call Telegram API to check if message is sent with correct params (use curl).|
|6|**Outbound Connectivity**|GitLab runner/server must have **internet access** to connect to Telegram API.|
|7|**Correct Endpoint URL**|Ensure GitLab webhook is posting to `https://api.telegram.org/bot<token>/sendMessage` and not mistyped.|
|8|**GitLab Integration Format**|Make sure you’re using **supported payload format** GitLab expects (especially when using topics).|

---
### 🧪 Test with `curl` (manual check for Telegram API):

```bash
curl -s -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage \
-d chat_id=<CHAT_ID> \
-d text="Test from curl"
```

> Replace `<YOUR_BOT_TOKEN>` and `<CHAT_ID>` with actual values.

- ✅ If this works: your bot/token/chat ID is **fine**.
- ❌ If this fails: fix based on Telegram response message.

---
### 🔁 Handling Topics in Supergroups

If you are using **topics**, you must provide both:

- `chat_id` (group ID with `-100...`)
- `message_thread_id` (topic ID)

```bash
curl -s -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage \
-d chat_id=-1001234567890 \
-d message_thread_id=1234 \
-d text="Test for topic"


      curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument" \
        -F chat_id=${TELEGRAM_CHAT_ID} \
        -F message_thread_id=${TELEGRAM_THREAD_ID} \
        -F document=@${CSV_FILE} \
        -F caption="📊 ${CI_PROJECT_NAME} Report - $(date '+%Y-%m-%d %H:%M')
        
        $(cat $REPORT_FILE)" \
        -F parse_mode=Markdown
```

> `message_thread_id` must be valid (get it via Telegram client or API).

---
### 🔧 Final Checklist for GitLab Integration (No Bias)

|Item|Expected Value|
|---|---|
|Bot token|Starts with `bot` and is **correct**|
|Chat ID|Correct numeric ID, for groups starts with `-100`|
|Thread ID (if topic)|Must be a valid `message_thread_id`|
|Bot in group|Yes, with send message rights|
|GitLab server outbound access|Can access `api.telegram.org`|
|Proxy/Firewall|No blocking Telegram API|
|GitLab CI/CD or Integration config|JSON format is **valid**|
|Test via curl|Should work from same GitLab host|

---

If you're stuck, paste:

- Your bot's token structure (only the format, not the real token)
- Chat ID and topic ID you're using
- Exact curl or GitLab webhook output

I'll help you debug deeper.


Telegram **does not currently provide an official API endpoint** to directly **list all topic IDs (forum threads)** from a group chat.

However, here’s the **only working method**:

---

### ✅ Step-by-Step Method (First Principles Based)

#### ✅ 1. Use `getUpdates` to capture topic IDs when messages are posted in those threads:

```bash
curl -s -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
```

> Replace `<YOUR_BOT_TOKEN>` with your actual bot token.

Then **look inside the JSON response** for:

```json
"message": {
  "message_thread_id": 1234,
  "chat": {
    "id": -100xxxxxxxxxx,
    "type": "supergroup"
  },
  ...
}
```

This shows the `message_thread_id` for the topic where the message was posted.

---

### 🧠 First: Telegram sends topic/thread metadata **only when messages** are posted in those topics **and the bot is a member**.

---
### 🔁 2. Alternative: Use `getForumTopicIconStickers` (limited)

If you're using **custom topic icons**, you might get topic-related sticker sets but not thread IDs.

```bash
curl -s -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getForumTopicIconStickers
```

> This only helps if you’re customizing icons — still **no topic IDs returned**.

---
### 🧪 Practical Trick (Until Telegram Adds API)

- Post a message in each topic manually or via bot.
- Call `getUpdates`.
- Extract all `message_thread_id` values.

---
### 🧰 Tip: Use jq to filter topic IDs

```bash
curl -s -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates \
| jq '.result[].message | select(.message_thread_id != null) | {topic: .message_thread_id, text: .text}'
```

---

Let me know if you want a small Python/Golang tool to scrape all topic IDs automatically via polling.