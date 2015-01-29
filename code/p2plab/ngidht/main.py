'''
Created on 6 Jul 2011

@author: denis
'''

import os, sys, signal, time, math, socket, fcntl, struct
import binascii

from PyQt4 import QtGui
app = QtGui.QApplication(sys.argv)

import qt4reactor
qt4reactor.install()

from PyQt4 import uic
from PyQt4 import QtCore

import entangled.dtuple
import entangled.kademlia.contact
import entangled.kademlia.msgtypes

import hashlib

import twisted.internet.reactor

# some parameters
gui_updateInterval = 1000   # GUI update interval in milliseconds
gui_messageLifeTime = 3     # message life time in GUI update intervals 

# some colors
qcol_black = QtGui.QColor(0, 0, 0)
qcol_darkgreen = QtGui.QColor(0, 128, 0)
qcol_darkred = QtGui.QColor(128, 0, 0)
qcol_darkblue = QtGui.QColor(0, 0, 128)
qcol_gray = QtGui.QColor(128, 128, 128)

def overlayKey(s):
    h = hashlib.sha1()
    h.update(str(s))
    return h

def log(s, color = QtGui.QColor(0, 0, 0)):
    s = '[%s] %s' % (time.strftime("%H:%M:%S"), s)
    print s
    mainWindow.teLog.setTextColor(color)
    mainWindow.teLog.append(s)
    
def keyToHex(s):
    return binascii.b2a_hex(s)

def hexToKey(s):
    return long(s, 16)

# from http://code.activestate.com/
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

##########################################################################
# Observer
##########################################################################

class TreeNode():
    def __init__(self, name):
        self.name = name
        self.info = name
        self.left = None
        self.right = None
        self.bucket = None
        self.bucketIndex = -1
        self.gItem = None

class Message():
    def __init__(self, name, color, direction, remoteId):
        '''
        @param color: QtGui.QColor() object
        @param direction: 0: incoming, 1: outgoing
        '''
        self.name = name
        self.color = color
        self.direction = direction
        self.remoteId = remoteId
        self.lifeTime = gui_messageLifeTime

