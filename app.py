from __future__ import print_function
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import sounddevice as sd
import speech_recognition as sr
import soundfile as sf
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu 
import googleformsapi
import chatgptapi
import pyperclip

# Config the page
st.set_page_config(page_title="Quiz", page_icon=":hourglass:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load assets
# URL de téléchargement direct de l'animation Lottie
lottie_url = "https://drive.google.com/uc?id=1jGWyBTXElRvCYb0fjSPvMifUw5z3tLP7&export=download"

# Fonction pour charger l'animation Lottie depuis l'URL
def load_lottie_animation(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

if "form" not in st.session_state:
    st.session_state["form"] = ""
    
# NavBar
with st.sidebar:
    selected = option_menu(
        menu_title="", #required
        options=["About Us","Generate","Contact Us"],#required
        icons = ["house","book","envelope"],
        menu_icon="cast",
        default_index=0,  
        )
# About Us Section
# About Us Section
if selected == "About Us":
    with st.container():
        left_column, right_column = st.columns([1.2,1])
        with left_column:
            # Define the text
            text = "Simply Speak and generate quizzes effortlessly"

            # Apply HTML formatting to change the color
            colored_text = f"<span style='color: #ff4b4b;'>{text}</span>"

            # Render the colored text using markdown
            st.markdown(f"<h3>{colored_text}</h3>", unsafe_allow_html=True)

            st.write("##")
            # Define the text content
            text = """
            Are you tired of spending valuable time creating quizzes from scratch? Look no further! 
            Our innovative Audio-to-Quiz Generator revolutionizes the way quizzes are created, making
            the process seamless, efficient, and highly personalized."""

            # Apply CSS styling to justify the text
            justified_text = f"<p style='text-align: justify;'>{text}</p>"

            # Render the justified text using markdown
            st.markdown(justified_text, unsafe_allow_html=True)
            
            st.write('##')
        
        with right_column:
            #st.header("SimplySpeak")
            # Displaying an image from a file
            image_file = "logo-black (1).svg"
            #st.image(image_file, format="svg")
            # Read the SVG file content
            with open(image_file, "r") as file:
                svg_content = file.read()
                
            components.html(svg_content ,height=500)
        

# Generate Section
elif selected == "Generate":
    # Quiz Subject Section
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            # Define the text
            text = "Quiz Subject"

            # Apply HTML formatting to change the color
            colored_text = f"<span style='color: #ff4b4b;'>{text}</span>"

            # Render the colored text using markdown
            st.markdown(f"<h3>{colored_text}</h3>", unsafe_allow_html=True)

            st.write("##")
            text = """
            We kindly request you to begin recording your audio with the following format: 
            """
            # Apply CSS styling to justify the text
            justified_text = f"<p style='text-align: justify;'>{text}</p>"

            # Render the justified text using markdown
            st.markdown(justified_text, unsafe_allow_html=True)
            
            text = """ " Your topic ,  x questions and y choices " 
            """
            
            # Apply CSS styling to justify the text
            justified_text = f"<p style='text-align: justify;'>{text}</p>"

            # Render the justified text using markdown
            st.markdown(justified_text, unsafe_allow_html=True)
            
            
            # Initialize prompt in session state
            if "prompt" not in st.session_state:
                st.session_state["prompt"] = ""

        

            if st.button("Start Recording"):
                    # Start recording audio
                    fs = 44100  # Sample rate
                    duration = 10  # Duration in seconds
                    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

                    # Wait for the recording to finish
                    sd.wait()

                    # Save the recorded audio to a WAV file
                    wav_file = "audio.wav"
                    sf.write(wav_file, recording, fs)

                    # Display the recorded audio
                    st.audio(wav_file)

                    # Convert the audio to text using Google Speech-to-Text API
                    # Start the transcription
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(wav_file) as source:
                        audio = recognizer.record(source)

                    # Wait for the transcription to finish
                    try:
                        transcribed_text = recognizer.recognize_google(audio, language="en-US")
                    except sr.UnknownValueError:
                        print("Speech recognition failed")
                    except sr.RequestError as e:
                        print("An error occurred: {}".format(e))
                    text = recognizer.recognize_google(audio)
                    st.write(text)
                    st.session_state["prompt"] = text  # Update the prompt value in session state
                    # Display the converted text in the prompt
                    # Default_text = st.text_area("  ", value=text)

            

            if st.button("Generate Questions"):
                prompt = st.session_state["prompt"]  # Retrieve the prompt from session state
                if prompt:
                    questions = chatgptapi.generate_questions("Generate a quiz about "+prompt+"without using a, b , c, A, 1 for choices")
                    #print(questions)
                    if questions:
                        content = questions[0]["message"]["content"]
                        resp = []
                        ques = []
                        # Split the data based on the question numbering
                        question_data = content.split('\n\n')

                        for item in question_data:
                            item = item.strip()  # Remove leading/trailing spaces
                            if item:
                                question, choices = item.split('\n', 1)  # Split into question and choices
                                question = question.strip()  # Remove leading/trailing spaces from the question
                                choices = choices.split('\n')  # Split choices into a list
                                choices = [choice.strip() for choice in choices]  # Remove leading/trailing spaces from choices
                                ques.append(question)
                                resp.append(choices)

                        print('Questions ',ques)
                        print('Responses ',resp)
                        
                        """
                        for i in range(len(ques)):
                            st.write(ques[i])
                            for j in range(len(resp[0])):
                                st.write(resp[i][j])
                        """
                        
                        # ques -> Contain the questions
                        # resp -> cona
                        google_from_url = googleformsapi.create_form(ques, resp)
                        st.session_state["form"] = google_from_url
                        
                        # Show Google Forms button
                        if st.button("Show Google Forms"):
                            st.markdown(f'<iframe src="{st.session_state["form"]}" width="800" height="600" frameborder="0" marginheight="0" marginwidth="0">Loading...</iframe>', unsafe_allow_html=True)

                        # Copy link button
                        if st.button("Copy Link"):
                            pyperclip.copy(st.session_state["form"])
                            st.success("Google Forms link copied to clipboard!")
                            st.stop()  # Stop the script execution after copying the link

            with right_column:  
                # Charger l'animation Lottie
                animation_json = load_lottie_animation(lottie_url)

                # Afficher l'animation Lottie à l'aide de st_lottie
                if animation_json is not None:
                    st_lottie(animation_json, height=300)
                else:
                    st.error("Échec du chargement de l'animation Lottie.")
                    
elif selected == "Contact Us":
    
    # Add your content for the Contact Us section here
    with st.container():
        # Define the text
        text = " Get in touch with us using the following contact information:"

        # Apply HTML formatting to change the color
        colored_text = f"<span style='color: #ff4b4b;'>{text}</span>"

        # Render the colored text using markdown
        st.markdown(f"<h3>{colored_text}</h3>", unsafe_allow_html=True)

        st.write("##")

        left_column, right_column = st.columns(2)
        with left_column:
            # Charger l'animation Lottie
                animation_json = load_lottie_animation('https://assets8.lottiefiles.com/packages/lf20_cwqf5i6h.json')
                # Afficher l'animation Lottie à l'aide de st_lottie
                if animation_json is not None:
                    st.markdown(f'<a href="https://github.com/ELGHAZI-85" target="_blank">{st_lottie(animation_json, height=200)}</a>', unsafe_allow_html=True)

                else:
                    st.error("Échec du chargement de l'animation Lottie.")
                
        with right_column:
            # Charger l'animation Lottie
                animation_json = load_lottie_animation('https://assets6.lottiefiles.com/packages/lf20_iotglorw.json')
                # Afficher l'animation Lottie à l'aide de st_lottie
                if animation_json is not None:
                    st.markdown(f'<a href="https://www.linkedin.com/in/fatima-el-ghazi-6ab626228/" target="_blank">{st_lottie(animation_json, height=200)}</a>', unsafe_allow_html=True)
                else:
                    st.error("Échec du chargement de l'animation Lottie.")
        

         

