# E-Commerce Chatbot


## Setup Instructions

1. **Clone the Repository**: 
    ```
    git clone https://github.com/your_username/e-commerce-chatbot.git
    ```

2. **Install Dependencies**: 
    ```
    cd e-commerce-chatbot
    pip install -r requirements.txt
    ```

3. **Environment Variables**:
    - Create a `.env` file in the project root directory.
    - Add your OpenAI API key to the `.env` file:
        ```
        OPENAI_API_KEY=your_openai_api_key
        ```

4. **Run the Application**:
    ```
    streamlit run chatbot.py
    ```



## Usage Instructions

1. **Ask a Query**:
    - Type your question in the text input field labeled "Your question".
    - Click the "Send" button to submit your query to the chatbot.

2. **Interact with the Chatbot**:
    - The chatbot will respond with relevant information extracted from provided FAQ documents and sample product listings.

3. **View Chat History**:
    - The conversation history is displayed below the input field.
