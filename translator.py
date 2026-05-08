import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import tempfile

app = tk.Tk()
app.title("Language Translator — CodeAlpha")
app.geometry("680x680")
app.configure(bg="#0f0f1a")
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

lang_names   = list(LANGUAGES.keys())
target_langs = lang_names[1:]

BG       = "#0f0f1a"
CARD     = "#16162a"
CARD2    = "#1e1e35"
BORDER   = "#2e2e50"
ACCENT   = "#7c3aed"
ACCENT2  = "#6d28d9"
TEXT     = "#f1f0ff"
MUTED    = "#6b7280"
GREEN    = "#10b981"
GREEN2   = "#059669"
PINK     = "#ec4899"
FONT_SM  = ("Arial", 9)
FONT_LG  = ("Arial", 12)
FONT_BOLD= ("Arial", 11, "bold")

# ── Header ─────────────────────────────────────────────────
header = tk.Frame(app, bg=CARD, height=70)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="Language Translator", bg=CARD, fg=TEXT,
         font=("Arial", 17, "bold")).place(x=24, y=10)
tk.Label(header, text="Powered by Google Translate  •  CodeAlpha Task 1",
         bg=CARD, fg=MUTED, font=FONT_SM).place(x=25, y=40)
tk.Label(header, text="  CodeAlpha Internship  ",
         bg=ACCENT, fg="white", font=FONT_SM,
         padx=6, pady=3).place(x=500, y=22)

tk.Frame(app, bg=BORDER, height=1).pack(fill="x")

# ── Main ───────────────────────────────────────────────────
main = tk.Frame(app, bg=BG)
main.pack(fill="both", expand=True, padx=24, pady=16)

# ── Language Row ───────────────────────────────────────────
lang_row = tk.Frame(main, bg=BG)
lang_row.pack(fill="x", pady=(0, 12))

style = ttk.Style()
style.theme_use("clam")
style.configure("M.TCombobox",
                fieldbackground=CARD2,
                background=CARD2,
                foreground=TEXT,
                arrowcolor=ACCENT,
                bordercolor=BORDER,
                lightcolor=CARD2,
                darkcolor=CARD2,
                selectbackground=ACCENT,
                selectforeground="white",
                padding=8)
style.map("M.TCombobox",
          fieldbackground=[("readonly", CARD2)],
          background=[("readonly", CARD2)],
          foreground=[("readonly", TEXT)])

src_card = tk.Frame(lang_row, bg=CARD,
                    highlightbackground=BORDER, highlightthickness=1)
src_card.pack(side="left", expand=True, fill="x")
tk.Label(src_card, text="FROM", bg=CARD, fg=MUTED,
         font=("Arial", 8, "bold")).pack(anchor="w", padx=14, pady=(10,4))
src_combo = ttk.Combobox(src_card, values=lang_names,
                         style="M.TCombobox", state="readonly",
                         font=FONT_LG, width=20)
src_combo.current(0)
src_combo.pack(padx=10, pady=(0,10), fill="x")

swap_frame = tk.Frame(lang_row, bg=BG, width=54)
swap_frame.pack(side="left", padx=8)
swap_frame.pack_propagate(False)

def do_swap():
    s = src_combo.get()
    t = tgt_combo.get()
    if s != "Auto Detect":
        src_combo.set(t)
        tgt_combo.set(s)

swap_btn = tk.Label(swap_frame, text="⇄", bg=CARD2, fg=ACCENT,
                    font=("Arial", 18, "bold"), cursor="hand2",
                    highlightbackground=BORDER, highlightthickness=1)
swap_btn.pack(expand=True, fill="both")
swap_btn.bind("<Button-1>", lambda e: do_swap())
swap_btn.bind("<Enter>",    lambda e: swap_btn.configure(bg=ACCENT, fg="white"))
swap_btn.bind("<Leave>",    lambda e: swap_btn.configure(bg=CARD2,  fg=ACCENT))

tgt_card = tk.Frame(lang_row, bg=CARD,
                    highlightbackground=BORDER, highlightthickness=1)
tgt_card.pack(side="left", expand=True, fill="x")
tk.Label(tgt_card, text="TO", bg=CARD, fg=MUTED,
         font=("Arial", 8, "bold")).pack(anchor="w", padx=14, pady=(10,4))
tgt_combo = ttk.Combobox(tgt_card, values=target_langs,
                         style="M.TCombobox", state="readonly",
                         font=FONT_LG, width=20)
tgt_combo.current(1)
tgt_combo.pack(padx=10, pady=(0,10), fill="x")

# ── Input Box ──────────────────────────────────────────────
in_frame = tk.Frame(main, bg=CARD,
                    highlightbackground=BORDER, highlightthickness=1)
in_frame.pack(fill="x", pady=(0,4))

in_top = tk.Frame(in_frame, bg=CARD)
in_top.pack(fill="x", padx=14, pady=(10,4))
tk.Label(in_top, text="ENTER TEXT", bg=CARD, fg=MUTED,
         font=("Arial", 8, "bold")).pack(side="left")
