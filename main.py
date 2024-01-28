import os
import time
import tkinter as tk
from os.path import join
from tkinter import Button, INSERT, END, messagebox
from tkinter import filedialog, Label

import PyPDF2
import gtts
import playsound

BGCOLOR = '#DCF2F1'

pdf_file = None


# Pick where to save audio
def the_path():
    path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    path = str(path)
    print(path)
    return path


# Upload PDF
def Upload():
    global pdf_file
    open('book.txt', 'w').close()
    filename = filedialog.askopenfilename(initialdir='/', title='Select a picture',
                                          filetypes=(('pdf files', '*.pdf'), ('all files', '*.*')))

    pdf_file = PyPDF2.PdfReader(filename)
    for i in range(len(pdf_file.pages)):
        with open('book.txt', 'a', encoding="utf-8") as book:
            text = pdf_file.pages[i].extract_text()
            book.write(f'{text}\n')

        with open('book.txt', 'r', encoding="utf-8") as doc:
            pdf_preview.insert(INSERT, doc.read())


# Convert and Save
def speak(text):
    global audio, tts
    time.sleep(2.5)
    if os.path.exists("voice.mp3"):
        os.remove("voice.mp3")
    else:
        messagebox.showerror(title='Error', message='There is no file to convert. Please upload first')
    tts = gtts.gTTS(text=text, lang=clicked.get())
    audio = 'voice.mp3'
    tts.save(audio)

    def save():
        path = the_path()
        audio_to_save = f'{join(path)}'
        tts.save(audio_to_save)
        pdf_preview.delete(1.0, END)

    return save


# play audio in the app
def preview():
    time.sleep(2)
    global audio
    try:
        playsound.playsound(audio)
    except NameError:
        messagebox.showerror(title='Error', message='There is no file to preview. Please upload and/or convert first')


# convert PDF to audio
def convert():
    global pdf_to_read
    with open('book.txt', encoding="utf-8") as book:
        pdf_to_read = book.read()
        speak(pdf_to_read)


def Save():
    try:
        save_audio = speak(pdf_to_read)
        save_audio()
    except NameError:
        messagebox.showerror(title='Error', message='There is no file to save. Please upload and/or convert first')


# GUI

window = tk.Tk()
window.title('PDF to Audio')
window.geometry('800x600')
window.config(bg=BGCOLOR)
frame = tk.Frame(window)
frame.config(bg=BGCOLOR)

Title = Label(frame, text='Convert PDF To Audio', bg=BGCOLOR, font=('Bold', 18))
Title.grid(row=0, column=3, columnspan=4)

pdf_preview = tk.Text(frame, width=78, height=10, font=14, padx=20, pady=20)
pdf_preview.grid(row=1, column=0, columnspan=12, pady=40)

button_upload = Button(frame, text='Upload', command=Upload)
button_upload.config(width=20, height=5)
button_upload.grid(row=4, column=0, columnspan=2)

button_convert = Button(frame, text='Convert', command=convert)
button_convert.config(width=20, height=5)
button_convert.grid(row=4, column=2, columnspan=2)

button_preview = Button(frame, text='Preview', command=preview)
button_preview.config(width=20, height=5)
button_preview.grid(row=4, column=4, columnspan=2)

button_save = Button(frame, text='Save', command=Save)
button_save.config(width=20, height=5)
button_save.grid(row=4, column=6, columnspan=2)

button_quit = Button(frame, text='Exit', command=window.quit)
button_quit.config(width=20, height=5)
button_quit.grid(row=4, column=8, columnspan=2)

Language_label = Label(frame, text='Select PDF Language', bg=BGCOLOR)
Language_label.grid(row=2, column=4, columnspan=2)

clicked = tk.StringVar()
clicked.set('en')
language = tk.OptionMenu(frame, clicked, 'en', 'fr', 'es', 'de', 'ar', 'af', 'it', 'pt', 'ru')
language.grid(row=3, column=4, columnspan=2, pady=20)
frame.pack(expand=True)
window.mainloop()
