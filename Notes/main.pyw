# Notes App (version 0.1) with csv
from tkinter import *
import os
import string
# Email
import smtplib
from email.message import EmailMessage
from Email_DB import connect
# Date - Time
from datetime import datetime

# Root Window
app = Tk()

# Page Default Colors
bg_color = '#FFFFFF'
fg_color = '#296296'
# Highlight Listbox Items
lb_bg_color = '#DDDDDD'
lb_fg_color = '#2A7FFF'
# Page Default Fonts
font_size = 'Arial, 12'

# New Note
def new_note(*args):

    # Hide New Note Button
    new_note_btn['text'] = ''
    new_note_btn['state'] = DISABLED
    new_note_btn.config(bg=bg_color, fg=bg_color)
    # Create Title Settings
    outer_frame.config(bg=fg_color)
    title_frame.config(bg=fg_color)
    title_label['text'] = 'Note Title:'
    title_label.config(bg=fg_color)
    title_entry.config(fg=fg_color)
    title_entry.focus()
    title_btn['text'] = 'Create'
    title_btn['state'] = NORMAL
    title_btn['command'] = create_title
    app.bind('<Return>', create_title)
    title_btn.config(bg=bg_color, fg=fg_color)


# Create Title
def create_title(*args):
    global get_title

    textarea.delete(1.0, END)
    title_entry.config(fg='#ddd')

    # Getters
    get_title = note_title.get()
    # Cap Title Words
    get_title = string.capwords(get_title)

    # Check if create title field is empty
    if get_title == '':
        title_entry.focus()
        title_entry.config(fg=fg_color)
        textarea['state'] = NORMAL
        textarea.config(fg='#A32627')   # Error msg in red
        textarea.insert(1.0, 'Please create a title for your note!')
    else:
        # Cursor focus on textarea
        textarea['state'] = NORMAL
        textarea.config(fg=fg_color)
        textarea.focus()
        
        # Show hidden footer buttons
        del_btn['text'] = 'Delete ' + get_title
        del_btn.config(bg='#A32627')
        del_btn['command'] = delete_note
        del_btn['state'] = NORMAL
        save_note_btn['text'] = 'Save Note'
        save_note_btn['state'] = NORMAL
        save_note_btn.config(bg=fg_color, fg=bg_color)
        save_note_btn['command'] = save_note
        # If user hits the return key on keyboard..
        # Return a new line in the textarea
        app.bind('<Return>', '\n')


# Save Note
def save_note(*args):
    global filename
    global get_title

    # Getter
    get_text = textarea.get(1.0, END)
    
    # Directory (saved notes use "user input title" as filename)
    filename = 'Notes/' + get_title

    try:
        # Create and write to file
        with open(filename, 'w') as f_write:
            f_write.write('____  ' +  get_title + '  ____' + '\n\n' + get_text)


        # Add new list to the textbox
        listbox_item.insert(0, get_title)
    except:
        # Else show error message
        textarea.config(fg='#A32627')
        textarea.insert(1.0, 'Sorry!\nWe have experienced an issue trying to save your note ' \
                        + get_title + '\n\nPlease try again.')

    # Change textarea color (if red)
    textarea.config(fg=fg_color)
    # Call page settings function
    page_settings()
    


# Delete Note (NOT saved to file at this time)
# Just removing content from screen
def delete_note():

    title_entry.delete(0, END)
    textarea.delete(1.0, END)
    textarea['state'] = DISABLED
    title_entry.focus()
    title_entry.config(bg=bg_color, fg=fg_color)
    app.bind('<Return>', create_title)
    del_btn['text'] = ''
    del_btn['state'] = DISABLED
    del_btn.config(bg=bg_color, fg=bg_color)
    save_note_btn['text'] = ''
    save_note_btn['state'] = DISABLED
    save_note_btn.config(bg=bg_color, fg=bg_color)


