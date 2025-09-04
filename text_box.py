import tkinter as tk
from queue import Queue, Empty

class TextDisplayGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Display")

        self.root.geometry("800x300")

        self.root.resizable(False, False)
        
        self.text_box = tk.Text(self.root, font=("Arial", 28), wrap="word")
        self.text_box.pack(expand=True, fill="both")

        self.queue = Queue()
        self.poll_queue()

    def poll_queue(self):
        try:
            while True:
                text = self.queue.get_nowait()  # retrieve next item in the queue
                self.text_box.delete("1.0", "end")
                self.text_box.insert("end", text)
        except Empty:
            pass
        
        self.root.after(100, self.poll_queue)  # poll every 100 ms

    def update_text(self, text):
        self.queue.put(text)

    def run(self):
        self.root.mainloop()
