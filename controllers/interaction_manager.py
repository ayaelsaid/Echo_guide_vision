import os
import PIL.Image

from config import (
    IMAGE_SAVE_DIRECTORY, IMAGE_FILENAME,
    AUDIO_RECORD_DURATION, AUDIO_FOLLOW_UP_DURATION
)


class InteractionManager:
    """
    Manages the full multimodal interaction flow between the user and the system.

    Responsibilities:
    - Captures image from camera
    - Records and transcribes user speech
    - Sends image and question to AI model
    - Speaks AI response back to user
    - Handles follow-up choices (new image, same image, or previous interaction)

    Dependencies:
        - camera_handler: Object to manage camera operations
        - factory_speak: Object to handle TTS output
        - record: Object to record audio
        - stt: Object to convert speech to text
        - save_image_func: Function to save PIL image to disk
        - interaction: Object to save/load interaction history
        - get_name: Object to load user name
        - init_ai: Function to query AI model with image and question
    """

    def __init__(self, camera_handler, factory_speak, record, stt,
                 save_image_func, interaction, get_name, init_ai):
        """
        Initializes the interaction manager with all required components.

        Args:
            camera_handler: CameraHandler instance
            factory_speak: TTS handler
            record: Audio recorder
            stt: Speech-to-text processor
            save_image_func: Function to save image to disk
            interaction: ORM handler for saving/loading interactions
            get_name: Object to retrieve user name
            init_ai: Function to query AI model with image and question
        """
        self.camera_handler = camera_handler
        self.factory_speak = factory_speak
        self.record = record
        self.stt = stt
        self.save_pil_image_to_disk = save_image_func
        self.interaction = interaction
        self.get_name = get_name
        self.init_ai = init_ai
        self.current_image = None
        self.current_saved_image_path = None

    def _get_gemma_3n_response(self, user_question, image):
        """
        Sends image and question to Gemini model and returns the response.

        Args:
            user_question (str): The user's question
            image (PIL.Image.Image): The image to analyze

        Returns:
            str: AI response or fallback message on error
        """
        try:
            response = self.init_ai(image, user_question)
            return response if response else "Sorry, I did not receive a response from the Gemini model."
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "I'm having trouble connecting to the AI. Please try again later."

    def start_interaction_flow(self):
        """
        Runs the full interaction loop with the user.

        Flow:
        - Greets user
        - Captures image
        - Records question
        - Sends to AI and speaks response
        - Saves interaction
        - Handles follow-up choices

        Returns:
            dict: Last interaction state containing question, response, and image path
        """
        print("Starting interaction flow...")

        self.camera_handler.start_camera()
        load = self.get_name.load_name()
        name = load.get('name')
        self.factory_speak.speak(f'Hi {name}! How are you doing?')

        try:
            while True:
                if self.current_image is None:
                    self.factory_speak.speak(f'Please set the camera for a moment {name}, I will take photo after 3. 1 2 3')
                    img = self.camera_handler.take_capture()
                    if img is None:
                        self.factory_speak.speak("Sorry, I couldn't capture an image. Please try again.")
                        break

                    self.current_saved_image_path = self.save_pil_image_to_disk(
                        img,
                        save_directory=IMAGE_SAVE_DIRECTORY,
                        filename=IMAGE_FILENAME
                    )
                    if self.current_saved_image_path is None:
                        self.factory_speak.speak("Failed to save the captured image. Please try again.")
                        break

                    self.current_image = img

                self.factory_speak.speak('Now, please ask your question about the image.')
                user_audio_data = self.record.record_audio_once(duration_seconds=AUDIO_RECORD_DURATION)
                user_question = self.stt.speech_to_text(user_audio_data)

                if not user_question:
                    self.factory_speak.speak('Sorry, I could not hear you clearly. I will describe the image generally.')
                    user_question = "Describe this image please."
                else:
                    self.factory_speak.speak(f'You said: {user_question}')

                print("Sending image and question to Gemini...")
                ai_response = self._get_gemma_3n_response(user_question, self.current_image)
                print(ai_response)
                self.factory_speak.speak(ai_response)

                self.interaction.save_last_interaction_orm(user_question, ai_response, self.current_saved_image_path)

                self.factory_speak.speak('Do you have another question or anything else you want to ask? Please say yes or no.')
                follow_up_audio = self.record.record_audio_once(duration_seconds=AUDIO_FOLLOW_UP_DURATION)
                follow_up_text = self.stt.speech_to_text(follow_up_audio)

                if "yes" in follow_up_text.lower():
                    choice_understood = False
                    choice_attempts = 0
                    max_choice_attempts = 3

                    while not choice_understood and choice_attempts < max_choice_attempts:
                        if choice_attempts == 0:
                            self.factory_speak.speak('Do you want to ask about a "new picture", "same picture", or recall "previous interaction"?')
                        else:
                            self.factory_speak.speak(f"I still didn't understand. Please say clearly: 'new', 'same', or 'previous'. (Attempt {choice_attempts + 1} of {max_choice_attempts})")

                        choice_audio = self.record.record_audio_once(duration_seconds=AUDIO_FOLLOW_UP_DURATION)
                        choice_text = self.stt.speech_to_text(choice_audio).lower()

                        print(f"DEBUG: User's choice understood as: {choice_text}")

                        new_keywords = ["new", "another", "fresh"]
                        same_keywords = ["same", "similar"]
                        previous_keywords = ["previous", "old", "last"]

                        if any(keyword in choice_text for keyword in new_keywords):
                            self.current_image = None
                            self.current_saved_image_path = None
                            self.factory_speak.speak("Alright, let's take another picture.")
                            choice_understood = True

                        elif any(keyword in choice_text for keyword in same_keywords):
                            self.factory_speak.speak("Okay, you can ask another question about the current image.")
                            choice_understood = True

                        elif any(keyword in choice_text for keyword in previous_keywords):
                            last_state = self.interaction.load_last_interaction_orm()
                            if last_state.get("question") and last_state.get("ai_response"):
                                self.factory_speak.speak(f"Your last question was: '{last_state['question']}', and the AI replied: '{last_state['ai_response']}'.")
                                if last_state.get("image_path") and os.path.exists(last_state["image_path"]):
                                    try:
                                        self.current_image = PIL.Image.open(last_state["image_path"])
                                        self.current_saved_image_path = last_state["image_path"]
                                        self.factory_speak.speak("I've reloaded the picture from our previous interaction. You can ask me about it now.")
                                    except Exception as img_e:
                                        print(f"Error reloading previous image for interaction: {img_e}")
                                        self.factory_speak.speak("I found the previous interaction details, but couldn't load the old picture. Let's take a new one.")
                                        self.current_image = None
                                        self.current_saved_image_path = None
                                else:
                                    self.factory_speak.speak("I found the previous interaction details, but no valid picture was saved or the file is missing. Let's take a new one.")
                                    self.current_image = None
                                    self.current_saved_image_path = None
                            else:
                                self.factory_speak.speak("I don't have a previous interaction saved. Let's take a new picture.")
                                self.current_image = None
                                self.current_saved_image_path = None
                            choice_understood = True

                        else:
                            choice_attempts += 1
                            if choice_attempts < max_choice_attempts:
                                print(f"DEBUG: Choice not understood. Retrying. Attempt {choice_attempts + 1}/{max_choice_attempts}")
                            else:
                                self.factory_speak.speak("I'm sorry, I couldn't understand your choice after multiple attempts. Ending the interaction. Goodbye!")
                                break

                    if not choice_understood and choice_attempts >= max_choice_attempts:
                        break

                elif "no" in follow_up_text.lower() or "enough" in follow_up_text.lower():
                    self.factory_speak.speak("Okay, thank you. Goodbye!")
                    break
                else:
                    self.factory_speak.speak("I didn't understand your response. I will end the interaction now.")
                    self.factory_speak.speak("Thank you. Goodbye!")
                    break

        finally:
            self.camera_handler.stop_camera()
            return self.interaction.load_last_interaction_orm()