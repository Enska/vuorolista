#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# Original class author: Petteri Klemola
# Used, modified and published with permission for this use by Tommi Ruuth.
#
# Author: Tommi Ruuth
# 
# VUOROLISTA sivut

import calendar
import datetime
import dircache
import os.path
import random
import re
import struct
import sys

# Maybe we need these too?
import pickle
# import cgi

# not needed here, form are handled on index-class
# import cgitb; cgitb.enable()
# My classes:
# import dbHandler
# import utils
# dataHandler-class for more sophisticated data usage. (will have db and file handling)
import dataHandler

class Render:
  # Luokka joka rakentelee itse��n kutsumalla nettisivun

    def __init__(self, url):
        # @params: Base URL for this page
        self.cssPrefix = ""
	# print "Debug:Render:__init__: url -> %s" % url
	self.setBaseUrl(url)
	# Mandatory config information
	# TODO: This is now called multiple times. Only once is needed (if it is usable 
	# for other objects also)
	#self.conf = prepConfigs()
	

    def header(self):
        print "Content-Type: text/html \n"
        print "<html>"
        print "<head>"
        print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-15\" />"
        print "<meta name=\"Authors\" content=\"Tommi Ruuth\" />"
        print "<link rel=\"stylesheet\" href=\"%s/pelit.css\" type=\"text/css\">" % self.getContextRoot()
        print "</head>"
        print "<body>"
        self.cssEnd()
        self.cssStart('sisalto')

    def footer(self):
        self.cssEnd()
	bsu = self.url(self.getBaseUrl(),'Etusivu')
	bso = self.inUrl('vuorolista', 'Vuorolistat')
	bsi = self.inUrl('userconf', 'K�ytt�j�t')
	bsy = self.inUrl('calconf', 'Kalenterin asetukset')	
	self.cssClass('%(1)s | %(2)s | %(3)s | %(4)s <br> Maintainer: enska AT medusapistetutkapistefi' % {'1':bsu, '2':bso, '3':bsi, '4':bsy}, 'footer')
	# self.cssClass('Maintainer: enska�tmedusapistetutkapistefi | %s' % self.url('testi','Footer part'), 'footer')
        print "</body>"
        print "</html>"

    def cssClass(self,text,cssClass):
        print "<div class=\""+self.cssPrefix+cssClass+"\">"+self.formatText(text)+"</div>"

    def cssStart(self,cssClass):
        print "<div class=\""+self.cssPrefix+cssClass+"\">"

    def cssEnd(self):
        print "</div>"

    def tableStart(self):
	 print "<table border=\"0\" >"

    def tableEnd(self):
        print "</table>"

    def tableRowStart(self):
	 print "<tr>"

    def tableRowEnd(self):
	 print "</tr>"

    def tableCellStart(self):
	 print "<td>"

    def tableCellEnd(self):
	 print "</td>"

    def addTableRow(self, descr, cont):
	 self.tableRowStart()
	 self.tableCellStart()
	 print descr
	 self.tableCellEnd()
	 self.tableCellStart()
	 print cont
	 self.tableCellEnd()
	 self.tableRowEnd()

    def addListToTableRow(self, itemList):
      self.tableRowStart()
      # To avoid huge lists, just add less than "lislen" rows
      lislen = 10
      if ( len(itemList) < lislen ):
	 for co in (itemList):
	    self.tableCellStart()
	    print co
	    self.tableCellEnd()
      else:
	 self.tableCellStart()
	 print "Ups, too long list of data, will not add it to the table here... (max. length %s )" % lislen
	 self.tableCellEnd()
      self.tableRowEnd()

    def tableSStart(self):
        print "</div>"

    def tableSEnd(self):
        print "</div>"

    def lB(self):
        print "<br />"

    def bStart(self):
        return "<b>"

    def bEnd(self):
        return "</b>"

    def objDiv(self):
        print " : "

    def formatText(self, text):
        text = str(text)
        return text.replace('\r\n','<br />')

    def setBaseUrl(self, bu):
	# @params: (str) URL
	# @return: none
	self.setContextRoot(bu)
	self.baseUrl = '%s' % bu

    def getBaseUrl(self):
	# @params: None
	# @return: (str) baseUrl
	return self.baseUrl

    def setContextRoot(self,bu):
        # sets contextRoot (no index-file on that path)
	cr = bu
	if (cr.endswith("index.py")):
	      cr = cr.rstrip('index.py')
	      cr = cr.rstrip("/")
	self.contextRoot = '%s' % cr

    def getContextRoot(self):
        # returns contextroot
	# @params: None
	# @return: (str) contextRoot
	return self.contextRoot

    def inUrl(self, url, text=None):
	# @params: URL, alias for it
        return self.url(self.baseUrl+"/"+url, text)

    def url(self, url, text=None):
        if text is None:
            text = url
        return "<a href=\"%(url)s\">%(text)s</a>" % {'url':url,'text':text}

