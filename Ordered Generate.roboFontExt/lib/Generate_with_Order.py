import os.path
from vanilla import Button, HorizontalLine, FloatingWindow, CheckBox, TextBox, PopUpButton, Drawer, TextEditor
from vanilla.dialogs import getFile, putFile
from mojo.roboFont import OpenWindow, CurrentFont


class GenerateWithOrder(object):
    """A simple extension to generate font with order from a FL Encoding file """
    def __init__(self):
        self.glyphOrder = []
        self.orderFileName = ''
        self.formats = ['otf', 'ttf', 'pfa']
        self.format = 'otf'
        self.decompose = True
        self.overlap = True
        self.autohint = True
        self.release = True
        
        self.w = FloatingWindow((200,270), "Generate", minSize=(200,270),)
        self.w.getEncoding = Button((10, 10, 180, 20), 'Get .enc file', callback=self.getEncodingCallback)
        self.w.viewEncoding = Button((10, 75, 180, 20), 'View encoding', callback=self.viewEncodingCallback)
        self.w.line = HorizontalLine((12, 103, -12, 1))
        
        self.w.formatLabel    = TextBox((15, 117, 60, 20), "Format")
        self.w.formatChoice   = PopUpButton((70, 115, 80, 20), self.formats, callback=self.formatCallback)
        self.w.decomposeCheck = CheckBox((20, 141, -10, 20), "Decompose", callback=self.decomposeCallback, value=self.decompose)
        self.w.overlapCheck   = CheckBox((20, 161, -10, 20), "Remove Overlap", callback=self.overlapCallback, value=self.overlap)
        self.w.autohintCheck  = CheckBox((20, 181, -10, 20), "Autohint", callback=self.autohintCallback, value=self.autohint)
        self.w.releaseCheck   = CheckBox((20, 201, -10, 20), "Release Mode", callback=self.releaseCallback, value=self.release)
        self.w.generate = Button((10, 232, 180, 20), 'Generate Font', callback=self.generateCallback)
    
        self.w.decomposeCheck.enable(False)
        
        self.w.viewEncoding.enable(False)
        self.w.formatChoice.enable(False)
        self.w.overlapCheck.enable(False)
        self.w.autohintCheck.enable(False)
        self.w.releaseCheck.enable(False)
        self.w.generate.enable(False)
        
        self.d = Drawer((170, 400), self.w, preferredEdge="right")
        self.d.text = TextEditor((10, 10, -10, -10), readOnly=True)
        
        self.d.open()
        self.d.toggle()
        self.w.open()

    def process_enc(self, p):
        order = []
        
        f = open(p)
        for line in f:
            if line.startswith(('#', '%')):
                pass
            else:
                l = line.split()
                if len(l[0]) != 0:
                    for i in l:
                        if not i.startswith(('#', '%', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')) and len(i) != 0:
                            order.append(i)
        f.close()
        
        self.glyphOrder = order

                
    def getEncodingCallback(self, sender):
        getFile(parentWindow=self.w, fileTypes=['enc', 'Enc'], resultCallback=self.processEncodingCallback)

    def viewEncodingCallback(self, sender):
        if not self.d.isOpen():
            t = "\n".join(self.glyphOrder)
            self.d.text.set(t)
        self.d.toggle()

    def processEncodingCallback(self, sender):
        if sender[0] is not None:
            fn = os.path.split(sender[0])[1]
            self.process_enc(sender[0])
            self.w.encodingTitle = TextBox((15, 34, 180, 17), "Encoding File:", alignment="left")
            self.w.encodingFileTitle = TextBox((15, 52, 180, 17), fn, alignment="left")
            
            self.w.viewEncoding.enable(True)
            self.w.formatChoice.enable(True)
            self.w.overlapCheck.enable(True)
            self.w.autohintCheck.enable(True)
            self.w.releaseCheck.enable(True)
            self.w.generate.enable(True)
            
    def formatCallback(self, sender):
        self.format = self.formats[sender.get()]
        if self.format == 'otf' or self.format == 'pfa':
            self.decompose = True
            self.w.decomposeCheck.enable(False)
            self.w.decomposeCheck.set(True)
        else:
            self.w.decomposeCheck.enable(True)

    def decomposeCallback(self, sender):
        if sender.get() == 0:
            self.decompose = False
        else:
            self.decompose = True

    def overlapCallback(self, sender):
        if sender.get() == 0:
            self.overlap = False
        else:
            self.overlap = True

    def autohintCallback(self, sender):
        if sender.get() == 0:
            self.autohint = False
        else:
            self.autohint = True

    def releaseCallback(self, sender):
        if sender.get() == 0:
            self.release = False
        else:
            self.release = True
            
    def generateCallback(self, sender):
        font = CurrentFont()
        d,f = os.path.split(font.path)
        f = f[:-3] + self.format
        putFile(messageText="Save Font", directory=d, fileName=f, parentWindow=self.w, resultCallback=self.processGenerateCallback)
        
    def processGenerateCallback(self, sender):
        path = sender
        font = CurrentFont()
        font.generate(path, self.format, decompose=self.decompose, autohint=self.autohint, releaseMode=self.release, glyphOrder=self.glyphOrder)

OpenWindow(GenerateWithOrder)