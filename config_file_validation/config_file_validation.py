#!/usr/bin/env python3

"""
Script for checking and editing the configuration file
for calculate engine balance
"""

import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
import re
import yaml

def valid_config():
    """ Validation of Records in config file
    """
    global errors
    errors = []

    for param in texts[2:10]:  # Check for missed parameters in config file
        if param not in mech.keys():
            print('\033[1;31m' + 'Missing parameter "' + param + \
                  '" in config variant "' + entry_mech['combo_config'].get() + \
                  '".\nEdit the file ' + conffile + '!' + '\033[0m')
            msg_error = 'Missing parameter "' + param + '" in config variant "' \
                        + entry_mech['combo_config'].get() + '".\nEdit the file\n' + conffile + '!'
            messagebox.showerror('Error', msg_error)
            yamledit(conffile)
            sys.exit()

    for argue in texts[2:10]:  # Check for missed values in config file
        if mech[argue] is None:
            print('\033[1;31m' + 'Missing value for "' + argue + \
                  '" in config variant "' + entry_mech['combo_config'].get() \
                  + '".\nEdit the file' + conffile + '!' + '\033[0m')
            msg_error = 'Missing value for "' + argue + '" in config variant "' \
                        + entry_mech['combo_config'].get() + '".\nEdit the file\n' + conffile + '!'
            messagebox.showerror('Error', msg_error)
            yamledit(conffile)
            sys.exit()

    for value in mech:  # Check for Data Types and formatting in config file
        if value == 'journals' or value == 'comment':
            pass
        elif value == 'Cylinders':
            if not isinstance(mech[value], int):
                errors.append('"Cylinders" not an integer!')
            if re.search(r',', str(mech[value])):
                errors.append('"," not allowed in ' + value + '!')
        elif value == 'Rows':
            if not isinstance(mech[value], int):
                errors.append('"Rows" not an integer!')
            if re.search(r',', str(mech[value])):
                errors.append('"," not allowed in ' + value + '!')
        else:
            if not isinstance(mech[value], float):
                errors.append('\"' + value + '\"' + 'not an float!')
            if re.search(r',', str(mech[value])):
                errors.append('"," not allowed in ' + value + '!')

    if mech['Rows'] > 2:
        errors.append('"Rows" value should be 1 or 2!')

    try:
        msg_error
    except NameError:
        text_errors['te'].delete(1.0, END)
        for item in errors:
            text_errors['te'].insert(END, item + "\n")

def wid_mech():
    """Build list of mechanical parameters of engine
    """
    global mech
    mech = {}

    for lbl, text, row in zip(lbls_mech_name, texts, rows):
        lbl = Label(frame1, text=text)
        lbl.grid(column=0, row=row, padx=PX, sticky=E)
        lbl.config(background=BG)

    lbl_dim = {}

    for lbl, dimension, row in zip(texts, dimensions, rows):
        lbl_dim[lbl] = Label(frame1, text=dimension)
        lbl_dim[lbl].grid(column=2, row=row, padx=PX, sticky=W)
        lbl_dim[lbl].config(background=BG)

    for mech_name, text, row in tuple(zip(entrys_mech_name, texts, rows)):
        if mech_name == 'combo_config':
            entry_mech[mech_name] = Combobox(frame1)
            entry_mech[mech_name]['values'] = (' '.join(sorted(fullconfig.keys())))
            entry_mech[mech_name].current(0)  # default value
            # entry_mech[mech_name].grid(column=1, row=0, pady=PY, sticky=W)
            config = entry_mech['combo_config'].get()
            mech = fullconfig[config]
            valid_config()
        elif mech_name == 'entry1':
            entry_mech[mech_name] = Text(frame1, width=23, height=4, wrap=WORD)
            entry_mech[mech_name].insert(1.0, str(mech['comment']))
        elif mech_name == 'combo_journal':
            entry_mech[mech_name] = Combobox(frame1, width=20)
            entry_mech[mech_name]['values'] = (' '.join(sorted(mech['journals'])))
            entry_mech[mech_name].current(0)  # default value
            entry_mech[mech_name].grid(column=1, row=9, pady=PY, sticky=W)
        else:
            entry_mech[mech_name] = Entry(frame1, width=20, justify=RIGHT)
            entry_mech[mech_name].insert(0, mech[text])
        entry_mech[mech_name].grid(column=1, row=row, pady=PY, sticky=W)

def config_selected(event):
    """Changes field values when changing configuration
    """
    global mech
    config = entry_mech['combo_config'].get()
    mech = fullconfig[config]
    valid_config()

    for poo, text in zip(entrys_cs, texts_cs):
        if poo == 'combo_journal':
            entry_mech['combo_journal'].delete(0, END)
            entry_mech['combo_journal']['values'] = (' '.join(sorted(mech['journals'])))
            entry_mech['combo_journal'].current(0)
        elif poo == 'entry1':
            entry_mech[poo].delete(1.0, END)
            entry_mech[poo].insert(1.0, str(mech[text]))
        elif poo == 'cell':
            journal_selected_cell(event)
        else:
            entry_mech[poo].delete(0, END)
            entry_mech[poo].insert(0, mech[text])


