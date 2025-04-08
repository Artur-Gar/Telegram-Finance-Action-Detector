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

📁 Output: A multitude of daily archives of all Telegram posts/messages

---

### **2. Named Entity Recognition (NER) — Identifying Ticker Mentions**

We analyze the text content to:
- Detect **ticker mentions** using **spaCy’s NER**
- Count how often each ticker appears across messages
- Identify unique named entities and track their frequency

📁 Output: A dataset of messages with extracted named entities (potential ticker mentions)

<table>
  <tr>
    <td align="center">
      <img src="2%20NER/Most%20Mentioned%20Tickers.png" alt="Most Mentioned Tickers" width="800">
      <br>
      <em>Figure 1: Most frequently mentioned tickers in Telegram chats</em>
    </td>
    <td align="center">
      <img src="2%20NER/Ticker%20Mentions%20by%20Date%20and%20Chat.png" alt="Ticker Mentions Over Time" width="800">
      <br>
      <em>Figure 2: Ticker mentions over time and across Telegram chats</em>
    </td>
  </tr>
</table>

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

Telegram-Finance-Action-Detector/
│
├── 1 Parsing/                            # Telegram message collection
│   ├── configs/                          # Chat/channel configuration files
│   ├── data/                             # Parsed raw message data
│   ├── tg_news/                          # Telegram parsing logic (e.g., using Pyrogram)
│   │   └── pyrogram_parser_short.py
│   └── tg chanels features.xlsx          # Chat metadata/features
│
├── 2 NER/                                # Named Entity Recognition (ticker extraction)
│   ├── data/                             # Intermediate NER outputs
│   ├── nlp_modules/                      # spaCy-based entity extraction + matching
│   ├── Chats_statistics.ipynb            # Visual analysis of NER results
│   ├── Most Mentioned Tickers.png        # Figure 1: bar chart of top tickers
│   ├── Ticker Mentions by Date and Chat.png  # Figure 2: heatmap over time and chats
│   └── spacy_little_example.ipynb        # NER demo notebook
│
├── 3 Matching NER and Candles/           # Price anomaly matching
│   ├── data/                             # Ticker OHLCV (candlestick) data
│   └── Matching_candles_and_tickers.ipynb  # Logic for linking NER + price movements
│
├── 4 Custom Library for Call to Action Identification/  # LLM-based intent detection
│   ├── configs/                          # Prompt schema definitions
│   ├── ners_and_calls_modules/           # Main LLM logic (Kor + GigaChat)
│   ├── README.md                         # Library usage instructions
│   └── testing.ipynb                     # Example usage of final LLM detection
│
├── all_chats_and_channels.xlsx           # Full list of observed Telegram chats
└── README.md                             # Main project documentation (this file)


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
