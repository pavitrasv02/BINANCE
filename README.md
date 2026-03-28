# Binance Futures Testnet Trading Bot

## Overview

This project is a production-style Python CLI trading bot that interacts with the Binance Futures Testnet (USDT-M). It allows users to place MARKET and LIMIT orders with proper validation, logging, and error handling.

This project demonstrates a production-style trading bot with modular architecture, structured logging, input validation, and robust error handling to simulate real-world trading system design.

---

## Features

* Place MARKET and LIMIT orders (BUY/SELL)
* Command-line interface using argparse
* Input validation with clear error messages
* Structured logging of API requests, responses, and errors
* Environment variable support for API credentials
* Confirmation prompt before order execution
* Clean and readable CLI output

---

## Project Structure

trading_bot/
cli.py
bot/
client.py
orders.py
validators.py
logging_config.py
requirements.txt
logs/
README.md

---

## Setup Instructions

### 1. Clone the repository

git clone <your-repo-link>
cd trading_bot


## Binance Testnet Setup


1. Create account and generate API keys

---

## Set API Credentials

### Option 1: Environment variables 

Windows:
set BINANCE_API_KEY=your_api_key
set BINANCE_API_SECRET=your_api_secret


---

## How to Run

### MARKET Order Example

python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

### LIMIT Order Example

python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000

---

## Output Example

========== ORDER REQUEST ==========
Symbol     : BTCUSDT
Side       : BUY
Type       : MARKET
Quantity   : 0.001
==================

Do you want to place this order? (yes/no): yes

========== ORDER RESPONSE ==========
Order ID     : 12345678
Status       : NEW
Executed Qty : 0.001
Avg Price    : N/A
==================

✓ ORDER EXECUTED SUCCESSFULLY

---

## Logs

All logs are stored in:
logs/app.log

Includes:

* Order requests
* API responses
* Errors

---

## Assumptions

* Only USDT trading pairs are supported
* LIMIT orders require price
* Binance Futures Testnet is used (no real funds involved)

---