def journal_selected_cell(event):
    """Changes journals field values when changing journal
    """
    len_j = int(mech['Cylinders'] / mech['Rows'])
    for i, text in zip(range(1, 5), texts_j):
        texts_values = list(map(float, mech['journals']\
                       [str(entry_mech['combo_journal'].get())][text].split(',')))
        for j in range(1, 9):
            cells_in_frame['cell_entry{0}{1}'.format(str(i), str(j))].delete(0, END)

        for j in range(1, len_j + 1):
            cells_in_frame['cell_entry{0}{1}'.format(str(i), str(j))].insert(0, texts_values[j - 1])


def journals_in_cell():
    """Build list of crank parameters
    """
    for j in range(1, 9):
        lbl_number = Label(frame2, text=j, bg=BG, font=('', 7, ''))
        lbl_number.grid(column=j, row=0, padx=PX, pady=0, sticky=S)

    len_j = int(mech['Cylinders'] / mech['Rows'])
    labels_in_frame = {}
    for i, j, text in zip(range(9, 13, 1), range(1, 5), texts_j):
        labels_in_frame['lbl' + str(i)] = Label(frame2, text=text, bg=BG)
        labels_in_frame['lbl' + str(i)].grid(column=0, row=j, padx=PX, pady=6, sticky=E)

    for i in range(1, 5):
        for j in range(1, 9):
            cells_in_frame['cell_entry' + str(i) + str(j)] = Entry(frame2, width=5, justify=RIGHT)
            cells_in_frame['cell_entry' + str(i) + str(j)].grid(row=i, column=j, pady=PY, sticky=W)
    for i, text in zip(range(1, 5), texts_j):
        texts_values = list(map(float, mech['journals']\
                       [str(entry_mech['combo_journal'].get())][text].split(',')))
        for j in range(1, len_j + 1):
            cells_in_frame['cell_entry{0}{1}'.format(str(i), str(j))].insert(0, texts_values[j - 1])

def errors_widget():
    """Build pop-up error frame
    """
    lbl_errors = Label(frame3, text='Detected Errors:')
    lbl_errors.grid(column=0, row=1, padx=PX, sticky=E)
    lbl_errors.config(background=BG)
    text_errors['te'] = Text(frame3, width=55, height=5, fg='red')
    text_errors['te'].grid(column=1, row=1, pady=PY, sticky=W)

def yamledit(conffile):
    """Build-in text editor of configuration
    """
    def new_file():
        global conffile
        conffile = ''
        text.delete(1.0, 'end')
        yamleditor.title('No Name -- ' + TITLE_ED)

    def open_file():
        global conffile
        conffile = filedialog.askopenfilename(defaultextension='.yaml', \
                   filetypes=[('YAML files', '*.yaml *.yml'), ('All files', '*.*')])
        if not conffile:
            return
        yamleditor.title(conffile + ' -- ' + TITLE_ED)
        text.delete(1.0, END)
        with open(conffile, 'r') as f:
            text.insert(INSERT, f.read())

    def save_file():
        global conffile
        if not conffile:
            conffile = filedialog.asksaveasfilename(defaultextension='.yaml', \
                       filetypes=[('YAML files', '*.yaml *.yml'), ('All files', '*.*')])
            yamleditor.title(conffile + ' -- ' + TITLE_ED)
        else:
            # return
            with open(conffile, 'w') as f:
                f.write(text.get(1.0, END))

    def save_file_as(event=None):
        global conffile
        conffile = filedialog.asksaveasfilename(defaultextension=".yaml", \
                   filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")])
        if not conffile:
            return
        yamleditor.title(conffile + ' - Config Editor')
        with open(conffile, "w") as f:
            f.write(text.get(1.0, END))

    def cut():
        text.event_generate("<<Cut>>")

    def copy():
        text.event_generate("<<Copy>>")

    def paste():
        text.event_generate("<<Paste>>")

    def undo(event=None):
        text.event_generate("<<Undo>>")

    def redo(envent=None):
        text.event_generate("<<Redo>>")

    def select_all(event=None):
        text.event_generate("<<SelectAll>>")

    FG_ED = 'black'
    BG_ED = 'snow'
    MYFONT_ED = ('Monospace', 11, '')
    TITLE_ED = 'Config Editor'

    yamleditor = Tk()
    yamleditor.title(TITLE_ED)
    yamleditor.geometry("850x600")

    text = Text(yamleditor, undo=True)
    text.focus_set()
    with open(conffile, 'r') as f:
        text.insert(INSERT, f.read())
    text.config(bg=BG_ED, fg=FG_ED, insertbackground=FG_ED, bd=0, padx=5, \
                pady=5, font=MYFONT_ED, wrap=WORD)
    text.pack(expand=True, fill=BOTH)

    yamleditor.bind('<Control-z>', undo)
    yamleditor.bind('<Control-y>', redo)
    yamleditor.bind('<Control-a>', select_all)
    yamleditor.bind('<Control-s>', save_file)

    bar = Menu(yamleditor)
    file_menu = Menu(bar, tearoff=0)
    file_menu.add_command(label='New', command=new_file)
    file_menu.add_command(label='Open', command=open_file)
    file_menu.add_separator()
    file_menu.add_command(label='Save', command=save_file)
    file_menu.add_command(label='Save as', command=save_file_as)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=yamleditor.quit)
    bar.add_cascade(label='File', menu=file_menu)

    edit_menu = Menu(bar, tearoff=0)
    edit_menu.add_command(label='Undo ', command=undo)
    edit_menu.add_command(label='Redo ', command=redo)
    edit_menu.add_separator()
    edit_menu.add_command(label='Cut', command=cut)
    edit_menu.add_command(label='Copy', command=copy)
    edit_menu.add_command(label='Paste ', command=paste)
    edit_menu.add_separator()
    edit_menu.add_command(label='Select All ', command=select_all)
    bar.add_cascade(label='Edit', menu=edit_menu)

    yamleditor.config(menu=bar)
    yamleditor.mainloop()

