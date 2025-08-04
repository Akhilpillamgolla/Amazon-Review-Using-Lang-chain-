import streamlit as st
import re
import os
from datetime import datetime
from dateutil import parser as date_parser
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = api_key
llm = ChatOpenAI(temperature=0.3)


st.title(" Amazon Phone Review Analyzer")
st.write("Upload a `.txt` file with product reviews and order data.")

uploaded_file = st.file_uploader("Choose a .txt file", type="txt")

if uploaded_file:
    raw_data = uploaded_file.read().decode("utf-8", errors="replace")
    entries = re.split(r"\n\s*\n", raw_data.strip())  

    valid_entries = []
    invalid_entries = []

    for i, entry in enumerate(entries, start=1):
        issues = []
        product_id_match = re.search(r"product_id:\s*(\w+)", entry, re.IGNORECASE)
        review_text_match = re.search(r"review_text:\s*(.+)", entry, re.IGNORECASE)
        order_date_match = re.search(r"order_date:\s*(\d{4}-\d{2}-\d{2})", entry)
        rating_match = re.search(r"rating:\s*(\d+)", entry)

        if not product_id_match:
            issues.append("Missing or malformed product_id")
        if not review_text_match:
            issues.append("Missing or malformed review_text")
        if not order_date_match:
            issues.append("Missing or malformed order_date")

        try:
            order_date = date_parser.parse(order_date_match.group(1)) if order_date_match else None
        except Exception:
            issues.append("Invalid date format")

        if issues:
            invalid_entries.append({
                "entry_number": i,
                "entry": entry,
                "issues": issues
            })
        else:
            valid_entries.append({
                "product_id": product_id_match.group(1).lower(),
                "review_text": review_text_match.group(1),
                "order_date": order_date,
                "rating": int(rating_match.group(1)) if rating_match else None
            })

    # choose a product ID and year
    selected_product_id = st.text_input(" Enter a Product ID to analyze", value="apple").lower()
    selected_year = st.number_input(" Enter a Year to count orders", min_value=2000, max_value=2100, value=2025)

    # Filter for selected product
    product_reviews = [d for d in valid_entries if d["product_id"] == selected_product_id]

    # Sentiment classification using LLM
    sentiment_prompt = PromptTemplate(
        input_variables=["review"],
        template="Classify the sentiment of this product review as Positive or Negative:\n\n{review}"
    )
    sentiment_chain = LLMChain(llm=llm, prompt=sentiment_prompt)

    positive_reviews = []
    negative_reviews = []

    for r in product_reviews:
        try:
            sentiment = sentiment_chain.run(review=r["review_text"])
            if "Positive" in sentiment:
                positive_reviews.append(r)
            elif "Negative" in sentiment:
                negative_reviews.append(r)
        except Exception as e:
            st.warning(f" LLM error on review: {r['review_text'][:50]}... — {str(e)}")

    # Summarize multiple positive reviews
    if positive_reviews:
        combined_reviews = " ".join([r["review_text"] for r in positive_reviews[:3]])
        summary_prompt = PromptTemplate(
            input_variables=["review"],
            template="Summarize the following positive product reviews and highlight their greatest features:\n\n{review}"
        )
        summary_chain = LLMChain(llm=llm, prompt=summary_prompt)
        try:
            summary = summary_chain.run(review=combined_reviews)
        except Exception as e:
            summary = f" Error generating summary: {str(e)}"
    else:
        summary = f"No positive reviews found for product '{selected_product_id}'."

    # Total orders in selected year
    orders_in_year = [d for d in valid_entries if d["order_date"].year == selected_year]
    total_orders_in_year = len(orders_in_year)

    # Display results
    st.subheader(" Summary Statistics")
    st.write(f"Total entries: {len(entries)}")
    st.write(f"Valid entries: {len(valid_entries)}")
    st.write(f"Invalid entries: {len(invalid_entries)}")

    st.subheader(f" Positive Review Summary for Product '{selected_product_id}'")
    st.write(summary)

    st.subheader(f" Total Negative Reviews for Product '{selected_product_id}'")
    st.write(len(negative_reviews))

    st.subheader(f" Total Orders in {selected_year}")
    st.write(total_orders_in_year)

    #  Show invalid entries
    if invalid_entries:
        st.subheader(" Invalid Entries")
        for item in invalid_entries:
            st.markdown(f"**Entry #{item['entry_number']}**")
            st.text(item["entry"])
            st.write("Issues:", item["issues"])
            st.markdown("---")
