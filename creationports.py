#!/usr/local/bin/python3.5
'''
Created on 14 oct. 2016

@author: ebernasconi

This script only run at the end of the day, and it generate a pickle file in disk

En memoria de Ezequiel Bernasconi 8 de julio de 1993 - 29 de Noviembre de 2016
https://drive.google.com/open?id=0Bz5ykwxqS9lBak1TX1hsbXRCR00

'''

""" Import libraries """

import os #Use this library to run bath commands#
import sys #Use this library to stop the execution#
import time #Use this library to gets the date and time#
import socket #Use this library to recover the server hostname#
import pickle #Use this library to works with the pickle file#
import logging #Use this library to generate a log file#
import smtplib #Use this library to connect into SMTP gmail server#
import getpass #User this library to recovers the user name#
from email.mime.text import MIMEText  #Use this library to set structure´s email#



def logoutIPTABLES():
    logging.debug("Calls logoutIPTABLES function successfully") #Calls success#

    iserror = 0

    while iserror == 0:
        logging.debug("Iptables entry number 1 deleted")
        iserror = os.system("/sbin/iptables -t nat -D POSTROUTING 1")
    else:
        logging.debug("No more entries")

    return iserror

def KMA():
    logging.debug("Calls KMA function successfully") #Calls success#
    PAIP = "10.11.1.2" #Set PA IP#
    KMAPath = "/script/wwp/XML/" #Set XML path#
    KMAName = "init-user-port-" + servername + ".xml" #Set XML name#
    KMATotal = KMAPath + KMAName #Set complete path#
    commandPA = '/usr/bin/wget --no-check-certificate --no-proxy --post-file= ' + KMATotal +  '" https://' + PAIP + '/api/?type=user-id&key=LUFRPT1aUEo5Mi8rQVhKZUp0eWhOcHB4Qy9RYWEyU1k9TVNDOWZDWnhONEpGSDJjc1JaZFEvNWt6R0xrbXBuaHM4MTJWMVh2NXpLTT0=&file-name=' + KMAName + '&client=wget&vsys=vsys1"' #Generate command#



    iserror = os.system(commandPA) #Api call#

    if iserror == 0:
        logging.info("Clear the PA successfully")
    else:
        logging.warning("Error in KMA")

    logging.debug("Ends KMA function") #End function#

def sendemail():
    logging.debug("Calls sendemail function successfully") #Call success#
    logging.debug("Sends the log in a email") #The final line in the log#
    completepath = logpath + logname #Complete log path#
    filetoread = open(completepath, "r") #Open the log in read mode#
    texttosend = filetoread.read() #Read all the log#
    filetoread.close() #Close the log#

    """ Create a email an send it """
    fromsend = "errortcoeltest@mercadolibre.com" #Trasnmitter#
    tosend = "ezequiel.bernasconi@mercadolibre.com, diego.silva@mercadolibre.com" #Receiver#

    #Create the email#
    emailtxt = texttosend #Emails body#
    email = MIMEText(emailtxt)
    email['From'] = fromsend
    email['To'] = tosend
    email['Subject']="creationsports log" #Subject in the email#
    #Connect SMTP Gmail#
    serverSMTP = smtplib.SMTP('mailer-is.ml.com',25) #Connect to nagios server nagiossl-ar#
    serverSMTP.ehlo()
    serverSMTP.sendmail(fromsend,tosend,email.as_string()) #Send the email#
    serverSMTP.close() #Close the connection#


""" Main """

starttime = time.time() #Start the clock#
servername = socket.gethostname() #Recovers the tcoel name#
username = getpass.getuser() #Recoves the user name#
userip = [ip for ip in socket.gethostbyname_ex(servername)[2] #Recovers the ip#
if not ip.startswith("127.")][:1] #Recover ip that does not start with 127#
userip = userip[0] #Remove []#

""" Start LOG """
logpath = "/var/log/" #Log path#
logname = "portslog.log" #Log name#
logfile = os.path.join(logpath, logname) #Set log path#
logging.basicConfig(level=logging.NOTSET, format="%(asctime)s " + servername + " %(filename)s[%(process)d][%(funcName)s] %(levelname)s " + username + " %(message)s", filename = logfile,
filemode = 'a',) #Log structure. Open the file in append mode#

logging.debug("START PROCESS " + time.strftime("%H:%M:%S")) #Start log#

""" Set piclkepath """
picklename = "portstatus.p" #Set pickle name#
picklepath = "//var/run/wwp/" + picklename #Set pickle path#


""" Create a list """
portstatus=[] #Creates a empty list that later contain dic#
logging.debug("Create a empty list") #List created#

""" Sets values for the for cicle """
initialport = 30000 #The initial port#
endport = 65400 #The ultimate start port that can be assigned#
addport = 200 #Number of ports that will be add#
forcounter = 0 #Cycle loop#

""" For Cycle ++200 """
for port in range(initialport, endport, addport):
    portstatusdic = {"userassigned": "NULL", "portassigned":port, "display":"0"} #Create a dic and adds it in the list#
    portstatus.append(portstatusdic) #Add the dic in the list#
    forcounter = forcounter + 1 #Add one to the counter loop#
else:
    if len(portstatus) == forcounter:
        logging.debug("Added " + str(len(portstatus)) + " dictionaries") #List ok#
    else:
        logging.warning("Checks the lens of the list") #List not ok#

""" Creates the pickle file """
try:
    filepickle =  open(picklepath, "wb") #Open the file in write binari mode#
    pickle.dump(portstatus, filepickle)   #Create the file and writes it#
    filepickle.close() #Close the file#
    logging.debug("File created on: " + picklepath + " with the name: " + picklename) #Confirms the path#
except:
    logging.error("File error, verify the path file")
    logging.error("Stop the run, impossible to create the binary file") #Action description#
    sys.exit() #Stop the run#


try:
    logoutIPTABLES()
except:
    logging.warning("Impossible calls logoutIPTABLES function") #Calls error#

try:
    KMA()
except:
    logging.debug("Impossible to calls KMA function") #Calls error#


logging.info("Script run time: - %s seconds -" % (time.time() - starttime)) #Display the script´s run time#
logging.debug("END PROCCESS - " + time.strftime("%H:%M:%S")) #End process#