class Observer():
    def __init__(self, node):
        self.node = node
        
        # poison the node with our GUI hooks
        self.node._protocol.__gui = self
        
        self.node._protocol.__realSendRPC = self.node._protocol.sendRPC
        self.node._protocol.sendRPC = self.__guiSendRPC
    
        self.node._protocol.__realDatagramReceived = self.node._protocol.datagramReceived
        self.node._protocol.datagramReceived = self.__guiDatagramReceived
        
        self.node._routingTable.__realAddContact = self.node._routingTable.addContact
        self.node._routingTable.addContact = self.__guiAddContact
        self.addContactRecursion = 0
        
        self.messages = list()
    
    def log(self, s, color = QtGui.QColor(0, 0, 0)):
        log(s, color)
    
    def __guiSendRPC(self, contact, method, args, rawResponse=False):
        color = qcol_black
        if method == 'response':
            color = qcol_gray
        isContact = "contact"    
        try:
            self.node._routingTable.getContact(contact.id)
        except ValueError:
            isContact = "non contact"
        self.log('Send %s: %s (%s)' % (keyToHex(contact.id), method, isContact), color)
        self.messages.append(Message(method, color, 1, contact.id))
        return self.node._protocol.__realSendRPC(contact, method, args, rawResponse)
    
    def __guiDatagramReceived(self, datagram, address):
        msgPrimitive = self.node._protocol._encoder.decode(datagram)
        message = self.node._protocol._translator.fromPrimitive(msgPrimitive)
        color = qcol_black
        if isinstance(message, entangled.kademlia.msgtypes.ErrorMessage):
            msg = 'error'
            color = qcol_darkred
        elif isinstance(message, entangled.kademlia.msgtypes.ResponseMessage):
            msg = 'response'
        else:
            msg = message.request
            if msg == 'findNode':
                color = qcol_gray
            if msg == 'findValue':
                color = qcol_gray
        
        isContact = "contact"
        if message.nodeID == self.node.id:
            isContact = "self"
        else:    
            try:
                self.node._routingTable.getContact(message.nodeID)
            except ValueError:
                isContact = "non contact"
        self.log('Recv %s: %s (%s)' % (keyToHex(message.nodeID), msg, isContact), color)
        self.messages.append(Message(msg, color, 0, message.nodeID))
        return self.node._protocol.__realDatagramReceived(datagram, address)
    
    def __guiAddContact(self, contact):
        self.addContactRecursion += 1
        try:
            hasContact = False
            try:
                self.node._routingTable.getContact(contact.id)
                hasContact = True
            except ValueError:
                pass
            self.node._routingTable.__realAddContact(contact)
            if not hasContact and self.addContactRecursion == 1:
                try:
                    if self.node._routingTable.getContact(contact.id).id == contact.id:
                        self.log('Added contact %s (%s:%d)' % (keyToHex(contact.id), contact.address, contact.port), qcol_darkblue)
                except ValueError:
                    pass
        except:
            pass
        self.addContactRecursion -= 1
    
    def __buildTree(self, treeNode, bit, indexLow, indexHigh):
        currentKey = self.kbuckets[indexLow].rangeMin
        currentBit = currentKey & (1 << bit-1)
        
        if indexLow == indexHigh:
            #if currentBit:
            #    currentBit = 1
            #treeNode.name = "%d: %d" % (bit, currentBit)
            treeNode.bucket = self.kbuckets[indexLow]
            treeNode.bucketIndex = indexLow
            treeNode.name += " (%s)" % len(self.kbuckets[indexLow])
            treeNode.info = "Min: %040x\nMax: %040x\n" % (self.kbuckets[indexLow].rangeMin, self.kbuckets[indexLow].rangeMax-1)
            treeNode.info += "Entries: %d\n" % len(self.kbuckets[indexLow]._contacts)
            for contact in self.kbuckets[indexLow]._contacts:
                treeNode.info += "\n%s %s:%d" % (keyToHex(contact.id), contact.address, contact.port)
            return
        
        nextBit = currentBit
        index = indexLow
        while nextBit == currentBit and index < indexHigh:
            index += 1
            nextKey = self.kbuckets[index].rangeMin
            nextBit = nextKey & (1 << bit-1)
        
        if nextBit == currentBit and index == indexHigh:
            # descend one bit
            self.__buildTree(treeNode, bit-1, indexLow, indexHigh)
        else:
            # split
            treeNode.left  = TreeNode("%s0" % treeNode.name)
            treeNode.right = TreeNode("%s1" % treeNode.name)
            self.__buildTree(treeNode.left,  bit-1, indexLow, index - 1)
            self.__buildTree(treeNode.right, bit-1, index, indexHigh)
    
    def printTree(self, tree, gap = ""):
        if tree.left:
            print gap, tree.name, " L"
            self.printTree(tree.left, gap + '  ')
        if tree.right:
            print gap, tree.name, " R"
            self.printTree(tree.right, gap + '  ')
        if not (tree.left or tree.right):
            print gap, tree.name
    
    def updateInfo(self):
        self.datastore = self.node._dataStore
        self.kbuckets = self.node._routingTable._buckets
        self.tree = TreeNode("")
        self.__buildTree(self.tree, 160, 0, len(self.kbuckets)-1)
        #self.printTree(self.tree)
        
    def __findTreeNode(self, bucketIndex, treeNode):
        if treeNode.bucketIndex == bucketIndex:
            return treeNode
        tn = None
        if treeNode.left:
            tn = self.__findTreeNode(bucketIndex, treeNode.left)
        if tn == None and treeNode.right:
            tn = self.__findTreeNode(bucketIndex, treeNode.right)
        return tn
        
    def findTreeNode(self, bucketIndex):
        return self.__findTreeNode(bucketIndex, self.tree)

##########################################################################
# MainWindow
##########################################################################

