```markdown
# 🚀 Binance Futures Trading Bot (Python CLI)

A modular **command-line trading bot** built in Python that executes real-time **Binance Futures trades** with proper validation, logging, and error handling.

---

## 📌 Overview

This project is a **CLI-based trading system** that allows users to place BUY/SELL orders on Binance Futures (Testnet). It is designed with a clean architecture separating validation, execution, and API interaction.

---

## ✨ Features

- ✅ Place **Market & Limit Orders**
- ✅ Supports **BUY (Long)** and **SELL (Short)**
- ✅ Binance Futures API Integration (Testnet)
- ✅ Real-time price fetching
- ✅ Input validation (symbol, quantity, order type)
- ✅ Minimum notional check (≥ 100 USDT)
- ✅ Logging system for debugging
- ✅ Error handling (API, network, validation)
- ✅ Time synchronization with Binance server

---

## 🏗️ Project Structure

```

trading_bot/
│
├── cli.py              # Entry point (CLI interface)
├── bot/
│   ├── client.py       # Binance API wrapper
│   ├── validators.py   # Input validation logic
│   ├── orders.py       # Order execution logic
│   └── logging_config.py
│__ project_summary.txt
├── requirements.txt
└── README.md




### ▶️ Run the bot

```bash
python -m cli --symbol ETHUSDT --side BUY --type MARKET --quantity 0.1
```

---

## 📥 Input Parameters

| Parameter    | Description               | Example |
| ------------ | ------------------------- | ------- |
| `--symbol`   | Trading pair              | ETHUSDT |
| `--side`     | BUY or SELL               | BUY     |
| `--type`     | MARKET or LIMIT           | MARKET  |
| `--quantity` | Amount to trade           | 0.1     |
| `--price`    | Required for LIMIT orders | 1900    |

---

## 📤 Example Output

### Before Order

```
ORDER REQUEST
Symbol: ETHUSDT
Side: BUY
Type: MARKET
Quantity: 0.1
```

### After Order

```
ORDER RESPONSE
Order ID: 8622648998
Status: NEW
Symbol: ETHUSDT
Side: BUY
Quantity: 0.100
```

---

## 🔄 Trading Logic

* 🟢 **BUY → Long Position** → Profit if price increases
* 🔴 **SELL → Short Position** → Profit if price decreases

### Closing Positions

* BUY → close with SELL
* SELL → close with BUY

---

## 🛡️ Validations Implemented

* ❌ Invalid symbol → rejected
* ❌ Quantity ≤ 0 → rejected
* ❌ Order value < 100 USDT → rejected
* ❌ API failures handled
* ❌ Time sync issues resolved


## 🔥 Future Improvements

* 📊 Position tracking & PnL calculation
* 🛑 Stop-loss / Take-profit
* 🔁 Retry mechanism for failed orders
* ⚙️ Dynamic precision & lot size handling
* 🔄 Auto quantity calculation


## 👨‍💻 Author

**Pavitra S V**
Computer Science Student | Backend & Web Development Enthusiast

```
```
