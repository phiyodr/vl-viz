import streamlit as st
import json
import pandas as pd
from PIL import Image
import os

st.title("Interactive Data-Explorer")
st.write("""
## This is Testversion v0.1
""")

# Load Dataset

pd.set_option('display.max_colwidth', None)
columns = ['imageId', 'question', 'answer', 'fullAnswer', 'groups', 'types']
my_df = pd.read_json(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "gqa_train_demo.json")),
                     orient="index")
my_df = my_df[columns]

# Search for Keywords and alter Dataset Dataframe accordingly

keys = st.text_input("Search for Keywords in Question and Answers")
new_df = pd.DataFrame(columns=columns)
for index, row in my_df.iterrows():
    if keys.lower() in row['question'].lower() or keys.lower() in row['fullAnswer'].lower() or keys.lower() in row[
        'answer'].lower():
        new_df = new_df.append(row)

if new_df is not None:
    show_df = new_df
else:
    show_df = my_df

st.dataframe(data=show_df)

# Display Selectbox with Data from Dataframe or Searchresults

display_dataset = st.selectbox("Select Dataset", (show_df.index.values.tolist()))

# st.dataframe(data = my_df)

if st.button("Display Selected"):
    image = my_df["imageId"][display_dataset]
    fullImgPath = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "gqa_train_demo", str(image)) + ".jpg")
    image = Image.open(fullImgPath)
    st.text("Question: " + my_df["question"][display_dataset])
    st.text("Answer: " + my_df["fullAnswer"][display_dataset] + "   (" + my_df["answer"][display_dataset] + ")")
    st.image(image)

if st.button("Reset"):
    show_df = my_df
    keys = ""
