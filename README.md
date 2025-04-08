# 📊 Detecting Calls to Action in Telegram Finance Channels and Analyzing Their Market Impact

## 🧩 Problem Statement

We aim to analyze messages in major financial Telegram groups and chats to detect **calls to action** related to **buying or selling securities**, and assess whether such messages **lead to significant price movements**.

---

## 🛠️ Project Pipeline Overview

The full task is divided into **four stages**:

---

### **1. Parsing Telegram Chats and Channels**

We collect raw data by:
- Extracting messages from relevant Telegram groups and channels using their **usernames or chat IDs**
- Saving all messages **daily** into `.xlsx` files over the observation period

📁 Output: A daily archive of all Telegram posts/messages

---

### **2. Named Entity Recognition (NER) — Identifying Ticker Mentions**

We analyze the text content to:
- Detect **ticker mentions** using **spaCy’s NER**
- Count how often each ticker appears across messages
- Identify unique named entities and track their frequency

📁 Output: A dataset of messages with extracted named entities (potential ticker mentions)

---

### **3. Price Anomaly Filtering and Matching**

We match message activity to actual market behavior:
- Filter ticker price data by **daily candlesticks**
- Detect **price anomalies** (e.g. spikes in high/low relative to the previous close)
- Match the anomalies to **ticker mentions on the same day or the day before**
- Extract only the messages that mention those tickers

📁 Output: Filtered dataset of potentially impactful messages

---

### **4. Final Analysis: LLM-based Detection of Calls to Action**

We use a custom-built library powered by an **LLM (GigaChat)** to determine:
- Which messages **mention tickers**
- Whether those messages contain a **call to action** (e.g., buy/sell signals)

📦 Custom module: `ners_and_calls_modules`  
📄 Detailed usage instructions inside that module’s README

---

## 📁 Folder Structure

ddddddddddddddddddddddd
ddddddddddddddddddddddd

---

## ✅ Final Goal

A structured dataset containing:
- The message text
- The detected ticker (via NER)
- Whether a **call to action** was present (via LLM)
- Whether a **price anomaly** occurred (via market data)

This pipeline enables compliance teams, market analysts, or research groups to:
- **Track influence** of Telegram chatter on stock price movements
- **Monitor behavioral signals** from unstructured social media content


---

## 🧠 Need Help?

Start by reading the [ners_and_calls_modules/README.md](ners_and_calls_modules/README.md)  
Or reach out to the project team if you'd like to integrate new data sources or models.

---

## 📝 Author

**Artur Garipov**  
[LinkedIn](https://www.linkedin.com/in/artur-garipov-36037a319) | [GitHub](https://github.com/Artur-Gar)