import tkinter as tk
from tkinter import messagebox
from gtts import gTTS
import pygame 
import os

class AudioCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Audio Calculator")
        master.geometry("400x600")
        
        # Display
        self.display = tk.Entry(master, width=30, justify='right', font=('Arial', 20))
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        
        # Buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        # Create buttons
        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            tk.Button(master, text=button, width=10, height=3, command=cmd).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Clear Button
        tk.Button(master, text='C', width=10, height=3, command=self.clear).grid(row=row, column=col, padx=5, pady=5)
        
        # Audio Control Buttons
        self.play_btn = tk.Button(master, text='Play Audio', width=10, height=3, command=self.play_audio)
        self.play_btn.grid(row=row+1, column=0, padx=5, pady=5)
        
        self.pause_btn = tk.Button(master, text='Pause Audio', width=10, height=3, command=self.pause_audio)
        self.pause_btn.grid(row=row+1, column=1, padx=5, pady=5)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Audio file path
        self.audio_file = 'calculator_output.mp3'

    def click(self, key):
        if key == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
                
                # Generate audio for the result
                self.generate_audio(str(result))
            except:
                messagebox.showerror("Error", "Invalid Input")
        else:
            self.display.insert(tk.END, key)

    def clear(self):
        self.display.delete(0, tk.END)
        
        # Stop and unload any playing audio
        pygame.mixer.music.stop()

    def generate_audio(self, text):
        try:
            # Remove existing audio file if it exists
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)
            
            # Convert text to speech
            tts = gTTS(text=f"The result is {text}", lang='en')
            tts.save(self.audio_file)
        except Exception as e:
            messagebox.showerror("Audio Error", str(e))

    def play_audio(self):
        try:
            # Check if audio file exists
            if os.path.exists(self.audio_file):
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.play()
            else:
                messagebox.showinfo("Audio", "No audio available. Calculate something first.")
        except Exception as e:
            messagebox.showerror("Play Error", str(e))

    def pause_audio(self):
        pygame.mixer.music.pause()

def main():
    root = tk.Tk()
    calculator = AudioCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()