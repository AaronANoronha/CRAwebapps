import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from textblob import TextBlob

st.title('Scrape Amazon Product Reviews')

url = st.text_input("Enter product review URL:")
page_num = int(st.number_input("Enter number of pages to scrape:"))

# Validate URL
if not url.startswith("https://"):
    st.write("Invalid URL")
else:
    data = []
    for i in range(1, page_num+1):
        # URL setup and HTML request
        r = requests.get(url + '&pageNumber=' + str(i))
        soup = BeautifulSoup(r.text, 'html.parser')
        reviews = soup.find_all('div', {'data-hook': 'review'})

        for item in reviews:
            review = {
                'title': item.find('a', {'data-hook': 'review-title'}).text.strip() if item.find('a', {
                    'data-hook': 'review-title'}) else None,
                'text': item.find('span', {'data-hook': 'review-body'}).text.strip() if item.find('span', {
                    'data-hook': 'review-body'}) else None,
            }
            if review['text'] is not None:
                data.append(review)

    df = pd.DataFrame(data)
    if 'text' in df.columns:
        df['sentiment'] = df['text'].apply(lambda x: TextBlob(x).sentiment[0])
    else:
        df['sentiment'] = df['title'].apply(lambda x: TextBlob(x).sentiment[0])

    df['sentiment_label'] = df['sentiment'].apply(
        lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

    import plotly.express as px

    labels = df['sentiment_label'].value_counts().index
    values = df['sentiment_label'].value_counts().values

    # Make sure negative label is included in the labels and values lists
    if 'Negative' not in labels:
        labels = list(labels) + ['Negative']
        values = list(values) + [0]

    fig = px.pie(names=labels, values=values)
    if st.checkbox("Show pie chart"):
        st.plotly_chart(fig)
    else:
        st.write("Pie chart is hidden")

    # Total number of reviews
    total_reviews = df.shape[0]
    st.sidebar.write("Total Reviews:", total_reviews)

    # Number of unique positive, negative, and neutral reviews
    positive_reviews = df[df['sentiment_label'] == "Positive"].shape[0]
    negative_reviews = df[df['sentiment_label'] == "Negative"].shape[0]
    neutral_reviews = df[df['sentiment_label'] == "Neutral"].shape[0]

    st.sidebar.write("Positive Reviews:", positive_reviews)
    st.sidebar.write("Negative Reviews:", negative_reviews)
    st.sidebar.write("Neutral Reviews:", neutral_reviews)

    # Add a filter to select sentiment label
    sentiment_filter = st.selectbox("Filter by Sentiment:", ["All", "Positive", "Negative", "Neutral"])

    if sentiment_filter == "Positive":
        df = df[df['sentiment_label'] == "Positive"]
    elif sentiment_filter == "Negative":
        df = df[df['sentiment_label'] == "Negative"]
    elif sentiment_filter == "Neutral":
        df = df[df['sentiment_label'] == "Neutral"]

    st.write(df)

    if st.button('Download as CSV'):
        st.write(df.to_csv(index=False))


