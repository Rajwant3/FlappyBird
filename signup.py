from tkinter import *
from tkinter import messagebox
import login #used to link login button
import mysql.connector  #For DB Connections
import sys  # sys.exit to exit the programs

###Sign Up Functionality
def signup(user,password,confirmPwd,root):
    
    username=user.get()  #Get username
    pwd=password.get()  #Get password
    cpwd=confirmPwd.get() #Get confirm password

    # Show error message if user name is empty
    if username=='Username' or username=='':
     messagebox.showerror("Invalid","Username is empty")
     return
    
    # Show error message if password is empty
    elif pwd=='Password' or pwd=='':
     messagebox.showerror("Invalid","Password is empty")
     return

    # Show error message if confirm password is empty
    elif cpwd=='Confirm Password' or cpwd=='':
     messagebox.showerror("Invalid","Confirm Password is empty")
     return
     
    # If password and confirm password matches, proceed for signup and save in DB. 
    if pwd==cpwd :
     print("Password Match SIGNUP")
      
     try:
        #This will setup a connection with the  mysql databse installed on our local machine.
        db=mysql.connector.connect(
        host="localhost",
        user="root",      #Username given for setup
        passwd="Signity@123",  #password for mysql
        database="lambton_224" #This will connect cursor with lambton_224 database
        )

        # This will provide a cursor to work with database queries.
        mycursor_224=db.cursor() 
        print("check username")
        #Check if username already exist in DB, show error message
        command="select username from lambton_224.flappy_bird_224 where username=%s"
       #Command and params
        mycursor_224.execute(command,(username,))
        #Fetch one record
        dbresult=mycursor_224.fetchone()
        print("Db username",dbresult)
        if dbresult!=None:
           messagebox.showerror("Username Exist","This username already exist, please choose a different username!")
           return
        else:
             #Create table to save credentials if it doesn't exist in DB.
            mycursor_224.execute("create table if not exists flappy_bird_224( username varchar(50) not null,password varchar(50) not null,id int primary key not  null auto_increment)")
            
            #Save credentials in DB.
            mycursor_224.execute("insert into flappy_bird_224(username,password) values(%s,%s)",(username,pwd))

            db.commit()  #Commit changes to the database
            messagebox.showinfo("Signup","Your  account has been successfully registered.")
            
            #Destroy signup window and open login window after successfull registeration.
            login_command(root)
     except mysql.connector.Error as err:
          print(err)
          #Handle exception if any error occur in DB connection.
          messagebox.showerror("Connection","DB Connection  failed!!")
    else:
        #Show error message if password and confirm password doesn't match.
        messagebox.showerror("Invalid","Password and Confirm Password both should match")



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
        password.config(show='')  #Convert Placeholder Password text in plain text from *

#This function will remove confirm password placeholder.
def on_enterCpwd(confirmPwd):
    print("in confirm pwd focus")
    confirmPwd.delete(0,'end')
    confirmPwd.config(show='*')  #Convert Confirm Password text in asterik *

#This function will add confirm password placeholder if password is empty.
def on_leaveCpwd(confirmPwd):
    name=confirmPwd.get()
    if(name==''):
        confirmPwd.insert(0,'Confirm Password')  
        confirmPwd.config(show='') #Convert Placeholder Confirm Password text in plain text from *


#This method will close window on cross button press
def on_closing(root):
    print("Window is closing...")
    root.destroy()
    root.closed=True
    sys.exit()
    
#This method will link login window with signup window    
def login_command(root):
    root.destroy() #Destroy signup window
    login.login_Window() #Open login window
    

    """
    Signup class created to demonstrate oops
    """
class Signup:
 #Method to handle signup window    
 def signup_Window(self): 
    window=Tk() #Create window for signup
    window.title('Signup') #Show signup title
    window.geometry('350x500+300+200')  #Dimensions of login window
    window.configure(bg='#fff')  #Background color of window is white
    window.resizable(False,False)  #Resizing is disabled as this can disturb layout of window.
    window.protocol("WM_DELETE_WINDOW",lambda: on_closing(window)) # Here lambda function is used to call method with params.
    window.closed=False  #Initial window closed param is false

    ################# Main signup Label #########
    Label(window,bg='white').place(x=50,y=50)
    frame=Frame(window,width=350,height=350,bg="white")
    frame.place(x=0,y=70)
    heading=Label(frame,text='Sign up',fg='#32a852',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
    heading.place(x=100,y=5)

    ############ Username textbox and label#################
    user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind('<FocusIn>', lambda event: on_enter(user))
    user.bind('<FocusOut>', lambda event: on_leave(user))
    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

    ############# Password textbox and label#################
    password=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    password.place(x=30,y=150)
    password.insert(0,'Password')
    password.bind('<FocusIn>', lambda event: on_enterpwd(password))
    password.bind('<FocusOut>', lambda event: on_leavepwd(password))
    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

    ############# Confirm Password textbox and label#################
    confirmPWD=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    confirmPWD.place(x=30,y=220)
    confirmPWD.insert(0,'Confirm Password')
    confirmPWD.bind('<FocusIn>', lambda event: on_enterCpwd(confirmPWD))
    confirmPWD.bind('<FocusOut>', lambda event: on_leaveCpwd(confirmPWD))
    Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)

    ###############Signup Button##########################
    Button(frame,width=39,pady=7,text='Sign up',bg='#32a852',fg='white',border=0,command=lambda:signup(user,password,confirmPWD,window)).place(x=35,y=280)
    label=Label(frame,text="I have an account",fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
    label.place(x=90,y=330)

    #############Login Button###################

    login=Button(frame,width=6,text='login',border=0,bg='white',cursor='hand2',fg='#32a852',command=lambda:login_command(window))
    login.place(x=200,y=330)

    ###############
    window.mainloop() # To keep window open
    return window.closed
    
    
 ####This function will be called only if file is executed as main module.
if __name__ == "__main__":
    print("Signup call from main")
    #Create Signup class object and call signup window function.
    singupObj=Signup()
    singupObj.signup_Window()
