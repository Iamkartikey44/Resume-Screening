import streamlit as st
import uuid
import constants
from dotenv import load_dotenv
from utils import *

if 'unique_id' not in st.session_state:
    st.session_state['unique_id']=''

   
load_dotenv()
st.set_page_config(page_title="Resume Screening Assistance")
st.title("HR - Resume Screening Assistance...💁")
st.subheader("I can help you in resume screening process")    

def main():
    
    job_description = st.text_area("Please paste the JOB Description here...",key='123')
    document_count = st.text_input("Number of Resumes to return",key='count')

    pdf = st.file_uploader("Upload Resume here, only PDF allowed",type=['pdf'],accept_multiple_files=True)

    submit = st.button("Help me with the analysis")

    if submit:
        with st.spinner('Wait for it...'):
            st.session_state['unique_id']=uuid.uuid4().hex

            final_docs_list = create_docs(pdf,st.session_state['unique_id'])
            st.write("*Resumes uploaded* :"+str(len(final_docs_list)))

            embeddings = create_embeddings_load_data()

            push_to_pinecone(constants.Pinecone_API_Key,constants.PINECONE_ENVIRONMENT,constants.PINECONE_INDEX,embeddings,final_docs_list)

            relavant_docs = similar_docs(job_description,document_count,constants.Pinecone_API_Key,constants.PINECONE_ENVIRONMENT,constants.PINECONE_INDEX,embeddings,st.session_state['unique_id'])

            st.write(":heavy_minus_sign:" * 30)

            for item in range(len(relavant_docs)):
                st.subheader("👉 "+str(item+1))
                st.write("**File** : "+relavant_docs[item][0].metadata['name'])

                with st.expander("Show Me 👀"):
                    st.info("**Match Score** : "+str(relavant_docs[item][1]))

                    summary = get_summary(relavant_docs[item][0])
                    st.write("**Summary** : "+summary)
        st.success("Hope I was able to save your time❤️")            

if __name__ == "__main__":
    main()



main()