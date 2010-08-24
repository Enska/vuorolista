#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
#
# Author: Tommi Ruuth
#
# dataHandler.py class for fetchin (if with db) and saving data.
#
# if handling data from directory (files) we have to have the file type.
#
# if using db, then this class all is saved. caller must take care data integrity.
#

import dircache
import os.path
import re
import string
import sys

class fileHandler:
  # This class/method is for FILE-listing 
  
  def __init__(self, sourceDirectory, sourceFiles=None):
    # @param: The directry of the source-files
    # This one is mandatory. -> TODO: check the param
    self.sdir = sourceDirectory
    if (sourceFiles==None):
      # No file to read given, so we read ALL from sourceDirectory
      # TODO: No good, in this way we read also the hidden, binary etc. files... 
      self.sourceFiles = self.listFiles(sourceDirectory)  
      #print "sourceFiles -> %s , sourceDirectory -> %s " % (self.sourceFiles, sourceDirectory)
    else:
      # TODO: Lets check that file exists
      fil2 = []
      fil2.insert(0, sourceDirectory  + "/" + sourceFiles)
      # print "fil2 -> %s, sourceFiles -> %s , sourceDirectory -> %s " % (fil2, sourceFiles, sourceDirectory)
      self.sourceFiles = fil2
    self.bigList =  {}
    cou = 0
    # print "dataHandler::filehanHandler::__init__: sourceFiles-list -> %s" % sourceFiles

    for sourceFile in self.sourceFiles:
      self.bigList[cou] = self.getDataFromFile(sourceFile)
      #print "dataHandler::fileHandler::__init__: Debug: result from bigList-list (%s : %s): %s\n\n" % (cou, sourceFile, self.bigList[cou])
      cou = cou + 1
      #print "saatiin:  %s" % self.bigList[cou-1]
    
    #for k in self.bigList:
      #print "fileHandler::__init__: Debug: BIGLIST: %s" % self.bigList[k]
    #c=0
    #for k in self.bigList[0]:
      #print "fileHandler::__init__: Debug: BIGLIST: %s" % self.bigList[0][c].get('name','err')
      #c+=1
    #print "bl1: %s" % self. bigList[0]
    #print "bl2: %s" % self.bigList[0][0].get("name", 'err')
    #print "bl2: %s" % self.bigList[0][1].get("name", 'err')    
    #print "len: %s" % len(self.bigList)


  def __len__(self):
    # if empty list, return 0
    self.leng = 0
    if ( self.bigList == "" ):
      true
    else:
      for aa in self.bigList[0]:
	self.leng += 1
    return self.leng

  def getDataFromFile(self, fileToRead):
    # This one reads the file trough. Collect everything from it and
    # returns it as a dict-list for the caller.
    #
    # FIX: Do a check that the file is really a txt-file.
    # print "dataHandler::fileHandler::getDataFromFile: Debug: file to read -> %s \n" % fileToRead
    #self.lista = {}
    try:
      filu = open(fileToRead, 'r')
      # Do file-check here, before readeing the content
      lcou=0
      multilist=[]
      for livi in filu.readlines() :
	if ( livi[:1] == '#' ) :
	  # Skip comment line
	  continue
	else :
	  self.lista = {}
	  # string.strip(livi)
	  #livi.strip()
	  # livi.strip("\n")
	  # TODO: Remove linebreak...
	  # livi+=livi.replace("\n","")
	  # TODO: break the line by separator and THEN separate each item from its key.
	  # rely on that "," is a item separator
	  if livi.count(',') > 0:
	    i1 = self.lineCutter(livi, ',')
	    for item in i1 :
	      key, value = self.fileLineSeparator(item, ':')
	      self.lista[key] = value
	      #print key, "-> ",value
	      #print "dataHandler::fileHandler::getDataFromFile: Debug: key -> \"%s\", values -> \"%s\" " % (key,value)
	    multilist.insert(lcou,self.lista)
	    lcou+=1
	  else :
	    if livi.count('=') > 0:
	      self.sep='='
	    else :
	      self.sep=':'
	    key, value = self.fileLineSeparator(livi, self.sep)
	    self.lista[key] = value
	    #print "dataHandler::fileHandler::getDataFromFile: Debug: key -> \"%s\", values -> \"%s\" " % (key,value)
	  	  
      filu.close()
    except IOError, err:
      self.lista[0] = 'Couldnt open datafile %s directory: (%r). <br>\n' % (fileToRead, err)
      # pass
      #print 'Couldnt open datafile %s directory: (%r). <br>\n' % (fileToRead, err)
    if len(multilist) > 1 :
      return multilist
    else :
      return self.lista

  def lineCutter(self, dataLine, separator) :
    # Params: one line  of data
    # Action: split line with separator
    if dataLine == '' :
      return "problem", "Line was empty"
    parts = dataLine.split(separator)
    return parts

  def fileLineSeparator(self, dataLine, separator) :
    # Params: one line of the read result.
    # Action: split the line on two parts (expect only one separator)
    if dataLine == '' :
      return "problem", "Line was empty"
    parts = dataLine.split(separator)
    return parts[0].strip(), parts[1].strip()

  def listFiles(self, dirr):
    # Read all the filenames and full paths to a list and returns this
    files2 = []
    if ( os.path.exists(dirr) == 1 ):
      try:
	files1 = dircache.listdir(dirr)
	# TODO: dircache is to be deprecated on ptyhon 2.6, this has to be changed...
	l = len(files1)
	#print "filut: %(1)s , len -> %(2)s <br>" % { '1':files1, '2':l }
	if ( len(files1) > 0 ):
	  snmpfilut1 = files1[:] # jotta voidaan muokata listaa
	  for fil in files1:
	    withdir = dirr + '/' + fil
	    files2.insert(files1.index(fil), dirr + '/' + fil)
	else:
	  files2.insert(1, "No files to read at directory %s ." % dirr)

	#print "filut: %(1)s  <br>" % { '1':files2}
      except IOError, err:
	print 'Couldnt open the file-directory (%r).' % ('dirr',), err
    
    return files2


  def getFilesList(self):
    # return datalist
    return self.sourceFiles

  def getVariableInd(self, ind, vari=None):
    # Return the value of file on index ind and named vari
    # Caller must know what to call
    # 
    #print "Debug getVariableInd(): list -> %s, ind -> %s, vari -> %s <br>" % (self.bigList[ind], ind, vari)
    return self.bigList[ind].get(vari, 'err, nothing to return')

  def getVarInd(self, ind1, ind2, vari=None):
    return self.bigList[ind1][ind2].get(vari, 'err')

  def getValue(self, ind1, ind2, vari=None):
    return self.bigList[ind1][ind2].get(vari, 'err')

  def getVariableName(self, item, vari=None):
    # Return the value of the variable "vari" and return the value (can be done straight also)
    # Caller must know what to call
    # 
    #print "Debug getVariableInd(): list -> %s, ind -> %s, vari -> %s <br>" % (self.bigList[ind], ind, vari)
    #return self.sourceFiles[item].get(vari, 'err, nothing to return')
    las = "empty"
    bla = 0
    for na in self.bigList:
      if self.bigList[na]["name"] == item:
	las = self.bigList[na].get(vari, "errrrr")
      else:
	#las = "na: %s ,item: %s, bl_na: %s" % (na, item, self.bigList[na])
	las = self.bigList[na]["name"]
	
      bla = bla + 1
      
    return las


class dbHandler:
  # This method os for database-listing of data
  # ONLY present as reminder as maybe-to-be-implemented someday
  def __init__(self, dbconfig):
    # We want to have the config data from file (or something)
    print "Just testing"

