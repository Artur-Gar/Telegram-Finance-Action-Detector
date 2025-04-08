# 🧠 `nlp_modules_2`

ners_and_calls_modules - A lightweight NLP library for Identifying **Calls to action in posts/messages** as part of a **Compliance workflow**.

It performs two core tasks:
1. **Identifying tickers** mentioned in a post
2. **Detecting calls to action** related to buying or selling those tickers

---

## 🔍 Task 1 — Ticker Identification

We use Named Entity Recognition (NER) + fuzzy matching to link entities to financial instruments.

### 🧩 Process:
- Uses **spaCy** to extract **named entities** (NERs) from a text.
- Matches each entity against a **reference table** of company names and tickers.
- For each **unique entity**, selects the ticker with the **highest similarity score**.
- Filters matches by a **confidence threshold**.

### 📤 Output:
A DataFrame with 3 columns:

| Column  | Description                                  |
|---------|----------------------------------------------|
| `text`  | The original message text                    |
| `NER`   | Named entity extracted from the text         |
| `ticker`| Most likely associated ticker                |

> Returned by the function: `find_and_filter_NERS(...)`

---

## 📣 Task 2 — Call-to-Action Detection (`find_call/`)

This module uses a Language Model (LLM) to determine whether a message includes a **call to action** regarding the mentioned security.

### ⚙️ How it works:
- Builds a **prompt schema** using the [`kor`](https://github.com/eyurtsev/kor) library.
- Customizes the **default prompt** (originally in English) to fit the task.
- Injects message `text`, `NER`, and `ticker` into the prompt.
- Sends the prompt to the LLM using Kor’s **chain** interface.
- Receives a binary response: `1` (call to action present) or `0` (none).

### ➕ Adds a 4th column to the DataFrame:

| Column  | Description                                   |
|---------|-----------------------------------------------|
| `call`  | Binary flag indicating presence of a call to action |

---

## 🚀 Usage

You only need to use **one function**:

```python
from your_module import get_ners_and_calls

df = get_ners_and_calls(
    text="your message here",
    filter_value=0.8  # confidence threshold for ticker matching (0–1)
)
