from langchain_openai import OpenAI
from pypdf import PdfReader
import pandas as pd
import re
from langchain.prompts import PromptTemplate


#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



#Function to extract data from text
def extracted_data(pages_data, api_key):

    template = """Extract all the following values : invoice no., Description, Quantity, date, 
        Unit price , Amount, Total, email, phone number and address from this data: {pages}
        Expected output: remove any currency symbols {{'Invoice no.': '1001329','Description': 'Office Chair','Quantity': '2','Date': '5/4/2023','Unit price': '1100.00','Amount': '2200.00','Total': '2200.00','Email': 'Santoshvarma0988@gmail.com','Phone number': '9999999999','Address': 'Mumbai, India'}}
        """
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)

    llm = OpenAI(temperature=.7, api_key=api_key)
    full_response=llm(prompt_template.format(pages=pages_data))
    
    return full_response


# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list, api_key):
    data = []

    for filename in user_pdf_list:
        print("filename: ", filename)
        raw_data=get_pdf_text(filename)
        print("raw_data: ", raw_data)
        #print("extracted raw data")

        llm_extracted_data=extracted_data(raw_data, api_key)
        #print("llm extracted data")
        #Adding items to our list - Adding data & its metadata

        pattern = r'{(.+)}'
        match = re.search(pattern, llm_extracted_data, re.DOTALL)

        if match:
            extracted_text = match.group(1)
            print("extracted_text: ", extracted_text)
            # Converting the extracted text to a dictionary
            data_dict = eval('{' + extracted_text + '}')
            print("data_dict: " , data_dict)
            data.append(data_dict)
            print("********************DONE***************")
        else:
            print("No match found.")

    df = pd.DataFrame.from_dict(data) 

    df.head()
    return df