char_var = tk.StringVar(value="0 / 500")
tk.Label(in_top, textvariable=char_var, bg=CARD,
         fg=MUTED, font=FONT_SM).pack(side="right")

input_text = tk.Text(in_frame, height=5, bg=CARD, fg=TEXT,
                     font=FONT_LG, insertbackground=ACCENT,
                     relief="flat", padx=14, pady=6,
                     wrap="word", selectbackground=ACCENT,
                     selectforeground="white", bd=0)
input_text.pack(fill="x", pady=(0,10))

def on_key(e):
    c = len(input_text.get("1.0", "end").strip())
    char_var.set(f"{c} / 500")
input_text.bind("<KeyRelease>", on_key)

# ── Translate Button ───────────────────────────────────────
def make_btn(parent, text, color, hover, cmd):
    b = tk.Button(parent, text=text, bg=color, fg="white",
                  font=FONT_BOLD, relief="flat", cursor="hand2",
                  pady=10, command=cmd, bd=0,
                  activebackground=hover, activeforeground="white")
    b.bind("<Enter>", lambda e: b.configure(bg=hover))
    b.bind("<Leave>", lambda e: b.configure(bg=color))
    return b

make_btn(main, "Translate  →", ACCENT, ACCENT2,
         lambda: do_translate()).pack(fill="x", pady=8)

# ── Output Box ─────────────────────────────────────────────
out_frame = tk.Frame(main, bg=CARD,
                     highlightbackground=BORDER, highlightthickness=1)
out_frame.pack(fill="x", pady=(0,10))

out_top = tk.Frame(out_frame, bg=CARD)
out_top.pack(fill="x", padx=14, pady=(10,4))
tk.Label(out_top, text="TRANSLATION", bg=CARD, fg=MUTED,
         font=("Arial", 8, "bold")).pack(side="left")
status_var = tk.StringVar()
status_lbl = tk.Label(out_top, textvariable=status_var,
                      bg=CARD, fg=GREEN, font=FONT_SM)
status_lbl.pack(side="right")

output_text = tk.Text(out_frame, height=5, bg=CARD, fg=GREEN,
                      font=FONT_LG, relief="flat", padx=14,
                      pady=6, wrap="word", state="disabled",
                      selectbackground=GREEN2,
                      selectforeground="white", bd=0)
output_text.pack(fill="x", pady=(0,10))

# ── Action Buttons ─────────────────────────────────────────
btn_row = tk.Frame(main, bg=BG)
btn_row.pack(fill="x", pady=(0,8))

make_btn(btn_row, "Speak",  GREEN,  GREEN2, lambda: do_speak()).pack(side="left", expand=True, fill="x", padx=(0,6))
make_btn(btn_row, "Copy",   CARD2,  BORDER, lambda: do_copy()).pack(side="left", expand=True, fill="x", padx=6)
make_btn(btn_row, "Clear",  CARD2,  BORDER, lambda: do_clear()).pack(side="left", expand=True, fill="x", padx=(6,0))

# ── Footer ─────────────────────────────────────────────────
tk.Frame(app, bg=BORDER, height=1).pack(fill="x")
tk.Label(app, text="Language Translator  •  CodeAlpha AI Internship  •  Task 1",
         bg=CARD, fg=MUTED, font=FONT_SM, pady=8).pack(fill="x")

# ── Logic ──────────────────────────────────────────────────
def do_translate():
    text = input_text.get("1.0", "end").strip()
    if not text:
        messagebox.showwarning("Empty", "Please enter some text first.")
        return
    try:
        status_var.set("Translating...")
        status_lbl.configure(fg=MUTED)
        app.update()
        src = LANGUAGES[src_combo.get()]
        tgt = LANGUAGES[tgt_combo.get()]
        result = GoogleTranslator(source=src, target=tgt).translate(text)
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("end", result)
        output_text.configure(state="disabled")
        status_var.set("✓ Translation successful")
        status_lbl.configure(fg=GREEN)
    except Exception as e:
        status_var.set(f"✗ Error: {e}")
        status_lbl.configure(fg=PINK)

def do_speak():
    text = output_text.get("1.0", "end").strip()
    if not text:
        messagebox.showwarning("Empty", "Translate something first.")
        return
    try:
        import os, time
        tgt = LANGUAGES[tgt_combo.get()]
        tts = gTTS(text=text, lang=tgt)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        audio_path = os.path.join(os.path.expanduser("~"), f"tts_{int(time.time())}.mp3")
        tts.save(audio_path)
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        status_var.set("Speaking...")
        status_lbl.configure(fg=GREEN)
    except Exception as e:
        status_var.set(f"✗ TTS Error: {e}")
        status_lbl.configure(fg=PINK)
        
def do_copy():
    text = output_text.get("1.0", "end").strip()
    if text:
        app.clipboard_clear()
        app.clipboard_append(text)
        status_var.set("✓ Copied!")
        status_lbl.configure(fg=GREEN)

def do_clear():
    input_text.delete("1.0", "end")
    output_text.configure(state="normal")
    output_text.delete("1.0", "end")
    output_text.configure(state="disabled")
    status_var.set("")
    char_var.set("0 / 500")

app.mainloop()