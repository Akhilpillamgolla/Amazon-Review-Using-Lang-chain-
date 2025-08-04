#  Amazon Product Analysis with LLM

This project uses Large Language Models (LLMs) to analyse customer reviews and order data stored as text. It extracts insights such as product feedback, feature highlights, and order statistics.

---

##  Tasks & Outputs

### 1. Summarise Positive Feedback
**Input**: Text reviews  
**Task**: Summarize positive sentiment  
**Output**:  
"Customers love the product `apple` for its durability, sleek design, and excellent customer support. Many praised its ease of use and value for money."

---

### 2. Identify Greatest Features of Product `apple`
**Task**: Extract top features from positive reviews  
**Output**:
- Long battery life  
- Lightweight and portable  
- Intuitive user interface  
- Fast performance

---

### 3. Total Number of Orders in 2024
**Input**: Order data in text format  
**Task**: Count entries with year = 2024  
**Output**:  
"Total orders: 28"

---

### 4. Total Number of Negative Reviews for Product `apple`
**Task**: Filter reviews by sentiment and product ID  
**Output**:  
"Product `apple` received 4 negative reviews."

---

##  Structure
- `data/` – Raw text reviews and order logs  
- `scripts/` – LLM-based analysis scripts  
- `outputs/` – Generated summaries and insights

---

##  Getting Started
Clone the repo and run the analysis scripts to extract insights from your text data.

