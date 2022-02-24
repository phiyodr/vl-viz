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
## This is Testversion v0.3.2
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
base_df['global'] = base_df['local'] = base_df['detailed'] = base_df['semantic'] = base_df['structural'] = ''

for i, row in base_df.iterrows():
    base_df.at[i, 'wordCount'] = len(row['question'].split(" "))
    base_df.at[i, 'global'] = row['groups']['global'] if (
            row['groups']['global'] is not None and bool(row['groups']['global']) is True) else 'No Entry'
    base_df.at[i, 'local'] = row['groups']['local'] if (
            row['groups']['local'] is not None and bool(row['groups']['local']) is True) else 'No Entry'
    base_df.at[i, 'detailed'] = row['types']['detailed'] if (
            row['types']['detailed'] is not None and bool(row['types']['detailed']) is True) else 'No Entry'
    base_df.at[i, 'semantic'] = row['types']['semantic'] if (
                row['types']['semantic'] is not None and bool(row['types']['semantic']) is True) else 'No Entry'
    base_df.at[i, 'structural'] = row['types']['structural'] if (
                row['types']['structural'] is not None and bool(row['types']['structural']) is True) else 'No Entry'

base_df.drop(['groups', 'types'], axis=1, inplace=True)


# Checkboxes

selection = st.radio(label="Please select in which columns you want to search",
                     options=('Questions', 'Answers', 'Both', 'None'), index=3)

keyphrase = st.text_input("Search for Keywords in Question and Answers")
options = st.multiselect('Search additional columns', ['global', 'local', 'detailed', 'semantic', 'structural'])
keywords = st.text_input("Enter Keywords")
words = keywords.split()


# Search by Keywords or phrases

sorted_df = pd.DataFrame()
for index, row in base_df.iterrows():
    #Search for Keywords
    if selection != 'None':
        if selection == "Questions":
            if keyphrase.lower() in row['question'].lower():
                sorted_df = sorted_df.append(row)
        if selection == "Answers":
            if keyphrase.lower() in keyphrase.lower() in row['answer'].lower():
                sorted_df = sorted_df.append(row)
        if selection == "Both":
            if keyphrase.lower() in row['question'].lower() or keyphrase.lower() in row['answer'].lower():
                sorted_df = sorted_df.append(row)

    if options is not None:
        for key in options:
            for word in words:
                if word.lower() in row[key].lower():
                    if index not in sorted_df.index.values:
                        sorted_df = sorted_df.append(row)

if sorted_df.empty and selection == 'None':
    sorted_df = base_df

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
