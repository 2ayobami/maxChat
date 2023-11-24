#importing socket which will be used for creating sockets that will send and
#receive message
import socket
#this is important to help connect to many clients as possible on a single 
#thread.
import threading
#tkinter good for bring alive the GUI that our clients will use to interact 
#with the system.
import tkinter as tk

#Useful for communicating with the system
import sys
#useful for wrapping text on the GUI
import textwrap
#Help us calculate and format time
from datetime import datetime


global receive_thread
global stop_thread

# Define constants for the client
HOST = 'localhost'
PORT = 8000

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Function to handle incoming messages
#this will help us create a user name set, which will be used to identify 
#users in the network
usernames_set = set()
#first connect to our socket as a client
client_socket.connect((HOST, PORT))

#create the rook for our tkinter object
root = tk.Tk()
#the configure method root element to have a background color of dark blue
root.configure(bg="#021691")
#the Title of our chat app Will be the name of the chatting app
root.title('MaxChat')

#first we create the function to handle incoming messages
def receive_messages():
    #the best way to look up for incoming message is to maintain a loop
    #that keep checking for that message
    while True:
        #we use the try block to ensure if no messages are found the code 
        #don't break.
        try:
            #first we check if this variable pre created as false is true
            #we exit the thread using the system framework.
            if stop_thread == True:
                sys.exit(0)
                break
            
            #if the client has message the data variable will be prepopulated
            data = client_socket.recv(1024).decode()
            
            #we break the loop if we don't find data
            if not data:
                break
            
            #the message type is used to detect of the client is logged in 
            #or not.
            msg_type = data[0]
            #the original message
            msg = data[1:]
            
            #we check the message type to check how to handle the message
            if msg_type == 'o':
                #this help us check if the message is in the user name set.
                if msg in usernames_set:
                    add_message(f"{msg} has just left the room", 'system')
                    usernames_set.remove(msg)
                else:
                    add_message(f"{msg} has just joined the room", 'system')
                    usernames_set.add(msg)
                #running this function to update online client
                update_online_clients(usernames_set)
            #if it is a capital O then it should be a list of user names
            elif msg_type == 'O':
                curr_online_users = msg.split(',')
                #calling the update method we can join the currrent users 
                #array with the username set
                usernames_set.update(curr_online_users)
                update_online_clients(curr_online_users)               

            elif msg_type in ['z', 'w']:
                add_message(msg, 'system')
            else:
                add_message(msg, 'others')
        except:
            #if something happend we just close the connection and break the
            #loop.
            client_socket.close()
            break

def send_message(event=None):
    #to get the message to send we get them from the input field we created
    #python tkinter.
    message = input_field.get()
    if len(usernames_set) == 0:
        root.title(f'Chat - {message}') 
    input_field.delete(0, tk.END)
    client_socket.send(message.encode())
    add_message(message, 'me')

def clear_chat():
     chat_window.config(state=tk.NORMAL)
     chat_window.delete('1.0', tk.END)
     chat_window.config(state=tk.DISABLED)




def on_closing():
    client_socket.close()
    sys.exit(0)


#here we create the chat frame with tkinter and make the root as the main 
#container of the frame.
chat_frame = tk.Frame(root)
#should ve designed to be aligned to the top with a padding of 15 at the x & 
#y axis
chat_frame.pack(side=tk.TOP, padx=15, pady=15)
#configure the background to be deep blue
chat_frame.configure(bg="#021691")

#we need to create the online client frame to help users see their online
#clients
online_clients_frame = tk.Frame(chat_frame)
#we pack it to the right with a padding to the x axis of 15
online_clients_frame.pack(side=tk.RIGHT, padx=15)
#to aviod color bubble we use the same background color for each.
online_clients_frame.configure(bg="#021691")

#next is the scrollbar.
scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_window = tk.Text(chat_frame, height=20, width=50,
                      yscrollcommand=scrollbar.set, wrap="word")
chat_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=15)

scrollbar.config(command=chat_window.yview)

chat_window.tag_config('user', foreground='#88C0D0')
chat_window.tag_config('server', foreground='#8FBCBB')
chat_window.tag_config('small', font=("Helvetica", 7))
chat_window.tag_config('greycolour', foreground="#E4E4ED")
chat_window.tag_config("me", justify="right")
chat_window.tag_config("others", justify="left")
chat_window.tag_config("system", justify="center")
chat_window.tag_config("right", justify="right")
chat_window.tag_config("small", font=("Helvetica", 7))
chat_window.tag_config("colour", foreground="#E4E4ED")