# Click on Listbox Item
def list_clicked(event):
    global file_name

    # Clear Email Message
    output_label['text'] = ''
    # Clear and enable the text area
    textarea.delete(1.0, END)
    textarea['state'] = NORMAL

    # New Note Button is now EMAIL BUTTON
    new_note_btn['text'] = 'Email'
    new_note_btn['state'] = NORMAL
    new_note_btn['command'] = prep_email
    app.bind('<Return>', DISABLED)
    new_note_btn.config(bg='#272727', fg=bg_color)

    # Hide title entry
    outer_frame.config(bg=bg_color)
    title_frame.config(bg=bg_color)
    title_label.config(bg=bg_color, fg=bg_color)
    title_entry.config(fg=bg_color)

    # Get (clicked on) listbox item
    selected = listbox_item.curselection()
    selected = int(selected[0])
    item = listbox_item.get(selected)

    # Make sure the (clicked on) listbox item..
    # is the same as in the directory
    if item == os.path.basename('Notes/' + str(item)):
        file_name = item
        
        # Read file
        with open('Notes/' + file_name) as f_read:
            show_content = f_read.read()


        # Show content
        listbox_item.config(selectbackground=lb_bg_color, selectforeground=lb_fg_color)
        textarea.config(fg=fg_color)
        textarea.insert(1.0, show_content)
        textarea.focus()
    else:
        # Display error and unhighlight listbox item
        listbox_item.config(selectbackground=bg_color, selectforeground=fg_color)
        textarea.insert(1.0, 'Sorry!\nFile not found\n\nPlease try again!')

    # Use title button for..
    # Update file content
    title_btn['text'] = 'Update Note'
    title_btn['state'] = NORMAL
    title_btn['command'] = update_file
    title_btn.config(bg='#269269', fg=bg_color)

    # Change commands for footer buttons
    del_btn['text'] = 'Delete ' + item
    del_btn['state'] = NORMAL
    del_btn.config(bg='#A32627')
    del_btn['command'] = delete_selected
    save_note_btn['text'] = 'Close'
    save_note_btn['state'] = NORMAL
    save_note_btn.config(bg=fg_color, fg=bg_color)
    save_note_btn['command'] = close_note


def update_file():

    # Getter
    get_update = textarea.get(1.0, END)

    # Write to file
    with open('Notes/' + file_name, 'w') as f_write:
        f_write.write(get_update)


    # Read file
    with open('Notes/' + file_name) as f_read:
        show_content = f_read.read()


    # Clear the text area, then show content
    textarea.delete(1.0, END)
    textarea['state'] = NORMAL
    textarea.insert(1.0, show_content)

def prep_email():

    # [New Note Button] is now [EMAIL BUTTON]
    new_note_btn['text'] = ''
    new_note_btn['state'] = DISABLED
    new_note_btn.config(bg=bg_color, fg=bg_color)
    
    # Show email (label, entry field, send button)
    outer_frame.config(bg='#272727')
    title_frame.config(bg='#272727')
    title_label['text'] = 'Email To:'
    title_label.config(bg='#272727', fg=bg_color)
    title_entry.config(fg='#272727')
    title_entry.focus()
    title_btn.config(bg=bg_color, fg='#272727')
    # Disable title button and..
    # Enable Email Button
    title_btn['text'] = 'Send'
    title_btn['state'] = NORMAL
    title_btn['command'] = send_mail
    app.bind('<Return>', send_mail)


def send_mail(*args):
    # Unhighlight listbox item
    listbox_item.config(selectbackground=bg_color, selectforeground=fg_color)

    # Getter
    # Using the Title Input Field now..
    # For getting the Email Input
    get_email = note_title.get()
    get_text = textarea.get(1.0, END)

    # Check if create title field is empty
    if get_email == '':
        title_entry.focus()
        title_entry.config(fg='#272727')
        output_label['text'] = 'Please enter an email address!'
        output_label.config(fg='#A32627')   # Error msg in red
    else:
        # Set output label text color to normal
        output_label['text'] = ''
        output_label.config(fg=fg_color)

        # Date
        dt = datetime.now().strftime('%d/%m/%Y %H:%M')

        # Get listbox item title for email subject
        selected = listbox_item.curselection()
        selected = int(selected[0])
        item = listbox_item.get(selected)

        # From Email Import
        EA = connect.EMAIL_USER
        EP = connect.EMAIL_PASS

        # Process Email
        msg = EmailMessage()
        msg['subject'] = item
        msg['From'] = EA
        msg['To'] = get_email
        msg.set_content(get_text)

        # Create CSV directory (if it doesn't exist)
        csv_name = 'CSV/'
        if csv_name != os.path.basename(csv_name):
            try:
                os.mkdir(csv_name)
            except:
                None

        # Send Email
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EA, EP)
                smtp.send_message(msg)


            # Saved successfully and email sent
            output_label['text'] = 'List: ' + item + '\n\nEmail sent to:\n' + get_email + '\n' + str(dt)

            # Write to csv file
            csv_filename = 'CSV/email_data.csv'
            text_data = get_text.strip()
            
            with open(csv_filename, 'a') as f_append_csv:
                f_append_csv.write(('\n'*2) + text_data + ',' + get_email + ',' + str(dt) + ('\n'*1))


        except:
            # Error message
            output_label.config(fg='#A32627')
            output_label['text'] = 'Email Server Error'\
                                   '\n\nSorry!\n\nWe have experienced a server issue.'\
                                   '\nPlease check your internet connection\nand try again.'


