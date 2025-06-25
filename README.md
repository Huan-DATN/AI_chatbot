# AI Chatbot Service

This service provides an AI-powered chatbot with two main capabilities:

1. FAQ answering using vector search and LLM
2. Database querying using SQL generation

## Architecture

The system uses a graph-based architecture with LangGraph to process user questions:

1. **Intent Detection**: Determines if the question is a FAQ or requires database access
2. **FAQ Processing**:
   - Retrieves relevant FAQ entries using vector similarity search
   - Generates answers based on retrieved FAQ entries
3. **SQL Processing**:
   - Generates SQL queries based on the user's question
   - Validates and executes the queries
   - Generates a natural language answer from the query results

## Setup

1. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-2.0-flash
   DB_URL=postgresql+psycopg2://username:password@host:port/database
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   REDIS_USERNAME=default
   REDIS_PASSWORD=password
   ```

## Running the Service

Start the service with:

```
python run.py
```

The service will be available at http://localhost:5000.

## API Endpoints

### Chatbot

- **POST /api/chat**
  - Request body: `{"message": "your question", "session_id": "optional_session_id"}`
  - Response: `{"response": {"answer": "bot's answer", "session_id": "session_id"}}`

### FAQ Management

- **GET /api/faq/**

  - Get all FAQs
  - Response: List of FAQ items

- **POST /api/faq/**

  - Add a new FAQ
  - Request body: `{"question": "FAQ question", "answer": "FAQ answer", "category": "optional category", "tags": ["optional", "tags"]}`
  - Response: Added FAQ item

- **GET /api/faq/search?q=search_query**
  - Search FAQs by query
  - Response: List of matching FAQ items with similarity scores
