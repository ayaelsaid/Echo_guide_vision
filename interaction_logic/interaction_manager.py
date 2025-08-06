import os
import PIL.Image

from config import (
    IMAGE_SAVE_DIRECTORY, IMAGE_FILENAME,
    AUDIO_RECORD_DURATION, AUDIO_FOLLOW_UP_DURATION
)

class InteractionManager:
    """Manages the overall interaction flow with the user."""

    def __init__(self, camera_handler, speak_func, record_audio_func, speech_to_text_func,
                 save_image_func, save_interaction_func, load_interaction_func, init_ai):
        self.camera_handler = camera_handler
        self.speak = speak_func
        self.record_audio_once = record_audio_func
        self.speech_to_text = speech_to_text_func
        self.save_pil_image_to_disk = save_image_func
        self.save_last_interaction_orm = save_interaction_func
        self.load_last_interaction_orm = load_interaction_func
        self.init_ai = init_ai
        self.current_image = None
        self.current_saved_image_path = None

    def _get_gemma_3n_response(self, user_question, image):
        """Helper to get response from Gemini model."""
        try:
            response = self.init_ai(image, user_question)
            return response if response else "Sorry, I did not receive a response from the Gemini model."
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "I'm having trouble connecting to the AI. Please try again later."
            

    def start_interaction_flow(self):
        """
        Runs the full interaction loop with the user.
        Returns the final state after the interaction ends.
        """
        print("Starting interaction flow...")

        self.camera_handler.start_camera()
        self.speak('Hi there! How can I help you?')

        try:
            while True:
                if self.current_image is None:
                    self.speak('Please look at the camera for a moment.')
                    img = self.camera_handler.take_capture()
                    if img is None:
                        self.speak("Sorry, I couldn't capture an image. Please try again.")
                        break

                    # Save the newly captured image to disk, overwriting the old one.
                    self.current_saved_image_path = self.save_pil_image_to_disk(img,
                                                                                save_directory=IMAGE_SAVE_DIRECTORY,
                                                                                filename=IMAGE_FILENAME)
                    if self.current_saved_image_path is None:
                        self.speak("Failed to save the captured image. Please try again.")
                        break
                    

                    self.current_image = img 

                self.speak('Now, please ask your question about the image.')
                user_audio_data = self.record_audio_once(duration_seconds=AUDIO_RECORD_DURATION)
                user_question = self.speech_to_text(user_audio_data)

                if not user_question:
                    self.speak('Sorry, I could not hear you clearly. I will describe the image generally.')
                    user_question = "Describe this image please."
                else:
                    self.speak(f'You said: {user_question}')

                print("Sending image and question to Gemini...")
                ai_response = self._get_gemma_3n_response(user_question, self.current_image)
                print(ai_response)
                self.speak(ai_response)

                self.save_last_interaction_orm(user_question, ai_response, self.current_saved_image_path)

                self.speak('Do you have another question or anything else you want to ask? Please say yes or no.')
                follow_up_audio = self.record_audio_once(duration_seconds=AUDIO_FOLLOW_UP_DURATION)
                follow_up_text = self.speech_to_text(follow_up_audio)

                if "yes" in follow_up_text.lower():
                    choice_understood = False
                    choice_attempts = 0
                    max_choice_attempts = 3

                    while not choice_understood and choice_attempts < max_choice_attempts:
                        if choice_attempts == 0:
                            self.speak('Do you want to ask about a "new picture", "same picture", or recall "previous interaction"?')
                        else:
                            self.speak(f"I still didn't understand. Please say clearly: 'new', 'same', or 'previous'. (Attempt {choice_attempts + 1} of {max_choice_attempts})")

                        choice_audio = self.record_audio_once(duration_seconds=AUDIO_FOLLOW_UP_DURATION)
                        choice_text = self.speech_to_text(choice_audio).lower()

                        print(f"DEBUG: User's choice understood as: {choice_text}")

                        new_keywords = ["new", "another", "fresh"]
                        same_keywords = ["same", "similar"]
                        previous_keywords = ["previous", "old", "last"]

                        if any(keyword in choice_text for keyword in new_keywords):
                            self.current_image = None
                            self.current_saved_image_path = None
                            self.speak("Alright, let's take another picture.")
                            choice_understood = True

                        elif any(keyword in choice_text for keyword in same_keywords):
                            self.speak("Okay, you can ask another question about the current image.")
                            choice_understood = True

                        elif any(keyword in choice_text for keyword in previous_keywords):
                            last_state = self.load_last_interaction_orm()
                            if last_state.get("question") and last_state.get("ai_response"):
                                self.speak(f"Your last question was: '{last_state['question']}', and the AI replied: '{last_state['ai_response']}'.")
                                if last_state.get("image_path") and os.path.exists(last_state["image_path"]):
                                    try:
                                        self.current_image = PIL.Image.open(last_state["image_path"])
                                        self.current_saved_image_path = last_state["image_path"]
                                        self.speak("I've reloaded the picture from our previous interaction. You can ask me about it now.")
                                    except Exception as img_e:
                                        print(f"Error reloading previous image for interaction: {img_e}")
                                        self.speak("I found the previous interaction details, but couldn't load the old picture. Let's take a new one.")
                                        self.current_image = None
                                        self.current_saved_image_path = None
                                else:
                                    self.speak("I found the previous interaction details, but no valid picture was saved or the file is missing. Let's take a new one.")
                                    self.current_image = None
                                    self.current_saved_image_path = None
                            else:
                                self.speak("I don't have a previous interaction saved. Let's take a new picture.")
                                self.current_image = None
                                self.current_saved_image_path = None
                            choice_understood = True

                        else:
                            choice_attempts += 1
                            if choice_attempts < max_choice_attempts:
                                print(f"DEBUG: Choice not understood. Retrying. Attempt {choice_attempts + 1}/{max_choice_attempts}")
                            else:
                                self.speak("I'm sorry, I couldn't understand your choice after multiple attempts. Ending the interaction. Goodbye!")
                                break

                    if not choice_understood and choice_attempts >= max_choice_attempts:
                        break

                elif "no" in follow_up_text.lower() or "enough" in follow_up_text.lower():
                    self.speak("Okay, thank you. Goodbye!")
                    break
                else:
                    self.speak("I didn't understand your response. I will end the interaction now.")
                    self.speak("thank you. Goodbye!")
                    break

        finally:
            self.camera_handler.stop_camera()
            return self.load_last_interaction_orm()