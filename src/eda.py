import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os
import psycopg2
from sqlalchemy import text

from db_connection import get_connection
def run():
    st.header("📊 Exploratory Data Analysis")
    st.subheader('Dataset Overview')
    
    @st.cache_data
    def load_data(path):
        return pd.read_csv(path)
    
    df = load_data(os.path.join("data/PRDECT-ID Dataset.csv"))
    st.dataframe(df)
    
    st.subheader('Input User')
    # akses database
    def insert_data(product, rating, review):
        conn = get_connection()
        with conn.session as session:
            session.execute(
                text("""
                    INSERT INTO user_input
                    (product, rating, review)

                    VALUES
                    (:product, :rating, :review)
                """),
                {
                    "product": product,
                    "rating": rating,
                    "review": review
                }
            )

            session.commit()
    
    with st.form("review_form"):

        product = st.text_input("Product")

        rating = st.slider(
            "Rating",
            min_value=1,
            max_value=5,
            value=5
        )

        review = st.text_area("Review")

        submit = st.form_submit_button("Submit")

    if submit:

        if product == "" or review == "":
            st.warning("Please complete all fields.")

        else:

            insert_data(
                product,
                rating,
                review
            )

            st.success("Review successfully saved!")