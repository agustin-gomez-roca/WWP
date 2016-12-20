#!/usr/local/bin/python3.5
'''
Created on 12 oct. 2016

@author: ebernasconi

This script only run when a user login

En memoria de Ezequiel Bernasconi 8 de julio de 1993 - 29 de Noviembre de 2016
https://drive.google.com/open?id=0Bz5ykwxqS9lBak1TX1hsbXRCR00


'''


""" Import libraries """
import os #Use this library to run bath commands#
import sys #Use this library to stop the execution#
import time #Use this library to gets the date and time#
import pickle #Use this library to works with the pickle file#
import logging #Use this library to generate a log file#
import socket #Use this library to recovers the server hostname#
import smtplib #Use this library to connect into SMTP gmail server#
from email.mime.text import MIMEText  #Use this library to set structure´s email#


""" Create the Class Callsed user """
class User():
    def __init__(self, servernamec, usernamec, serveripc, displayc):
        self.servernamec = servernamec
        self.usernamec = usernamec
        self.serveripc = serveripc
        self.displayc = displayc
        logging.info("__INIT__ success") #__INIT__ generate#

    def secondlogin(self):
        logging.debug("Calls secondlog function successfully") #Calls success#
        counter = 0 #Initialize the counter#

        try:
            filepickle =  open(picklepath, "rb") #Open the file in write binari mode#
            portstatus = pickle.load(filepickle) #Load the pickle file that contain a list with dic#
            filepickle.close() #Close the file#
            logging.debug("Pickle file open successfully only in read mode") #Open file in read mode#
        except:
            logging.error("Impossible to open the pickle file") #The file can not be open#

        while counter < len(portstatus)-1:
            isthisuser = portstatus[counter]["userassigned"] #Recovers user name#
            isthisdisplay = portstatus[counter]["display"] #Recovers display number#

            if isthisuser == self.usernamec and isthisdisplay == self.displayc:
                """ If the user is equal to username and is the same sesion"""
                logging.debug("The user is loging in other Sunray")
                """End"""
                logging.info("Script run time: --- %s seconds ---" % (time.time() - starttime)) #Display the script´s run time#
                logging.debug("END PROCCESS - " + time.strftime("%H:%M:%S")) #End process#
                sys.exit(1) #Stop the run#
            else:
                """ Add the counter validation because we can have every user in the list null"""
                counter = counter+1 #If the user is not equal to username we can not release the port. Add +1 to the counter#

        logging.debug("The user is not log in a server")

        try:
            self.setport() #Call setport functions#
        except:
            logging.warning("Impossible Calls setport function") #Call error#

    def setport(self):

        logging.debug("Calls setport function successfully") #Calls success#
        counter = 0 #Initialize the counter#

        try:
            filepickle =  open(picklepath, "rb") #Open the file in write binari mode#
            portstatus = pickle.load(filepickle) #Load the pickle file that contain a list with dic#
            filepickle.close() #Close the file#
            logging.debug("Pickle file open successfully only in read mode") #Open file in read mode#
        except:
            logging.error("Impossible to open the pickle file") #The file can not be open#

        isnull = str(portstatus[counter]["userassigned"]) #Recover the user name that is hosted in the counterf dictionary#

        while isnull != "NULL":
            """ If the user is not equal to NULL """
            counter = counter+1 #If the user is not equal to NULL we can not assign the port. Add +1 to the counter#
            isnull = portstatus[counter]["userassigned"]  #Recovers the next user name to continue looping#
        else:
            """ If the user is equal to null """
            inicialport = portstatus[counter]["portassigned"] #Recovers the inicial port#
            portstatus[counter]["userassigned"] = self.usernamec #Assigns the user to port#
            portstatus[counter]["display"] = self.displayc

            logging.debug("The port " + str(inicialport) + " is ready to be assigned") #Port and user details#

            try:
                filepickle =  open(picklepath, "wb")  #Open the file in write binari mode#
                pickle.dump(portstatus, filepickle) #Write the list in the pickle file#
                filepickle.close() #Close the file#
                logging.debug("Pickle file open successfully this time in write mode") #Open file in write mode#
            except:
                logging.error("Impossible to open the pickle file, maybe the path is bad or another user using it") #pickle error when try to write the file#

            try:
                self.createxml(inicialport) #Calls xml function#
            except:
                logging.warning("Impossible to Calls createxml functions") #Call error#

            try:
                self.loginPA(inicialport) #Calls loginPA function#
            except:
                logging.warning("Impossible to Calls loginPA function") #Call error#

        logging.debug("Ends setport function") #End function#

    def createxml(self, inicialportf):
        logging.debug("Calls createxml function successfully") #Calls success#
        logging.debug("The xml path is: " + xmlpath) #Confirms the path#

        """ Generate the XML file """
        try:
            xmlfile = open(xmlpath, 'w') #Creates the xml file#
            logging.debug("Writting the xml file for: " + username) #Confirms the name#
        except:
            logging.warning("xml file can not open, please check the path") #Error when try to create the file#

        try:
            #/n is equal to enter#
            xmlfile.write("<uid-message>\n")
            xmlfile.write("<payload>\n")
            xmlfile.write("<login>\n")
            #Use // but in the xml only print one of these#
            xmlfile.write('<entry name="ml\\' + self.usernamec + '" ip="' + self.serveripc + '" blockstart="' + str(inicialportf) + '"/>\n') #We add +200 becasuse we need the final port in the ranged#
            xmlfile.write("</login>\n")
            xmlfile.write("</payload>\n")
            xmlfile.write("<type>update</type>\n")
            xmlfile.write("<version>1.0</version>\n")
            xmlfile.write("</uid-message>")
            xmlfile.close()
            logging.debug("xml file created successfully") #Confirms created#
        except:
            logging.error("xml file not created") #Call error#

        logging.debug("Ends createxml function") #End function#

    def loginPA(self, inicialportf):
        logging.debug("Calls loginPA function successfully") #Calls success#

        blankusername = " " + self.usernamec + " "
        commandiptable = "/sbin/iptables -t nat -A POSTROUTING -m owner --uid-owner " + blankusername +  " -p tcp -j SNAT --to-source " + self.serveripc + ":" + str(inicialportf) + "-" + str(inicialportf+199) #Adds the user in the iptable#
        iserror = os.system(commandiptable) #Runs the command in console#

        """ Valid is the os return a error """
        if iserror == 0:
            logging.debug("Add " + username + " successfully in iptables") #Run the command iptables successfully#
        else:
            logging.error("Impossible to add the user in iptables") #The command return an error#


        PAip = "10.11.1.2" #Palo Alto network ip#
        logging.debug("Set the PA IP equal to " + PAip) #Confirms the PA ip#

        commandPA = '/usr/bin/wget --no-proxy --no-check-certificate --delete-after --post-file=' + xmlpath + ' "https://' + PAip + '/api/?type=user-id&key=LUFRPT1aUEo5Mi8rQVhKZUp0eWhOcHB4Qy9RYWEyU1k9TVNDOWZDWnhONEpGSDJjc1JaZFEvNWt6R0xrbXBuaHM4MTJWMVh2NXpLTT0=&file-name=' + xmlname + '&client=wget&vsys=vsys1"' #Login the user in the PA-API#
        iserror = os.system(commandPA) #Runs the command in console#

        """ Valid is the os return a error """
        if iserror == 0:
            """ If it is zero, os runs the command successfully """
            logging.debug("Log " + username + " in the PA successfully") #Run the command wget successfully#
        else:
            """ If it is not zero, os runs the command with error """
            logging.error("Impossible to login the user in PA") #The command return an error#

        logging.debug("Ends loginPA function") #End function#

