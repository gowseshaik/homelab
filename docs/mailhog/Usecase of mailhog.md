<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
No, **MailHog does not send emails to real recipients**.

It acts as a **fake SMTP server** that **captures emails locally** for testing and debugging.

You can:
- Send emails _to_ MailHog from your app
- View those emails in MailHog’s web UI
- Inspect content, headers, attachments
- Resend emails _within_ MailHog (to test again internally)

But MailHog **won’t deliver emails to external addresses**. It’s only for local/dev use.

If you want to send real emails, you must configure your app to use a real SMTP service (e.g., Gmail SMTP, SendGrid, AWS SES).

