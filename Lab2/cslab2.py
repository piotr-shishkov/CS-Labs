from tkinter import *
from tkinter import Tk, Text, BOTH, W, N, E, S, filedialog
from tkinter.ttk import Frame, Button, Label, Style
from auditparser import ParseAudit

### TKinter frame

class Lab2App(Frame):
    def __init__(self):
        super().__init__()

        self.SetupUi()

    def SetupUi(self):
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.search_entry = Entry(self)
        self.search_entry.grid(sticky=E + W + S + N, pady=10, padx=50, row=0, column=1)

        self.search_entry.focus_set()

        find_bt = Button(self, text='Search...', command=self.Search)
        find_bt.grid(sticky=W, pady=4, padx=5, row=0, column=2)

        open_bt = Button(self, text="Open AUDIT file", command=self.OpenFile)
        open_bt.grid(sticky=S, row=5, column=0, pady=4, padx=50)

        save_bt = Button(self, text="Save AUDIT file", command=self.SaveFile)
        save_bt.grid(sticky=S, row=5, column=2, pady=4, padx=50)

        self.text_field = Text(self)
        self.text_field.grid(row=1, column=0, columnspan=3, rowspan=4,
                             padx=5, sticky=E + W + S + N)

        self.scrollbar = Scrollbar(self)
        self.text_field.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_field.yview)
        self.scrollbar.grid(column=3, row=1, rowspan=4, sticky=N + S + W)

    def OpenFile(self):
        file = filedialog.askopenfile(mode="r", defaultextension=".audit", filetypes=[("Audit files", "*.audit")])

        if not file:
            return

        f = open(file.name, "r")

        structure = ParseAudit(f.read())

        self.text_field.config(state=NORMAL)
        structure = [cols[2:] for cols in structure]
        structure = [item for s in structure for item in s]

        self.checkbuttons = []
        self.vars = []

        for i in range(len(structure)):
            var = IntVar(value=0)
            cb = Checkbutton(self.text_field, text=structure[i], variable=var, onvalue=1, offvalue=0,
                             bg='white', cursor='hand2', wraplength=900, justify=LEFT)
            self.text_field.window_create("end", window=cb)
            self.text_field.insert("end", "\n")
            self.checkbuttons.append(cb)
            self.vars.append(var)

        self.text_field.config(state=DISABLED)

    def SaveFile(self):
        file = filedialog.asksaveasfile(mode="w", defaultextension=".audit")
        f = open(file.name, "w")
        for cb, var in zip(self.checkbuttons, self.vars):
            text = cb.cget("text")
            value = var.get()
            if value == 1:
                f.write("%s\n" % (text))
        f.close()

    def Search(self):
        self.text_field.tag_remove('found', '1.0', END)

        s = self.search_entry.get()
        if s:
            idx = '1.0'
            while 1:
                idx = self.text_field.search(s, idx, nocase=1,
                                             stopindex=END)
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(s))

                self.text_field.tag_add('found', idx, lastidx)
                idx = lastidx

            self.text_field.tag_config('found', foreground='red')
        self.search_entry.focus_set()

### MAIN CODE

root = Tk()
app = Lab2App()
root.title("CS Lab #2 | Piotr Shishkov (FAF-193)")
root.geometry("900x600")
root.mainloop()