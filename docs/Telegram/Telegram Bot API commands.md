A concise list of **Telegram Bot API commands** (methods) you can use via `curl` or HTTP calls:

---
### ✅ Commonly Used Telegram Bot API Methods

|Method|Purpose|
|---|---|
|`getMe`|Get bot info (username, ID, etc.)|
|`getUpdates`|Poll new messages and events|
|`sendMessage`|Send text message to a chat|
|`sendPhoto`|Send image/photo|
|`sendDocument`|Send file (PDF, DOC, etc.)|
|`sendVideo`|Send video file|
|`sendAudio`|Send audio/music file|
|`sendVoice`|Send voice message|
|`sendMediaGroup`|Send multiple media (album)|
|`sendLocation`|Send GPS location|
|`sendChatAction`|Send "typing", "uploading", etc.|
|`forwardMessage`|Forward message from one chat to another|
|`copyMessage`|Copy message without linking|
|`editMessageText`|Edit existing message text|
|`deleteMessage`|Delete a message|

---
### 🔧 Chat & Group Management

|Method|Purpose|
|---|---|
|`getChat`|Get chat info|
|`getChatAdministrators`|List admins in a group|
|`getChatMember`|Get info of a user in a chat|
|`getChatMemberCount`|Get number of members|
|`leaveChat`|Bot leaves the chat|
|`kickChatMember`|Remove user from group|
|`banChatMember`|Ban a user|
|`unbanChatMember`|Unban a user|
|`restrictChatMember`|Restrict user permissions|
|`promoteChatMember`|Grant admin rights|
|`setChatPermissions`|Set default permissions for group|

---
### 💬 Forum & Topics (Supergroups with topics)

|Method|Purpose|
|---|---|
|`createForumTopic`|Create a new topic/thread|
|`editForumTopic`|Rename topic|
|`closeForumTopic`|Close the topic|
|`reopenForumTopic`|Reopen topic|
|`deleteForumTopic`|Delete topic|
|`unpinAllForumTopicMessages`|Unpin all messages in topic|
|`getForumTopicIconStickers`|Get available stickers for topic icons|

---
### 🔒 Webhook & Auth

|Method|Purpose|
|---|---|
|`setWebhook`|Set webhook URL|
|`deleteWebhook`|Remove webhook|
|`getWebhookInfo`|Check current webhook status|

---
### 🧪 Interactive Features

|Method|Purpose|
|---|---|
|`answerCallbackQuery`|Respond to inline button clicks|
|`sendPoll`|Create a poll|
|`stopPoll`|End a poll|
|`sendDice`|Send dice animation|
|`sendGame`|Send a game (via BotFather registration)|
To work with your **Telegram topic "gnatrading"**, you first need the **topic’s `message_thread_id`**, because Telegram uses this ID — not the name — for all API interactions with topics.

---
### ✅ Steps to Get `message_thread_id` for "gnatrading"

#### 🧪 1. Send a message to the "gnatrading" topic
- Use Telegram app.
- Post any message **into the "gnatrading" topic** (from your account or bot).

#### 🛰️ 2. Call `getUpdates` to capture the thread ID:

```bash
curl -s -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
```

> Replace `<YOUR_BOT_TOKEN>` with your actual token.

#### 🔍 3. Look for this block in the output:

```json
{
  "message": {
    "message_thread_id": 1234,
    "chat": {
      "id": -100xxxxxxxxxx,
      "type": "supergroup"
    },
    "text": "Test message in gnatrading"
  }
}
```

- `chat.id`: the **group ID**
    
- `message_thread_id`: the **ID of topic "gnatrading"**
    

You can use `jq` to filter easily:

```bash
curl -s -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates \
| jq '.result[].message | select(.message_thread_id != null) | {topic_id: .message_thread_id, text: .text}'
```

---
### 📩 Now send messages to "gnatrading" topic using this:

```bash
curl -s -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage \
-d chat_id=-100xxxxxxxxxx \
-d message_thread_id=1234 \
-d text="Hello GNATrading!"
```