class MainWindow(QtGui.QMainWindow):

    def __init__(self, *args):
        '''
        Constructor
        '''
        QtGui.QMainWindow.__init__(self, *args)
        # just pass self
        uic.loadUi("mainWindow.ui", self)
        self.teLog.clear()
        
        self.gsceneTree = QtGui.QGraphicsScene()
        self.gviewTree.setScene(self.gsceneTree)
        self.gsceneKeys = QtGui.QGraphicsScene()
        self.gviewKeys.setScene(self.gsceneKeys)
        
        self.node = None
        self.bgNodes = []
        self.observer = None
        self.selectedId = 0
        
        self.twBucket.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Key"))
        self.twBucket.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Locator"))
        
        self.twDatastore.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Key"))
        self.twDatastore.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Value"))
        self.twDatastore.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Last Published"))
        self.twDatastore.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem("Orig. Publisher ID"))
        self.twDatastore.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem("Orig. Publish Time"))
        
        self.updateTimer = QtCore.QTimer()
        QtCore.QObject.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.updateGViews)
        
    def destroyBgNetwork(self):
        if len(self.bgNodes):
            log('Destroying background network...')
            i = len(self.bgNodes)
            self.tabWidget.setCurrentIndex(0)
            self.pbBgNodes.setMaximum(i)
            self.pbBgNodes.setValue(i)
            for node in self.bgNodes:
                os.kill(node, signal.SIGTERM)
                time.sleep(0.15)
                i -= 1
                self.pbBgNodes.setValue(i)
        
    def closeEvent(self, event):
        self.destroyBgNetwork()
        print "GUI closed"
        self.deleteLater()
        twisted.internet.reactor.stop()
        print "Reactor stopped"
        if twisted.internet.reactor.threadpool is not None:
            twisted.internet.reactor.threadpool.stop()
            print "Thread-pool stopped"
        sys.exit()
        
    def on_btnJoin_released(self):
        knownNodes = []
        if self.leRemoteIP.text().length() > 0 and self.leRemotePort.text().length() > 0:
            knownNodes = [(str(self.leRemoteIP.text()), int(self.leRemotePort.text()))]
        
        log("Setting alpha = 1")
        entangled.kademlia.constants.alpha = 1
        
        log("Setting k = %d" % int(self.cbKParam.currentText()))
        entangled.kademlia.constants.k = int(self.cbKParam.currentText())
        
        # our node
        log("Known nodes: %s" % (knownNodes))
        self.node = entangled.dtuple.DistributedTupleSpacePeer( udpPort=int(self.leLocalPort.text()) )
        
        self.observer = Observer(self.node)
        
        self.leLocalIP.setEnabled(False)
        self.leLocalPort.setEnabled(False)
        self.leRemoteIP.setEnabled(False)
        self.leRemotePort.setEnabled(False)
        self.cbKParam.setEnabled(False)
        self.btnJoin.setEnabled(False)
        self.btnBgLaunch.setEnabled(True)
        
        self.node.joinNetwork(knownNodes)
        
        self.leNodeId.setText(keyToHex(self.node.id))
        self.updateTimer.start(gui_updateInterval)
        
    def on_btnBgLaunch_released(self):
        amount = 0
        startPort = 0
        try:
            amount = int(self.leBgNodes.text())
        except:
            log("Background nodes: \"%s\" not a number" % self.leBgNodes.text())
            return
        try:
            startPort = int(self.leBgStartingPort.text())
        except:
            log("Starting port: \"%s\" not a number" % self.leBgStartingPort.text())
            return
        if amount < 1:
            return
        
        self.btnBgLaunch.setEnabled(False)
        port = startPort
        ipAddr = get_ip_address('eth0')
        self.bgNodes = []
        self.pbBgNodes.setMaximum(amount)
        log('Creating Kademlia network...')
        for i in range(amount):
            time.sleep(0.15)
            self.bgNodes.append(os.spawnlp(os.P_NOWAIT, 'python', 'python', 'nginode.py', str(port), str(ipAddr), str(self.leLocalPort.text())))
            port += 1
            self.pbBgNodes.setValue(i)
        self.pbBgNodes.setValue(amount)
        
    def on_leKeyText_textChanged(self):
        try:
            s = overlayKey(self.leKeyText.text()).hexdigest()
            self.leKeyHash.setText(s)
        except UnicodeEncodeError:
            self.leKeyHash.setText("<invalid>")
        
    def on_btnClearValue_released(self):
        self.leValue.setText("")
        
    def on_btnPut_released(self):
        h = None
        try:
            h = overlayKey(self.leKeyText.text())
        except UnicodeEncodeError:
            log("Error: Keys currently limited to ASCII-only characters", qcol_darkred)
            return
        self.leKeyHash.setText(h.hexdigest())
        key = h.digest()
        value = str(self.leValue.text())

        def completed(result):
            log("Storage finished", qcol_darkgreen)
        
        log("Storage of key %s" % h.hexdigest(), qcol_darkgreen)
        df = self.node.iterativeStore(key, value)
        df.addCallback(completed)
    
    def on_btnGet_released(self):
        h = None
        try:
            h = overlayKey(self.leKeyText.text())
        except UnicodeEncodeError:
            log("Error: Keys currently limited to ASCII-only characters", qcol_darkred)
            return
        self.leKeyHash.setText(h.hexdigest())
        
        key = h.digest()
        
        def showValue(result):
            if type(result) == dict:
                value = result[key]
                if type(value) != str:
                    value = '%s: %s' % (type(value), str(value))
                log('Lookup returned %s' % (value), qcol_darkgreen)
            else:
                value = '(not found)'
                log('Lookup for key %s failed' % (h.hexdigest()), qcol_darkred)
            self.leValue.setText(value)
            
        def error(failure):
            log("A lookup error occurred: %s" % (failure.getErrorMessage()), qcol_darkred)
        
        log('Lookup for key %s (%s)' % (h.hexdigest(), self.leKeyText.text()), qcol_darkgreen)
        df = self.node.iterativeFindValue(key)
        df.addCallback(showValue)
        df.addErrback(error)
        
    def on_btnDelete_released(self):
        h = None
        try:
            h = overlayKey(self.leKeyText.text())
        except UnicodeEncodeError:
            log("Error: Keys currently limited to ASCII-only characters", qcol_darkred)
            return
        self.leKeyHash.setText(h.hexdigest())
        
        key = h.digest()
        
        def completed(result):
            log("Deletion finished", qcol_darkred)
            
        def error(failure):
            log("A deletion error occurred: %s" % (failure.getErrorMessage()), qcol_darkred)
        
        df = self.node.iterativeDelete(key)
        df.addCallback(completed)
        df.addErrback(error)
        
    def on_btnRefreshBuckets_released(self):
        self.updateInfo(self.observer)
        
    def on_teLog_selectionChanged(self):
        selectedText = str(self.teLog.textCursor().selectedText())
        try:
            self.selectedId = long(selectedText, 16)
        except:
            self.selectedId = 0
        
    def on_cbBucket_currentIndexChanged(self, index):
        index = self.cbBucket.currentIndex()
        if index < 0:
            #self.twBucket.setRowCount(0)
            return
        bucket = self.observer.kbuckets[index] # todo: use dynamic observer
        self.lbBucketKeyRange.setText("%040x-%040x" % (bucket.rangeMin, bucket.rangeMax-1))
        self.twBucket.setRowCount(len(bucket))
        i = 0
        for contact in bucket._contacts:
            self.twBucket.setItem(i, 0, QtGui.QTableWidgetItem(keyToHex(contact.id)))
            self.twBucket.setItem(i, 1, QtGui.QTableWidgetItem("%s:%d" % (contact.address, contact.port)))
            i += 1
        tn = self.observer.findTreeNode(index)
        if tn and tn.gItem:
            tn.gItem.setDefaultTextColor(qcol_darkred)

    def updateGViews(self):
        # timer update
        self.updateInfo(self.observer)
        self.updateTreeGraphics(self.observer)
        self.updateKeysGraphics(self.observer)

    def updateInfo(self, observer):
        observer.updateInfo()
        curI = self.cbBucket.currentIndex()
        self.cbBucket.clear()
        
        i = 0
        for bucket in observer.kbuckets:
            self.cbBucket.addItem("%d: %040x" % (i, bucket.rangeMin), bucket)
            i += 1
            
        if curI >= i or curI < 0:
            curI = 0
        self.cbBucket.setCurrentIndex(curI)
        self.on_cbBucket_currentIndexChanged(curI)
        
        self.updateDatastore(self.observer)
        
    def updateTreeGraphics(self, observer):
        self.gsceneTree.clear()
        
        def drawTree(self, tree, x, y, level = 0):
            ti = self.gsceneTree.addText(tree.name)
            ti.setPos(x - ti.boundingRect().width()/2, y - ti.boundingRect().height()/2)
            ti.setToolTip(tree.info)
            tree.gItem = ti
            level += 1
            if tree.left:
                self.gsceneTree.addLine(x, y+10, x-150/level, y+20)
                drawTree(self, tree.left, x-150/level, y+30, level)
            if tree.right:
                self.gsceneTree.addLine(x, y+10, x+150/level, y+20)
                drawTree(self, tree.right, x+150/level, y+30, level)
            
        drawTree(self, observer.tree, 200, 5)
        
        if self.cbBucket.currentIndex() >= 0:
            tn = self.observer.findTreeNode(self.cbBucket.currentIndex())
            if tn and tn.gItem:
                tn.gItem.setDefaultTextColor(QtGui.QColor(200, 0, 0))
                
    def updateKeysGraphics(self, observer):
        self.gsceneKeys.clear()
        d = min(self.gviewKeys.width(), self.gviewKeys.height())-60
        cx = 30 + d/2
        cy = cx
        
        def addMark(self, text, val, qcolor = QtGui.QColor(0, 128, 0), drawText = False, r = 6):
            rad = (float(val) / float(2**160)) * 2 * math.pi
            x = cx + d/2*math.sin(rad)
            y = cy - d/2*math.cos(rad)
            gi = self.gsceneKeys.addEllipse(x-r, y-r, 2*r, 2*r, QtGui.QPen(), QtGui.QBrush(qcolor))
            if drawText:
                ti = self.gsceneKeys.addText(text)
                x = x + (ti.boundingRect().width()/2-r)  * (-1 + math.sin(rad))
                y = y + (ti.boundingRect().height()/2-r) * (-1 + math.cos(rad)) - math.cos(rad)*ti.boundingRect().height()
                ti.setPos(x, y)
            else:
                gi.setToolTip(text)
            return gi
        
        # mark
        addMark(self, "0", 0, QtGui.QColor(0, 0, 0), True, 1)
        addMark(self, "2^159", 2**159, QtGui.QColor(0, 0, 0), True, 1)
        
        # current k-bucket
        i = self.cbBucket.currentIndex()
        if i >= 0:
            bucket = observer.kbuckets[i]
            path = QtGui.QPainterPath()
            arcLen = (float(bucket.rangeMax-bucket.rangeMin) / float(2**160))*360
            startAngle = 360 - (float(bucket.rangeMax) / float(2**160))*360 + 90
            path.moveTo(cx, cy)
            path.arcTo(30, 30, d, d, startAngle, arcLen)
            path.moveTo(cx, cy)
            self.gsceneKeys.addPath(path, QtGui.QPen(QtGui.QColor(220, 220, 220)), QtGui.QBrush(QtGui.QColor(220, 220, 220)))
        
        # circle
        self.giKeyCircle = self.gsceneKeys.addEllipse(30, 30, d, d)
        
        # our node
        self.giLocalNode = self.gsceneKeys.addEllipse(cx-6, cy-6, 12, 12, QtGui.QPen(), QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        self.giLocalNode.setToolTip("Local node ID:\n%s" % keyToHex(self.node.id))
        addMark(self, "Local node ID:\n%s" % keyToHex(self.node.id), long(keyToHex(self.node.id), 16), QtGui.QColor(255, 255, 255), False, 4)
        
        # contacts
        contactGItems = {}
        for bucket in observer.kbuckets:
            for contact in bucket._contacts:
                s = keyToHex(contact.id)
                contactGItems[contact.id] = addMark(self, "%s\n%s:%d" % (s, contact.address, contact.port), long(s, 16))
                
        # current key
        s = str(self.leKeyHash.text())
        if len(s) == 40:
            addMark(self, "Current key:\n%s" % s, hexToKey(s), QtGui.QColor(255, 255, 0), False, 4)
            
        # current selected text
        if self.selectedId > 0:
            addMark(self, "Current log selection:\n%040x" % self.selectedId, self.selectedId, QtGui.QColor(255, 0, 0), False, 4)
            
        # messages
        for message in observer.messages:
            if message.remoteId != self.node.id and message.color != qcol_gray:
                keyAsLong = long(keyToHex(message.remoteId), 16)
                giNode = None
                if contactGItems.has_key(message.remoteId): # a contact
                    giNode = contactGItems[message.remoteId]
                else: # remote node not a contact, add temporarily
                    giNode = addMark(self, keyToHex(message.remoteId), keyAsLong, QtGui.QColor(128, 255, 128))
                gi = self.gsceneKeys.addLine(QtCore.QLineF(QtCore.QPointF(cx, cy), giNode.boundingRect().center()), QtGui.QPen(message.color))
                ti = self.gsceneKeys.addText(message.name)
                if message.direction == 1: # outgoing
                    ti.setPos(self.giLocalNode.boundingRect().center())
                else: # incoming
                    x = giNode.boundingRect().center().x()
                    y = giNode.boundingRect().center().y()
                    if keyAsLong < 2**159:
                        ti.setPos(x + 8, y - ti.boundingRect().height()/2)
                    else:
                        ti.setPos(x - ti.boundingRect().width() - 8, y - ti.boundingRect().height()/2)
            message.lifeTime -= 1
            
        # clean up messages
        while len(observer.messages) > 0 and observer.messages[0].lifeTime == 0:
            observer.messages.pop(0)
        
    def updateDatastore(self, observer):
        keys = observer.datastore.keys()
        self.twDatastore.setRowCount(len(keys))
        i = 0
        for key in keys:
            self.twDatastore.setItem(i, 0, QtGui.QTableWidgetItem(keyToHex(key)))
            self.twDatastore.setItem(i, 1, QtGui.QTableWidgetItem(str(observer.datastore.__getitem__(key))))
            self.twDatastore.setItem(i, 2, QtGui.QTableWidgetItem(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(observer.datastore.lastPublished(key)))))
            self.twDatastore.setItem(i, 3, QtGui.QTableWidgetItem(keyToHex(observer.datastore.originalPublisherID(key))))
            self.twDatastore.setItem(i, 4, QtGui.QTableWidgetItem(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(observer.datastore.originalPublishTime(key)))))
            i += 1
            
