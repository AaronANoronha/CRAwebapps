from textblob import TextBlob
import cleantext
import plotly.express as px
import pandas as pd
import streamlit as st
st.header('Sentiment Analysis')
if st.sidebar.checkbox("Text Input", True, key=1):
 with st.expander('Analyze Text',expanded=False):
    text = st.text_input('Text here: ')
    if text:
        if isinstance(text, str):
            blob = TextBlob(text)
            polarity = round(blob.sentiment.polarity, 2)
            subjectivity = round(blob.sentiment.subjectivity, 2)
            st.write('Polarity: ', polarity)
            st.write('Subjectivity: ', subjectivity)

            if polarity >= 0.5:
                sentiment = "Positive"
            elif polarity == 0:
                sentiment = "Neutral"
            else:
                sentiment = "Negative"
            st.write('Sentiment: ', sentiment)
        else:
            st.write("Error: Input text is not a string.")

    pre = st.text_input('Clean Text: ')
    if pre:
        st.write(cleantext.clean(pre, clean_all=False, extra_spaces=True,
                                 stopwords=True, lowercase=True, numbers=True, punct=True))

if st.sidebar.checkbox("Csv Upload", True, key=2):
    with st.expander('Analyze CSV', expanded=True):

        upl = st.file_uploader('Upload file')


        def score(x):
            blob1 = TextBlob(str(x))
            return blob1.sentiment.polarity


        def analyze(x):
            if x >= 0.5:
                return 'Positive'
            elif x == 0:
                return 'Neutral'
            else:
                return 'Negative'


        if upl:
            df = pd.read_excel(upl)
            df['review_body'] = df['review_body'].astype(str)
            df['score'] = df['review_body'].apply(score)
            df['analysis'] = df['score'].apply(analyze)
        else:
            st.write("Please upload a file to continue.")

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

if 'df' in locals():
    csv = convert_df(df)
    st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='sentiment.csv',
                    mime='text/csv',
                )

if upl:
 sentiments = df['analysis'].value_counts()
 if 'sentiments' in locals() or 'sentiments' in globals():
     fig = px.pie(sentiments, values=sentiments.values, names=sentiments.index)
 else:
     print("")

if st.checkbox("Show pie chart"):
    st.plotly_chart(fig)
else:
    st.write("Pie chart is hidden")

if st.sidebar.checkbox("Review Filter", True, key=3):

    if not upl:
        st.write("Please upload the file")
    elif "df" not in locals():
        st.write("Please upload the file")
    else:
        filter_ = st.selectbox("Filter by Sentiment", ['All'] + df["analysis"].unique().tolist())

    if "filter_" not in locals():
        st.write()
    else:
        if filter_ == 'All':
            filtered_df = df
        else:
            filtered_df = df[df['analysis'] == filter_]
        st.write(filtered_df)
else:
 filtered_df = df[df["analysis"] == filter_]
 st.write(filtered_df)
if st.sidebar.checkbox("Show/hide Sentiment Summary", False, key=4):
    with st.expander('Summary of reviews',expanded=True):
        if "df" not in locals():
            st.write("Please upload the file")
        else:
         pos = len(df[df["analysis"] == "Positive"])
         neg = len(df[df["analysis"] == "Negative"])
         neu = len(df[df["analysis"] == "Neutral"])
         st.sidebar.write("Sentiment Summary:")
         st.sidebar.write(f"Total Reviews : {pos + neg +neu}")
         st.sidebar.write(f"Positive: {pos}")
         st.sidebar.write(f"Negative: {neg}")
         st.sidebar.write(f"Neutral: {neu}")






