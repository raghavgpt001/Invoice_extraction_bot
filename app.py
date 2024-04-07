import streamlit as st
from utils import *


def main():
    st.set_page_config(page_title="Invoice Extraction Bot")
    st.title("Invoice Extraction Bot...💁 ")
    st.subheader("I can help you in extracting invoice data")
    if 'API_Key' not in st.session_state:
        st.session_state['API_Key'] =''
    st.session_state['API_Key']= st.sidebar.text_input("What's your OpenAI API key?",type="password")

    # Upload the Invoices (pdf files)
    pdf = st.file_uploader("Upload invoices here, only PDF files allowed", type=["pdf"],accept_multiple_files=True)

    submit=st.button("Extract Data")

    if submit:
        with st.spinner('Wait for it...'):
            df=create_docs(pdf, st.session_state['API_Key'])
            st.write(df.head())

            data_as_csv= df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download data as CSV", 
                data_as_csv, 
                "benchmark-tools.csv",
                "text/csv",
                key="download-tools-csv",
            )
        st.success("Hope I was able to save your time❤️")


#Invoking main function
if __name__ == '__main__':
    main()