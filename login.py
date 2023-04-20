from tkinter import *
from tkinter import messagebox
import mysql.connector  #For DB Connections
import sys  # sys.exit to exit the programs


#This file is created separately for login functionality.

Window_open=True  # Variable to track if window is closed

#This function will remove username placeholder.
def on_enter(user):
    user.delete(0,'end')

#This function will add username placeholder if username is empty.
def on_leave(user):
    name=user.get()
    if(name==''):
        user.insert(0,'Username')

#This function will remove password placeholder.
def on_enterpwd(password): 
    password.delete(0,'end')
    password.config(show='*') #Convert Password text in asterik *



#This function will add password placeholder if password is empty.
def on_leavepwd(password):
    name=password.get()
    if(name==''):
        password.insert(0,'Password') 
        password.config(show='') #Convert Placeholder Password text in plain text from *

#This method will close window on cross button press
def on_closing(root):
    print("Login Window is closing...")
    root.destroy()
    root.closed=True
    sys.exit()

#This method will link login window with signup window    
def signup_command(root):
    root.destroy() #Destroy login window if user press signup button.
    from signup import Signup  # Import Signup class
    singupObj=Signup()  #Create Signup class object
    root.closed= singupObj.signup_Window()  #Call  signup window method
    

#Method to handle login window    
def login_Window():
 root=Tk()  #Create window for login
 root.title('Login') #Show login title
 root.geometry('350x450+300+200')  #Dimensions of login window
 root.configure(bg='#fff')   #Background color of window is white
 root.resizable(False,False) #Resizing is disabled as this can disturb layout of window.
 root.protocol("WM_DELETE_WINDOW",lambda: on_closing(root)) # Here lambda function is used to call method with params.
 root.closed=False  #Initial window closed param is false

 ################# Main login Label #########
 Label(root,bg='white').place(x=50,y=50)
 frame=Frame(root,width=350,height=350,bg="white")
 frame.place(x=0,y=70)
 heading=Label(frame,text='Login in',fg='#32a852',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
 heading.place(x=100,y=5)

 #############Username textbox and label#################
 user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
 user.place(x=30,y=80)
 user.insert(0,'Username')
 user.bind('<FocusIn>', lambda event: on_enter(user))  #Bind function to remove username placeholder.
 user.bind('<FocusOut>', lambda event: on_leave(user))  #Bind function to add place holder.
 Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

 #############Password textbox and label#################
 password=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
 password.place(x=30,y=150)
 password.insert(0,'Password')
 password.bind('<FocusIn>', lambda event: on_enterpwd(password)) #Bind function to remove password placeholder.
 password.bind('<FocusOut>', lambda event: on_leavepwd(password))  #Bind function to add place holder.
 Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)
########################################################

#############Login Button###################
 Button(frame,width=39,pady=7,text='Login',bg='#32a852',fg='white',border=0,command=lambda:signin(user,password,root)).place(x=35,y=204)

###############Signup Button##########################
 label=Label(frame,text="Don't have an account?",fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
 label.place(x=75,y=270)
 sign_up=Button(frame,width=6,text='Sign Up',border=0,bg='white',cursor='hand2',fg='#32a852',command=lambda:signup_command(root))
 sign_up.place(x=215,y=270)
 root.mainloop() # To keep window open

 print("Return value for root closed is: ",root.closed)
 return not root.closed  #Return value to start game based on login status.


###Sign In Functionality
def signin(user,password,root):

    username=user.get()  #Fetch Username
    pwd=password.get() #Fetch password

    
    # Show error message if user name is empty
    if username=='Username' or username=='':
     messagebox.showerror("Invalid","Username is empty")
     return
    
    # Show error message if password is empty
    elif pwd=='Password' or pwd=='':
     messagebox.showerror("Invalid","Password is empty")
     return
    #Match credentials with database
    else:
       try:
        #This will setup a connection with the  mysql databse installed on our local machine.
        db=mysql.connector.connect(
        host="localhost",
        user="root",      #Username given for setup
        passwd="Signity@123",  #password for mysql
        database="lambton_224" #This will connect cursor with lambton_224 database
        )

        mycursor_224=db.cursor() # This will provide a cursor to work with database queries.
        #Command to get data from table flappy_bird_224
        command="select username,password from lambton_224.flappy_bird_224 where username=%s and password=%s"
       #Command and params
        mycursor_224.execute(command,(username,pwd))
        #Fetch one record
        dbresult=mycursor_224.fetchone()
        print("DB Data",dbresult)

        #Show error message if no data found in DB with given credentials
        if dbresult==None:
           messagebox.showerror("Invalid","Invalid username or password!")
           return False
        else:
           #Welcome user 
           messagebox.showinfo("Login",("Welcome "+username))
           root.destroy() #Destroy login window.
           return True
       except:
          #Handle exception if any error occur in DB connection.
          messagebox.showerror("Connection","DB Connection  failed!!")


####This function will be called only if file is executed as main module.
if __name__ == "__main__":
    print("Login call from main")
    login_Window()

