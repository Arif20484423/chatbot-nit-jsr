import logging
from dotenv import load_dotenv
import streamlit as st
from streamlit_mic_recorder import speech_to_text
from htmlTemplates import css, bot_template, user_template
# from generate import QuestionAnsweringModel
# import pandas as pd
from deep_translator import GoogleTranslator
from langdetect import detect

from embed_data import save_to_vector_db
from qa_bot import create_qa_bot
import json

class ChatBot:
    def __init__(self):
        self.conversation = None
        self.history = None
        # df = pd.read_csv("../data/data2.csv", sep=";")
        # if "model" not in st.session_state:
        #   st.session_state.model = QuestionAnsweringModel(df)
        with open("scraped_data.json", "r", encoding="utf-8") as f:
            scraped_data = json.load(f)

        # 2. Store + Embed
        vectordb = save_to_vector_db(scraped_data)

        # 3. Create QA Chatbot
        self.qa_bot = create_qa_bot(vectordb)

    def main(self):
        logging.basicConfig(level=logging.INFO)
        logging.info("Starting app...")

        load_dotenv()

        st.set_page_config(page_title='Nit Jsr Chatbot',
                           page_icon='./static/robot.jpg', initial_sidebar_state='auto')

        if "history" not in st.session_state:
            st.session_state.history = [
                {
                    "role": "bot",
                    "content": "Hello, I am an Nit Jsr Query Expert. How can I help you?"
                }
            ]

        self.load_ui()

    def generate_response(self, user_question):
        # response = st.session_state.model.generate_response(user_question)
        # return response
        response = self.qa_bot(user_question)
        return response["answer"]

    def load_css_styles(self):
        st.write(css, unsafe_allow_html=True)

    def display_sidebar(self):
        st.sidebar.title("Nit Jsr Chatbot")
        st.sidebar.markdown(
            """
            This is a chatbot that answers questions about Nit Jamshedpur.
            """
        )

    def display_messages(self, history):
        for message in history:
            if message['role'] == 'user':
                st.markdown(user_template.replace(
                    '{{MSG}}', message['content']), unsafe_allow_html=True)
            else:
                st.markdown(bot_template.replace(
                    '{{MSG}}', message['content']), unsafe_allow_html=True)

    def handle_user_input(self, user_question):
        user_answer = self.generate_response(user_question)
        st.session_state.history.append({
            "role": "bot",
            "content": user_answer
        })
        # if user_question:
        #     detected_language=detect(user_question)
        #     translated_question = GoogleTranslator(source='auto', target='en').translate(user_question)
        #     st.session_state.history.append({
        #         "role": "user",
        #         "content": translated_question
        #     })
            
        #     response_content = self.generate_response(translated_question)
        #     final_answer = GoogleTranslator(source='auto', target=detected_language).translate(response_content)
        #     st.session_state.history.append({
        #         "role": "bot",
        #         "content": final_answer
        #     })

    def load_ui(self):
        self.load_css_styles()

        self.display_sidebar()

        st.title('Hello, I am an AI Chatbot for NIT Jamshedpur 👩🏻‍🦰')
        user_question = st.text_input('Ask a question about Nit Jamshedpur:')

        # audio_text = speech_to_text(language="auto", start_prompt="Start recording", stop_prompt="Stop recording", key='stt')
        # if audio_text:
        #     user_question=audio_text
        #     st.write("Voice text: ",audio_text)
        
        # audio_text = None
        # if 'audio_captured' not in st.session_state:
        #     st.session_state.audio_captured = None
        # if st.session_state.audio_captured is None:
        #     audio_text = speech_to_text(language="auto",start_prompt="Start recording",stop_prompt="Stop recording",key="stt")

        #     if audio_text:
        #         st.session_state.audio_captured = audio_text
        #         st.write("Voice text:", audio_text)
        # # Once used, clear it
        # if st.session_state.audio_captured:
        #     self.handle_user_input(st.session_state.audio_captured)
        #     st.session_state.audio_captured = None
        # else:
        #     self.handle_user_input(user_question)

        if "audio_text" not in st.session_state:
            st.session_state.audio_text = None
        new_audio = speech_to_text(language="auto",start_prompt="Start recording",stop_prompt="Stop recording",key="stt")
        if new_audio:
            st.session_state.audio_text = new_audio
            st.write("Voice text:", new_audio)
        if st.session_state.audio_text is not None:
            final_question = st.session_state.audio_text

            # Reset so that next time typed input works
            st.session_state.audio_text = None
        else:
            # Use typed text ONLY when voice isn’t active
            final_question = user_question
        self.handle_user_input(final_question)
        self.display_messages(st.session_state.history)

    def run(self):
        self.main()


if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.run()


# https://www.shiksha.com/college/nit-jamshedpur-national-institute-of-technology-24366/questions-15?sort_by=relevance
# https://education.indianexpress.com/engineering-university/national-institute-of-technology-nit-jamshedpur#faqs
# https://www.indcareer.com/en/nit-jamshedpur-admission/#Frequently_Asked_Questions_FAQs
# https://www.collegedekho.com/colleges/nit-jamshedpur-qna
# https://www.careers360.com/university/national-institute-of-technology-jamshedpur/all-questions?page=15
# https://www.upgrad.com/universities/nit-jamshedpur/admissions/
# https://collegedunia.com/qna?college=25584
