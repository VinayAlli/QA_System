# Install required packages
import torch
import numpy as np
from transformers import pipeline
import streamlit as st
from pyngrok import ngrok
import time

# Set up ngrok tunnel
ngrok.set_auth_token("2tfJOAvSpeuqeDYkoe9d100zcSB_4KaV3bVjtKrnqPFGTdjYy")  # Replace with your actual token

# Terminate existing processes and wait for cleanup
ngrok.kill()
time.sleep(2)  # Allow time for process termination

# Create new tunnel with explicit process management
try:
    public_url = ngrok.connect(8501, bind_tls=True)
    print("App URL:", public_url)
except Exception as e:
    st.error(f"Failed to start ngrok: {str(e)}")
    st.stop()

# Streamlit app code
st.title("Question Answering System")
context = st.text_area("Context")
question = st.text_input("Question")

# Use a more appropriate QA model
try:
    qa_pipeline = pipeline('question-answering', 
                         model='distilbert-base-cased-distilled-squad')
except Exception as e:
    st.error(f"Model loading failed: {str(e)}")
    st.stop()

if st.button("Get Answer"):
    if context and question:
        try:
            result = qa_pipeline(question=question, context=context)
            st.write(f"**Answer:** {result['answer']}")
            st.write(f"**Score:** {result['score']:.2f}")
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")
    else:
        st.warning("Please provide context and question.")

# Cleanup when Streamlit stops (optional)
import atexit
@atexit.register
def shutdown():
    ngrok.kill()