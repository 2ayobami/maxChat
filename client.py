#importing socket which will be used for creating sockets that will send and
#receive message
import socket
#this is important to help connect to many clients as possible on a single 
#thread.
import threading
#tkinter good for bring alive the GUI that our clients will use to interact 
#with the system.
import tkinter as tk
from tkinter import *
#useful in alerting important message to our users
from tkinter import messagebox
#useful to create our tree view for our products
from tkinter import ttk
from PIL import ImageTk,Image 

#Useful for communicating with the system
import sys
#useful for wrapping text on the GUI
import textwrap
#Help us calculate and format time
from datetime import datetime
#importing the os module to commuciate with the current operating system
import os
#this will help us create different random values using the string module
import random
import string
#useful for parsing database file of the local server.
import json

#This global variable is declared global to help handle the threading
#request from servers
global receiveThread
#this global variable will help us stop the threading request from server
global stopThread

#another set I will like to create is the set for the product on the 
#server. This will help use display products on the store page that
#is hosted by the server.
productList  = list()


# Define constants for the host
#this is the host ip address and port
#clients will connect using the remote IP and port of rooms
HOST = 'localhost'
PORT = 5555

#the database from the local server
database    = open("database.json", "r")
data        = str(database.read())
#useful mainly to the current client who is the admin of the current 
#server
database    = json.loads( data if data else "{}" )
global icon

# Create a socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
GUI_BG1 = "#E4E4ED"

# Function to handle incoming messages
#this will help us create a user name set, which will be used to identify 
#users in the network
usernamesSet = set()
#first connect to our socket as a client
clientSocket.connect((HOST, PORT))
# holds the main chat gui
global root
# Holds the admin panel for managing products
global gui1
# holds the user dashboard panel
global gui2
# holds the moderator registeration panel. This allows any user to 
# register with a chat server
global gui3
#This holds the moderators panel where they can manage products
global gui4

global gui5
global gui6
global gui7
global gui8
global gui9
root = False
gui1  = False
gui2  = False
gui3  = False
gui4  = False
gui5  = False
gui6  = False
gui7 = False
gui8 = False
gui9 = False

def onClosing():      
    clientSocket.close()            
    sys.exit(0)


def destroy():
    global root
    global gui1
    global gui2
    global gui3
    global gui4
    global gui5
    global gui6
    global gui7
    global gui8
    global gui9
    if root :
        root.destroy()
        root = False
    if gui2 :    
        gui2.destroy()
        gui2 = False
    if gui3 :    
        gui3.destroy()
        gui3 = False
    if gui1 :
        gui1.destroy()
        gui1 = False
    if gui4 :
        gui4.destroy()
        gui4 = False
    if gui5 :
        gui5.destroy()
        gui5 = False
    if gui6 :
        gui6.destroy()
        gui6 = False
    if gui7 :
        gui7.destroy()
        gui7 = False
    if gui8 :
        gui8.destroy()
        gui8 = False
    if gui9 :
        gui9.destroy()
        gui9 = False
    
def on_click_me() :
    return True
    
