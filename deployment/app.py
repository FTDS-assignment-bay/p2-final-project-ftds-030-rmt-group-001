# import libraries yang dibutuhkan
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# konfigurasi laman streamlit agar menjadi lebih lebar
st.set_page_config(layout="wide")

# panggil dataset ke dalam aplikasi
df = pd.read_csv('deployment/books_dataset_cleaned.csv')

# panggil model TF-IDF
with open('deployment/laibrarian.pkl', 'rb') as file:
    tfidf_desc = pickle.load(file)

# custom CSS untuk container
st.markdown(
    """
    <style>
    body {
        background-color: white;
    }
    .book-container {
        border: 1px solid #ddd;
        padding: 10px;
        margin: 10px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# pasang logo untuk ditampilkan
st.image('lai.png', width=200)

# tulis subheader
st.write('###### Discover your new journey in literature.')

# konfigurasi sidebar untuk filter pencarian
with st.sidebar:
    st.header('Search with filter!')
    sidebar_rating = st.radio(
        "Choose a minimum rating:",
        options=[1,2,3,4,5],
        index=2,
        format_func=lambda x: f"{x}"
    )
    sidebar_author = st.selectbox(
        'Filter by author:',
        [''] + sorted(df['authors'].unique())  
    )
    sidebar_submit = st.button('Search by filter')

    if sidebar_submit:
        st.write("##### Current Filters:")
        st.write(f"- Minimum Rating: {sidebar_rating}")
        if sidebar_author:
            st.write(f"- Author: {sidebar_author}")

    if st.button("Reset"):
        sidebar_rating = 3
        sidebar_author = ''

# form utama untuk input deskripsi buku
with st.form('input'):
    text_input = st.text_input("or you can just describe the book you're looking for:", help='i.e. story about fantasy kingdom')
    submitted = st.form_submit_button("Surprise me!")

    if submitted:
        if text_input.strip():
            user_tfidf = tfidf_desc.transform([text_input])

            # filter berdasarkan minimum rating
            filtered_df = df.copy()  # Copy the DataFrame to avoid modifying the original

            if not filtered_df.empty:
                # mengubah teks menjadi vektor TF-IDF
                filtered_tfidf = tfidf_desc.transform(filtered_df['full_desc'])

                # menghitung cosine similarity
                similarities = cosine_similarity(user_tfidf, filtered_tfidf)
                
                # ambil top 8 buku dengan nilai similarity tertinggi
                top_indices = similarities[0].argsort()[-8:][::-1]
                
                st.write("##### Based on your input, we can recommend:")

                # tampilkan rekomendasinya
                for i in range(0, len(top_indices), 4):
                    row = st.columns(4)
                    for j in range(4):
                        if i + j < len(top_indices):
                            book_index = top_indices[i + j]
                            book = filtered_df.iloc[book_index]
                            with row[j]:
                                st.markdown(f"""
                                <div class="book-container">
                                    <img src="{book['thumbnail']}" width="150">
                                    <h5>{book['title']}</h5>
                                    <p><span style="font-size: 15px; font-weight: bold;">★{book['average_rating']}</span></p>
                                    <p><span style="font-size: 15px;">{book['authors']}</span></p>
                                    <p><span style="font-size: 15px;">{book['published_year']}</span></p>
                                    <p><span style="font-size: 15px;">{book['categories']}</span></p>
                                </div>
                                """, unsafe_allow_html=True)
                                with st.popover('Description', use_container_width=True):
                                    st.markdown(book['description'])
                                st.link_button('Buy Here :money_with_wings:', url='http://www.bukabuku.com/', use_container_width=False, type='primary', disabled=False)
        else:
            st.write('Please provide the book description.')

# tampilkan rekomendasi untuk filter dari sidebar
if sidebar_submit:
    filtered_df = df[df['average_rating'] >= sidebar_rating]

    if sidebar_author:
        filtered_df = filtered_df[filtered_df['authors'] == sidebar_author]

    if not filtered_df.empty:
        st.write("##### Books based on the specified criteria:")
        for i in range(0, min(8, len(filtered_df)), 4):
            row = st.columns(4)
            for j in range(4):
                if i + j < len(filtered_df):
                    book = filtered_df.iloc[i + j]
                    with row[j]:
                        st.markdown(f"""
                        <div class="book-container">
                            <img src="{book['thumbnail']}" width="150">
                            <h4>{book['title']}</h4>
                            <p><span style="font-size: 15px; font-weight: bold;">★{book['average_rating']}</span></p>
                            <p><span style="font-size: 15px;">{book['authors']}</span></p>
                            <p><span style="font-size: 15px;">{book['published_year']}</span></p>
                            <p><span style="font-size: 15px;">{book['categories']}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                        with st.popover('Description', use_container_width=True):
                            st.markdown(book['description'])
                        st.link_button('Buy Here :money_with_wings:', url='http://www.bukabuku.com/', use_container_width=False, type='primary', disabled=False)
    else:
        st.write('No books found with the specified criteria.')
