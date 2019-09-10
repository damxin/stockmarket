# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

from xml.dom.minidom import parse
import xml.dom.minidom

from finance.util import GlobalCons as gc

DBDSTAG="ds"
LOGICNAMEATTR="logic_name"
DBTYPEATTR="db_type"
SERVERATTR="server"
PORTATTR="port"
USERNAMEATTR="user_name"
PASSWORDATTR="password"
DATABASEATTR="database"

class XMLCFG:
    def __init__(self,xmlfilepath):
        self.xmlfilepath = xmlfilepath
        self.dbcfgdict={}

    def getDbInfoFromXmlFile(self):
        DOMTree = xml.dom.minidom.parse(self.xmlfilepath)
        collection = DOMTree.documentElement
        dss = collection.getElementsByTagName(DBDSTAG)
        for ds in dss:
            dsdict = {}
            if ds.hasAttribute(DBTYPEATTR):
                dsdict[gc.DBTYPEKEY] = ds.getAttribute(DBTYPEATTR)
            if ds.hasAttribute(SERVERATTR):
                dsdict[gc.SERVERKEY] = ds.getAttribute(SERVERATTR)
            if ds.hasAttribute(PORTATTR):
                dsdict[gc.PORTKEY] = ds.getAttribute(PORTATTR)
            if ds.hasAttribute(USERNAMEATTR):
                dsdict[gc.USERNAMEKEY] = ds.getAttribute(USERNAMEATTR)
            if ds.hasAttribute(PASSWORDATTR):
                dsdict[gc.PASSWORDKEY] = ds.getAttribute(PASSWORDATTR)
            if ds.hasAttribute(DATABASEATTR):
                dsdict[gc.DATABASEKEY] = ds.getAttribute(DATABASEATTR)
            if ds.hasAttribute(LOGICNAMEATTR):
                logicnamecfg = ds.getAttribute(LOGICNAMEATTR)
                self.dbcfgdict[logicnamecfg]=dsdict
        # print(self.dbcfgdict)



# if __name__ == '__main__':
#     dbcfg = XMLCFG("F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml")
#     dbcfg.getDbInfoFromXmlFile()