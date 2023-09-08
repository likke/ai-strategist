# langchain_helper.py

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler  
from dotenv import load_dotenv
import os

load_dotenv()

openapi_key = os.getenv("OPENAPI_KEY")

os.environ['OPENAI_API_KEY'] = openapi_key

class StratGenerator:
    def __init__(self, model_name, brand, brand_description, industry_type, target_audience, additional_instructions, max_tokens=822):
        self.llm = ChatOpenAI(temperature=0.8, max_tokens=max_tokens, model_name=model_name, streaming=True)
        self.brand = brand
        self.brand_description = brand_description
        self.industry_type = industry_type
        self.target_audience = target_audience
        self.additional_instructions = additional_instructions

        # Initialize the templates and chains here
        self.initialize_templates_and_chains()

    def initialize_templates_and_chains(self):
        self.setup()

    def setup(self):
        prompt_template_1 = PromptTemplate(
            input_variables=['brand', 'brand_description', 'industry_type', 'target_audience', 'additional_instructions'],
            template="Persona: You are an astute and intelligent group of brand marketers for a Forbes 500 company. \nInstructions: Based on the brand and tagline, description, industry, and target audience, create a brand summary.\nDescription of {brand}: {brand_description}.\nIndustry: {industry_type}\nTarget Audience: {target_audience}\n Additional Instructions: {additional_instructions}\n. Complete the following details for the brand summary and show as result. Be precise based on input but don't change the template: \nTEMPLATE:\nBrand Overview:\nBrand Name:\nBrand Tagline:\nBrand Description:\nBrand Mission/Vision:\nTarget Audience:\nIndustry/Niche:\nKey Competitors:\nPoints of Differentiation:\n(BE SURE TO APPEND '|' as a separator between each of the above fields)\n"
        )

        prompt_template_2 = PromptTemplate(
            input_variables=['AI_analysis', 'brand', 'industry_type', 'target_audience'],
            template="Brand Summary: {AI_analysis}\nBased on the brand summary, create a detailed content analysis for {brand} of Industry: {industry_type} and Target Audience: {target_audience}.\nOutput should be in this template:\nStrengths and Weaknesses:\nMarket Position:\nTop 5 Problems of Brand's Audience:\n:\nGoals of the Content:\nDesired Audience Response:"
        )

        prompt_template_3 = PromptTemplate(
            input_variables=['first_draft', 'brand', 'industry_type', 'target_audience'],
            template="Strategy Phase 1 of {brand}: {first_draft}\nBased on the analysis, make a unique and creative content plan for {brand} in this industry {industry_type} for the {target_audience} target audience. Follow this template for the analysis.\nTop 5 Content Types to Focus on:\nTop 3 Content Platforms to Focus on:\nSuggested Posting Frequency and Schedules:\nKey Messages to Convey:\n"
        )

        prompt_template_4 = PromptTemplate(
            input_variables=['AI_analysis_2', 'brand', 'industry_type', 'target_audience', 'first_draft'],
            template="Strategy Phase 2 of {brand}: {first_draft} \n Based on the content plan at {AI_analysis_2}, make a unique and creative content pillar, content buckets and, initial content titles for {brand} of {industry_type} for {target_audience} as target audience: {AI_analysis_2}\n\n Write in this template:\nTop 5 Content Topics based on Key Messages:\nTop 10 Content Subtopics based on Topics:\nTop 30 Content Titles based on subtopics and content types:\n For the content titles, use this format: content type, suggested platform, execution details. Make each topic and title unique but compelling for the audience based on their top problems:"
        )

        prompt_template_5 = PromptTemplate(
            input_variables=['brand', 'industry_type', 'target_audience', 'user_feedback', 'final_output'],
            template="Latest strat draft you made of {brand} of {industry_type} for {target_audience} as target audience: {final_output}\nThis draft has the following user comment: {user_feedback}\nYour response to the comment:"
        )
        chain_1 = LLMChain(llm=self.llm, prompt=prompt_template_1, output_key="AI_analysis")
        chain_2 = LLMChain(llm=self.llm, prompt=prompt_template_2, output_key="first_draft")
        chain_3 = LLMChain(llm=self.llm, prompt=prompt_template_3, output_key="AI_analysis_2")
        chain_4 = LLMChain(llm=self.llm, prompt=prompt_template_4, output_key="final_output")
        self.chain_5 = LLMChain(llm=self.llm, prompt=prompt_template_5, output_key="final_output_with_feedback")

        self.sequential_chain = SequentialChain(
            chains=[chain_1, chain_2, chain_3, chain_4],
            input_variables=['brand', 'brand_description', 'industry_type', 'target_audience', 'additional_instructions'],
            output_variables=['AI_analysis', 'first_draft', 'AI_analysis_2', 'final_output']
        )

    def generate(self, st_callback):  # Add the callback handler as a parameter
        self.llm.callbacks = [st_callback]  # Set the callback handler

        input_data = {
            'brand': self.brand,
            'brand_description': self.brand_description,
            'industry_type': self.industry_type,
            'target_audience': self.target_audience,
            'additional_instructions': self.additional_instructions
        }

        response = self.sequential_chain(input_data)
        self.previous_response = response  # Save the output to the state
        return response


    def generate_with_feedback(self, user_feedback, st_callback):  # Add the callback handler as a parameter
        self.llm.callbacks = [st_callback]  # Set the callback handler
        input_data = {
            'brand': self.brand,
            'brand_description': self.brand_description,
            'industry_type': self.industry_type,
            'target_audience': self.target_audience,
            'additional_instructions': self.additional_instructions,
            'user_feedback': user_feedback,
            'AI_analysis_2': self.previous_response['AI_analysis_2'],  # Now we're accessing it from the saved state
            'final_output': self.previous_response['final_output']
        }

        response = self.chain_5(input_data)
        return response
