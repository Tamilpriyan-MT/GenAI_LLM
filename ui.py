import tkinter as tk
from tkinter import messagebox, Canvas, Scrollbar
from PIL import Image, ImageTk
import os
import requests
import ollama
from llm_axe import OnlineAgent, OllamaChat

class ChatbotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbot")
        self.root.geometry("900x650")
        self.root.configure(bg="#1e1e2e")

        # Load Classic Background Image
        self.bg_label = tk.Label(self.root)
        self.bg_label.place(relwidth=1, relheight=1)
        self.load_background()

        # Header
        self.header = tk.Frame(self.root, bg="#2a2a40", height=60)
        self.header.pack(fill="x")

        tk.Label(self.header, text="AI Chatbot", fg="white", bg="#2a2a40", font=("Arial", 20, "bold")).pack(side="left", padx=20)

        self.new_chat_icon = self.load_icon("new_chat", "https://img.icons8.com/ios/50/ffffff/speech-bubble-with-dots.png")
        self.new_chat_btn = tk.Button(self.header, text=" New Chat", image=self.new_chat_icon, compound="left",
                                      command=self.new_chat, bg="#4caf50", fg="white", font=("Arial", 14, "bold"), padx=10, pady=5)
        self.new_chat_btn.pack(side="right", padx=10, pady=10)

        self.home_icon = self.load_icon("home", "https://img.icons8.com/ios/50/ffffff/home.png")
        self.home_btn = tk.Button(self.header, text=" Home", image=self.home_icon, compound="left",
                                  command=self.go_home, bg="#ff6b6b", fg="white", font=("Arial", 14, "bold"), padx=10, pady=5)
        self.home_btn.pack(side="right", padx=10, pady=10)

        # Chat Area
        self.chat_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.chat_frame.pack(expand=True, fill="both", padx=20, pady=10)

        self.canvas = Canvas(self.chat_frame, bg="#1e1e2e", highlightthickness=0)
        self.scrollbar = Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1e1e2e")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Input Area
        self.input_frame = tk.Frame(self.root, bg="#2a2a40")
        self.input_frame.pack(fill="x", padx=20, pady=10)

        self.user_input = tk.Entry(self.input_frame, bg="#3a3a50", fg="white", font=("Arial", 14), width=70, bd=2, relief="solid")
        self.user_input.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        self.user_input.bind("<Return>", self.send_message)

        self.send_icon = self.load_icon("send", "https://img.icons8.com/ios/50/ffffff/sent.png")
        self.send_btn = tk.Button(self.input_frame, text=" Send", image=self.send_icon, compound="left",
                                  command=self.send_message, bg="#ff6b6b", fg="white", font=("Arial", 14, "bold"), padx=15, pady=8, relief="raised", bd=3)
        self.send_btn.pack(side="right", padx=10, pady=10)

        self.clear_icon = self.load_icon("clear", "https://img.icons8.com/ios/50/ffffff/eraser.png")
        self.clear_btn = tk.Button(self.input_frame, text=" Clear Chat", image=self.clear_icon, compound="left",
                                   command=self.clear_chat, bg="#ffcc00", fg="black", font=("Arial", 14, "bold"), padx=15, pady=8, relief="raised", bd=3)
        self.clear_btn.pack(side="right", padx=10, pady=10)

        # Initialize AI model
        self.model_name = 'mistral'
        self.llm = OllamaChat(model=self.model_name)
        self.online_agent = OnlineAgent(llm=self.llm)
        self.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

    def load_background(self):
        """Downloads and sets a classic-themed background image."""
        image_url = "https://source.unsplash.com/1600x900/?vintage,classic"
        image_path = "classic_background.jpg"

        if not os.path.exists(image_path):
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(image_path, "wb") as file:
                    file.write(response.content)

        if os.path.exists(image_path):
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((900, 650), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            # Set the background image
            self.bg_label.config(image=self.bg_photo)
            self.bg_label.image = self.bg_photo

    def load_icon(self, name, url):
        """Downloads and loads an icon."""
        icon_path = f"{name}.png"
        if not os.path.exists(icon_path):
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(icon_path, "wb") as file:
                    file.write(response.content)

        if os.path.exists(icon_path):
            icon = Image.open(icon_path).resize((20, 20), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(icon)

        return None  # Return None if icon fails to load

    def add_message_bubble(self, text, sender):
        """Creates a chat bubble for user or bot messages."""
        bubble_frame = tk.Frame(self.scrollable_frame, bg="#3a3a50", padx=10, pady=5)
        bubble_label = tk.Label(bubble_frame, text=text, wraplength=500, justify="left",
                                font=("Arial", 14), fg="white", bg="#4caf50" if sender == "user" else "#2a2a40",
                                padx=15, pady=10)

        if sender == "user":
            bubble_frame.pack(anchor="e", padx=10, pady=5)
            bubble_label.pack()
        else:
            bubble_frame.pack(anchor="w", padx=10, pady=5)
            bubble_label.pack()

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    def send_message(self, event=None):
        message = self.user_input.get().strip()
        if message:
            self.add_message_bubble(message, sender="user")
            self.user_input.delete(0, tk.END)

            # Get AI response
            self.messages.append({"role": "user", "content": message})
            response = ollama.chat(model=self.model_name, messages=self.messages)
            ai_response = response['message']['content']
            
            self.add_message_bubble(ai_response, sender="bot")

            self.messages.append({"role": "assistant", "content": ai_response})

    def clear_chat(self):
        """Clears chat bubbles from the UI."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

    def new_chat(self):
        self.clear_chat()
        messagebox.showinfo("New Chat", "Started a new chat session.")

    def go_home(self):
        messagebox.showinfo("Home", "Returning to Home Screen")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotUI(root)
    root.mainloop()
