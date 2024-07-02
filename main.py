import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI

template = """
    Below is a draft text that may be poorly worded.
    Your goal is to:
    - Properly redact the draft text
    - Convert the draft text to a specified tone
    - Convert the draft text to a specified dialect
    
    Below is the draft text, tone, and dialect:
    DRAFT: {draft}
    TONE: {tone}
    DIALECT: {dialect}

    YOUR {dialect} RESPONSE:
"""

#PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["tone", "dialect", "draft"],
    template=template,
)

#Page title and header
st.set_page_config(page_title="Re-write your text")
st.header("Re-write your text")



st.markdown("Re-write your text in different styles.")

#Input OpenAI API Key

st.markdown("## Convo like a pro")

def get_openai_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

openai_key = get_openai_key()



# Input
st.markdown("## Enter the text you want to re-write")

def get_draft_text():
    draft = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft

draft_text = get_draft_text()


# Prompt template tunning options
col1, col2 = st.columns(2)


with col1:
    option_tone = st.selectbox(
        'Which tone would you like your redaction to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))

# Output
st.markdown("### Your Re-written text:")

#LLM and key loading function
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm


if (draft_text):
    if(not openai_key):
        st.warning('Please insert OpenAI API Key. \
            Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_key)
    print(llm)
    
    prompt_with_draft = prompt.format(
        tone=option_tone, 
        dialect=option_dialect, 
        draft=draft_text
    )

    improved_redaction = llm(prompt_with_draft)

    if len(draft_text.split(" ")) < 3:
        st.write("Please complete a sentance. Minimum 3 words are required.")
        st.stop()
    else : 
        st.write(improved_redaction)








