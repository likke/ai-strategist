import streamlit as st
from langchain_helper import StratGenerator
from langchain.callbacks import StreamlitCallbackHandler

# Set up Streamlit page settings
st.set_page_config(page_title='Dasho Content Co-strategist', page_icon=':pencil:', layout='centered', initial_sidebar_state='collapsed')

# Define custom colors and styles
# These will be used for customizing the CSS later
primaryColor = "#4E89AE"
startGradientColor = "#ffaa00"
endGradientColor = "#FFFFFF"
textColor = "#2E5266"
font = "Roboto, sans-serif"
secondaryBackgroundColor = "#fcdede"
buttonColor = "#ffaa00"

# Custom CSS for styling the Streamlit app
custom_css = f"""
<style>
    body {{
        background: linear-gradient(90deg, {startGradientColor}, {endGradientColor});
        color: {textColor};
        font-family: {font};
        line-height: 1.6;
    }}
    .stButton > button {{
        background-color: {buttonColor};
        color: {endGradientColor};
        font-family: {font};
        border-radius: 10px;
        border: none;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .stTextInput > div > div > input, 
    textarea {{
        color: {textColor};
        border-radius: 10px;
        border: 2px solid {secondaryBackgroundColor}; /* Changed to gradient start color */
        padding: 10px 15px;
    }}
    .css-2trqyj {{
        background-color: rgba(255, 170, 0, 0.1); /* Light version of gradient start color for readability */
        color: {textColor};
        font-family: {font};
        border-radius: 10px;
        padding: 10px;
        margin-top: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .newest_message {{
        background-color: rgba(78, 137, 174, 0.2);
        padding: 15px;
        border-radius: 15px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Add a title to the Streamlit app
st.title("Dasho Content Co-strategist")

# Add a blank line
st.text("")

# Create a collapsible section (expander) to describe how the app works
expander_info = st.expander('How Does This Work?', expanded=False)
with expander_info:
    st.write("### **How the Dasho Content Co-strategist Works**")
    
    st.write("The Dasho Content Co-strategist is a powerful tool that harnesses the capabilities of AI to summarize your brand and create a content strategy in preparation for production. Below is an overview of how the application operates:")

    st.markdown("**1. Model Selection**")
    st.write("- Choose between two models: GPT-4 and GPT-3.5-Turbo.")
    st.write("- GPT-4 (Recommended): More intelligent and creative but runs slower.")
    st.write("- GPT-3.5-Turbo: Faster but less capable than GPT-4.")

    st.markdown("**2. Token Length Selection**")
    st.write("- Choose between three token lengths: Short, Medium, and Long.")
    st.write("- Short: Good for captions and short descriptions.")
    st.write("- Medium: Good for call-to-action messages and newsletters.")
    st.write("- Long: Good for longer blog posts and articles, as well as short stories and poems.")

    st.markdown("**3. Input Details**")
    st.write("- Provide details like your brand, brand description, industry, and target audience.")
    st.write("- The more accurate your inputs, the better the generated strategy will align with your expectations.")

    st.markdown("**4. Strat Generation**")
    st.write("- Click the 'Generate Strat' button.")
    st.write("- The AI will use your inputs to generate a strat. This process may take a few moments, so your patience is appreciated.")

    st.markdown("**5. Review AI Analysis and First Strat**")
    st.write("- The application will display an AI analysis of your inputs, which gives insights into how the AI perceived your inputs.")
    st.write("- You'll then see the first iteration of the strat of the brand.")

    st.markdown("**6. AI's Second Round of Analysis**")
    st.write("- The AI will critically assess the first strat.")
    st.write("- A second, more refined strat is then presented based on this analysis.")

    st.markdown("**7. Feedback and Revisions**")
    st.write("- If the strat isn't quite right, provide feedback in the designated field.")
    st.write("- Click 'Send Feedback', and the AI will generate a new version of the strat considering your comments.")

    st.markdown("**8. Feedback Thread**")
    st.write("- This section displays all previous feedback and the AI's corresponding responses.")
    st.write("- It's a great way to track changes and see the evolution of the strat.")

    st.write("With these steps, the Dasho Content Co-strategist ensures that you receive quality strategy for your content team to tailor-fit for your brand.")


# Create another collapsible section for user input
expander_inputs = st.expander('Inputs', expanded=True)
with expander_inputs:
    # Create selection boxes for model and token length
    model_options = ['gpt-3.5-turbo', 'gpt-4']
    selected_model = st.selectbox('Select Model:', model_options)
    token_length_options = {
    'Long': 1022,
    'Medium': 550,
    'Short': 150
    }
    selected_token_length = st.selectbox('Token Length:', list(token_length_options.keys()))
    st.markdown("---")

    # Initialize state variables
    if 'strat_gen' not in st.session_state:
        st.session_state['strat_gen'] = None
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

    industry_type_options = [
        '',
        'Agriculture and Farming',
        'Automotive and Transportation',
        'Banking and Finance',
        'Construction and Real Estate',
        'Education and Training',
        'Energy and Utilities',
        'Entertainment and Media',
        'Food and Beverage',
        'Healthcare and Medical',
        'Hospitality and Tourism',
        'Information Technology (IT) and Software',
        'Manufacturing and Production',
        'Nonprofit and Social Services',
        'Retail and Consumer Goods',
        'Telecommunications',
        'Professional Services',
        'Government and Public Administration',
        'Legal Services',
        'Environmental Services',
        'E-commerce and Online Retail',
        'Aerospace and Defense',
        'Pharmaceuticals and Biotechnology',
        'Sports and Recreation',
        'Arts and Culture',
        'Insurance',
        'Marketing and Advertising',
        'Wholesale and Distribution',
        'Transportation and Logistics',
        'Research and Development',
        'Architecture and Design'
    ]
    industry_type = st.selectbox('Industry:', sorted(industry_type_options))
 
    target_audience_options = [
        '',
        'Millennials (Generation Y)',
        'Gen Z (Generation Z)',
        'Baby Boomers',
        'Working Professionals',
        'Parents and Families',
        'Students and Academics',
        'Small Business Owners',
        'Entrepreneurs and Startups',
        'Tech Enthusiasts',
        'Health and Fitness Enthusiasts'
    ]
    target_audience = st.selectbox('Target Audience:',  sorted(target_audience_options))
    additional_instructions = st.text_area('Additional Information (Optional):', '')


# Check if all required fields are filled and the Generate Strat button is clicked
if brand and brand_description and industry_type and target_audience and st.button('Generate Strat'):
    st.markdown("---")
    if not st.session_state['strat_gen']:
        # Initialize the StratGenerator object with the selected token length
        st.session_state['strat_gen'] = StratGenerator(selected_model, brand, brand_description, industry_type, target_audience, additional_instructions, token_length_options[selected_token_length])
    container = st.empty()  # Use empty to be able to continually update the output
    st_callback = StreamlitCallbackHandler(container)  # Initialize the Streamlit callback handler
    response = st.session_state['strat_gen'].generate(st_callback)  # Pass the callback handler to the generate method
    st.session_state['output_generated'] = True
    st.session_state['current_response'] = response
    container.write("")  # Clears the container after use

# Create an optional collapsible section to display output
output_expander = st.expander("Show/Hide Output", expanded=True)
with output_expander:
    if st.session_state['output_generated']:
        response = st.session_state.get('current_response', {})
        st.header("FINAL OUTPUT")

        # Display Brand Summary
        st.subheader("AI Brand Summary")
        st.write(response['AI_analysis'].strip())

        # Display Brand Strategy
        st.subheader("Content Strategy")
        st.write(response['first_draft'].strip())

        # Display Content Topics or Content Pillars
        st.subheader("Content Plan")
        strat_text = response['AI_analysis_2'].strip().split("|")
        for section in strat_text:
            st.write(" ", section)

        # Display Content Subtopoics or Content Buckets
        st.subheader("Content Execution")
        st.write(response['final_output'].strip())
    
# Check if feedback has been provided by the user
if st.session_state['output_generated']:
    st.markdown("---")
    if 'user_feedback' not in st.session_state:
        st.session_state['user_feedback'] = ''

    user_feedback = st.text_input('Feedback:', value=st.session_state['user_feedback'])

    if st.button('Send Feedback') and user_feedback:
        # Initialize the Streamlit callback handler and generate the output
        st_callback = StreamlitCallbackHandler(st.empty())  # Initialize the Streamlit callback handler
        new_response = st.session_state['strat_gen'].generate_with_feedback(user_feedback, st_callback)  # Pass the callback handler to the generate_with_feedback method

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

# Add copyright notice and support email at the bottom
st.caption("© 2023 DashoContent. All rights reserved.")
st.caption("Email for support or feedback: info@contentdash.app")