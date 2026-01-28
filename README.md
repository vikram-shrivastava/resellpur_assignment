# ResellPur Assignment — AI-Powered Marketplace Assistant 🤖🛒

An AI-powered assistant for a second-hand marketplace that uses LLMs + simple agent-based logic to help both buyers and sellers make smarter decisions during buying/selling conversations.

This project focuses on building practical AI features that can be integrated into a resale marketplace platform.

---

## ✨ Features Implemented

### 1️⃣ Price Suggestion (Negotiation Support)
Helps users get a fair price range for a product based on details like:
- Category
- Brand
- Condition
- Age (in months)
- Asking price
- Location

### 2️⃣ Chat Moderation
Detects and blocks invalid or unsafe messages, such as:
- Phone numbers
- Sensitive information
- Policy-violating messages (basic moderation)

---

## ⚙️ Setup Instructions (Run Locally)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/vikram-shrivastava/resellpur_assignment.git
cd resellpur_assignment
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Configure Environment Variables

Create a `.env` file in the root directory with the following content:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 6️⃣ Run the Server

```bash
python main.py
```

🚀 **Server will start on:** `http://localhost:8000`

---

## 🧪 API Testing

### ✅ 1) Price Suggestion API (`/negotiate`)

**Endpoint:**
```
POST http://localhost:8000/negotiate
```

**Request Body:**
```json
{
  "id": "1",
  "title": "iPhone",
  "category": "Mobile",
  "brand": "Apple",
  "condition": "Good",
  "age_months": "24",
  "asking_price": "35000",
  "location": "Mumbai"
}
```

**Response:**
```json
{
  "fair_price_range": "25000-34000",
  "reasoning": "The Price of iPhone of 24 months old with this model has a price range between this in the second hand market",
  "is_fraud":false
}
```

---

### ✅ 2) Chat Moderation API (`/moderate`)

**Endpoint:**
```
POST http://localhost:8000/moderate
```

**Request Body:**
```json
{
  "incoming_message": "My mobile number is 9876543210"
}
```

**Response:**
```json
{
  "status": "Invalid message",
  "reason": "The phone number found in the message"
}
```

---

## 📌 Notes

- Make sure Python 3.7+ is installed on your system
- Keep the virtual environment activated while running the project
- Ensure you have valid API keys for GROQ and TAVILY services
- The `.env` file should never be committed to the repository

---

## 🛠️ Tech Stack

- **Python** - Core programming language
- **FastAPI** - Web framework for building APIs
- **LLM Integration** - For intelligent price suggestions and chat moderation
- **GROQ API** - LLM service provider
- **TAVILY API** - Search and data retrieval

---

## 📝 License

This project is part of an assignment and is available for educational purposes.

---

## 👨‍💻 Author

**Vikram Shrivastava**

GitHub: [@vikram-shrivastava](https://github.com/vikram-shrivastava)