# Delete file from directory and..
# from listbox also
def delete_selected():

    # Get (clicked item) from listbox
    selected = listbox_item.curselection()
    selected = int(selected[0])
    item = listbox_item.get(selected)

    filename = 'Notes/' + str(item)

    # Make sure the (clicked item) from listbox..
    # is the same as in the directory and..
    # remove file
    if item == os.path.basename(filename):
        os.remove(filename)
    else:
        # Display error
        textarea.insert(1.0, 'Sorry!\nFile not found\n\nPlease try again!')
    
    # Remove item from the listbox
    item = listbox_item.delete(selected)
    # Call page settings function
    page_settings()


def close_note(*args):

    # Copy textarea to file on close
    with open('Notes/' + file_name, 'w') as f_write:
        f_write.write(textarea.get(1.0, END))


    # Call page settings function
    page_settings()


# Triggered from defs (save_note), (delete_selected), (close_note)
def page_settings():

    logo_frame.focus()
    # Hide title entry
    outer_frame.config(bg=bg_color)
    title_frame.config(bg=bg_color)
    title_label.config(bg=bg_color, fg=bg_color)
    title_entry.config(fg=bg_color)
    title_entry.delete(0, END)
    # Disable title button
    title_btn.config(bg=bg_color, fg=bg_color)
    title_btn['text'] = ''
    title_btn['state'] = DISABLED
    # Disable delete button
    del_btn['text'] = ''
    del_btn['state'] = DISABLED
    del_btn.config(bg=bg_color, fg=bg_color)
    # Disable save note button
    save_note_btn['text'] = ''
    save_note_btn['state'] = DISABLED
    save_note_btn.config(bg=bg_color, fg=bg_color)
    # Show New Note Button
    new_note_btn['text'] = 'New Note +'
    new_note_btn['state'] = NORMAL
    new_note_btn['command'] = new_note
    app.bind('<Return>', new_note)
    new_note_btn.config(bg=fg_color, fg=bg_color)
    # Unhighlight listbox item
    listbox_item.config(selectbackground=bg_color, selectforeground=fg_color)
    # Clear Text Area
    textarea.delete(1.0, END)
    textarea['state'] = DISABLED
    # Clear Email Message
    output_label['text'] = ''


# Getters
note_title = StringVar()

# Left Frame ___________________________________________________________________________
# For Logo, Listbox (display saved notes), and Button (new note) ______________________
left_frame = Frame(app, bg=bg_color)
left_frame.pack(side='left', fill='both', expand=True)

# Inside Left Frame

# Logo Frame __________________________________________________________________________
logo_frame = Frame(left_frame, bg=fg_color)
logo_frame.pack(fill='x')

# App Title Label.. (we will change this for a logo image later)
photo = PhotoImage(file="images/note.png")
app_title_label = Label(logo_frame, image=photo, bg=fg_color, border=0)
# app_title_label.photo = photo
app_title_label.pack(fill='both', pady=20)

# app_title_label = Label(logo_frame, text='NOTES', bg=fg_color, fg=bg_color, font=font_size)
# app_title_label.pack(fill='x', pady=40)

# Listbox Frame ________________________________________________________________________
lists_frame = Frame(left_frame, bg=bg_color)
lists_frame.pack(fill='both', padx=(6, 0), pady=8, expand=True)

