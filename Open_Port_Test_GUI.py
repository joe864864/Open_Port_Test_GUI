"""
Title: Open_Port_Test_GUI
Author: Joseph Scott
Build Date: January 2020
Description: GUI application to test what ports for an IP Address or host are open. Allows user to specify ip address, port range, and timeout. 
Ability to save and load saved runs, and help section.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import HORIZONTAL
from tkinter import messagebox
import socket
import os
import json

class MyGUI:
    #init main window
    def __init__(self):

        # Create the main window widget
        self.main_window = tk.Tk()

        #Set window size and title
        self.main_window.minsize(500,250)
        self.main_window.title("Open Port Test")

        #Save file
        self.filename = "save.json"

        #String vars
        #used to auto populate feilds from saved
        self.savedIP = tk.StringVar()
        self.savedIP.set("")
        self.savedStartPort = tk.StringVar()
        self.savedStartPort.set("")
        self.savedEndPort = tk.StringVar()
        self.savedEndPort.set("")
        self.savedTimeout = tk.StringVar()
        self.savedTimeout.set("")

        #Setup string vars for output text
        self.outputText1 = tk.StringVar()
        self.outputText1.set("-")

        self.outputText2 = tk.StringVar()
        self.outputText2.set("-")

        #Double var to hold progress bar position
        self.progressVar = tk.DoubleVar()
        self.progressVar.set(0)

        #Create frames
        self.title_frame = tk.Frame(self.main_window)
        self.load_save_frame = tk.Frame(self.main_window)
        self.ip_frame = tk.Frame(self.main_window)
        self.ports_frame = tk.Frame(self.main_window)
        self.timeout_frame = tk.Frame(self.main_window)
        self.submit_frame = tk.Frame(self.main_window)
        self.progress_frame = tk.Frame(self.main_window)
        self.output_frame = tk.Frame(self.main_window)
        self.help_quit_frame = tk.Frame(self.main_window)

        #Populate title frame
        #Title label
        self.titleLabel = tk.Label(self.title_frame, text="Open Port Test", font=("Consolas 30 bold"))
        self.titleLabel.pack(padx=5, pady=5)

        #Populate save load frame
        #Save and load buttons
        self.load = tk.Button(self.load_save_frame, text='Load', command=self.loadDataWindow, width = 10)
        self.save = tk.Button(self.load_save_frame, text='Save', command=self.saveDataWindow, width = 10)
        self.load.pack(side='left', padx=5, pady=5)
        self.save.pack(side='left', padx=5, pady=5)

        #Populate IP frame
        #ip label and entry
        self.ipLabel = tk.Label(self.ip_frame, text="Address or host:", width='25')
        self.ipEntry = tk.Entry(self.ip_frame, width='15', textvariable=self.savedIP)
        self.ipLabel.pack(side='left', padx=5, pady=5)
        self.ipEntry.pack(side='left', padx=5, pady=5)

        #Populate port frame
        #Port label, start port entry, -, end port entry
        self.portsLabel = tk.Label(self.ports_frame, text="Ports (start-end):", width='25')
        self.startPortEntry = tk.Entry(self.ports_frame, width='5', textvariable=self.savedStartPort)
        self.dashLabel = tk.Label(self.ports_frame, text="-", width='1')
        self.endPortEntry = tk.Entry(self.ports_frame, width='5', textvariable=self.savedEndPort)
        self.portsLabel.pack(side='left', padx=5, pady=5)
        self.startPortEntry.pack(side='left', padx=5, pady=5)
        self.dashLabel.pack(side='left', pady=5)
        self.endPortEntry.pack(side='left', padx=5, pady=5)

        #Populate timeout frame
        #Timeout label and entry
        self.timeoutLabel = tk.Label(self.timeout_frame, text="Timeout in Sec (Default: 1):", width='25')
        self.timeoutEntry = tk.Entry(self.timeout_frame, width='15', textvariable=self.savedTimeout)
        self.timeoutLabel.pack(side='left', padx=5, pady=5)
        self.timeoutEntry.pack(side='left', padx=5, pady=5)

        #Populate save and submit buttons
        self.submit = tk.Button(self.submit_frame, text='Submit', command=self.submition, width = 10)
        self.submit.pack(side='left', padx=5, pady=5)

        #Populate help and quit button
        self.help = tk.Button(self.help_quit_frame, text='Help', command=self.helpBox, width = 10)
        self.quit = tk.Button(self.help_quit_frame, text='Quit', command=self.main_window.destroy, width = 10)
        self.help.pack(side='left', padx=5, pady=5)
        self.quit.pack(side='left', padx=5, pady=5)

        #Populate progress frame
        #Create progress bar
        self.progress = ttk.Progressbar(self.progress_frame, orient = HORIZONTAL, length = 120, mode = 'determinate', maximum=100, variable=self.progressVar)
        self.progress.pack(pady=5)

        #Populate output frame
        #2 rows, 1 label each
        self.outputLabel1 = tk.Label(self.output_frame, textvariable=self.outputText1)
        self.outputLabel1.pack(side='top', padx=5, pady=5)
        self.outputLabel2 = tk.Label(self.output_frame, textvariable=self.outputText2)
        self.outputLabel2.pack(side='bottom', padx=5, pady=5)

        #pack frames
        self.title_frame.pack()
        self.load_save_frame.pack()
        self.ip_frame.pack()
        self.ports_frame.pack()
        self.timeout_frame.pack()
        self.submit_frame.pack()
        self.progress_frame.pack()
        self.output_frame.pack()
        self.help_quit_frame.pack()

        # Enter the tk main loop.
        tk.mainloop()

    #Called when user presses help button
    #Displays help message box
    def helpBox(self):
        messagebox.showinfo("Help",
        "Load: Opens window that allows user to select a save which can be loaded or deleted.\n\n"+
        "Save: Opens window that allows user to enter name for save or select a save to overwrite.\n\n"+
        "Address or host: Input a valid ip address or host name.\nEx. 192.168.1.1 or www.python.org\n\n"+
        "Ports (start-end): Enter begining port and ending port to test a range. Enter the same number in both boxes to test a single port. Available ports: 0-65535\n\n"+
        "(Optional) Timout in Sec: Enter time allowed for port responce in seconds. Defualt is 1 second. For the most reliable response use 5 seconds.\n\n"+
        "Submit: Tests ports.")

    #Creates load window, called when load button is clicked
    def loadDataWindow(self):

        if os.path.exists(self.filename):
            #create top level winow
            self.load_window = tk.Toplevel()

            #Set window size and title
            self.load_window.minsize(500,250)
            self.load_window.title("Load Save")

            #stringVar for load error messages
            self.messageText = tk.StringVar()
            self.messageText.set("")

            #Get current available saves
            savenames = self.getSaveNames()

            #Holds dropdown(option menu) defualt
            self.dropVar = tk.StringVar()
            self.dropVar.set(savenames[0])

            #create load window frames
            load_title_frame = tk.Frame(self.load_window)
            load_choice_frame = tk.Frame(self.load_window)
            load_submit_frame = tk.Frame(self.load_window)
            load_message_frame = tk.Frame(self.load_window)
            load_cancel_frame = tk.Frame(self.load_window)

            #load window title
            TitleLabel = tk.Label(load_title_frame, text="Load Save", font=("Consolas 30 bold"))
            TitleLabel.pack(padx=5, pady=5)

            #load window choose save to load
            choiceLabel = tk.Label(load_choice_frame, text="Please choose save to load:", width='25')
            choiceOpt = tk.OptionMenu(load_choice_frame, self.dropVar, *savenames)
            choiceOpt.config(width=15)
            choiceLabel.pack(side='left', padx=5, pady=5)
            choiceOpt.pack(side='left', padx=5, pady=5)

            #load window delete and load window
            deleteSubmit = tk.Button(load_submit_frame, text='Delete Save', command=self.delete_save, width = 10)
            loadSubmit = tk.Button(load_submit_frame, text='Load Save', command=self.loadData, width = 10)
            deleteSubmit.pack(side='left', padx=5, pady=5)
            loadSubmit.pack(side='left', padx=5, pady=5)

            #load window label, used for error messages
            MessageLabel = tk.Label(load_message_frame, textvariable=self.messageText)
            MessageLabel.pack(padx=5, pady=5)

            #load window label, cancel save
            cancel = tk.Button(load_cancel_frame, text="Cancel", command=self.load_window.destroy, width = 10)
            cancel.pack(padx=5, pady=5)

            #pack load winodw frames
            load_title_frame.pack()
            load_choice_frame.pack()
            load_submit_frame.pack()
            load_message_frame.pack()
            load_cancel_frame.pack()

            #needed if allow no iteraction with main window
            #self.main_window.wait_window(load_window)

        else:
            self.outputText1.set("No saves")

    #verify delete submition
    def delete_save(self):
        if os.path.exists(self.filename):
            try:
                #read
                with open(self.filename, 'r') as f:
                    data = json.load(f)

                #Verify user wants to delete
                for x in data['saves']:
                    if x['SaveName'] == self.dropVar.get():
                        MsgBox = tk.messagebox.askquestion ('Confirm deletion',
                            'Are you sure you want to delete: ' + self.dropVar.get() +'\n'
                            + 'Address: ' + x['Address'] + '\n'
                            + 'Start Port: ' + x['StartPort'] + '\n'
                            + 'End Port: ' + x['EndPort'] + '\n'
                            + 'Timeout: ' + x['Timeout'] + '\n',
                            icon = 'warning')

                #If user confirms deletion
                if MsgBox == 'yes':
                    try:
                        #read
                        with open(self.filename, 'r') as f:
                            data = json.load(f)

                        count = 0
                        toremove = 0

                        for x in data['saves']:
                            if x['SaveName'] == self.dropVar.get():
                                toremove = count
                            count += 1
                        del data['saves'][toremove]

                        self.messageText.set(self.dropVar.get() + ' deleted successfully')
                        self.outputText1.set(self.dropVar.get() + ' deleted successfully')

                        #Write
                        with open(self.filename, 'w') as outfile:
                            json.dump(data, outfile)

                        self.load_window.destroy()

                    except:
                        self.messageText.set('An error occurred deleting ' + self.dropVar.get() + ' from: ' + self.filename)
                        print('An error occurred deleting ' + self.dropVar.get() + ' from: ' + self.filename)
                else:
                    self.messageText.set('Deletion of ' + self.dropVar.get() + ' canncelled.')
            except:
                self.messageText.set('An error occurred reading saves from: ' + self.filename)
        else:
            self.outputText1.set("No save file exists.")

    #Get name of saves
    def getSaveNames(self):

        if os.path.exists(self.filename):

            #list holds save names
            savenames = []

            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)

                for x in data['saves']:
                    savenames.append(x['SaveName'])

            except IOError:
                self.messageText.set('An error occurred loading saves from: ' + self.filename)
                print('An error occurred loading save from:', self.filename)
            return savenames
        else:
            self.outputText1.set("No save file exists.")

    #loads data from choosen save
    def loadData(self):

        if os.path.exists(self.filename):
            try:
                #read
                with open(self.filename, 'r') as f:
                    data = json.load(f)

                #get data from json
                for x in data['saves']:
                    if x['SaveName'] == self.dropVar.get():
                        self.savedIP.set(x["Address"])
                        self.savedStartPort.set(x["StartPort"])
                        self.savedEndPort.set(x["EndPort"])
                        self.savedTimeout.set(x["Timeout"])

                self.messageText.set('Data loaded successfully.')
                self.outputText1.set('Data loaded successfully from save: ' + self.dropVar.get())
                self.load_window.destroy()

            except:
                self.messageText.set('An error occurred loading data from: ' + self.filename)
                print('An error occurred loading data from:', self.filename)
        else:
            self.outputText1.set("No current saves")
            self.load_window.destroy()

    #Creates load window, called when load button is clicked
    def saveDataWindow(self):

        #create top level winow
        self.save_window = tk.Toplevel()

        #Set window size and title
        self.save_window.minsize(500,250)
        self.save_window.title("Save")

        #stringVar for save error messages
        self.messageText = tk.StringVar()
        self.messageText.set("")

        #Get current available saves
        if os.path.exists(self.filename):
            self.savenames = self.getSaveNames()
        else:
            self.savenames = []

        #Holds dropdown(option menu) defualt
        self.dropVar = tk.StringVar()
        self.dropVar.set(None)

        self.saveName = tk.StringVar()
        self.saveName.set("")

        #create save window frames
        save_title_frame = tk.Frame(self.save_window)
        save_choice_frame = tk.Frame(self.save_window)
        save_submit_frame = tk.Frame(self.save_window)
        save_message_frame = tk.Frame(self.save_window)
        save_cancel_frame = tk.Frame(self.save_window)

        #save window title
        TitleLabel = tk.Label(save_title_frame, text="Save", font=("Consolas 30 bold"))
        TitleLabel.pack(padx=5, pady=5)

        #save window choose save to load
        choiceLabel = tk.Label(save_choice_frame, text="Please enter name for save or \n select one to overwrite:", width='25')
        choiceEntry = tk.Entry(save_choice_frame, width='15', textvariable=self.saveName)
        choiceOpt = tk.OptionMenu(save_choice_frame, self.dropVar, None, *self.savenames)
        choiceOpt.config(width=15)
        choiceLabel.pack(side='left', padx=5, pady=5)
        choiceEntry.pack(side='left', padx=5, pady=5)
        choiceOpt.pack(side='left', padx=5, pady=5)

        #save window submit button
        saveSubmit = tk.Button(save_submit_frame, text='Submit', command=self.saveData, width = 10)
        saveSubmit.pack(side='left', padx=5, pady=5)

        #save window label, used for error messages
        MessageLabel = tk.Label(save_message_frame, textvariable=self.messageText)
        MessageLabel.pack(padx=5, pady=5)

        #save window label, cancel save
        cancel = tk.Button(save_cancel_frame, text="Cancel", command=self.save_window.destroy, width = 10)
        cancel.pack(padx=5, pady=5)

        #pack save winodw frames
        save_title_frame.pack()
        save_choice_frame.pack()
        save_submit_frame.pack()
        save_message_frame.pack()
        save_cancel_frame.pack()

        #needed if allow no iteraction with main window
        #self.main_window.wait_window(self.save_window)

    #Called when user clicks save button
    #Saves current entrys to file
    def saveData(self):

        #Used to track valid input
        valid = True

        nameOfSave = self.saveName.get()

        #check of save name was enters
        if len(nameOfSave) == 0:
            if self.dropVar.get() == 'None':
                valid = False
                self.messageText.set("No save name")
            else:
                nameOfSave = self.dropVar.get()

        #validate data to be saved
        if valid:
            valid = self.validate(self.messageText)
        else:
            self.messageText.set("Invalid data")

        if valid:
            try:
                #if save file exists
                if os.path.exists(self.filename):
                    #read
                    with open(self.filename, 'r') as f:
                        data = json.load(f)

                    #If save name alreay exists
                    if nameOfSave in self.savenames:
                        for x in data['saves']:
                            if x['SaveName'] == nameOfSave:
                                MsgBox = tk.messagebox.askquestion ('Overwrite',
                                'Are you sure you want to overwrite previous save?\n'
                                + 'Address: ' + x['Address'] + ' --> ' + self.ipEntry.get() + '\n'
                                + 'Start Port: ' + x['StartPort'] + ' --> ' + self.startPortEntry.get() + '\n'
                                + 'End Port: ' + x['EndPort'] + ' --> ' + self.endPortEntry.get() + '\n'
                                + 'Timeout: ' + x['Timeout'] + ' --> ' + self.timeoutEntry.get() + '\n',
                                icon = 'warning')

                                if MsgBox == 'yes':
                                    x['Address'] = self.ipEntry.get()
                                    x['StartPort'] = self.startPortEntry.get()
                                    x['EndPort'] = self.endPortEntry.get()
                                    x['Timeout'] = self.timeoutEntry.get()
                                    self.outputText1.set("Save successful")
                                else:
                                    self.outputText1.set("Save cancelled")

                    #If new save name
                    else:
                        data['saves'].append({
                            "SaveName": nameOfSave,
                            "Address": self.ipEntry.get(),
                            "StartPort": self.startPortEntry.get(),
                            "EndPort": self.endPortEntry.get(),
                            "Timeout": self.timeoutEntry.get()
                        })
                        self.outputText1.set("Save successful")

                #if save file doest exist yet
                else:
                    data = {}
                    data['saves'] = []
                    data['saves'].append({
                        "SaveName": nameOfSave,
                        "Address": self.ipEntry.get(),
                        "StartPort": self.startPortEntry.get(),
                        "EndPort": self.endPortEntry.get(),
                        "Timeout": self.timeoutEntry.get()
                    })
                    self.outputText1.set("Save successful")

                #write
                with open(self.filename, 'w') as outfile:
                    json.dump(data, outfile)

                self.save_window.destroy()

            except:
                self.messageText.set('An error occurred with file: ' + self.filename)

    #Called when user clicks submit button
    #Validates inputs, calls testport, and outputs results
    def submition(self):

        #if all inputs were valid
        if self.validate(self.outputText1):

            ip = self.ipEntry.get()
            portStart = int(self.startPortEntry.get())
            portEnd = int(self.endPortEntry.get())
            timeout = float(self.timeoutEntry.get())

            #setuo vars
            openPorts = []
            currentPort = portStart
            output = ""

            #loop through ports testing each
            while(currentPort <= portEnd):
                temp = self.testPort(ip,currentPort,timeout)
                self.progressVar.set(((currentPort-portStart)/(portEnd-portStart))*100)
                self.outputText1.set("Time left: "+str(int((portEnd-currentPort)*timeout))+" Seconds - Total time: "+str(int((portEnd-portStart)*timeout))+" Seconds")
                if temp >= 0:
                    self.outputText2.set("Port: " + str(currentPort) + " OPEN")
                else:
                    self.outputText2.set("Port: " + str(currentPort) + " NOT OPEN")
                try:
                    #self.main_window.update_idletasks()
                    self.main_window.update()
                except:
                    break

                currentPort+=1

                #If port was connected add to list
                if temp >= 0:
                    openPorts.append(temp)

            print('--------------------------')
            print("Done")
            print('--------------------------')

            #Setup output
            output = output + "Open ports for " + str(ip) + ": "

            #Configure output
            if len(openPorts) == 0:
                output = output + "NONE"
            else:
                for count in range(len(openPorts)):
                    if len(openPorts) == 0:
                        output = output + "NONE"
                    elif count+1 == len(openPorts):
                        output = output + str(openPorts[count])
                    elif count+2 == len(openPorts) and len(openPorts) == 2:
                        output = output + str(openPorts[count]) + " and "
                    elif count+2 == len(openPorts):
                        output = output + str(openPorts[count]) + ", and "
                    else:
                        output = output + str(openPorts[count]) + ", "

            self.outputText2.set(output)
            print(output, end='')
            print('\n', end='')
            print("Ports tested: ", portStart,"-", portEnd, sep='')

    #Test port
    #takes address, port, and timeout
    #returns -1 if not able to connect or port number if connected
    def testPort(self,address,port, timeout):
        s = socket.socket()
        s.settimeout(timeout)
        open = -1
        try:
            s.connect((address, port))
        except Exception:
            print("Could not connect to: ",address,':',port,sep='')
        else:
            print("Connected: ",address,':',port,sep='')
            open = port
        finally:
            s.close()
        return open

    #Validate input data
    #Validates ip, port, and timeout
    def validate(self, outputText):
        valid = True

        #validate ip or hostname (ipEntry entry)
        try:
            ip = self.ipEntry.get()
            if socket.gethostbyname(ip) == ip:
                print('{} is a valid IP address'.format(ip))
                valid = True
            elif socket.gethostbyname(ip) != ip:
                print('{} is a valid hostname'.format(ip))
                valid = True
        except:
            outputText.set("Invalid IP")
            valid = False

        #Validate port start and end entry
        #Port must be equal to or between 0 and 65535
        #Port start must be less than or eqaul to port end
        if valid:
            try:
                portStart = int(self.startPortEntry.get())
                portEnd = int(self.endPortEntry.get())
                if portStart >= 0 and portStart <= 65535 and portStart<=portEnd:
                    valid = True
                elif(portStart>portEnd):
                    valid = False
                    outputText.set("Invalid End Port")
                else:
                    valid = False
                    outputText.set("Invalid Start Port")
            except:
                valid = False
                outputText.set("Invalid Port")

        if valid:
            try:
                if valid and portEnd >= 0 and portEnd <= 65535:
                    valid = True
                else:
                    valid = False
                    outputText.set("Invalid End Port")
            except:
                valid = False
                outputText.set("Invalid End Port")

        #Validate timeout entry
        #Must be greater then 0
        #If nothings entered, defaults to 1
        if valid:
            try:
                timeout = float(self.timeoutEntry.get())
            except ValueError:
                #timeout = 1
                self.savedTimeout.set("1")
                valid = True
            else:
                if(timeout <= 0):
                    valid = False
                    outputText.set("Invalid time out")

        return valid

# Create an instance of the MyGUI class.
my_gui = MyGUI()