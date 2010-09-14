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
  
  def __init__(self, jep):
    # Set basics for the page
    Render.__init__(self, jep)
    # TODO: Set curr date here and also the other "class-global" variables
    
    self.confDir='data'
    self.calFile="calen.txt"
    self.errors=''

    try:
      # Let's read the stuff and prepare for problems
      self.calObject = dataHandler.fileHandler(self.confDir, self.calFile)
      self.confFiles = self.calObject.getFilesList()

    except IOError :
      #  (self.confDir "/" self.userFile)
      self.errors="File or directory (%s) doesnt exist." % ("jees")
    #except Exception :
      #self.errors="Exception raised by sub-class."

  def doPage(self, jep) :
    self.header()
    self.cssClass('Vuorolista sivusto | %s ' %self.url(self.baseUrl, 'Etusivu'),'header')

    if len(self.errors) > 0 :
      # ERROR: We have found problem
      print "There was some problems with handling of data. Reason should be below."
      self.lB()
      print "Reason of the problem: %s" % self.errors
	
    else :
      
      # can raise IndexError
      #print "obj: %s,%s" % (self.calObject.getValue(0,0,"date"), self.calObject.getValue(0,1,"date"))
      self.lB()
      self.l1 = len(self.calObject)
      print "pit: %s" % self.l1
      self.lB()
      
      self.kk = 0
      
      self.tableStart()
      self.na = ["Pvm","Aamuvuoro","Iltavuoro","Huomiot","Poissa"]
      self.addListToTableRow(self.na)
      #while self.calObject.getValue(0,self.kk,"date") :
      #for kk in self.calObject :
      while self.kk < self.l1 :
	try:
	  
	  #print "pvm: %s, shifts: %s, %s, notes: %s, away: %s " % (self.d1, self.s1, self.s2, self.n1, self.a1)
	  #self.lB()

	  self.a = [0,1,2,3,4]
	  self.a[0] = self.calObject.getValue(0,self.kk,"date")
	  self.a[1] = self.calObject.getValue(0,self.kk,"shift1")
	  self.a[2] = self.calObject.getValue(0,self.kk,"shift2")
	  self.a[3] = self.calObject.getValue(0,self.kk,"notes")
	  self.a[4] = self.calObject.getValue(0,self.kk,"away")
	    
	  self.addListToTableRow(self.a)

	  
	  self.kk += 1
      
	except IndexError :
	  print "Calendar list handling went out of bounds..."

      # Ok, whole loop is done
      self.tableEnd()  

      
    
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
    print "<p>Uuden kalenterin asetukset.<br><br>N�m� asetetaan kerran, jonka j�lkeen kalenterin muuttamiseksi pit�� luoda uusi kalenteri.</p>"
       
    print "<form name=\"input\" action=\"%s\" method=\"post\">" % (self.baseUrl+"/createcal")
    print "Kalenterin nimi: <input type=\"text\" name=\"name\"/> "
    self.lB()
    print "Ty�vuoro 1."
    self.lB()
    print "Nimi: <input type=\"text\" name=\"shift1name\"/> (esim. aamuvuoro)"
    self.lB()
    print " Tunnit : <input type=\"text\" name=\"shift1\"/> (esim. 04:00-12:00)"
    self.lB()
    print "Ty�vuoro 2."
    self.lB()
    print "Nimi: <input type=\"text\" name=\"shift2name\"/> (esim. iltavuoro)"
    self.lB()
    print "Tunnit: <input type=\"text\" name=\"shift2\"/> (esim. 10:00-18:00)"
    self.lB()
    print "Ty�vuoro 3."
    self.lB()
    print "Nimi: <input type=\"text\" name=\"shift3name\"/> (esim. p�iv�vuoro)"    
    self.lB()
    print "Tunnit: <input type=\"text\" name=\"shift3\"/> (esim. 08:00-16:00)"
    self.lB()
    print "Aloitusp�iv� <input type=\"text\" name=\"startdate\"/> (vvvv-kk-pp Mist� p�iv�st� kalenteri alkaa.)"
    self.lB()
    print "Loppumisp�iv� <input type=\"text\" name=\"enddate\"/> (vvvv-kk-pp Mihin p�iv��n asti kalenteri kest��. Max. 1 vuosi)"
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
      self.errors=''

      try:
	# Let's read the stuff and prepare for problems
	self.confObject = dataHandler.fileHandler(self.confDir, self.userFile)
	self.confFiles = self.confObject.getFilesList()

      except IOError :
	#  (self.confDir "/" self.userFile)
	self.errors="File or directory (%s) doesnt exist." % ("jees")
      except Exception :
	#print "dataHandler.testi() raised an exception"
	#self.patho = self.confDir"/"self.userFile
	self.errors="Exception raised by sub-class."


      # Lets check that directory exists
      #if ( os.path.exists(self.confDir)) :
	# Read config-file, create list of users
	#self.confData = self.confObject.getVariableInd(0)
	#getDataFromFile(self.confObject)
	#print "Debug: pituus -> %s " % (len(self.confFile))
	#print "ny: %s" % self.confData
	#self.printAll()
      #else:
	# ERROR, this dir doesnt exist, create error message instead of resultlist
	#errmsg = ["ERROR: Directory ("+self.confDir+") doesnt exist..."] 
	#self.confData = errmsg


   def doPage(self, something) :
      # something should be the possible data of "old" machine

      self.header()
      self.cssClass('Config-page | %s ' %self.url(self.baseUrl, 'Frontpage'),'header')

      self.lB()
      if len(self.errors) > 0 :
	# ERROR: We have found problem
	print "There was some problems with. Reason should be below."
	self.lB()
	print "Reason of the problem: %s" % self.errors
	
      else :
	# Normal case, continue as usual
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

	try:
	  print "Trying to catch Exception"
	  self.lB()
	  self.confObject.testi()
	except Exception :
	  print "dataHandler.testi() raised an exception"

      self.footer()


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
    print "Formin avaimet: %s" % self.form2.keys()
    self.lB()
    self.calname = self.form2.getvalue("name")
    self.calsf1 = self.form2.getvalue("shift1")
    self.calsf1name = self.form2.getvalue("shift1name")
    self.calsf2 = self.form2.getvalue("shift2")
    self.calsf2name = self.form2.getvalue("shift2name")
    self.calsf3 = self.form2.getvalue("shift3")
    self.calsf3name = self.form2.getvalue("shift3name")
    self.startd = self.form2.getvalue("startdate")
    self.endd = self.form2.getvalue("enddate")
    #calsf1 = self.form2.getvalue("name")
    #calsf1 = self.form2.getvalue("name")
    
    # Sanity checks:
    # startd < ennd
    if ( self.startd.count('-') == 2) or ( self.endd.count('-') == 2) :
      self.staparts = self.startd.split("-")
      self.endparts = self.endd.split("-")
    # We should also check that every parts is interger type and length is correct
      self.startnum = self.staparts[0],self.staparts[1],self.staparts[2]
      self.endnum = self.endparts[0],self.endparts[1],self.endparts[2]
    else :
      # ERrror
      print "p�iv�m��r�muoto ei ole validi (vvvv-kk-pp)..."
      # For the testing we use fixed dates
      print "Debug: FIksatut p�iv�t."
      self.startnum = "2010-01-01"
      self.endnum = "2010-03-31"
      self.lB()


    # TODO: subfunctions for the date calculation
    # before that, no need to do checks
    if (1) > (3):
      print "Error. Aloitysp�iv� _ei_ voi olla my�h�isempi kuin lopetusp�iv�: %s - %s" % (self.startd, self.endd)
    else :
      # lets create some calendar
      #self.hmm.Calendar(calendar.MONDAY)
      #print calendar.itermonthdates(self.staparts[0], self.staparts[1])
      #calendar.setfirstday(calendar.MONDAY)
      #d2 = datetime.date.today()
      #print 'd1 : %s' % d2
      #print datetime.date.setfirstday(calendar.MONDAY)
      #print calendar.itermonthdates(2010,07)
      calendar.setfirstweekday(0)
      #self.m1 = calendar.calendar(2010, 02)
      self.m1 = calendar.monthcalendar(2010, 03)
      self.m2 = calendar.month(2010, 04, 1, 1)
      self.lB()
      print self.m1
      self.lB()
      print "<pre>", self.m2 ,"</pre>"
      #for d in self.m2:
	#if d != "":
	  #print d
	  #self.lB()
      
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