def init_config_file():
    """Filling fields with data
    """
    global conffile, fullconfig

    # Config file selection
    conffile = filedialog.askopenfilename(title="Open config file", initialdir="./", \
               filetypes=(("YAML files", "*.yaml *.yml"), ("All files", "*.*")))

    if conffile:
        with open(conffile, 'r') as yamlfile:
            fullconfig = yaml.safe_load(yamlfile)

    frame1.forget()

    errors_widget()

    wid_mech()

    journals_in_cell()

    entry_mech['combo_config'].bind("<<ComboboxSelected>>", config_selected)

    entry_mech['combo_journal'].bind("<<ComboboxSelected>>", journal_selected_cell)

# tkinter window initialisation

PX = 10  # padding x
PY = 5  # padding y
BG = 'grey90'
MYFONT = ("Monospace", 8, "bold")

root = Tk()
root.title("Engine_balance. Configuration file checking and editing tool ")
# root.geometry('540x650')
root.config(background=BG)

mainmenu = Menu(root)
root.config(menu=mainmenu)
configmenu = Menu(mainmenu, tearoff=0)
configmenu.add_command(label="Open YAML File", command=init_config_file)
configmenu.add_command(label="Edit Config As Text", command=lambda: yamledit(conffile))
configmenu.add_command(label="Quit", command=root.destroy)
mainmenu.add_cascade(label="Config", menu=configmenu)


# Top Frame
frame1 = Frame(root, borderwidth=0, bg=BG, padx=0)
frame1.grid(column=0, columnspan=3, row=0, sticky=W)

# Middle Frame
frame2 = Frame(root, borderwidth=0, bg=BG, padx=20)
frame2.grid(column=0, columnspan=3, row=11, sticky=W)

# Bottom Frame
frame3 = Frame(root, borderwidth=0, bg=BG, padx=0)
frame3.grid(column=0, columnspan=3, row=13, sticky=W)

separator = ttk.Separator(master=root, orient=HORIZONTAL)
separator.grid(column=0, row=12, columnspan=3, pady=15, sticky=EW)

entry_mech = {}
text_errors = {}
cells_in_frame = {}

lbls_mech_name = ['lbl_config', 'lbl1', 'lbl2', 'lbl3', 'lbl4', 'lbl5', 'lbl6', 'lbl7', 'lbl8', 'lbl9', 'lbl_journal']
entrys_mech_name = ['combo_config', 'entry1', 'entry2', 'entry3', 'entry4', 'entry5', 'entry6', 'entry7', 'entry8',
                    'entry9', 'combo_journal']
texts = ['Select Config Variant:', 'Comment', 'Cylinders', 'Rows', 'Y', 'mrcp', 'mrot', 'L', 'R', 'Omega',
         'Select Journal:']
rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
dimensions = ['', '', '', '', 'grad', 'kg', 'kg', 'm', 'm', 'sec⁻¹', '']

entrys_cs = ['combo_journal', 'entry1', 'entry2', 'entry3', 'entry4', 'entry5', 'entry6', 'entry7', 'entry8', 'entry9',
             'cell']
texts_cs = [None, 'comment', 'Cylinders', 'Rows', 'Y', 'mrcp', 'mrot', 'L', 'R', 'Omega', 'geometry_angles_l',
            'geometry_angles_r', 'geometry_dists_l', 'geometry_dists_r']

texts_j = ['geometry_angles_l', 'geometry_angles_r', 'geometry_dists_l', 'geometry_dists_r']

init_config_file()

root.mainloop()
