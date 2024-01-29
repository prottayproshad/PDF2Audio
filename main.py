import os
import pyttsx3
import PyPDF2
from tkinter import Tk, Button, Label, filedialog, StringVar, ttk
from threading import Thread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class PDFToSpeechApp:
    def __init__(self, master):
        self.master = master
        master.title("Pratoy's Audio Converter")
        master.geometry("800x450")

        self.frame = ttk.Frame(master)
        self.frame.pack(expand=True, fill="both", anchor="center")

        self.label = Label(self.frame, text="Select the target PDF file:")
        self.label.pack(pady=(100, 10), side="top")

        self.select_button = Button(self.frame, text="Upload", command=self.browse_pdf)
        self.select_button.pack(pady=10)

        self.convert_button = Button(self.frame, text="Convert to AudioBook", command=self.convert_to_mp3)
        self.convert_button.pack_forget()

        self.progress_bar = ttk.Progressbar(self.frame, mode="indeterminate")
        self.progress_bar.pack_forget()

        self.file_label_var = StringVar()
        self.file_label = Label(self.frame, textvariable=self.file_label_var)
        self.file_label.pack(pady=10)

        self.pdf_path = ""
        self.output_path = ""

    def browse_pdf(self):
        self.pdf_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")])
        self.file_label_var.set(os.path.basename(self.pdf_path))
        self.convert_button.pack(pady=5)

    def convert_to_mp3(self):
        if not self.pdf_path:
            return

        # Disable UI elements during conversion
        self.select_button.config(state="disabled")
        self.convert_button.config(state="disabled")
        

        # Run conversion in a separate thread to avoid freezing the UI
        conversion_thread = Thread(target=self.perform_conversion)
        conversion_thread.start()
        

    def perform_conversion(self):
        pdf_text = self.extract_text_from_pdf(self.pdf_path)

        self.output_path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3")]
        )
        self.progress_bar.pack(pady=5)
        self.progress_bar.start()

        self.output_path = os.path.splitext(self.output_path)[0] + ".mp3"

        self.text_to_speech(pdf_text, self.output_path)

        # Enable UI elements after conversion
        self.select_button.config(state="normal")
        self.convert_button.config(state="normal")
        self.progress_bar.stop()

        # Update label to indicate completion
        self.file_label_var.set("Done")
        self.convert_button.pack_forget()
        self.progress_bar.pack_forget()

    def text_to_speech(self, text, output_file):
        engine = pyttsx3.init()
        # engine.say(text)
        engine.save_to_file(text, output_file)
        engine.runAndWait()

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
        except Exception as e:
            print(f"Error: {e}")
        return text

if __name__ == "__main__":
    root = Tk()
    app = PDFToSpeechApp(root)
    root.mainloop()