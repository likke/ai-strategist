import streamlit as st
from langchain_helper import ArticleGenerator
from langchain.callbacks import StreamlitCallbackHandler

# Set page config
st.set_page_config(page_title='Dasho Article Generation', page_icon=':pencil:', layout='centered', initial_sidebar_state='collapsed')

# Define custom colors for layout
primaryColor = "#ffae00"
backgroundColor = "#F0F2F6"
secondaryBackgroundColor = "#F6336699"
textColor = "#000000"
font = "sans-serif"

# Define custom css
custom_css = f"""
<style>
    body {{
        background-color: {backgroundColor};
        color: {textColor};
        font-family: {font};
    }}
    .stButton > button {{
        background-color: {primaryColor};
        color: {backgroundColor};
        font-family: {font};
    }}
    .css-2trqyj {{
        background-color: {secondaryBackgroundColor};
        color: {textColor};
        font-family: {font};
    }}
    .stTextInput > div > div > input {{
        color: {textColor};
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("Dasho Draft Generator")
st.markdown("---")

# Initialize state variables
if 'article_gen' not in st.session_state:
    st.session_state['article_gen'] = None
if 'feedbacks' not in st.session_state:
    st.session_state['feedbacks'] = []
if 'outputs' not in st.session_state:
    st.session_state['outputs'] = []

brand = st.text_input('Brand:', '')
brand_description = st.text_input('Brand Description:', '')
content_type_options = ['', 'Article', 'Blog Post', 'Email Newsletter', 'Newsletter', 'Infographics', 'Short Story', 'Press Release', 'Product Description', 'Product Review', 'Social Media Captions', 'Twitter Captions', 'Advertisement', 'Shortform Video Script', 'SEO-Optimized Article', 'Social Media Post']
content_type = st.selectbox('Content Type:', sorted(content_type_options))
topic = st.text_input('Topic:', '')
writing_style = st.text_input('Writing Style:', '')
target_audience = st.text_input('Target Audience:', '')
additional_instructions = st.text_area('Additional Information (Optional):', '')

st.markdown("---")

if brand and brand_description and content_type and topic and writing_style and target_audience and st.button('Generate Draft'):
    if not st.session_state['article_gen']:
        # Initialize the ArticleGenerator object
        st.session_state['article_gen'] = ArticleGenerator(content_type, brand, brand_description, topic, writing_style, target_audience, additional_instructions)
    with st.empty():  # Use empty to be able to continually update the output
        st_callback = StreamlitCallbackHandler(st.container())  # Initialize the Streamlit callback handler
        response = st.session_state['article_gen'].generate(st_callback)  # Pass the callback handler to the generate method

    st.header("FINAL OUTPUT")

    # Display AI Analysis
    st.subheader("AI Analysis")
    st.write(response['AI_analysis'].strip())

    # Display First Draft
    st.subheader("First Draft")
    st.write(response['first_draft'].strip())

    # Display Second AI Analysis
    st.subheader("AI Analysis of First Draft")
    article_text = response['AI_analysis_2'].strip().split("|")
    for section in article_text:
        st.write(" ", section)
    
    # Display Second Draft
    st.subheader("Second Draft")
    st.write(response['final_output'].strip())
    st.markdown("---")

if 'user_feedback' not in st.session_state:
    st.session_state['user_feedback'] = ''

user_feedback = st.text_input('Feedback:', value=st.session_state['user_feedback'])

if st.button('FEEDBACK SYSTEM IS BROKEN, PLEASE IGNORE') and user_feedback:
    # Initialize the Streamlit callback handler and generate the output
    st_callback = StreamlitCallbackHandler(st.empty())  # Initialize the Streamlit callback handler
    new_response = st.session_state['article_gen'].generate_with_feedback(user_feedback, st_callback)  # Pass the callback handler to the generate_with_feedback method

    # Update session state with the new feedback and output
    st.session_state['feedbacks'].append(user_feedback)
    st.session_state['outputs'].append(new_response['final_output_with_feedback'].strip())

    # Clear the feedback input field
    st.session_state['user_feedback'] = ''

# Feedback thread rendering should be done outside st.empty() context
if st.session_state['feedbacks']:
    st.markdown("---")

    # Display the new results
    st.subheader("Feedback Thread")
    for feedback, output in zip(st.session_state['feedbacks'], st.session_state['outputs']):
        st.caption(f"Feedback: {feedback}")
        st.write(f"Output: {output}")
        st.markdown("---")