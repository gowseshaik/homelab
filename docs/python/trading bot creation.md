Build a trading bot that receives updates and runs in Docker.

---
### 🔧 First, choose your setup:

1. **Exchange source**:  
    Do you want to fetch updates from:
    - Binance?
    - Coinbase?
    - NSE/BSE (India)? -Yes
    - Yahoo Finance?
    - Any other?

2. **Updates type**:
    - Price changes?
    - Volume? -> yes
    - Order book?
    - Trade signals?

3. **Notification method**:
    - Console logs?
    - Telegram? - Yes
    - Email?
    - Dashboard?

4. **Bot behavior (optional)**:
    - Just monitor?
    - Simulated trading?
    - Real trading with API keys?

---
### ✅ Basic Skeleton Plan

#### 1. **Project Structure**
```
trading-bot/
├── bot.py
├── requirements.txt
├── Dockerfile
└── config.json  (optional)
```

#### 2. **Python example (binance client skeleton)**
Want me to start with a simple Binance (or Yahoo) live price poller + Telegram notifier?  
Once confirmed, I’ll give you:

- Clean Python code (polling + Telegram send)
- `requirements.txt`
- `Dockerfile`
- `docker run` command

Just tell me:
- Your preferred data source (e.g., Binance, Yahoo)
- Whether to send alerts via Telegram or just print in logs