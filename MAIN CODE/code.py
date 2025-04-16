import speech_recognition as sr
import pyttsx3
import cv2
import mediapipe as mp
import numpy as np
import threading
import time
from pynput import keyboard
import tkinter as tk
from tkinter import ttk, messagebox
import sys

class AccessibilityAssistant:
    def __init__(self):
        # Initialize speech components
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # Initialize sign language components
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils
        
        # UI components
        self.root = tk.Tk()
        self.root.title("Accessibility Assistant")
        self.root.geometry("800x600")
        self.setup_ui()
        
        # State variables
        self.listening = False
        self.sign_language_active = False
        self.camera_thread = None
        self.exit_flag = False
        self.last_sign_time = time.time()
        
        # Keyboard shortcut
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        
    def setup_ui(self):
        """Set up the graphical user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Accessibility Assistant", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Accessibility Modes")
        mode_frame.pack(fill=tk.X, pady=10)
        
        # Voice control section
        voice_frame = ttk.Frame(mode_frame)
        voice_frame.pack(fill=tk.X, pady=5)
        
        self.voice_btn = ttk.Button(voice_frame, text="Start Voice Control", command=self.toggle_voice_control)
        self.voice_btn.pack(side=tk.LEFT, padx=5)
        
        self.voice_status = ttk.Label(voice_frame, text="Status: Inactive", foreground="red")
        self.voice_status.pack(side=tk.LEFT, padx=5)
        
        # Sign language section
        sign_frame = ttk.Frame(mode_frame)
        sign_frame.pack(fill=tk.X, pady=5)
        
        self.sign_btn = ttk.Button(sign_frame, text="Start Sign Language Recognition", command=self.toggle_sign_language)
        self.sign_btn.pack(side=tk.LEFT, padx=5)
        
        self.sign_status = ttk.Label(sign_frame, text="Status: Inactive", foreground="red")
        self.sign_status.pack(side=tk.LEFT, padx=5)
        
        # Output console
        console_frame = ttk.LabelFrame(main_frame, text="Output Console")
        console_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.console = tk.Text(console_frame, height=15, state='disabled')
        scrollbar = ttk.Scrollbar(console_frame, command=self.console.yview)
        self.console.configure(yscrollcommand=scrollbar.set)
        
        self.console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Exit button
        exit_btn = ttk.Button(main_frame, text="Exit", command=self.cleanup_and_exit)
        exit_btn.pack(pady=10)
        
    def log_message(self, message):
        """Add message to the console output"""
        self.console.config(state='normal')
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state='disabled')
        
    def speak(self, text):
        """Convert text to speech"""
        self.log_message(f"Assistant: {text}")
        self.engine.say(text)
        threading.Thread(target=self.engine.runAndWait, daemon=True).start()
        
    def toggle_voice_control(self):
        """Toggle voice control on/off"""
        self.listening = not self.listening
        
        if self.listening:
            self.voice_btn.config(text="Stop Voice Control")
            self.voice_status.config(text="Status: Active", foreground="green")
            self.speak("Voice control activated. How can I help you?")
            threading.Thread(target=self.voice_control_loop, daemon=True).start()
        else:
            self.voice_btn.config(text="Start Voice Control")
            self.voice_status.config(text="Status: Inactive", foreground="red")
            self.speak("Voice control deactivated.")
            
    def voice_control_loop(self):
        """Main loop for voice control"""
        while self.listening and not self.exit_flag:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    self.log_message("Listening...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    
                try:
                    command = self.recognizer.recognize_google(audio).lower()
                    self.log_message(f"User said: {command}")
                    self.process_voice_command(command)
                except sr.UnknownValueError:
                    self.log_message("Could not understand audio")
                except sr.RequestError as e:
                    self.log_message(f"Recognition error: {e}")
                    
            except Exception as e:
                self.log_message(f"Error in voice control: {e}")
                time.sleep(1)
                
    def process_voice_command(self, command):
        """Process recognized voice commands"""
        if 'hello' in command:
            self.speak("Hello there! How can I assist you today?")
        elif 'time' in command:
            current_time = time.strftime("%H:%M")
            self.speak(f"The current time is {current_time}")
        elif 'date' in command:
            current_date = time.strftime("%B %d, %Y")
            self.speak(f"Today's date is {current_date}")
        elif 'stop listening' in command:
            self.listening = False
            self.voice_btn.config(text="Start Voice Control")
            self.voice_status.config(text="Status: Inactive", foreground="red")
            self.speak("Voice control deactivated.")
        elif 'exit' in command or 'quit' in command:
            self.cleanup_and_exit()
        elif 'open' in command:
            app = command.split('open ')[-1]
            self.speak(f"Opening {app}")
            # Add actual application opening logic here
        elif 'search' in command:
            query = command.split('search ')[-1]
            self.speak(f"Searching for {query}")
            # Add actual search logic here
        else:
            self.speak(f"I heard you say: {command}. This is a basic implementation. More commands can be added.")
            
    def toggle_sign_language(self):
        """Toggle sign language recognition on/off"""
        self.sign_language_active = not self.sign_language_active
        
        if self.sign_language_active:
            self.sign_btn.config(text="Stop Sign Language Recognition")
            self.sign_status.config(text="Status: Active", foreground="green")
            self.speak("Sign language recognition activated.")
            self.start_sign_language_recognition()
        else:
            self.sign_btn.config(text="Start Sign Language Recognition")
            self.sign_status.config(text="Status: Inactive", foreground="red")
            self.speak("Sign language recognition deactivated.")
            self.stop_sign_language_recognition()
            
    def start_sign_language_recognition(self):
        """Start the sign language recognition thread"""
        if self.camera_thread is None or not self.camera_thread.is_alive():
            self.camera_thread = threading.Thread(target=self.sign_language_loop, daemon=True)
            self.camera_thread.start()
            
    def stop_sign_language_recognition(self):
        """Stop the sign language recognition"""
        # The loop will check self.sign_language_active and exit when False
        
    def sign_language_loop(self):
        """Main loop for sign language recognition"""
        cap = cv2.VideoCapture(0)
        
        while self.sign_language_active and not self.exit_flag:
            success, image = cap.read()
            if not success:
                continue
                
            # Flip the image horizontally for a later selfie-view display
            image = cv2.flip(image, 1)
            
            # Convert the BGR image to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process the image and detect hands
            results = self.hands.process(image_rgb)
            
            # Draw hand annotations on the image
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                # Sign recognition
                current_time = time.time()
                if current_time - self.last_sign_time > 1:  # Prevent repeated detection
                    self.recognize_sign(results)
                
            # Display the image
            cv2.imshow('Sign Language Recognition', image)
            if cv2.waitKey(5) & 0xFF == 27:  # ESC key
                break
        cap.release()
        cv2.destroyAllWindows()
        
    def recognize_sign(self, results):
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
        
            # Get key landmark positions
            thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]
            index_mcp = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
            wrist = landmarks[self.mp_hands.HandLandmark.WRIST]
            
            # Calculate finger positions
            thumb_extended = thumb_tip.x < wrist.x
            index_extended = index_tip.y < index_mcp.y
            middle_extended = middle_tip.y < index_mcp.y
            ring_extended = ring_tip.y < index_mcp.y
            pinky_extended = pinky_tip.y < index_mcp.y
            
            # "Hello" sign - all fingers raised
            if all([index_extended, middle_extended, ring_extended, pinky_extended]) and thumb_extended:
                self.log_message("Detected sign: Hello")
                self.speak("Hello sign detected")
                self.last_sign_time = time.time()

            # "Help" sign - all fingers curled
            elif not any([index_extended, middle_extended, ring_extended, pinky_extended]):
                self.log_message("Detected sign: Help")
                self.speak("Help sign detected")
                self.last_sign_time = time.time()

            # "Yes" sign - thumb extended, other fingers curled
            elif thumb_extended and not any([index_extended, middle_extended, ring_extended, pinky_extended]):
                self.log_message("Detected sign: Yes")
                self.speak("Yes sign detected")
                self.last_sign_time = time.time()

            # "No" sign - index finger extended, others curled
            elif index_extended and not any([thumb_extended, middle_extended, ring_extended, pinky_extended]):
                self.log_message("Detected sign: No")
                self.speak("No sign detected")
                self.last_sign_time = time.time()

            # "OK" sign - thumb and index touching, others curled
            elif (np.linalg.norm(np.array([thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y])) < 0.03 and
                  not any([middle_extended, ring_extended, pinky_extended])):
                self.log_message("Detected sign: OK")
                self.speak("OK sign detected")
                self.last_sign_time = time.time()

            # "A" sign - closed fist
            elif not any([thumb_extended, index_extended, middle_extended, ring_extended, pinky_extended]):
                self.log_message("Detected sign: A")
                self.speak("A sign detected")
                self.last_sign_time = time.time()

            # "B" sign - all fingers extended
            elif all([thumb_extended, index_extended, middle_extended, ring_extended, pinky_extended]):
                self.log_message("Detected sign: B")
                self.speak("B sign detected")
                self.last_sign_time = time.time()

    def on_key_press(self, key):
        """Handle keyboard shortcuts"""
        try:
            if key == keyboard.Key.f1:
                self.toggle_voice_control()
            elif key == keyboard.Key.f2:
                self.toggle_sign_language()
        except AttributeError:
            pass
            
    def cleanup_and_exit(self):
        """Clean up resources and exit"""
        self.exit_flag = True
        self.listening = False
        self.sign_language_active = False
        
        if self.camera_thread and self.camera_thread.is_alive():
            self.camera_thread.join(timeout=1)
            
        self.root.quit()
        self.root.destroy()
        sys.exit()
        
    def run(self):
        """Run the main application"""
        self.root.protocol("WM_DELETE_WINDOW", self.cleanup_and_exit)
        self.speak("Accessibility Assistant initialized. Press F1 for voice control or F2 for sign language recognition.")
        self.root.mainloop()

if __name__ == "__main__":
    assistant = AccessibilityAssistant()
    assistant.run()