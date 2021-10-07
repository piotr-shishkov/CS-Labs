from tkinter import *
from tkinter import filedialog
from auditparser import ParseAudit

### TKinter frame

class Lab1App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(side="bottom")
        self.parent = parent
        self.parent.configure(background='white')

        self.openBt = Button(self, text="Open Audit File", command=self.OpenFile,
        width=15, height=1, bg="#3483eb", fg="#000000", font=("Arial", "16"))
        self.openBt.pack(side="left")

        self.saveBt = Button(self, text="Save Audit File", command=self.SaveFile,
        width=15, height=1, bg="#7deb34", fg="#000000", font=("Arial", "16"))
        self.saveBt.pack(side="right")

        self.textField = Text(bg="#c2c2c2", fg="black", font=("Arial", "16"))
        self.textField.pack(fill="both", expand=1)

    def OpenFile(self):
        file = filedialog.askopenfile(mode="r", defaultextension=".audit")

        if not file:
            return

        f = open(file.name, "r")
        form = '{}{}'
        structure = ParseAudit(f.read())

        self.textField.config(state="normal")

        for (line, depth, text) in structure:
            self.textField.insert("end", form.format('.  ' * depth, text))
            self.textField.insert("end", '\n')

        self.textField.config(state="disabled")

    def SaveFile(self):
        file = filedialog.asksaveasfile(mode="w", defaultextension=".audit")
        f = open(file.name, "w")
        f.write(self.textField.get("1.0", "end"))
        f.close()

### MAIN CODE

root = Tk()
app = Lab1App(root)
root.title("CS Lab #1 | Piotr Shishkov (FAF-193)")
root.geometry("900x600")
root.mainloop()