def shopScreen() :
    #destroy()
    global gui5
    
    if gui5 :
        gui5.deiconify()
        return
    
    global icon
    gui5 = tk.Toplevel()
    gui5.configure(background=GUI_BG1)
    gui5.title("MaxChat Shop - Shop")
    #the Title of our chat app Will be the name of the chatting app
    icon = PhotoImage(file="JUMIA-HOT-2-2.png")
    gui5.iconphoto( False, icon )
    gui5.geometry("600x500")    
    frame = tk.Frame( gui5, bg="blue", width=600, height = 500 )
    frame.pack()
    label = Label( frame, text="MaxChat Shop Page - Product List")
    label.grid(row=0,column=1)
    
    
    # create a vertical scrollbar-no need
    # to write orient as it is by
    # default vertical
    v = Scrollbar(gui5)
  
    # attach Scrollbar to root window on 
    # the side
    v.pack(side = RIGHT, fill = Y)
    def hide() :
        gui5.withdraw()
    
    button = tk.Button(frame, text="Back to Chat", command = hide)
    button.grid(row=0,column=0)
    
    
    def onGUI5Closing() :
        gui5.withdraw()
        
    gui5.protocol("WM_DELETE_WINDOW", onGUI5Closing)
    
    if True:
        if not "product_details" in database :
            database["product_details"] = list()
            
        #check the length of the products in the database, if none
        #create a sample product for the user.
        length = len( productList )
        
        if length == 0 :
            #each product is a dictionary of values.
            sample1 = dict()
            sample1["name"] = "Sample Product 1"
            sample1["description"] = "This a Sample Product 1"
            sample1["quantity"] = "10"
            sample1["price"] = "10.00"
            sample1["image"] = "product1.png"
            #product ID variable
            PID     = random.choices( string.ascii_uppercase + string.digits, k=10)
            PID     = ''.join(PID)
            sample1["PID"] = PID
            productList.append( sample1 )
            sample2 = dict()
            sample2["name"] = "Sample Product 2"
            sample2["description"] = "This a Sample Product 2"
            sample2["quantity"] = "5"
            sample2["price"] = "60.00"
            sample2["image"] = "product2.png"
            #product ID variable
            PID     = random.choices( string.ascii_uppercase + string.digits, k=10)
            PID     = ''.join(PID)
            sample2["PID"] = PID
            productList.append( sample2 )
            sample3 = dict()
            sample3["name"] = "Sample Product 3"
            sample3["description"] = "This a Sample Product 3"
            sample3["quantity"] = "50"
            sample3["price"] = "5.00"
            sample3["image"] = "product3.png"
            sample4 = dict()
            sample4["name"] = "Sample Product 4"
            sample4["description"] = "This a Sample Product 4"
            sample4["quantity"] = "50"
            sample4["price"] = "50.00"
            sample4["image"] = "product3.png"
            #product ID variable
            PID     = random.choices( string.ascii_uppercase + string.digits, k=10)
            PID     = ''.join(PID)
            sample4["PID"] = PID
            productList.append( sample4 )
            
        # Add grid layout
        #frame.grid()

        # Create 8 frames (4 rows, 2 columns)
        frame.frames = [tk.Frame(frame, bg="grey", width=400, height=300) for _ in range(len(productList))]
        #detecting rows available on the program
        rows    = 0
        # Place the frames in the grid layout
        for i, framed in enumerate(frame.frames):
            i += 2
            rows = i//2
            framed.grid(row=i//2, column=i%2)

        # Add image, price label, and buy now button to each frame
        for i, framed in enumerate(frame.frames):
            image_url = productList[i]["image"]
            img = Image.open(image_url)
            img = img.resize((200, 200), Image.LANCZOS) # Resize the image
            image = ImageTk.PhotoImage(img) # Replace with your own image file paths
            image_label = tk.Label(framed, image=image)
            image_label.image = image # Keep reference to avoid garbage collection
            image_label.pack()

            price_label = tk.Label(framed, text="Price: $"+productList[i]["price"])
            price_label.pack()
            quantity_label = tk.Label(framed, text="Quantity: "+productList[i]["quantity"])
            quantity_label.pack()

            buy_now_button = tk.Button(framed, text="Buy Now", command=lambda index=productList[i]["PID"]: buy_now(index))
            buy_now_button.pack()
    
        # # Replace this with the code to add the item to your cart page
        
        # #store all the products in a products variable
        # products    = productList
        
        # #We will be displaying the products in a server with 
        # #a tree view.
        # tree    = ttk.Treeview( gui5, columns=("SKU", "Name", "Description", "Quantity", "Price", "Image" ), show="headings" )
        # style   = ttk.Style()
        # style.configure('Treeview', rowheight=100)
        
        # #add headings to the column
        # tree.heading("SKU", text="Product SKU")
        # tree.heading("Name", text="Product Name")
        # tree.heading("Description", text="Product Description")
        # tree.heading("Quantity", text="Quantity")
        # tree.heading("Price", text="Price")
        # tree.heading("Image", text="Image")
        
        # #setting the default width of each column.
        # tree.column("SKU", width=50)
        # tree.column("Name", width=70)
        # tree.column("Description", width=200)
        # tree.column("Quantity", width=40)
        # tree.column("Price", width=60)
        # tree.column("Image", width=100)
        
        # #next is to loop through all the products to add them to the
        # #view.
        # i = 0
        # #photo = list()
        # for product in products :
            # # img  = Image.open(product["image"]) 
            # photo = ImageTk.PhotoImage(file="product1.png")
            # btn = ttk.Button(tree, text="Buy", command=on_click_me)
            # # label = Label(image=photo)
            # # label.image = photo            
            # tree.insert(parent='', index='end', iid=i, open=True,text="",image=photo, value=("Text", btn))
            # i+=1
            
           # # tree.insert("","end", value=(product["PID"],product["name"], product["description"],product["quantity"],product["price"], btn )) 
            
        # tree.pack()
    # except:  
        # messagebox.showinfo("Error Viewing Product", "An error occured while requesting for products from the server") 
    #we add the delete window protocol to the on close function.    
    
    gui5.mainloop()
    
def buy_now(PID):
        print("Adding item "+str(PID)+" to cart.")

        
def shopNow():
    #destroy()
    global gui6
    
    if gui6 :
        gui6.deiconify()
        return
    
    global icon
    gui6=tk.Toplevel()
    gui6.configure(background=GUI_BG1)
    gui6.title("MaxChat Shop - Add Product")
    #the Title of our chat app Will be the name of the chatting app
    icon = PhotoImage(file="JUMIA-HOT-2-2.png")
    gui6.iconphoto( False, icon )
    gui6.geometry("700x500")    
    ppp1=Label(gui6, text="Product Id ",bg=GUI_BG1, font=('', 20))
    ppp1.grid(row=4,column=2)
    e1 = Entry(gui6)
    e1.grid(row=4,column=4)
        
    ppp2=Label(gui6 , text="Product Name ",bg=GUI_BG1, font=('', 20))
    ppp2.grid(row=6,column=2)
    e2 = Entry(gui6)
    e2.grid(row=6,column=4)
        
    ppp3=Label(gui6, text="Product Description ",bg=GUI_BG1, font=('', 20))
    ppp3.grid(row=8,column=2)
    e3 = Entry(gui6)
    e3.grid(row=8,column=4)
        
    ppp4=Label(gui6, text="Price ",bg=GUI_BG1, font=('', 20))
    ppp4.grid(row=10,column=2)
    e4 = Entry(gui6)
    e4.grid(row=10,column=4)
        
    def addproduct():
        print("Add Product")
        ID=e1.get()
        NAME=e2.get()
        DESCRIPTION=e3.get()
        PRICE=e4.get()
        if not "product_details" in cur :
            cur["product_details"] = list()
                
        cur["product_details"].append({
            "ID":ID,
            "name":NAME,
            "description":DESCRIPTION,
            "price":PRICE
        })
            
        with open("database.json", "w" ) as file :
            json.dump( database, file )
        
            
        # cur.execute(e)
        #cur.execute("insert into PRODUCT_details values(&ID,'&NAME','&DESCRIPTION',&PRICE)")
            #con.commit()
        #cur.execute("SELECT * from product_details")
        D=database["product_details"];
        sstr=""
        for i in D:
            sstr=sstr+str(i)+"\n"
            print(i)
        messagebox.showinfo("Product List", sstr)

    def viewproduct():
        print("View")
        PID=e1.get()
            # a="select * from product_details where ID="+PID
            # cur.execute(a)
            # con.commit()
            #cur.execute("select * from product_details")
        D=cur["product_details"];
        sstr=""
        print(len(D))
        for i in D:
            if i["ID"] == PID:
                sstr=sstr+str(i)+"\n"
            print(i)
    
        messagebox.showinfo("View Product Details", sstr)
        
    def delproduct():
        print("del product")
        PID=e1.get()
        # f="DELETE from product_details where ID="+PID
        # cur.execute(f)
        # con.commit()
        # cur.execute("SELECT * from product_details")
        D=database["product_details"]
        sstr=""
        for i in range(len( D ) ) :
            if D[i]["ID"] == PID :
                del D[i]
            else:
                sstr=sstr+str(D[i])+"\n"
            print(i)
        messagebox.showinfo("Product Details- After Deletion", sstr)
    
    def onGUI6Closing() :
        gui6.withdraw()
                    
    addBtn12 = Button(gui6, text = "ADD PRODUCT",font=('', 12),command=addproduct)
    addBtn12.grid(row =18, column = 3)
    addBtn13 = Button(gui6, text = "VIEW PRODUCT",font=('', 12),command=viewproduct)
    addBtn13.grid(row =18, column = 4)
    addBtn14 = Button(gui6, text = "DELETE PRODUCT",font=('', 12),command=delproduct)
    addBtn14.grid(row =18, column = 5)
    #we add the delete window protocol to the on close function.
    gui6.protocol("WM_DELETE_WINDOW", onGUI6Closing)
    gui6.mainloop()





def mainloop():
    #destroy()
    global root
    #create the rook for our tkinter object
    root = tk.Tk()
    #the configure method root element to have a background color of dark blue
    root.configure(bg="#021691")
    #the Title of our chat app Will be the name of the chatting app
    icon = PhotoImage(file="JUMIA-HOT-2-2.png")
    root.iconphoto( False, icon )
    root.title('MaxChat')
    
    #first we create the function to handle incoming messages
    def receiveMessages():
        #the best way to look up for incoming message is to maintain a loop
        #that keep checking for that message
        while True:
            #we use the try block to ensure if no messages are found the code 
            #don't break.
            try:
                #first we check if this variable pre created as false is true
                #we exit the thread using the system framework.
                if stopThread == True:
                    sys.exit(0)
                    break
                
                #if the client has message the data variable will be prepopulated
                data = clientSocket.recv(1024).decode()
                
                #we break the loop if we don't find data
                if not data:
                    break
                
                #the message type is used to detect of the client is logged in 
                #or not.
                msgType = data[0]
                #the original message
                msg = data[1:]
                
                #we check the message type to check how to handle the message
                if msgType == 'o':
                    #this help us check if the message is in the user name set.
                    if msg in usernamesSet:
                        addMessage(f"{msg} has just left the room", 'system')
                        usernamesSet.remove(msg)
                    else:
                        addMessage(f"{msg} has just joined the room", 'system')
                        usernamesSet.add(msg)
                    #running this function to update online client
                    update_online_clients(usernamesSet)
                #if it is a capital O then it should be a list of user names
                elif msgType == 'O':
                    curr_online_users = msg.split(',')
                    #calling the update method we can join the currrent users 
                    #array with the username set
                    usernamesSet.update(curr_online_users)
                    update_online_clients(curr_online_users)               

                elif msgType in ['z', 'w']:
                    addMessage(msg, 'system')
                    
                #this shows the product is coming from the server
                #the client is connected to
                elif msgType in ['p', 'P']:
                    #we believe the remaining message should be a jsonable 
                    #message
                    productList.append( json.loads( msg ))
                else:
                    addMessage(msg, 'others')
            except:
                #if something happend we just close the connection and break the
                #loop.
                clientSocket.close()
                break

    def sendMessage(event=None):
        #to get the message to send we get them from the input field we created
        #python tkinter.
        message = inputField.get()
        if len(usernamesSet) == 0:
            root.title(f'MaxChat - {message}') 
        inputField.delete(0, tk.END)
        clientSocket.send(message.encode())
        addMessage(message, 'me')

    def clearChat():
         chatWindow.config(state=tk.NORMAL)
         chatWindow.delete('1.0', tk.END)
         chatWindow.config(state=tk.DISABLED)


    def on_listbox_double_click(event):
        # Get the selected item from the listbox
        selection = onlineClientsListbox.get(
            onlineClientsListbox.curselection())

        # Perform the desired action, e.g. print the selected item
        inputField.delete(0, tk.END)
        inputField.insert(tk.END, f"@{selection} ")
        inputField.focus_set()
        # print(selection)

    
    
    #here we create the chat frame with tkinter and make the root as the main 
    #container of the frame.
    chatFrame = tk.Frame(root)
    #should ve designed to be aligned to the top with a padding of 15 at the x & 
    #y axis
    chatFrame.pack(side=tk.TOP, padx=15, pady=15)
    #configure the background to be deep blue
    chatFrame.configure(bg="#021691")

    #we need to create the online client frame to help users see their online
    #clients
    onlineClientsFrame = tk.Frame(chatFrame)
    #we pack it to the right with a padding to the x axis of 15
    onlineClientsFrame.pack(side=tk.RIGHT, padx=15)
    #to aviod color bubble we use the same background color for each.
    onlineClientsFrame.configure(bg="#021691")

    #next is the scrollbar.
    scrollbar = tk.Scrollbar(chatFrame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    chatWindow = tk.Text(chatFrame, height=20, width=50,
                          yscrollcommand=scrollbar.set, wrap="word")
    chatWindow.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=15)

    scrollbar.config(command=chatWindow.yview)

    chatWindow.tag_config('user', foreground='#88C0D0')
    chatWindow.tag_config('server', foreground='#8FBCBB')
    chatWindow.tag_config('small', font=("Helvetica", 7))
    chatWindow.tag_config('greycolour', foreground="#E4E4ED")
    chatWindow.tag_config("me", justify="right")
    chatWindow.tag_config("others", justify="left")
    chatWindow.tag_config("system", justify="center")
    chatWindow.tag_config("right", justify="right")
    chatWindow.tag_config("small", font=("Helvetica", 7))
    chatWindow.tag_config("colour", foreground="#E4E4ED")

    chatWindow.config(state=tk.DISABLED)

    chatWindow.configure(background='black')

    root.option_add("*Font", "TkFixedFont")
    root.option_add("*sent.Font", "TkFixedFont")
    root.option_add("*received.Font", "TkFixedFont")

    input_frame = tk.Frame(root)
    input_frame.pack(side=tk.BOTTOM, padx=15, pady=15)
    input_frame.configure(bg="#2B354A")

    inputField = tk.Entry(input_frame, width=40)
    inputField.bind("<Return>", sendMessage)
    inputField.pack(side=tk.LEFT)

    sendButton = tk.Button(input_frame, text="Send", command=sendMessage)
    sendButton.pack(side=tk.LEFT)
    sendButton.configure(bg="#E4E4ED", fg="#2B354A")

    clearChatButton = tk.Button(input_frame, text="Clear Chat", command=clearChat)
    clearChatButton.pack(side=tk.LEFT)
    clearChatButton.configure(bg="#E4E4ED", fg="#2B354A")

    shopButton = tk.Button(input_frame, text="Shop", command=shopScreen)
    shopButton.pack(side=tk.LEFT)
    shopButton.configure(bg="#E4E4ED", fg="#2B354A")

    shopButton = tk.Button(input_frame, text="Add Product", command=shopNow)
    shopButton.pack(side=tk.LEFT)
    shopButton.configure(bg="#E4E4ED", fg="#2B354A")

    onlineClientsLabel = tk.Label(onlineClientsFrame, text="Online Clients:")
    onlineClientsLabel.pack(side=tk.TOP)
    onlineClientsLabel.configure(bg="#2B354A", fg="#E4E4ED")

    onlineClientsListbox = tk.Listbox(onlineClientsFrame, height=20, width=20)
    onlineClientsListbox.pack(side=tk.BOTTOM, padx=10, pady=10)

    onlineClientsListbox.configure(bg="#4F5869", fg="#E4E4ED", highlightbackground="#8FADCC",
                                     highlightcolor="#8FADCC", selectbackground="#8FADCC", selectforeground="#E4E4ED")
    
    onlineClientsListbox.bind("<Double-Button-1>", on_listbox_double_click)
    
    # Function to update the list of online clients
    def update_online_clients(online_clients):
        # Clear the current list of online clients
        onlineClientsListbox.delete(0, tk.END)

        # Add each online client to the listbox
        for client in online_clients:
            onlineClientsListbox.insert(tk.END, client)
    
    def get_time_formatted():
        return datetime.now().strftime("%a %I-%M %p \n")


    def addMessage(msg, sender):
        
        chatWindow.config(state=tk.NORMAL)

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
                
        
        chatWindow.insert(tk.END, '\n ', text_position)
        chatWindow.insert(tk.END, get_time_formatted(),('small', 'greycolour', text_position))
        chatWindow.insert(tk.END, ' ', text_position)

        chatWindow.config(state=tk.DISABLED)
        
        message = tk.Label(chatWindow, fg=fa, text=msg, wraplength=200, font=("Arial", 10), bg=bg_color, bd=4, justify=text_direction, relief="flat", anchor="center")

        # chatWindow.insert(tk.END, '\n ', 'center')
        # chatWindow.window_create(tk.END, window=message)
        # chatWindow.config(foreground="#0000CC", font=("Helvetica", 9))
        # chatWindow.yview(tk.END)

        chatWindow.window_create(tk.END, window=message)
        chatWindow.insert(tk.END, '\n', "center")
        chatWindow.tag_add(tags, "end-2l", "end-1c")
        chatWindow.config(foreground="#0000CC", font=("Helvetica", 9))
        chatWindow.yview(tk.END)



        

    def send(msg, is_sent=False):
        chatWindow.config(state=tk.NORMAL)
        # chatWindow.insert(tk.END, get_time_formatted()+' ', ("small", "left", "greycolour"))
        chatWindow.insert(tk.END, '\n ', "right")
        chatWindow.window_create(tk.END, window=tk.Label(chatWindow, fg="#000000", text=msg,
                                                          wraplength=200, font=("Arial", 10), bg="lightblue", bd=4, justify="left"))
        chatWindow.insert(tk.END, '\n ', "left")
        chatWindow.config(foreground="#0000CC", font=("Helvetica", 9))
        chatWindow.yview(tk.END)

        
    # Create a new thread to handle incoming messages
    #predefine the 
    stopThread = False
    receiveThread = threading.Thread(target=receiveMessages)
    receiveThread.start()
    #we add the delete window protocol to the on close function.
    root.protocol("WM_DELETE_WINDOW", onClosing)
    #root.mainloop()
mainloop()
# Start the main loop
tk.mainloop()
