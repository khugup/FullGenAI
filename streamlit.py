import streamlit as st
import pandas as pd
import streamlit as st
import numpy as np


# title of the application

# st.title("Hello streamlit")

# Display a simple text

# st.write("This is a simple text")


# Create a simple dataframe

# df=pd.DataFrame({
#     'first_column': [1,2,3,4,5,6],
#     'second_column':[10,20,30,40]
# })


# # Display the dataframe

# st.write("This a dataframe")
# st.write(df)



# st.write("hello")
# chart_data=pd.DataFrame(
#     np.random.randn(20,3),columns=['a','b','c'])
# st.line_chart(chart_data)



st.title("This is streamlit")
name=st.text_input("Enter your name")
age=st.slider("Select your age:",0,100,25)
st.write(f"Your age is {age}")
options=['python','java','c','c++','cobol']
choice=st.selectbox("Choose your favourite language",options)
st.write(f"Favourite language is {choice}")
df=pd.DataFrame({
    'first_column': [1,2,3,4],
    'second_column':[10,20,30,40]
})
st.write(df)

uploaded_file=st.file_uploader("Choose a csv file",type='csv')
if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    st.write(df)