import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import tempfile

app = tk.Tk()
app.title("Language Translator — CodeAlpha")
app.geometry("600x520")
app.configure(bg="#2b2b3b")
app.resizable(False, False)

pygame.mixer.init()

LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Urdu": "ur",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Turkish": "tr",
    "Dutch": "nl",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Punjabi": "pa",
}

lang_names = list(LANGUAGES.keys())

BG     = "#2b2b3b"
BOX    = "#1e1e2e"
ACCENT = "#7c3aed"
TEXT   = "#e2e8f0"
MUTED  = "#9ca3af"
GREEN  = "#6ee7b7"
FONT     = ("Segoe UI", 11)
FONT_BIG = ("Segoe UI", 13)

def styled_label(parent, text, **kw):
    return tk.Label(parent, text=text, bg=BG, fg=MUTED, font=FONT, **kw)

tk.Label(app, text="Language Translator", bg=BG, fg="#a78bfa",
         font=("Segoe UI", 16, "bold")).pack(pady=(18, 4))
tk.Label(app, text="CodeAlpha Internship — Task 1", bg=BG,
         fg=MUTED, font=("Segoe UI", 9)).pack(pady=(0, 14))

sel_frame = tk.Frame(app, bg=BG)
sel_frame.pack(padx=30, fill="x")

styled_label(sel_frame, "Source language:").grid(row=0, column=0, sticky="w", pady=4)
src_combo = ttk.Combobox(sel_frame, values=lang_names, font=FONT, state="readonly", width=28)
src_combo.current(0)
src_combo.grid(row=0, column=1, padx=(10,0), pady=4)

styled_label(sel_frame, "Target language:").grid(row=1, column=0, sticky="w", pady=4)
tgt_combo = ttk.Combobox(sel_frame, values=lang_names[1:], font=FONT, state="readonly", width=28)
tgt_combo.current(1)
tgt_combo.grid(row=1, column=1, padx=(10,0), pady=4)

styled_label(app, "Enter text to translate:").pack(anchor="w", padx=30, pady=(10,2))
input_text = tk.Text(app, height=5, width=68, bg=BOX, fg=TEXT,
                     font=FONT_BIG, insertbackground=TEXT,
                     relief="flat", padx=10, pady=8, wrap="word")
input_text.pack(padx=30)

btn_frame = tk.Frame(app, bg=BG)
btn_frame.pack(pady=10, padx=30, fill="x")

def do_translate():
    text = input_text.get("1.0", "end").strip()
    if not text:
        messagebox.showwarning("Empty", "Please enter some text first.")
        return
    try:
        src = LANGUAGES[src_combo.get()]
        tgt = LANGUAGES[tgt_combo.get()]
        result = GoogleTranslator(source=src, target=tgt).translate(text)
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("end", result)
        output_text.configure(state="disabled")
        status_var.set("Translation successful")
        status_label.configure(fg=GREEN)
    except Exception as e:
        status_var.set(f"Error: {e}")
        status_label.configure(fg="#f87171")

def do_speak():
    text = output_text.get("1.0", "end").strip()
    if not text:
        messagebox.showwarning("Empty", "Translate something first.")
        return
    try:
        tgt = LANGUAGES[tgt_combo.get()]
        tts = gTTS(text=text, lang=tgt)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            pygame.mixer.music.load(f.name)
            pygame.mixer.music.play()
        status_var.set("Speaking...")
        status_label.configure(fg=GREEN)
    except Exception as e:
        status_var.set(f"TTS Error: {e}")
        status_label.configure(fg="#f87171")

def do_copy():
    text = output_text.get("1.0", "end").strip()
    if text:
        app.clipboard_clear()
        app.clipboard_append(text)
        status_var.set("Copied to clipboard!")
        status_label.configure(fg=GREEN)

def do_clear():
    input_text.delete("1.0", "end")
    output_text.configure(state="normal")
    output_text.delete("1.0", "end")
    output_text.configure(state="disabled")
    status_var.set("")

BTN_CFG = dict(font=("Segoe UI", 10, "bold"), relief="flat",
               padx=12, pady=7, cursor="hand2")

tk.Button(btn_frame, text="Translate", bg=ACCENT, fg="white",
          command=do_translate, **BTN_CFG).pack(side="left", expand=True, fill="x", padx=(0,4))
tk.Button(btn_frame, text="Speak", bg="#1d9e75", fg="white",
          command=do_speak, **BTN_CFG).pack(side="left", padx=4)
tk.Button(btn_frame, text="Copy", bg="#3b3b50", fg=TEXT,
          command=do_copy, **BTN_CFG).pack(side="left", padx=4)
tk.Button(btn_frame, text="Clear", bg="#3b3b50", fg=TEXT,
          command=do_clear, **BTN_CFG).pack(side="left", padx=(4,0))

styled_label(app, "Translation:").pack(anchor="w", padx=30, pady=(2,2))
output_text = tk.Text(app, height=5, width=68, bg=BOX, fg=GREEN,
                      font=FONT_BIG, relief="flat", padx=10, pady=8,
                      wrap="word", state="disabled")
output_text.pack(padx=30)

status_var = tk.StringVar()
status_label = tk.Label(app, textvariable=status_var, bg=BG, fg=GREEN, font=FONT)
status_label.pack(pady=6)

app.mainloop()