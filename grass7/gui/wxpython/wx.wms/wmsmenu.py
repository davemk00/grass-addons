#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon Jul 11 04:58:20 2011

import wx
from wxPython.wx import *
from wx.lib.pubsub import Publisher
from urllib2 import Request, urlopen, URLError, HTTPError
from parse import parsexml, isServiceException, populateLayerTree, isValidResponse
from WMSMapDisplay import NewImageFrame
from addserver import AddServerFrame
from ServerInfoAPIs import addServerInfo, removeServerInfo, updateServerInfo, initServerInfoBase, getAllRows
from LoadConfig import loadConfigFile


# begin wxGlade: extracode
# end wxGlade



class wmsFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wmsFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.URL = wx.StaticText(self, -1, "URL")
        self.ServerList = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_SIMPLE)
        self.LayerTree = wx.TreeCtrl(self, -1, style=wx.TR_HAS_BUTTONS|wx.TR_NO_LINES|wx.TR_MULTIPLE|wx.TR_MULTIPLE|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)
        self.username = wx.StaticText(self, -1, "UserName")
        self.usernameInput = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_TAB)
        self.password = wx.StaticText(self, -1, "Password")
        self.passwordInput = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_TAB|wx.TE_PASSWORD)
        self.GetCapabilities = wx.Button(self, -1, "GetCapabilities")
        self.GetMaps = wx.Button(self, -1, "GetMaps")
        self.addServer = wx.Button(self, -1, "Manage Servers")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT_ENTER, self.OnServerListEnter, self.ServerList)
        self.Bind(wx.EVT_COMBOBOX, self.OnServerList, self.ServerList)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnLayerTreeSelChanged, self.LayerTree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnLayerTreeActivated, self.LayerTree)
        self.Bind(wx.EVT_BUTTON, self.OnGetCapabilities, self.GetCapabilities)
        self.Bind(wx.EVT_BUTTON, self.OnGetMaps, self.GetMaps)
        self.Bind(wx.EVT_BUTTON, self.OnAddServer, self.addServer)
        # end wxGlade
        
        #Sudeep's Code Starts
        #self.urlInput.SetValue('http://www.gisnet.lv/cgi-bin/topo')
        self.usernameInput.Disable()
        self.passwordInput.Disable()
        if( not loadConfigFile(self)):
            print 'Config File Error, Unable to start application...'
            self.Close()
            return

        self.soup, open = initServerInfoBase('ServersList.xml')
        if(not open):
            self.Close()
            return
        self.__populate_Url_List(self.ServerList)
        self.selectedURL="No server selected"
        self.layerTreeRoot = self.LayerTree.AddRoot("Layers")
        Publisher().subscribe(self.onAddServerFrameClose, ("Add_Server_Frame_Closed"))
        Publisher().subscribe(self.onUpdateServerListmessage, ("update.serverList"))
        
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.AddServerisClosed = True
        
        #items = ["a", "b", "c"]
        #itemId = self.LayerTree.AppendItem(self.layerTreeRoot, "item")
        #self.LayerTree.AppendItem(itemId, "inside")
        #Sudeep's Code Ends 
    def __set_properties(self):
        # begin wxGlade: wmsFrame.__set_properties
        self.SetTitle("wmsFrame")
        self.LayerTree.SetMinSize((400, 250))
        self.usernameInput.SetMinSize((189, 27))
        self.passwordInput.SetMinSize((189, 27))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wmsFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.FlexGridSizer(2, 2, 1, 1)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(self.URL, 0, 0, 0)
        sizer_3.Add(self.ServerList, 0, 0, 0)
        sizer_2.Add(sizer_3, 0, 0, 0)
        sizer_2.Add(self.LayerTree, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.username, 0, 0, 0)
        grid_sizer_1.Add(self.usernameInput, 0, 0, 0)
        grid_sizer_1.Add(self.password, 0, 0, 0)
        grid_sizer_1.Add(self.passwordInput, 0, 0, 0)
        sizer_2.Add(grid_sizer_1, 0, wx.EXPAND, 0)
        sizer_4.Add(self.GetCapabilities, 0, 0, 0)
        sizer_4.Add(self.GetMaps, 0, 0, 0)
        sizer_4.Add(self.addServer, 0, 0, 0)
        sizer_2.Add(sizer_4, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_1.Add(sizer_2, 1, wx.ALL|wx.EXPAND|wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
    def __update_Url_List(self, ComboBox):
        ComboBox.Clear()
        for key, value in self.servers.items():
            ComboBox.Append(value.servername+self.name_url_delimiter+value.url)
            #ComboBox.Append(value.servername+" "+self.name_url_delimiter+" "+value.url)
        #print self.servers
        return
        
   


    def __populate_Url_List(self, ComboBox):
        self.servers = getAllRows(self.soup)
        for key, value in self.servers.items():
            ComboBox.Append(value.servername+self.name_url_delimiter+value.url)
            #ComboBox.Append(value.servername+" "+self.name_url_delimiter+" "+value.url)
        #print self.servers
        return
    
    
        '''f = open('serverList.txt','r')
        lines = f.readlines()
        self.servers = {}
        for line in lines:
            row = line.split()
            print row
            if(len(row) == 4) :
                self.servers[row[0]] = row[1]
            name = row[0]+" "+row[1][7:45]
            ComboBox.Append(name)
        f.close()'''

    def OnGetCapabilities(self, event): # wxGlade: wmsFrame.<event_handler>
        if(self.selectedURL == "No server selected"):
            print 'no url selected\n returning...\n'
            return
        
        self.usernameInput.Enable()
        self.passwordInput.Enable()
        #Sudeep's Code Starts
        #url = 'http://www.gisnet.lv/cgi-bin/topo?request=GetCapabilities&service=wms&version=1.1.1'
        self.LayerTree.CollapseAndReset(self.layerTreeRoot)
        #url = self.urlInput.GetValue() 
        url = self.selectedURL
        url = url + '?request=GetCapabilities&service=wms&version=1.1.1'
        print url
        req = Request(url)
        try:
            response = urlopen(req)
            xml = response.read()
            if(not isValidResponse(xml)):
                print 'Not a valid Get Capabilities reponse'
                return
            if(isServiceException(xml)):
                print 'Service Exception in Get Capabilities'
                return
            #for testing pruposes
            #f=open('in1.xml','r')
            #xml=f.read()
            #f.close()
            #self.statusbar.SetStatusText(xml) 
            reslist = parsexml(xml)
            populateLayerTree(xml,self.LayerTree, self.layerTreeRoot)
            #for res in reslist:
            #       self.LayerTree.AppendItem(self.layerTreeRoot, res)
            #self.Layers.SetValue(st) 
            #print xml
            self.LayerTree.Expand(self.layerTreeRoot)
        except HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        except URLError, e: 
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        except ValueError, e:
            print 'Value error'
            print 'Reason: ', e.reason
        except:
            print 'urlopen exception, unable to fetch data for getcapabilities'
        else:
            print 'Successful'
            #Sudeep's Code Ends
        event.Skip()
        
    
    def OnGetMaps(self, event): # wxGlade: wmsFrame.<event_handler>
        #Sudeep's Code Starts
        #self.layerName = self.layerSelected.GetValue()
        #url = self.urlInput.GetValue()
        print self.selectedURL
        if(self.selectedURL == "No server selected"):
            print 'no url selected\n returning...\n'
            return
            
        
        self.url_in = self.selectedURL
        getMap_request_url = self.url_in
        getMap_request_url += '?service=WMS&request=GetMap&version=1.1.1&format=image/png&width=800&height=600&srs=EPSG:3059&layers='
        getMap_request_url += self.layerName+'&bbox=584344,397868,585500,398500'
        
        print getMap_request_url
    
        req = Request(getMap_request_url)
        try:
            response = urlopen(req)
            image = response.read()
            #print image
            if(isServiceException(image)):
                print 'Service Exception has occured'
            else:
                outfile = open('map.png','wb')
                outfile.write(image)
                outfile.close()
                NewImageFrame()
            
            
        except HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        except URLError, e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        else:
            print 'Successful'
            #Sudeep's Code Ends
            event.Skip()

    
    def OnServerListEnter(self, event): # wxGlade: wmsFrame.<event_handler>
        return
        '''
        print "Event handler `OnServerListEnter' not implemented"
        #Sudeep's Code Starts
        print self.ServerList.CurrentSelection
        newUrl = self.ServerList.GetValue()
        self.ServerList.Append(newUrl)
        
        url = newUrl.split()
        if(len(url)==2):
            self.servers[url[0]] = url[1]
            f = open('serverList.txt','a')
            f.write(newUrl+"\n")
            f.close()
            self.selectedURL = url[1]
            print self.selectedURL
            print self.servers
  
        else:
            print "Format not recognized, Format: Severname URL"
        #Sudeep's Code Ends
        event.Skip()
        '''
    def printDict(self,dict):
        for key in dict.keys():
            print "the key name is" + key + "and its value is" 
        
    def OnServerList(self, event): # wxGlade: wmsFrame.<event_handler>
        print "Event handler `OnServerList' not implemented"
        #Sudeep's Code Starts
        print self.ServerList.CurrentSelection
        url = self.ServerList.GetValue()
        urlarr = url.split(self.name_url_delimiter)
        print "OnServerList:printing urlarr"
        print urlarr
        print urlarr[0]
        #print urlarr[0].encode()
        #self.printDict(self.servers)
        print "OnServerList: done"
        if(len(urlarr)==2):
            self.selectedURL = self.servers[urlarr[0]].url
            print self.selectedURL
        else:
            print "Wrong format of URL selected"
        #Sudeep's Code Ends
        event.Skip()

    def OnLayerTreeActivated(self, event): # wxGlade: wmsFrame.<event_handler>
        #Sudeep's Code Starts
        print "OnLayerTreeActivated: ", self.LayerTree.GetItemText(event.GetItem())
        #Sudeep's Code Ends
        print "Event handler `OnLayerTreeActivated' not implemented"
        event.Skip()

    def OnLayerTreeSelChanged(self, event): # wxGlade: wmsFrame.<event_handler>
        #self.layerName = self.LayerTree.GetItemText(event.GetItem())
        #print "Event handler `OnLayerTreeSelChanged' not implemented"
        self.selectedLayerList = []
        self.layerName = ""
        print "Selected layers:"
        for sellayer in self.LayerTree.GetSelections():
            layerName = self.LayerTree.GetItemText(sellayer)
            self.selectedLayerList += [layerName]
            self.layerName += ","+layerName
            
        self.layerName = self.layerName[1:]
        print self.layerName
        #print "Event handler `OnLayerTreeSelChanged' not implemented"
        event.Skip()

    def onAddServerFrameClose(self, msg):
        self.AddServerisClosed = True
        self.addServer.Enable()
        self.servers = msg.data
        self.__update_Url_List(self.ServerList)
        #frame = self.GetParent()
        #frame.Show()
    
    def onUpdateServerListmessage(self, msg):
        self.servers = msg.data
        self.__update_Url_List(self.ServerList)
        
    def OnAddServer(self, event): # wxGlade: wmsFrame.<event_handler>
        print 'before add server call'
        self.AddServerisClosed = False
        self.addServer.Disable()
        AddServerFrame(self)
        #print 'after add server call'
        #print "Event handler `OnAddServer' not implemented"
        #event.Skip()
        return 
    
    def OnQuit(self, event):
        msg = ""
        print 'in quit'
        if(not self.AddServerisClosed):
            Publisher().sendMessage(("WMS_Menu_Close"), msg)
        self.Destroy()
        return
# end of class wmsFrame

#Sudeep's Code Starts
def DisplayWMSMenu():
        app = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        wms_Frame = wmsFrame(None, -1, "")
        app.SetTopWindow(wms_Frame)
        wms_Frame.Show()
        app.MainLoop()
#Sudeep's Code Ends

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    wms_Frame = wmsFrame(None, -1, "")
    app.SetTopWindow(wms_Frame)
    wms_Frame.Show()
    app.MainLoop()