def sendemail():
    """ Create a email an send it """
    fromsend = "errorports@mercadolibre.com" #Trasnmitter#
    tosend = "agustin.gomezroca@mercadolibre.com" #Receiver#
    #Create de email#
    emailtxt = "Al usuario " + username + " en el servidor " + servername + " no se le han podido asignar puertos"
    email = MIMEText(emailtxt)
    email['From'] = fromsend
    email['To'] = tosend
    email['Subject']="Error ports in " + servername
    #Connect SMTP Gmail#
    serverSMTP = smtplib.SMTP('mailer-is.ml.com',25) #Connect to nagios server nagiossl-ar#
    serverSMTP.ehlo()
    serverSMTP.sendmail(fromsend,tosend,email.as_string()) #Send the email#
    serverSMTP.close() #Close the connection#



""" Main """
starttime = time.time() #Start the clock#

""" Set dada """
servername = socket.gethostname() #Recovers the tcoel name#
username = sys.argv[1] #Recovers the user name from command line argument 1#
display = sys.argv[2] #Recovers the display sesion number from command line argument 2#
serverip = [ip for ip in socket.gethostbyname_ex(servername)[2] #Recover the ip#
if not ip.startswith("127.")][:1]
serverip = serverip[0] #Remove []#

""" Start LOG """
logpath = "/var/log/" #Log path#
logname = "portslog.log" #Log name#
logfile = os.path.join(logpath, logname) #Set log path#
logging.basicConfig(level=logging.NOTSET, format="%(asctime)s " + servername + " %(filename)s[%(process)d][%(funcName)s] %(levelname)s " + username + " %(message)s", filename = logfile,
filemode = 'a',) #Log structure. Open the file in append mode#

logging.debug("START PROCESS " + time.strftime("%H:%M:%S")) #Start log#
logging.info("The server is: " + servername + " (" + serverip + ")") #Confirms the server and serve´s ip#
logging.info("The user, display is: " + username + " " + display) #Confirms the username#


""" Set Path"""
picklepath = "/var/run/wwp/portstatus.p" #Set pickle path#
logging.debug("The pickle path is " + picklepath) #Confirms the path#
xmlname = username + "login.xml" #Set xml name#
xmlpath = "/var/run/wwp/XML/login/" + xmlname #Set xml path#

""" Create a User object Callsed userloged and Calls setport function """
try:
    userloged = User(servername, username, serverip, display) #Create the user userloged#
    logging.info("User creates successfully") #Object created#
except:
    logging.error("Impossible creates the object user") #Object error#

try:
    userloged.secondlogin() #Calls setport function#
except Exception: #Use Exception, because sys.exit return a error and stop de run#
    logging.warning("Impossible Calls secondlogin function") #Call error#

"""End"""
logging.info("Script run time: --- %s seconds ---" % (time.time() - starttime)) #Display the script´s run time#
logging.debug("END PROCCESS - " + time.strftime("%H:%M:%S")) #End process#
