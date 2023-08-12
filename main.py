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
    .newest_message {{
    background-color: rgba(255, 235, 205, 0.5);
    padding: 15px;
    border-radius: 25px;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.title("Dasho Draft Generator")
st.text("")
expander = st.expander('How Does This Work?', expanded=False)
with expander:
    st.write("""
    This application uses a sophisticated AI model to generate written content based on your inputs. 

    Here are the steps:

    1. Select a model. The default model is gpt-4. GPT-4 runs at a slow pace but is much more intelligent and creative than GPT-3.5-Turbo. GPT-3.5-Turbo runs at a much faster pace but is less intelligent and creative than GPT-4.
    2. Fill in the text fields with the appropriate information about your brand, target audience, content type, topic, and writing style.
    3. Click on the 'Generate Draft' button. The application will start generating the written content. It might take a moment, so please be patient.
    4. The application will first show you an AI analysis of your inputs, followed by a first draft of the content. 
    5. The application will then perform a second analysis on the first draft and present a second (final) draft.
    6. If you have any feedback or if you want the AI to make revisions, you can provide your feedback in the 'Feedback' text field and click on 'Send Feedback'. The application will then generate a new version of the content based on your feedback.
    7. All of your feedback and corresponding output from the AI will be displayed in the 'Feedback Thread'.
    """)
if 'input_expander_state' not in st.session_state:
    st.session_state['input_expander_state'] = True
expander = st.expander('Show/Hide Inputs', expanded=st.session_state['input_expander_state'])
with expander:
    model_options = ['gpt-4', 'gpt-3.5-turbo']
    selected_model = st.selectbox('Select Model:', model_options)

    st.markdown("---")

    # Initialize state variables
    if 'article_gen' not in st.session_state:
        st.session_state['article_gen'] = None
    if 'feedbacks' not in st.session_state:
        st.session_state['feedbacks'] = []
    if 'outputs' not in st.session_state:
        st.session_state['outputs'] = []
    if 'output_generated' not in st.session_state:
        st.session_state['output_generated'] = False
    if 'show_output' not in st.session_state:
        st.session_state['show_output'] = True


    brand = st.text_input('Brand:', '')
    brand_description = st.text_input('Brand Description:', '')
    content_type_options = ['', 'Article', 'Blog Post', 'Email Newsletter', 'Newsletter', 'Infographics', 'Short Story', 'Press Release', 'Product Description', 'Product Review', 'Social Media Captions', 'Twitter Captions', 'Advertisement', 'Shortform Video Script', 'SEO-Optimized Article', 'Social Media Post']
    content_type = st.selectbox('Content Type:', sorted(content_type_options))
    topic = st.text_input('Topic:', '')
    writing_style = st.text_input('Writing Style:', '')
    target_audience = st.text_input('Target Audience:', '')
    additional_instructions = st.text_area('Additional Information (Optional):', '')

if brand and brand_description and content_type and topic and writing_style and target_audience and st.button('Generate Draft'):
    st.markdown("---")
    if not st.session_state['article_gen']:
        # Initialize the ArticleGenerator object
        st.session_state['article_gen'] = ArticleGenerator(selected_model, content_type, brand, brand_description, topic, writing_style, target_audience, additional_instructions)
    container = st.empty()  # Use empty to be able to continually update the output
    st_callback = StreamlitCallbackHandler(container)  # Initialize the Streamlit callback handler
    response = st.session_state['article_gen'].generate(st_callback)  # Pass the callback handler to the generate method
    st.session_state['output_generated'] = True
    st.session_state['current_response'] = response
    container.write("")  # Clears the container after use

output_expander = st.expander("Show/Hide Output", expanded=True)

with output_expander:
    if st.session_state['output_generated']:
        response = st.session_state.get('current_response', {})
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
    
if st.session_state['output_generated']:
    st.markdown("---")
    if 'user_feedback' not in st.session_state:
        st.session_state['user_feedback'] = ''

    user_feedback = st.text_input('Feedback:', value=st.session_state['user_feedback'])

    if st.button('Send Feedback') and user_feedback:
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
    st.subheader("Feedback Thread")
    
    # Start from the last feedback since it's the newest
    for index, (feedback, output) in enumerate(zip(reversed(st.session_state['feedbacks']), reversed(st.session_state['outputs']))):
        
        if index == 0:  # If it's the newest message
            st.markdown(f'<div class="newest_message"><caption>Feedback: {feedback}</caption><br>Output: {output}</div>', unsafe_allow_html=True)
        else:
            st.caption(f"Feedback: {feedback}")
            st.write(f"Output: {output}")
        
        st.markdown("---")
