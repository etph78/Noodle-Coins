import streamlit as st
import pandas as pd
import requests
import openpyxl
from io import BytesIO

st.title("✨ Noodle Coins app")

xlsx_file_init = 'https://www.bankhapoalim.co.il/sites/default/files/media/DohotKaspiem/120012411.xlsx'
# xlsx_file_init = 'https://noodle-coins.streamlit.app/'

# col1,col2 = st.columns([1,2])
# col1.title('File:')
url = ''
with st.form('get_excel'):
    url = st.text_input('Copy Excel Link into Here')
    #b = st.text_input('b')
    submit = st.form_submit_button('Get Excel File')

if submit:
    #col2.title(f'{xlsx_file}')
    if url == '':
        url = xlsx_file_init
    st.write(f'Your Excel File is:')
    st.write(f'{url}')
    # Send a GET request
    response = requests.get(url)
    st.write(f'response.status_code: {response.status_code}')  # prints: 200
    # st.write(f'response.headers: {response.headers}')  # prints headers
    # st.write(f'response.text: {response.text}')  # prints the content of the response 
    
    if response.ok:
        try:
            # Read the content of the response with pandas
            df = pd.read_excel(io.BytesIO(response.content))
            # df = pd.read_excel(url, engine='openpyxl')
            st.write(f'The file was read correctly')
        except Exception as e:
            st.write(f'Error: {e}')
            df = pd.DataFrame()
            data = {
                "Questions": [0, 1, 2, 3],
                "Answers": ['a', 'b', 'c', 'd',],
            }
            df = pd.DataFrame(data)
    else:
        st.write(f'Error - Bad Response') 
        data = {
            "Questions": [0, 1, 2, 3],
            "Answers": ['a', 'b', 'c', 'd',],
        }    
        df = pd.DataFrame(data)

st.divider()





st.divider()

st.write(f'XLSX Data:')
st.write(df)

st.divider()
st.divider()


st.write(
    "We are so glad to see you here. ✨ "
)

data = {
    "Questions": [0, 1, 2, 3],
    "Answers": ['a', 'b', 'c', 'd',],
}

df = pd.DataFrame(data)

st.write(df)

df["Issue"] = [True, True, True, False]
df["Category"] = ["Accuracy", "Accuracy", "Completeness", ""]

new_df = st.data_editor(
    df,
    column_config={
        "Questions": st.column_config.TextColumn(width="medium", disabled=True),
        "Answers": st.column_config.TextColumn(width="medium", disabled=True),
        "Issue": st.column_config.CheckboxColumn("Mark as annotated?", default=False),
        "Category": st.column_config.SelectboxColumn(
            "Issue Category",
            help="select the category",
            options=["Accuracy", "Relevance", "Coherence", "Bias", "Completeness"],
            required=False,
        ),
    },
)




st.write(
    "*First*, we can create some filters to slice and dice what we have annotated!"
)

col1, col2 = st.columns([1, 1])
with col1:
    issue_filter = st.selectbox("Issues or Non-issues", options=new_df.Issue.unique())
with col2:
    category_filter = st.selectbox(
        "Choose a category",
        options=new_df[new_df["Issue"] == issue_filter].Category.unique(),
    )

st.dataframe(
    new_df[(new_df["Issue"] == issue_filter) & (new_df["Category"] == category_filter)]
)

st.markdown("")
st.write(
    "*Next*, we can visualize our data quickly using `st.metrics` and `st.bar_plot`"
)

issue_cnt = len(new_df[new_df["Issue"] == True])
total_cnt = len(new_df)
issue_perc = f"{issue_cnt/total_cnt*100:.0f}%"

col1, col2 = st.columns([1, 1])
with col1:
    st.metric("Number of responses", issue_cnt)
with col2:
    st.metric("Annotation Progress", issue_perc)

df_plot = new_df[new_df["Category"] != ""].Category.value_counts().reset_index()

st.bar_chart(df_plot, x="Category", y="count")

st.write(
    "Here we are at the end of getting started with streamlit! Happy Streamlit-ing! :balloon:"
)

