import streamlit as st 
from PIL import Image


st.title("LDS Visitor Ratio Analysis in Counties with and Without Temples")

image = Image.open('./assets/images/newplot.png')

st.image(image, caption='LDS Visitor to Population Ratio by County')


st.write("""
This chart shows the individual census block groups' LDS visitor ratio to the overall population with them being grouped by counties that have temples and those that don't.
         
Interesting to see how it is the opposite of what is expected with the higher member to population ratio being in counties that do not currently have temples
 """)