chat_window.config(state=tk.DISABLED)

chat_window.configure(background='black')

root.option_add("*Font", "TkFixedFont")
root.option_add("*sent.Font", "TkFixedFont")
root.option_add("*received.Font", "TkFixedFont")

input_frame = tk.Frame(root)
input_frame.pack(side=tk.BOTTOM, padx=15, pady=15)
input_frame.configure(bg="#2B354A")

input_field = tk.Entry(input_frame, width=40)
input_field.bind("<Return>", send_message)
input_field.pack(side=tk.LEFT)

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)
send_button.configure(bg="#E4E4ED", fg="#2B354A")

clear_chat_button = tk.Button(input_frame, text="Clear Chat", command=clear_chat)
clear_chat_button.pack(side=tk.LEFT)
clear_chat_button.configure(bg="#E4E4ED", fg="#2B354A")

online_clients_label = tk.Label(online_clients_frame, text="Online Clients:")
online_clients_label.pack(side=tk.TOP)
online_clients_label.configure(bg="#2B354A", fg="#E4E4ED")

online_clients_listbox = tk.Listbox(online_clients_frame, height=20, width=20)
online_clients_listbox.pack(side=tk.BOTTOM, padx=10, pady=10)

online_clients_listbox.configure(bg="#4F5869", fg="#E4E4ED", highlightbackground="#8FADCC",
                                 highlightcolor="#8FADCC", selectbackground="#8FADCC", selectforeground="#E4E4ED")


def get_time_formatted():
    return datetime.now().strftime("%a %I-%M %p \n")


def add_message(msg, sender):
    
    chat_window.config(state=tk.NORMAL)

    fa = "#13f252"
    bg_color = "black"
    text_position = ""
    tags = ""
    text_direction = tk.LEFT

    match sender:
        case 'others':
            text_position = "left"
            fa = "#13f252"
            tags = 'others'
        case 'system':
            text_position = "center"
            fa = "#ffffff"
            tags = 'system'
            text_direction = tk.CENTER
        case 'me':
            text_position = "right"
            fa = "#fc541c"
            tags = 'me'
            
    
    chat_window.insert(tk.END, '\n ', text_position)
    chat_window.insert(tk.END, get_time_formatted(),('small', 'greycolour', text_position))
    chat_window.insert(tk.END, ' ', text_position)

    chat_window.config(state=tk.DISABLED)
    
    message = tk.Label(chat_window, fg=fa, text=msg, wraplength=200, font=("Arial", 10), bg=bg_color, bd=4, justify=text_direction, relief="flat", anchor="center")

    # chat_window.insert(tk.END, '\n ', 'center')
    # chat_window.window_create(tk.END, window=message)
    # chat_window.config(foreground="#0000CC", font=("Helvetica", 9))
    # chat_window.yview(tk.END)

    chat_window.window_create(tk.END, window=message)
    chat_window.insert(tk.END, '\n', "center")
    chat_window.tag_add(tags, "end-2l", "end-1c")
    chat_window.config(foreground="#0000CC", font=("Helvetica", 9))
    chat_window.yview(tk.END)



    

def send(msg, is_sent=False):
    chat_window.config(state=tk.NORMAL)
    # chat_window.insert(tk.END, get_time_formatted()+' ', ("small", "left", "greycolour"))
    chat_window.insert(tk.END, '\n ', "right")
    chat_window.window_create(tk.END, window=tk.Label(chat_window, fg="#000000", text=msg,
                                                      wraplength=200, font=("Arial", 10), bg="lightblue", bd=4, justify="left"))
    chat_window.insert(tk.END, '\n ', "left")
    chat_window.config(foreground="#0000CC", font=("Helvetica", 9))
    chat_window.yview(tk.END)



def on_listbox_double_click(event):
    # Get the selected item from the listbox
    selection = online_clients_listbox.get(
        online_clients_listbox.curselection())

    # Perform the desired action, e.g. print the selected item
    input_field.delete(0, tk.END)
    input_field.insert(tk.END, f"@{selection} ")
    input_field.focus_set()
    # print(selection)


online_clients_listbox.bind("<Double-Button-1>", on_listbox_double_click)


# Function to update the list of online clients
def update_online_clients(online_clients):
    # Clear the current list of online clients
    online_clients_listbox.delete(0, tk.END)

    # Add each online client to the listbox
    for client in online_clients:
        online_clients_listbox.insert(tk.END, client)


# Create a new thread to handle incoming messages
#predefine the 
stop_thread = False
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

#we add the delete window protocol to the on close function.
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
tk.mainloop()
