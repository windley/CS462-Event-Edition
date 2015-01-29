#! /usr/bin/env python
#
# This library is free software, distributed under the terms of
# the GNU Lesser General Public License Version 3, or any later version.
# See the COPYING file included in this archive
#

import pygtk
pygtk.require('2.0')
import os, sys, gtk, gobject

from twisted.internet import gtk2reactor
gtk2reactor.install()
import twisted.internet.reactor

from twisted.internet import defer
from twisted.internet.protocol import Protocol, ServerFactory, ClientCreator

import hashlib

import entangled.node
from entangled.kademlia.datastore import SQLiteDataStore


class FileServer(Protocol):
    def dataReceived(self, data):
        request = data.strip()
        for entry in os.walk(self.factory.sharePath):
            for filename in entry[2]:
                if filename == request:
                    fullPath = '%s/%s' % (entry[0], filename)
                    f = open(fullPath, 'r')
                    buf = f.read()
                    self.transport.write(buf)
                    f.close()
                    break
        self.transport.loseConnection()

class FileGetter(Protocol):
    def connectionMade(self):
        self.buffer = ''
        self.filename = ''
        
    def requestFile(self, filename, guiWindow):
        self.window = guiWindow
        self.filename = filename
        self.transport.write('%s\r\n' % filename)

    def dataReceived(self, data):
        self.buffer += data
    
    def connectionLost(self, reason):
        if len(self.buffer) == 0:
             dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                        gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                        "An error occurred; file could not be retrieved.")
             dialog.run()
             dialog.destroy()
             return
     
        fd = gtk.FileChooserDialog(title=None, action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                   buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
        fd.set_default_response(gtk.RESPONSE_OK)
        fd.set_current_name(self.filename)
        response = fd.run()
        if response == gtk.RESPONSE_OK:
            destfilename = fd.get_filename()
            f = open(destfilename, 'w')
            f.write(self.buffer)
            f.close()
        fd.destroy()


class FileShareWindow(gtk.Window):
    def __init__(self, node):
        gtk.Window.__init__(self)
        
        self.set_default_size(640, 480)
        
        self.trayIcon = gtk.status_icon_new_from_stock(gtk.STOCK_FIND)
        self.trayIcon.connect('popup-menu', self._trayIconRightClick)
        self.trayIcon.connect('activate', self._trayIconClick)
        
        self.node = node
        
        self.connect("delete-event", self._hideWindow)
        
        # Layout the window
        highLevelVbox = gtk.VBox(spacing=3)
        self.add(highLevelVbox)
        highLevelVbox.show()
        
        notebook = gtk.Notebook()
        notebook.set_tab_pos(pos=gtk.POS_TOP)
        notebook.show()
        highLevelVbox.pack_start(notebook,expand=True, fill=True)
        
        vbox = gtk.VBox(spacing=3)
        vbox.show()
        
        notebook.append_page(vbox, gtk.Label('Search P2P Network'))

        
        
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)
        # Create tree model
        model = self.createListStore([])
        # Create tree view
        self.dhtTreeView = gtk.TreeView(model)
        self.dhtTreeView.set_rules_hint(True)
        self.dhtTreeView.set_search_column(0)
        self.dhtTreeView.connect('row-activated', self.downloadFile)
        # Add the tree view to the scrolling window
        sw.add(self.dhtTreeView)
        # column for file name/description
        column = gtk.TreeViewColumn('File list:', gtk.CellRendererText(), text=0)
        column.set_sort_column_id(0)
        self.dhtTreeView.append_column(column)

        # Add the controls
        # Search for keyword
        hbox = gtk.HBox(False, 8)
        hbox.show()
        label = gtk.Label("Search:")
        hbox.pack_start(label, False, False, 0)
        label.show()
        entryKeyword = gtk.Entry()
        hbox.pack_start(entryKeyword, expand=True, fill=True)
        entryKeyword.show()
        
        button = gtk.Button('Search')
        hbox.pack_start(button, expand=False, fill=False)
        button.connect("clicked", self.search, entryKeyword)
        button.show()
        
        self.progressBar = gtk.ProgressBar()
        self.progressBar.show()
        hbox.pack_start(self.progressBar, expand=True, fill=True)
        self.progressBar.show()
        
        vbox.pack_start(hbox, expand=False, fill=False)
        
        
        ######### Publish data
        vbox = gtk.VBox(spacing=3)
        vbox.show()
        notebook.append_page(vbox, gtk.Label('Share Local Files'))
        
        
        # List view
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)
        model = self.createListStore([])
        self.localTreeView = gtk.TreeView(model)
        self.localTreeView.set_rules_hint(True)
        self.localTreeView.set_search_column(0)
        self.localTreeView.connect('row-activated', self.downloadFile)
        sw.add(self.localTreeView)
        column = gtk.TreeViewColumn('Shared Files:', gtk.CellRendererText(), text=0)
        column.set_sort_column_id(0)
        self.localTreeView.append_column(column)
        
        
        hbox = gtk.HBox(False, 8)
        hbox.show()
        label = gtk.Label("Share directory:")
        hbox.pack_start(label, False, False, 0)
        label.show()
        self.entryDir = gtk.Entry()
        hbox.pack_start(self.entryDir, expand=True, fill=True)
        self.entryDir.show()
        button = gtk.Button('Browse')
        hbox.pack_start(button, expand=False, fill=False)
        button.connect("clicked", self.browseDirectory, self.entryDir.get_text)
        button.show()
        button = gtk.Button('Publish')
        hbox.pack_start(button, expand=False, fill=False)
        button.connect("clicked", self.publishDirectory, self.entryDir.get_text)
        button.show()
        vbox.pack_start(hbox, expand=False, fill=False)

        self._setupTCPNetworking()

        self.show_all()

    def _showTrayIconMenu(self, event_button, event_time, icon):
        menu = gtk.Menu()
        if not self.get_property('visible'):
            showItem = gtk.MenuItem('Show main window')
            showItem.connect('activate', self._trayIconClick)
            showItem.show()
            menu.append(showItem)
        item = gtk.MenuItem('Quit')
        item.connect('activate', gtk.main_quit)
        item.show()
        menu.append(item)
        menu.popup(None, None, gtk.status_icon_position_menu, event_button,event_time, icon)

    def _trayIconRightClick(self, icon, event_button, event_time):
        self._showTrayIconMenu(event_button, event_time, icon)

    def _trayIconClick(self, icon):
        if self.get_property('visible'):
            self.hide_all()
        else:
            self.show_all()
            

    def _hideWindow(self, *args):
        self.hide_all()
        return True

    def _setupTCPNetworking(self):
        # Next lines are magic:
        self.factory = ServerFactory()
        self.factory.protocol = FileServer
        self.factory.sharePath = '.'
        twisted.internet.reactor.listenTCP(int(sys.argv[1]), self.factory)


    def createListStore(self, data):
        lstore = gtk.ListStore(gobject.TYPE_STRING)
        for item in data:
            iter = lstore.append()
            lstore.set(iter, 0, item)
        return lstore
    
    def search(self, sender, entryKeyword):
        sender.set_sensitive(False)
        keyword = entryKeyword.get_text()
        entryKeyword.set_sensitive(False)
        def gotValue(result):
            sender.set_sensitive(True)
            entryKeyword.set_sensitive(True)
            model = self.createListStore(result)
            self.dhtTreeView.set_model(model)
        def error(failure):
            print 'GUI: an error occurred:', failure.getErrorMessage()
            sender.set_sensitive(True)
            entryKeyword.set_sensitive(True)
        df = self.node.searchForKeywords(keyword)
        df.addCallback(gotValue)
        df.addErrback(error)
    
    def publishDirectory(self, sender, dirPathFunc):
        sender.set_sensitive(False)
        path = dirPathFunc()
        files = []
        paths = []
        outerDf = defer.Deferred()
        self.factory.sharePath = path
        for entry in os.walk(path):
            for file in entry[2]:
                if file not in files and file not in ('.directory'):
                    files.append(file)
                    paths.append(entry[0])
        files.sort()
        model = self.localTreeView.get_model()
        
        print 'files: ', len(files)
        def publishNextFile(result=None):
            if len(files) > 0:
                #twisted.internet.reactor.iterate()
                filename = files.pop()
                iter = model.append()
                print '-->',filename
                model.set(iter, 0, '%s/%s' % (paths.pop(), filename))
                df = self.node.publishData(filename, self.node.id)
                df.addCallback(publishNextFile)
            else:
                print '** done **'
                outerDf.callback(None)
        def completed(result):
            sender.set_sensitive(True)
        publishNextFile()
        outerDf.addCallback(completed)
    
    def browseDirectory(self, sender, dirPathFunc):
        fd = gtk.FileChooserDialog(title='Choose directory to share...', action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OK,gtk.RESPONSE_OK))
        fd.set_default_response(gtk.RESPONSE_OK)
        path = dirPathFunc().strip()
        if len(path):
            fd.set_current_folder(path)
        response = fd.run()
        if response == gtk.RESPONSE_OK:
            self.entryDir.set_text(fd.get_filename())
        fd.destroy()
        
    def downloadFile(self, treeView, path, column):
        model = treeView.get_model()
        iter = model.get_iter(path)
        filename = model.get(iter, 0)[0]
        h = hashlib.sha1()
        h.update(filename)
        key = h.digest()
        
        def getTargetNode(result):
            targetNodeID = result[key]
            df = self.node.findContact(targetNodeID)
            return df
        def getFile(protocol):
            if protocol != None:
                protocol.requestFile(filename, self)
        def connectToPeer(contact):
            if contact == None:
                dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                        gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                        "File could not be retrieved.\nThe host that published this file is no longer on-line.")
                dialog.run()
                dialog.destroy()
            else:
                c = ClientCreator(twisted.internet.reactor, FileGetter)
                df = c.connectTCP(contact.address, contact.port)
                return df
        
        df = self.node.iterativeFindValue(key)
        df.addCallback(getTargetNode)
        df.addCallback(connectToPeer)
        df.addCallback(getFile)
        
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage:\n%s UDP_PORT  [KNOWN_NODE_IP  KNOWN_NODE_PORT]' % sys.argv[0]
        print 'or:\n%s UDP_PORT  [FILE_WITH_KNOWN_NODES]' % sys.argv[0]
        print '\nIf a file is specified, it should containg one IP address and UDP port\nper line, seperated by a space.'
        sys.exit(1)
    try:
        int(sys.argv[1])
    except ValueError:
        print '\nUDP_PORT must be an integer value.\n'
        print 'Usage:\n%s UDP_PORT  [KNOWN_NODE_IP  KNOWN_NODE_PORT]' % sys.argv[0]
        print 'or:\n%s UDP_PORT  [FILE_WITH_KNOWN_NODES]' % sys.argv[0]
        print '\nIf a file is specified, it should contain one IP address and UDP port\nper line, seperated by a space.'
        sys.exit(1)
    
    if len(sys.argv) == 4:
        knownNodes = [(sys.argv[2], int(sys.argv[3]))]
    elif len(sys.argv) == 3:
        knownNodes = []
        f = open(sys.argv[2], 'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            ipAddress, udpPort = line.split()
            knownNodes.append((ipAddress, int(udpPort)))
    else:
        knownNodes = None

    try:
        os.makedirs(os.path.expanduser('~')+'/.entangled')
    except OSError:
        pass
    dataStore = None#SQLiteDataStore(os.path.expanduser('~')+'/.entangled/fileshare.sqlite')
    node = entangled.node.EntangledNode(udpPort=int(sys.argv[1]), dataStore=dataStore)
    node.invalidKeywords.extend(('mp3', 'png', 'jpg', 'txt', 'ogg'))
    node.keywordSplitters.extend(('-', '!'))
    window = FileShareWindow(node)
    
    window.set_title('Entangled File Sharing Demo')
    window.present()
    
    node.joinNetwork(knownNodes)
    twisted.internet.reactor.run()