##########################################################################
# main
##########################################################################
if __name__ == '__main__':
    print "NGI-Lab: Kademlia-based DHT"
    
    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print 'Usage:\n\t%s UDP_PORT [KNOWN_NODE_IP KNOWN_NODE_PORT]' % sys.argv[0]
        #print 'or:\n\t%s UDP_PORT [FILE_WITH_KNOWN_NODES]' % sys.argv[0]
        #print '\nIf a file is specified, it should containg one IP address and UDP port\nper line, seperated by a space.'
        sys.exit(0)
        
    if len(sys.argv) > 1:
        try:
            int(sys.argv[1])
        except ValueError:
            print '\nUDP_PORT must be an integer value.\n'
            print 'Usage:\n\t%s UDP_PORT [KNOWN_NODE_IP KNOWN_NODE_PORT]' % sys.argv[0]
            #print 'or:\n\t%s UDP_PORT  [FILE_WITH_KNOWN_NODES]' % sys.argv[0]
            #print '\nIf a file is specified, it should contain one IP address and UDP port\nper line, seperated by a space.'
            sys.exit(1)
    
    if len(sys.argv) == 4:
        knownNodes = [(sys.argv[2], int(sys.argv[3]))]
    #elif len(sys.argv) == 3:
    #    knownNodes = []
    #    f = open(sys.argv[2], 'r')
    #    lines = f.readlines()
    #    f.close()
    #    for line in lines:
    #        ipAddress, udpPort = line.split()
    #        knownNodes.append((ipAddress, int(udpPort)))
    else:
        knownNodes = None
    
    mainWindow = MainWindow()
    
    if len(sys.argv) > 1:
        mainWindow.leLocalPort.setText(sys.argv[1])
    
    if knownNodes and len(knownNodes) > 0:
        mainWindow.leRemoteIP.setText(knownNodes[0][0])
        mainWindow.leRemotePort.setText(str(knownNodes[0][1]))
    
    mainWindow.show()

    twisted.internet.reactor.run()
    
