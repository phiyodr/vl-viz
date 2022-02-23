import numpy as np
import streamlit as st
import pandas as pd
from PIL import Image
import os

# Set Page-Settings

st.set_page_config(page_title="Interactive Data-Explorer", page_icon="chart_with_upwards_trend",
                   initial_sidebar_state="expanded")
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.title("Interactive Data-Explorer")
st.write("""
## This is Testversion v0.2
""")
st.markdown("***")

# Select and load Dataset

select_dataset = st.sidebar.selectbox(label="Select the Dataset to display", options=["gqa_train_demo"])

pd.set_option('display.max_colwidth', None)
columns = ['imageId', 'question', 'answer', 'fullAnswer', 'groups', 'types']
base_df = pd.read_json(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", select_dataset + ".json")),
                       orient="index")
base_df = base_df[columns]
base_df['wordCount'] = 0

for i, row in base_df.iterrows():
    base_df.at[i, 'wordCount'] = int(len(row['question'].split(" ")))

# Checkboxes

selection = st.radio(label="Please select in which columns you want to search",
                     options=('Questions', 'Answers', 'Both'))

# Search by Keywords or phrases

keys = st.text_input("Search for Keywords in Question and Answers")
sorted_df = pd.DataFrame(columns=columns)
for index, row in base_df.iterrows():
    if selection == "Questions":
        if keys.lower() in row['question'].lower():
            sorted_df = sorted_df.append(row)
    if selection == "Answers":
        if keys.lower() in keys.lower() in row['answer'].lower():
            sorted_df = sorted_df.append(row)
    if selection == "Both":
        if keys.lower() in row['question'].lower() or keys.lower() in row['answer'].lower():
            sorted_df = sorted_df.append(row)

if not sorted_df.empty:
    displayed_df = sorted_df
    st.dataframe(data=displayed_df)

    # Display Selectbox with Data from Dataframe or Searchresults

    display_dataset = st.selectbox("Select Dataset", (displayed_df.index.values.tolist()))

    # st.dataframe(data = my_df)

    if display_dataset:
        image = base_df["imageId"][display_dataset]
        fullImgPath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data", "gqa_train_demo", str(image)) + ".jpg")
        image = Image.open(fullImgPath)
        st.text("Question: " + base_df["question"][display_dataset])
        st.text("Answer: " + base_df["fullAnswer"][display_dataset] + "   (" + base_df["answer"][display_dataset] + ")")
        st.image(image)
else:
    st.error("No Dataset fit your requirements.")

if st.button("Reset"):
    st.write("Sadly, that does not work (Yet)")
    st.experimental_rerun()
