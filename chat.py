from dotenv import load_dotenv
import streamlit as st
import os
import openai

st.set_page_config(page_title="Chatbot Interface")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = [{'author': "system", 'text': "Ask a Query"}]

def add_message(author, text):
    if text:  # Ensure we don't add empty messages
        st.session_state['conversation_history'].append({'author': author, 'text': text})

def dispaly_answers():
    for index, message in enumerate(st.session_state['conversation_history']):
        if message['author'] == "User":
            st.text_area("", value=message['text'], height=75, key=f"user_{index}", disabled=True)
        else:  # Chatbot's messages
            st.text_area("", value=message['text'], height=100, key=f"bot_{index}", disabled=True)

faqs = '''
General Questions
 1. What is the return policy?
 a. Our return policy lasts 30 days. If 30 days have gone by since your purchase, unfortunately, we can’t offer you a refund or exchange. Items must be returned in their original condition.
 
 2. Howcan I track my order?
 a. You can track your order by using the tracking number provided in your shipping confirmation email or by logging into your account on our website.
 
 3. What payment methods are accepted?
 a. Weaccept Visa, MasterCard, American Express, Discover, PayPal, and store credit.
 
 4. CanI change or cancel my order?
 a. Orders can be changed or cancelled within 1 hour of placement. After this period, we cannot guarantee changes or cancellations.
 
 5. Do you offer international shipping?
 a. Yes, we ship internationally. Shipping charges and delivery times vary based on the destination. Additional taxes and duties may apply.
 '''
 
prod_spec = '''

 Product Specific
 6. Is there a warranty on electronic products?
 a. Yes, most electronic products come with a one-year manufacturer's warranty covering defects in material and workmanship.
 
 7. CanI return a clothing item if it doesn't fit?
 a. Yes, clothing items can be returned if they don't fit. Please ensure the items are unworn and have the original tags attached.
 
 8. What should I do if I receive a damaged item?
 a. If you receive a damaged item, please contact customer service immediately with photographic evidence of the damage.
 
 9. HowdoIuse a promo code?
 a. Enter your promo code at checkout in the designated box. Only one promo code can be used per order.
 
 10. Are gift cards refundable?
 a. No, gift cards are not refundable or redeemable for cash, except where required by law.
 
'''

sample_prod = '''

 1. Echo Dot (4th Gen)
    ● Category: Smart Home
    ● Price: $49.99
    ● Description: The latest Echo Dot provides improved sound quality for music and voice assistance with Alexa. Compact design to fit perfectly into small spaces.
    ● Warranty: 1 year
    ● Customer Reviews: 4.5/5 stars, based on 2,000 reviews.
 2. Levi's Men's 501 Original Fit Jeans
    ● Category: Men’s Clothing
    ● Price: $59.99
    ● Description: Classic 501 jeans with button fly. 100% Cotton, straight leg, available in multiple colors and sizes. Machine washable.
    ● Return Policy: 30-day returns with original tags.
    ● Customer Reviews: 4.7/5 stars, based on 3,500 reviews.
 3. Samsonite Winfield 2 Hardside Luggage
    ● Category: Travel Gear
    ● Price: $229.00
    ● Description: Durable polycarbonate luggage with spinner wheels, TSA-compatible lock, and adjustable handle. Lightweight design for easy travel.
    ● Warranty: 10-year limited warranty
    ● Customer Reviews: 4.6/5 stars, based on 1,200 reviews.
 4. Sony WH-1000XM4 Wireless Noise-Canceling Headphones
    ● Category: Electronics
    ● Price: $349.99
    ● Description: Industry-leading noise cancellation, up to 30 hours of battery life, touch sensor controls, and high-quality audio experience.
    ● Warranty: 1 year
    ● Customer Reviews: 4.8/5 stars, based on 4,500 reviews.
 5. Instant Pot Duo 7-in-1 Electric Pressure Cooker
    ● Category: Kitchen Appliances
    ● Price: $89.99
    ● Description: Multi-functional cooker: pressure cooker, slow cooker, rice cooker, steamer, sauté, yogurt maker, and warmer. Easy to use and clean.
    ● Warranty: 1 year
    ● Customer Reviews: 4.7/5 stars, based on 9,000 reviews.
    
'''
st.header("E-commerce Chatbot")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your question:", key="chat_input")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    print('submitted')
    add_message("User", user_input)
    
    qa_prompt = user_input + f"""\n Below are the references to answer the question above. 
        Go through the references and accurately identify the related FAQ or product detail from 
        the reference that the above question is related to, and answer accordingly(just return the answer only).\n\n"
        {faqs} + "\n\n" + {prod_spec} + "\n\n" + {sample_prod}"""

    classifiers = ['Place Order', 'Track Order', 'Return Order']
    classifier_prompt = user_input + f"""\n You are a classifier, understand the query and return 
    the suitable option from the provided list of choices. Just return the choice without extra text\n\n"
    Classifers: {classifiers} + "\n\n"
    Example: "For the query: Order the new cargo track pant. The response is: Place order \n\n"""

    prompt_with_context =  qa_prompt


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a knowledgeable assistant."},
                  {"role": "user", "content": prompt_with_context}],
        temperature=0.7,
        max_tokens=150,
    )

    if response and response.choices and len(response.choices) > 0:
        chat_response = response.choices[0].message['content']  # Correctly access the content of the message
        add_message("Chatbot", chat_response.strip())
    else:
        add_message("Chatbot", "Sorry, I couldn't generate a response.")

dispaly_answers()