class defaultPage(Render) :

   def __init__(self, jep):
      # Set basics for the page
      Render.__init__(self, jep)
      # TODO: Read the calendar data from file (date, range, old edits).

   def doPage(self) :
      self.header()
      self.cssClass('Vuorolista sivusto | %s ' %self.url(self.baseUrl, 'Etusivu'),'header')
      print "<p>Yksinkertainen vuorolistasivusto.<br><br></p>"
      self.cssClass('Vuorolista | %s ' % self.inUrl('vuorolista', 'Vuorolistat'), 'tilasto')
      self.cssClass('K�ytt�j�nhallinta | %s ' % self.inUrl('userconf', 'User config'), 'tilasto')
      self.footer()

class vuoroLista(Render) :

#   def __init__(self, jep):
      # Set basics for the page
      #Render.__init__(self, jep)
      # TODO: Set curr date here and also the other "class-global" variables

   def doPage(self, jep) :
      self.header()
      self.cssClass('Vuorolista sivusto | %s ' %self.url(self.baseUrl, 'Etusivu'),'header')
      print "<p>Testi<br><br></p>"
      #calendar.weekday(2010,08,24)
      d1 = datetime.datetime.date(datetime.datetime.now())
      #d2 = datetime.date.weekday(1,1,2010)
      #d2 = datetime.datetime.date(2010, 01, 01).isoweekday()
      d2 = datetime.date.today()
      print 'd1 : %s' % d2
      dd = 1
      nyt = datetime.date.today()
      while dd < 13 :
	if datetime.date(nyt.year, dd, 01).isoweekday() == 1 :
	  print "JEEE, se on maanantai"
	print "first date %s " % datetime.date(nyt.year, dd, 01)
	self.lB()
	dd +=1
      
      
      self.footer()