# Listbox for Saved Notes
listbox_item = Listbox(\
    lists_frame, bg=bg_color, fg=fg_color, font=font_size, \
    selectbackground=bg_color, selectforeground=fg_color, highlightthickness=0, border=0)
listbox_item.bind('<<ListboxSelect>>', list_clicked)
listbox_item.pack(side='left', fill='both', expand=True)

# Listbox vertical scroll-bar
yscroll = Scrollbar(lists_frame, command=listbox_item.yview, orient=VERTICAL)
yscroll.pack(side='right', fill='y', anchor='e', expand=True)
listbox_item.config(yscrollcommand=yscroll.set)

# New Note Frame for Button _________________________________________________________
new_note_frame = Frame(left_frame, bg=fg_color)
new_note_frame.pack(side='bottom', fill='x')

# New Note Button
new_note_btn = Button(\
    new_note_frame, text='New Note +', bg=fg_color, fg=bg_color, relief='flat', command=new_note)
new_note_btn['state'] = NORMAL
app.bind('<Return>', new_note)
new_note_btn.pack(fill='x')

# Right Frame _________________________________________________________________________
# For Note Title (create),
# Text (write note, display saved notes), and Buttons (save, close, delete notes) ______
right_frame = Frame(app, bg=bg_color)
right_frame.pack(side='right', fill='both', expand=True)

# Outer Frame for Title Frame (user input to create title for note) _____________________
### Outer Frame (START)
outer_frame = Frame(right_frame, bg=bg_color)
outer_frame.pack(fill='both')

# Note Title Frame (create)
title_frame = Frame(outer_frame, bg=bg_color)
title_frame.pack(ipady=20)

# Title Label
title_label = Label(title_frame, bg=bg_color, fg=bg_color, font=font_size)
title_label.pack(side='left', pady=19, anchor='w')

# Title Entry Field
title_entry = Entry(\
    title_frame, width=24, bg=bg_color, fg=bg_color, font='Arial, 12', border=0, textvariable=note_title)
title_entry.pack(side='left', padx=5, pady=19, ipady=3)

# Button (submit title)
title_btn = Button(title_frame, bg=bg_color, fg=bg_color, relief='flat')
title_btn['state'] = DISABLED
title_btn.pack(side='left', pady=19)

### Outer Frame (END) ______________________________________________________________

# Email Sent Frame (message) ______________________________________________________________
message_frame = Frame(right_frame, bg=bg_color)
message_frame.pack(fill='x')

# Output (Email Message) Label
output_label = Label (message_frame, justify='left', bg=bg_color, fg=fg_color, font=font_size)
output_label.pack(side='left', padx=(10, 0), pady=20)

# Text Frame (type note) ______________________________________________________________
text_frame = Frame(right_frame, bg=bg_color)
text_frame.pack(fill='both', expand=True)

# Text Area Field
textarea = Text(text_frame, height=12, wrap=WORD, bg=bg_color, fg=bg_color, font=font_size, border=0)
textarea['state'] = DISABLED
textarea.pack(fill='both', padx=10, pady=(0, 20), expand=True)

# Footer Frame (delete note) __________________________________________________________
footer_frame = Frame(right_frame, bg=bg_color)
footer_frame.pack(side='bottom', fill='x')

# Button (delete note)
del_btn = Button(footer_frame, bg=bg_color, fg=bg_color, relief='flat')
del_btn['state'] = DISABLED
del_btn.pack(side='left', fill='x', expand=True)

# Button (save note)
save_note_btn = Button(footer_frame, bg=bg_color, fg=bg_color, relief='flat')
save_note_btn['state'] = DISABLED
save_note_btn.pack(side='right', fill='x', expand=True)

dir_name = 'Notes/'
if dir_name != os.path.basename(dir_name):
    try:
        os.mkdir(dir_name)
    except:
        None

# On load.. Display the content of the listbox (existing files)
file_name = os.listdir('Notes/')
for file in file_name:
    listbox_item.insert(0, file)

# Root Defaults _______________________________________________________________________
if __name__ == '__main__':
    app.title('Notes')
    app.iconbitmap('images/note.ico')
    app.geometry('700x640-0+56')
    app.configure(bg=bg_color)
    app.mainloop()
