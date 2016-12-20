#!/usr/local/bin/python3.5
'''
Created on 15 oct. 2016

@author: ebernasconi

This script only run when a user logout

En memoria de Ezequiel Bernasconi 8 de julio de 1993 - 29 de Noviembre de 2016
https://drive.google.com/open?id=0Bz5ykwxqS9lBak1TX1hsbXRCR00


'''

""" Import libraries """
import os #Use this library to run bath commands#
import sys #Use this library to stop the execution#
import time #Use this library to gets the date and time#
import pickle #Use this library to works with the pickle file#
import socket #Use this library to recover the server hostname#
import logging #Use this library to generate a log file#


class User():
    def __init__(self, servernamec, usernamec, serveripc, displayc):
        self.servernamec = servernamec
        self.usernamec = usernamec
        self.serveripc = serveripc
        self.displayc = display
        logging.info("__INIT__ success") #__INIT__ generate#

    def finduser (self):

        logging.debug("Calls finduser function successfully") #Calls success#
        counter = 0 #Initialize the counter#

        try:
            filepickle =  open(picklepath, "rb") #Open the file in write binari mode#
            portstatus = pickle.load(filepickle) #Load the pickle file that contain a list with dic#
            filepickle.close() #Close the file#
            logging.debug("Pickle file open successfully only in read mode") #Open file in read mode#
        except:
            logging.error("Impossible to open the pickle file") #The file can not be open#

        continueloop = True #Set in True to loop until finds the user and the display#

        while continueloop == True and counter < len(portstatus)-1:

            isthisuser = portstatus[counter]["userassigned"] #Recovers user name#
            isthisdisplay = portstatus[counter]["display"] #Recovers display sesion#

            if isthisuser == self.usernamec and isthisdisplay == self.displayc:
                """ If the user is equal to username """
                portstatus[counter]["userassigned"] = "NULL" #Rename the username to NULL and retrieve the port to assign it later#
                portstatus[counter]["display"] = "0"
                inicialport = portstatus[counter]["portassigned"] #Recover the port that was freed#

                try:
                    filepickle =  open(picklepath, "wb")  #Open the file in write binari mode#
                    pickle.dump(portstatus, filepickle) #Write the list in the pickle file#
                    filepickle.close() #Close the file#
                    logging.debug("Pickle file open successfully this time in write mode") #Open file in write mode#
                    logging.debug("Start the free actions for " + isthisuser + " - " + isthisdisplay +  ". The port that will be free is: " + str(inicialport)) #Port to release details#
                except:
                    logging.error("Impossible to open the pickle file") #The file can not be open#

                try:
                    self.createxml(inicialport) #Calls xml function#
                except:
                    logging.warning("Impossible to Calls createxml functions") #Call error#

                try:
                    self.logoutPA(inicialport) #Calls logoutPA function#
                except:
                    logging.warning("Impossible to Calls logoutPA functions") #Call error#

                continueloop = False #Set the loop variable in false no stop the cicle#

            else: #else If#
                """ If the user is not equal to username or the display is diferent """
                counter = counter+1 #If the user is not equal to username we can not release the port. Add +1 to the counter#




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
            xmlfile.write("<logout>\n")
            #Use // but in the xml only print one of these#
            xmlfile.write('<entry name="ml\\' + self.usernamec + '" ip="' + self.serveripc + '" blockstart="' + str(inicialportf) + '"/>\n')
            xmlfile.write("</logout>\n")
            xmlfile.write("</payload>\n")
            xmlfile.write("<type>update</type>\n")
            xmlfile.write("<version>1.0</version>\n")
            xmlfile.write("</uid-message>")
            xmlfile.close()
            logging.debug("xml file created successfully") #Confirms created#
        except:
            logging.error("xml file not created") #Confirms created#

        logging.debug("Ends createxml function") #End function#

    def logoutPA(self, inicialportf2):
        inicialportf2 = int(inicialportf2)
        logging.debug("Calls logoutPA function successfully") #Calls success#
        PAip = "10.11.1.2" #Palo Alto network ip#
        logging.debug("Set the PA IP equal to " + PAip) #Confirms the PA ip#

        commandPA = "/usr/bin/wget --no-proxy --no-check-certificate --post-file=" + xmlpath + ' "https://' + PAip + '/api/?type=user-id&key=LUFRPT1aUEo5Mi8rQVhKZUp0eWhOcHB4Qy9RYWEyU1k9TVNDOWZDWnhONEpGSDJjc1JaZFEvNWt6R0xrbXBuaHM4MTJWMVh2NXpLTT0=&file-name=' + xmlname + '&client=wget&vsys=vsys1"' #Logout the user in the PA-API#
        iserror = os.system(commandPA) #Runs the command in console#

        """ Valid is the os return a error """
        if iserror == 0:
            """ If it is zero, os runs the command successfully """
            logging.debug("Free " + username + " in the PA successfully") #Run the command wget successfully#
        else:
            """ If it is not zero, os runs the command with error """
            logging.error("Impossible to logout the user in PA") #The command return an error#

        commandiptable = '/sbin/iptables -t nat -D POSTROUTING $(/sbin/iptables -t nat -L --line-numbers |awk -v rango="' + str(inicialportf2) + '-' + str(inicialportf2+199) + '"' + " '($NF ~ rango) {print $1}')" #Recovers the user line in the IP table that had benn assigned and removes it from the ip table#

        iserror = os.system(commandiptable) #Runs the command in console#

        """ Valid is the os return a error """
        if iserror == 0:
            logging.debug("Free " + username + " successfully in iptables") #Run the command iptables successfully#
        else:
            logging.error("Impossible to logout the user in iptables") #The command return an error#

        logging.debug("Ends logoutPA function") #End function#

""" Main """
starttime = time.time() #Start the clock#

""" Set Data """
servername = socket.gethostname() #Recovers the tcoel name#
username = sys.argv[1] #Recovers the user name from command line argument 1#
display = sys.argv[2] #Recovers the display sesion number from command line argument 2#
serverip = [ip for ip in socket.gethostbyname_ex(servername)[2] #Recovers the ip#
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
logging.info("The user is: " + username) #Confirms the username#


""" Set Path"""
picklepath = "/var/run/wwp/portstatus.p" #Set pickle path#
logging.debug("The pickle path is " + picklepath) #Confirms the path#
xmlname = username + "logout.xml" #Set xml name#
xmlpath = "/var/run/wwp/XML/logout/" + xmlname #Set xml path#

""" Create a User object Callsed userloged and Calls finduser function """

try:
    userloged = User(servername, username, serverip, display) #Create the user userloged#
    logging.info("User creates successfully") #Object created#
except:
    logging.error("Impossible creates the object user") #Objects error#

try:
    userloged.finduser() #Calls find user function#
except:
    logging.warning("Impossible Calls finduser function") #Call error#

"""End"""
logging.info("Script run time: --- %s seconds ---" % (time.time() - starttime)) #Display the script´s run time#
logging.debug("END PROCCESS - " + time.strftime("%H:%M:%S")) #End process#
exit