class calConf(Render) :
  

  def __init__(self, jep):
    # Set basics for the page
    Render.__init__(self, jep)
    # TODO: Set curr date here and also the other "class-global" variables

  def doPage(self, jep) :
    self.header()
    self.cssClass('Calendar settings | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
    print "<p>Calendar config page <br><br></p>"
       
    print "<form name=\"input\" action=\"%s\" method=\"post\">" % (self.baseUrl+"/createcal")
    print "Calendar name: <input type=\"text\" name=\"name\"/>"
    self.lB()
    print "Workshift 1: <input type=\"text\" name=\"shift1\"/>"
    self.lB()
    print "Workshift 2: <input type=\"text\" name=\"shift2\"/>"
    self.lB()
    print "Workshift 3: <input type=\"text\" name=\"shift3\"/>"
    self.lB()
    print "Start date: <input type=\"text\" name=\"startdate\"/>"
    self.lB()
    print "End date: <input type=\"text\" name=\"enddate\"/>"
    self.lB()

    print "<input type=\"submit\" value=\"Create new calendar\"/>";
    print "</form>"
     
    self.footer()


class userConf(Render) :

   def __init__(self, jep):
      Render.__init__(self, jep)

      # Users

      self.confDir='etc'
      self.userFile="users.cfg"

      # Lets check that directory exists
      if ( os.path.exists(self.confDir)) :
	# Read config-file, create list of users
	self.confObject = dataHandler.fileHandler(self.confDir, self.userFile)
	self.confFiles = self.confObject.getFilesList()
	#self.confData = self.confObject.getVariableInd(0)
	#getDataFromFile(self.confObject)
	#print "Debug: pituus -> %s " % (len(self.confFile))
	#print "ny: %s" % self.confData
	#self.printAll()
      else:
	# ERROR, this dir doesnt exist, create error message instead of resultlist
	errmsg = ["ERROR: Directory ("+self.confDir+") doesnt exist..."] 
	self.confData = errmsg


   def doPage(self, something) :
      # something should be the possible data of "old" machine

      self.header()
      self.cssClass('Config-page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')

      self.lB()

      #print "Debug: possible param from html-form -> %s <br>" % something
      self.lB()
      print "obj: %s,%s" % (self.confObject.getValue(0,0,"name"), self.confObject.getValue(0,1,"name"))
      self.lB()
      print "pit: %s" % len(self.confObject)
      self.lB()

      print "<form name=\"input\" action=\"%s\" method=\"post\">" % (self.baseUrl+"/update")
      print "User: <input type=\"text\" name=\"server\"/>"
      self.lB()
      self.tableStart()

      machlist = ["id", "user", "Full name"]
      self.addListToTableRow(machlist)
      #print "lala: %s" % self.confFile
      cou = 0
      aite = len(self.confObject)
      while cou < aite :
      
	machlist[0] = cou + 1
	mac = self.confObject.getValue(0,cou,"name")
	#print mac
	machlist[1] = "<b> %s </b>" % self.inUrl("server/" + mac, mac)
	machlist[2] = "<input type=\"radio\" name=\"mac\" value=\"mac\" />"
	self.addListToTableRow(machlist)
	cou += 1

      cou = 0
      self.tableEnd()
      # print "</input >"

      print "<input type=\"submit\" value=\"Modify\"/>";
      print "</form>"

      # testing the form page
      #self.addMachineInfoForm("testi")

      self.footer()

   def addMachineInfoForm(self, mach):

      self.eds = prepData("/var/www/tommi/data")
      self.lili = self.eds.getFilesList()
      print "Machine config-files: <br>"
      for lin in self.lili:
	 print "%s <br> \n" % lin

      self.namelist = ['name', 'ip', 'dns', 'snmpver', 'snmpcomm', 'desc', '2', 'user', 'passu']

      self.emplist = {}
      self.emplist[self.namelist[0]] = "Unique, shor describing name of the machine (like dns name)."
      self.emplist[self.namelist[1]] = "IP"
      self.emplist[self.namelist[2]] = "DNS name of the machine."
      self.emplist[self.namelist[3]] = "Version of snmp (v2 only)."
      self.emplist[self.namelist[4]] = "Snmp community pharse."
      self.emplist[self.namelist[5]] = "Description of the machine"
      self.emplist[self.namelist[6]] = "tba"
      self.emplist[self.namelist[7]] = "Your username for this page"
      self.emplist[self.namelist[8]] = "Your password to save data"
      

      # testing the function, to see that the form works and saves dataFiles
      # TODO: move the editing page on its own, either with old data or to have new data
      self.doMachineForm(self.emplist)
      # emplist["name", "ip", "phar", "snmpver"] = "koneen nimi", "koneen ip", "jotain", "jossain"
      # print "list %s::%s" % (emplist.get("name", "nooooooo"), emplist.get("ip", "nooooooo"))
      if (mach == "uusi") :
	 # This is a new machine, no data to fetch
	 print "New data..."
	 #print "list %s" % emplist
	 self.doMachineForm(emplist)

      else:
	 # This is an old machine, fetch data and show it to the user
	 self.lB()
	 print "Old data..."


   def doMachineForm(self, datalist):
      # Create form with the data we received
      # maybe this could be done with javascript or similar?
      dsli = datalist
      namelist = self.namelist
      self.lB()
      target = (self.baseUrl+"/savedata")
      # For testing, there is additional python class
      # target = "http://localhost/tommi/formHandler.py"
      print "<p>Give information for the new machine. This is send to %s </p>"  % target
      print "<form name=\"id=newdata\" action=\"%s\" method=\"post\">" % target
      self.tableStart()
      for nametin in (namelist):
	 self.a = [0,1,2]
	 self.a[0] = "%s :" % nametin
	 self.a[1] = "<input type=\"text\" name=\"%(1)s\" value=\"test-%(1)s\" />" % { '1':nametin }
	 self.a[2] = "%(2)s" % { '2':dsli.get(nametin, "Errrr") }
	 self.addListToTableRow(self.a)

      self.tableEnd()
      self.lB()
      self.lB()

      print "<input type=\"submit\" value=\"Save data\"/>";
      print "<input type=\"reset\" value=\"Cancel (clear data)\"/>";
      print "</form>"

class saveData(Render) :
  # NOTE: Actual data saving is done on dataHandler class.

  def __init__(self, ds, form):
    Render.__init__(self, ds)
    self.workDir = ds
    if ( form ) :
      self.form2 = form
    else :
      self.form2 = "No data received from form."
    # Lets check that directory exists
    if ( os.path.exists(self.workDir)):
      # Yep, get files if there are any
      self.oldFilesList = prepData(self.workDir)
    else:
      # ERROR, this dir doesnt exist, print to screen
      print "ERROR: Directory (%s) doesnt exist (check your configs). " % self.workDir

  def doPage(self, fform):
    
    # Show what we got
    self.header()
    self.cssClass('Info-sivu | %s ' %self.url(self.baseUrl, 'Etusivu'),'header')
    #print self.getContextRoot()
    print "<p>Tietojen k�sittely <br><br></p>"
    print self.form2
    self.lB()

    self.footer()


class createCal(Render) :
  # NOTE: This is only meant to be used once, when creating new calendar

  def __init__(self, ds, form):
    Render.__init__(self, ds)
    self.workDir = ds
    if ( form ) :
      self.form2 = form
    else :
      self.form2 = "No data received from form."
    # Lets check that directory exists
    if ( os.path.exists(self.workDir)):
      # Yep, get files if there are any
      self.oldFilesList = prepData(self.workDir)
    else:
      # ERROR, this dir doesnt exist, print to screen
      print "ERROR: Directory (%s) doesnt exist (check your configs). " % self.workDir

  def doPage(self, fform):
    self.header()
    self.cssClass('Info-page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
    #print self.getContextRoot()
    print "<p>Creating new calendar <br><br></p>"
    #print self.form2
    self.lB()
    print self.form2.keys()
    self.lB()
    calname = self.form2.getvalue("name")
    calsf1 = self.form2.getvalue("shift1")
    calsf2 = self.form2.getvalue("shift2")
    calsf3 = self.form2.getvalue("shift3")
    startd = self.form2.getvalue("startdate")
    endd = self.form2.getvalue("enddate")
    #calsf1 = self.form2.getvalue("name")
    #calsf1 = self.form2.getvalue("name")
    self.lB()

    self.footer()


class prepConfigs(Render) :
  
   def __init__(self):
      # Read configurations from config-file. 
      # This file and its directory are fixed at here. 
      # 
      
      # NOTE: relative path
      self.confDir='etc'

      # Lets check that directory exists
      if ( os.path.exists(self.confDir)):
	# Read config-file, create list of users
	self.confFile = dataHandler.fileHandler(self.confDir, 'users.cfg')
	#print "Debug: pituus -> %s " % (len(self.confFile))
	#self.printAll()

      else:
	# ERROR, this dir doesnt exist, create error message instead of resultlist
	errmsg = ["ERROR: Directory ("+self.confDir+") doesnt exist..."] 
	self.confFile = errmsg
	
   def printAll(self):
      confFile = self.confFile
      # print "sivuParseri.py::prepConfigs::printAll: Debug:", confFile
      print "sivuParseri.py::prepConfigs::printAll: Debug var: %s" % confFile.getVariableInd(0, "confDir")
      print "sivuParseri.py::prepConfigs::printAll: Debug var: %s" % confFile.getVariableInd(0, "serverConfDir")
      print "sivuParseri.py::prepConfigs::printAll: Debug var: %s" % confFile.getVariableInd(0, "snmpDir")
      #print "sivuParseri.py::prepConfigs::printAll: Debug var: %s" % confFile.getVariableInd(0, "confDir")	


   # NOTE For each FIXED config variable, we create a own function    
   def getServerConfDir(self):
      confFile = self.confFile
      return confFile.getVariableInd(0, "serverConfDir")

   def getSnmpDir(self):
      confFile = self.confFile
      return confFile.getVariableInd(0, "snmpDir")

   def getAllConf(self):
      # Ok. Lets return what ever we got...
      return self.confFile

class doSaveDataPage(Render) :

   def __init__(self, URL, dataFromForm):
      Render.__init__(self, URL)
      self.filledForm = dataFromForm
      self.valuesList = {}
      self.oldFiles = prepData("data")

      # print "Content-Type: text/html \n"
      # print "Deb: %s <br> \n" % dataFromForm


   def doPage(self, data):
      # TODO: handle data
      values = self.valuesList
      formData = self.filledForm
      oldFiles = self.oldFiles
      filesDir = 'mach_confs'
      self.resultFile = ''
      self.blaah = saveData("data")

      self.header()
      self.cssClass('Reply-page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
      print "<p>Data save has been tried, see results below.</p>"
      
      values['debug'] = 1 # Set to 0 to have dummy data
      values['hasData'] = 1 # Set to 1, we dont know if there is any data
      values['user'] = ""
      values['passu'] = ""
      values['name'] = ""
      values['ip'] = ""
      values['dns'] = ""
      values['snmpver'] = ""
      values['snmpcomm'] = ""
      values['1'] = ""
      values['2'] = ""
      # print "Debug: list: %s <br> \n" % formData

      if ( len(formData) > 0 ):
	 values['hasData'] = 0
	 for valname in (values):
	    # tt1 = formData.getfirst(valname, "ERR: got nothing from html-form")
	    # print "debug: form: getfirst: (name) %s -> (value) %s \n <br>" % (valname, tt1)
	    filledList = formData.getlist(valname)
	    for pl in (filledList):
	       if ( values[valname] == "" ):
		  values[valname] = pl
		  # print "Debug: values for-loop: %s <br><br> \n" % pl
	       else:
		  values[valname + pl] = pl

      else:
	 values['hasData'] = 1 # Set to 1, NO data
	 # print "ERROR: No html-form data received... <br> \n"

      if ( values['debug'] == 0 ):
	values['hasData'] = 0 # Set to 0, we want see some data for debug reasons
	values['user'] = "a1"
	values['passu'] = "a2"
	values['name'] = "a3"
	values['ip'] = "a4"
	values['dns'] = "a5"
	values['snmpver'] = "a6"
	values['snmpcomm'] = "a7"
	values['1'] = "a8"
	values['2'] = "a9"

      if (values['hasData'] == 0):
	 print "<p>Data from FORM to be saved. <br> \n"

	 # Check if it was old config (from the filename (not the best way...))
	 # succ = self.blaah.saveDataToFile(oldFiles, values)
	 succ = self.blaah.saveDataToFile(filesDir, values)
	 # resFile = open(values["name"], "w")
	 
	 # Working way
	 # resultFile = open(os.path.join('etc', 'filu1-%s' % values['name']), 'wb')
	 # for lk in (values):
	    # print " %s -> %s  <br> \n" % (lk, values[lk])
	    # val = "%s : %s \n" % (lk, values[lk])
	    # resultFile.write(val)
	
	 # resultFile.close()
	    
	    # Example code
	    # commentfile = open(os.path.join(indexdir,'comment-%s' % filename), 'wb')
	    # pickle.dump(comments, commentfile)
	    # commentfile.close()

	 print "</p>"

      else:
	 print "<p>ERROR: No data received from form... Nothing to save. </p> \n"


      self.footer()


class debugPage(Render) :

   def __init__(self, URL, messa):
      Render.__init__(self, URL)
      #mes = self.messa
      # self.ds = prepData("/home/tommi/omat/python/snmpinfo/snmp_kyselyt")
      # self.bigList = snmpParseri.Parser(self.ds.getFilesList())

   def doPage(self, URL, messa):
      #@params: name of server or instance
      #@return: None
      self.header()
      self.cssClass('DEBUG-page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')
      print "<p> This is Debug page. <br> It is shown because it is uncommented from the index-page.</p>"
      self.bStart()
      print "<p>"
      print "Debug context-root: "
      self.lB()
      print "%s" % self.getContextRoot()
      self.lB()
      self.lB()
      print "Debug URL: "
      self.lB()
      print "%s" % URL
      self.lB()
      self.lB()
      print "Debug message:"
      self.lB()
      print "%s" % messa
      print "</p>"
      self.bEnd()
      self.lB()
      self.footer()



# Error("Err -> sivuParseri.addAllServerInfo, no statistic to show.").doPage("addAllServerInfo")

class Error(Render):
   def __init__(self, text):
      self.text = text
      Render.__init__(self, text)
      self.prefix = [
            'Ongelmia j�sennyksess�',
            'K�rp�nen',
            'J�rjestelm� huumeessa',
            'Suoritus kohtasi seuraavan virhetilanteen',
            'Fehler',
            'Kone on t�t� mielt�',
            'Saisit puolestani jatkaa, mutta',
            ]

   def doPage(self, classn, message):
     # We dont do header or footer, because the caller does these...
     #self.header()
     self.lB()
     self.lB()	
     self.cssClass("<b> %s </b> ->  %s " % (classn, message), 'testi')
     self.lB()
     # self.cssClass("%s -> <b>%s:</b> %s" % message, (random.choice(self.prefix), self.text), 'virhe')
     #self.footer()
