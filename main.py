import streamlit as st
from langchain_helper import ArticleGenerator

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
content_type_options = ['', 'Article', 'Blog Post', 'Email Newsletter', 'Infographics', 'Short Story', 'Press Release', 'Product Description', 'Product Review', 'Social Media Captions', 'Advertisement', 'SEO-Optimized Articles', 'Social Media Post']
content_type = st.selectbox('Content Type:', sorted(content_type_options))
topic = st.text_input('Topic:', '')
writing_style = st.text_input('Writing Style:', '')
target_audience = st.text_input('Target Audience:', '')
additional_instructions = st.text_area('Additional Information:', '')

st.markdown("---")

if brand and brand_description and content_type and topic and writing_style and target_audience and additional_instructions:
    if not st.session_state['article_gen']:
        # Initialize the ArticleGenerator object
        st.session_state['article_gen'] = ArticleGenerator(content_type, brand, brand_description, topic, writing_style, target_audience, additional_instructions)
    
    response = st.session_state['article_gen'].generate()

    st.header(response['brand'].strip())

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
    
    # Display Final Output
    st.subheader("Final Output")
    st.write(response['final_output'].strip())
    st.markdown("---")
    user_feedback = st.text_input('Feedback:', '')
        # Add button to submit feedback
    if st.button('Submit Feedback') and user_feedback:
            new_response = st.session_state['article_gen'].generate_with_feedback(user_feedback)
            # Append the feedback and response to the lists in the session state
            st.session_state['feedbacks'].append(user_feedback)
            st.session_state['outputs'].append(new_response['final_output_with_feedback'].strip())
            st.markdown("---")

            # Display the new results
            st.subheader("Feedback Thread")
            for feedback, output in zip(st.session_state['feedbacks'], st.session_state['outputs']):
                st.caption(f"Feedback: {feedback}")
                st.write(f"Output: {output}")
                st.markdown("---")

            # Reset the user_feedback field for the next feedback
            st.session_state['user_feedback'] = ''
