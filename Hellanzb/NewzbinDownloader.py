import os, httplib, urllib, Hellanzb.NZBQueue
from Hellanzb.Log import *
from Hellanzb.NZBDownloader import NZBDownloader 
__id__ = '$Id$'

class NewzbinDownloader(NZBDownloader):

	def __init__(self):
		"""Nothing to see here, move along"""
	
	def download(self, msgId):
		"""Fetch an NZB from newzbin.com and add it to the queue."""

		info('Downloading newzbin ID: ' + msgId)
		params = urllib.urlencode({'username': Hellanzb.NEWZBIN_USERNAME, 'password': Hellanzb.NEWZBIN_PASSWORD, 'reportid': msgId})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn = httplib.HTTPConnection("v3.newzbin.com:80")
		conn.request("POST", "/dnzb/", params, headers)
		response = conn.getresponse()
		if not response.getheader('X-DNZB-RCode') == '200':		
			error('Unable to download newzbin NZB: ' + msgId + ' (' + response.getheader('X-DNZB-RText') + ')') 
			return
		info('Newzbin nzb ID: ' + msgId + ' downloaded successfully')
		dest = Hellanzb.QUEUE_DIR  + response.getheader('X-DNZB-Name').replace('/','').replace('\\','') + '.nzb'

		#Pass category information on
		category = ''		
		if Hellanzb.CATEGORIZE_DEST:
			category = response.getheader('X-DNZB-Category')		
		
		out = open(dest, 'wb')
		out.write(response.read())
		out.close
		conn.close()
		
		Hellanzb.NZBQueue.enqueueNZBs(dest, category = category)

		return True

	def canDownload():
		""" Whether or not the conf file supplied www.newzbin.com login info """
		noInfo = lambda var : not hasattr(Hellanzb, var) or getattr(Hellanzb, var) == None
		if noInfo('NEWZBIN_USERNAME') or noInfo('NEWZBIN_PASSWORD'):
			return False
		return True

	canDownload = staticmethod(canDownload)
