import streamlit as st
import re



"""
Streamlit Code
"""
def main():
    st.title("Are Two Texts the same?")
    st.write("Copy and Paste two texts into the boxes to check if they are the same\n\n")

    col1, col2 = st.columns(2)

    col1.header("Ground Truth")
    with col1:
        text_a = st.text_area(label="Copy & Paste Your GT Text Here", height=400)

    col2.header("Test")
    with col2:
        text_b = st.text_area(label="Copy & Paste Your Test Text Here", height=400)

    if st.button(label="Click it when ready ... "):
        res = compare_texts(text_a, text_b)
        
        if res is True:
            st.write("The texts are the same")
        else:
            st.write("The texts are not the same")


def compare_texts(txt_a, txt_b):
    
    split_a = split_with_re(txt_a)
    split_b = split_with_re(txt_b)
    
    same = True
    
    for tok_a, tok_b in zip(split_a, split_b):
        if tok_a != tok_b:
            same = False
            break
        else:
            continue

    return same

       
def split_with_re(text):
    return re.split('[,. \t]', text)

if __name__ == "__main__":
    main()
