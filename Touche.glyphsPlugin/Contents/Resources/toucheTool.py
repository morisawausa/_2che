# coding=utf-8
from __future__ import division, print_function, unicode_literals
from Touche import Touche
from Foundation import NSUserDefaults
from vanilla import CheckBox, Group, List, ProgressSpinner, Button, TextBox, FloatingWindow
#from robofab.world import CurrentFont
from GlyphsApp import *
import time, objc

from builtins import chr

class ToucheTool():

    def __init__(self):
        NSUserDefaults.standardUserDefaults().registerDefaults_({"ToucheWindowHeight":340})
        self.windowHeight = NSUserDefaults.standardUserDefaults().integerForKey_("ToucheWindowHeight")
        self.minWindowHeight = 340
        if self.windowHeight < self.minWindowHeight:
            self.windowHeight = self.minWindowHeight
        self.closedWindowHeight = 100
        self.w = FloatingWindow((180, self.windowHeight), 'Touché!', minSize=(180,340), maxSize=(250,898))
        self.w.bind("resize", self.windowResized_)
        self.isResizing = False
        p = 10
        w = 160

        # options
        self.w.options = Group((0, 0, 180, 220))

        buttons = {
            "checkSelBtn": {"text": "Check selected glyphs", "callback": self.checkSel_, "y": p},
        }
        for button, data in buttons.items():
            setattr(self.w.options, button,
            Button((p, data["y"], w - 22, 22), data["text"], callback=data["callback"], sizeStyle="small"))

        self.w.options.zeroCheck = CheckBox((p, 35, w, 20), "Ignore zero-width glyphs", value=True, sizeStyle="small")
        self.w.options.progress = ProgressSpinner((w - 8, 13, 16, 16), sizeStyle="small")

        # Modification(Nic): prev / next buttons
        self.w.options.prevButton = Button((w + 22, 35, 10, 10), "Prev Button", callback=self.prevPair_)
        self.w.options.prevButton.bind("uparrow", [])

        self.w.options.nextButton = Button((w + 22, 35, 10, 10), "Next Button", callback=self.nextPair_)
        self.w.options.nextButton.bind("downarrow", [])

        # /Modification(Nic)

        # Modification(Nic): prev / next buttons

        self.w.options.decrementKerningHigh = Button((w + 22, 35, 10, 10), "Decrement Kerning High", callback=self.decrementKerningByHigh_)
        self.w.options.decrementKerningHigh.bind("leftarrow", ["command"])

        self.w.options.decrementKerningLow = Button((w + 22, 35, 10, 10), "Decrement Kerning Low", callback=self.decrementKerningByLow_)
        self.w.options.decrementKerningLow.bind("leftarrow", [])

        self.w.options.incrementKerningHigh = Button((w + 22, 35, 10, 10), "Increment Kerning High", callback=self.incrementKerningByHigh_)
        self.w.options.incrementKerningHigh.bind("rightarrow", ["command"])

        self.w.options.incrementKerningLow = Button((w + 22, 35, 10, 10), "Increment Kerning Low", callback=self.incrementKerningByLow_)
        self.w.options.incrementKerningLow.bind("rightarrow", [])

        # /Modification(Nic)

        # results
        self.w.results = Group((0, 220, 180, -0))
        self.w.results.show(False)

        textBoxes = {"stats": -34, "result": -18}
        for box, y in textBoxes.items():
            setattr(self.w.results, box, TextBox((p, y, w, 14), "", sizeStyle="small"))

        # list and preview
        self.w.outputList = List((0,58,-0,-40),
            [{"left glyph": "", "right glyph": ""}], columnDescriptions=[{"title": "left glyph", "width": 90}, {"title": "right glyph"}],
            showColumnTitles=False, allowsMultipleSelection=False, enableDelete=False, selectionCallback=self.showPair_)
        self.w.outputList._setColumnAutoresizing()
        self._resizeWindow(False)
        self.w.open()


    # callbacks

    # Modification(Nic): Incrementing and Decrementing the Pair Index in the list.

    def prevPair_(self, sender=None):
        currentIndices = self.w.outputList.getSelection()
        prevIndices = map(lambda i: max(i - 1, 0), currentIndices)
        if (len(self.w.outputList) > 0):
            self.w.outputList.setSelection(prevIndices)

    def nextPair_(self, sender=None):
        currentIndices = self.w.outputList.getSelection()
        nextIndices = map(lambda i: min(i + 1, len(self.w.outputList) - 1), currentIndices)
        if (len(self.w.outputList) > 0):
            self.w.outputList.setSelection(nextIndices)

    # /Modification(Nic)

    # Modification(Nic): Incrementing and Decrementing the Pair Index in the list.

    def decrementKerningByLow_(self, sender=None):
        print('dec by low')
        currentIndices = self.w.outputList.getSelection()
        currentPair = self.w.outputList[currentIndices[0]]
        increment = Glyphs.intDefaults['GSKerningIncrementLow']
        self.bumpKerningForPair(currentPair['left glyph'], currentPair['right glyph'], -increment)

    def decrementKerningByHigh_(self, sender=None):
        print('dec by high')
        currentIndices = self.w.outputList.getSelection()
        currentPair = self.w.outputList[currentIndices[0]]
        increment = Glyphs.intDefaults['GSKerningIncrementHigh']
        self.bumpKerningForPair(currentPair['left glyph'], currentPair['right glyph'], -increment)

    def incrementKerningByLow_(self, sender=None):
        print('inc by low')
        currentIndices = self.w.outputList.getSelection()
        currentPair = self.w.outputList[currentIndices[0]]
        increment = Glyphs.intDefaults['GSKerningIncrementLow']
        self.bumpKerningForPair(currentPair['left glyph'], currentPair['right glyph'], increment)

    def incrementKerningByHigh_(self, sender=None):
        print('inc by high')
        currentIndices = self.w.outputList.getSelection()
        currentPair = self.w.outputList[currentIndices[0]]
        increment = Glyphs.intDefaults['GSKerningIncrementHigh']
        self.bumpKerningForPair(currentPair['left glyph'], currentPair['right glyph'], increment)

    # /Modification(Nic)

    # Modification(Nic): Routine to increment/decrement kerning properly
    def bumpKerningForPair(self, left, right, increment):
        leftGlyph, rightGlyph = self.f[left], self.f[right]
        k = self.f.kerningForPair(self.f.selectedFontMaster.id, leftGlyph.rightKerningKey, rightGlyph.leftKerningKey)
        if k > 10000: k = 0 # Glyphs uses MAXINT to signal no kerning.
        self.f.setKerningForPair(self.f.selectedFontMaster.id, leftGlyph.rightKerningKey, rightGlyph.leftKerningKey, k + increment)

    # Modification(Nic)

    def checkAll_(self, sender=None):
        self.check_(useSelection=False)

    def checkSel_(self, sender=None):
        self.check_(useSelection=True)

    def check_(self, useSelection):
        self._resizeWindow(enlarge=False)
        self.checkFont(useSelection=useSelection, excludeZeroWidth=self.w.options.zeroCheck.get())

    def showPair_(self, sender=None):
        try:
            index = sender.getSelection()[0]
            glyphs = [self.f[gName] for gName in self.touchingPairs[index]]
            ActiveFont = self.f
            EditViewController = ActiveFont.currentTab
            if EditViewController is None:
                tabText = "/%s/%s" %(glyphs[0].name, glyphs[1].name)
                ActiveFont.newTab(tabText)
            else:
                textStorage = EditViewController.graphicView()
                if not hasattr(textStorage, "replaceCharactersInRange_withString_"): # compatibility with API change in 2.5
                    textStorage = EditViewController.graphicView().textStorage()
                LeftChar = ActiveFont.characterForGlyph_(glyphs[0])
                RightChar = ActiveFont.characterForGlyph_(glyphs[1])
                if LeftChar != 0 and RightChar != 0:
                    selection = textStorage.selectedRange()
                    if selection.length < 2:
                        selection.length = 2
                        if selection.location > 0:
                            selection.location -= 1

                    NewString = ""
                    if LeftChar < 0xffff and RightChar < 0xffff:
                        NewString = "%s%s" % (chr(LeftChar), chr(RightChar))
                    else:
                        print("Upper plane codes are not supported yet")

                    textStorage.replaceCharactersInRange_withString_(selection, NewString)
                    selection.length = 0
                    selection.location += 1
                    textStorage.setSelectedRange_(selection)
            #self.w.preview.set(glyphs)
        except IndexError:
            pass

    # checking
    @objc.python_method
    def _hasSufficientWidth(self, g):
        # to ignore combining accents and the like
        if self.excludeZeroWidth:
            # also skips 1-unit wide glyphs which many use instead of 0
            if g.width < 2 or g.parent.subCategory == "Nonspacing":
                return False
        return True

    @objc.python_method
    def _trimGlyphList(self, glyphList):
        newGlyphList = []
        for g in glyphList:
            bounds = g.bounds
            if bounds.size.width > 0 and self._hasSufficientWidth(g):
                newGlyphList.append(g)
        return newGlyphList

    def windowResized_(self, window):
        posSize = self.w.getPosSize()
        Height = posSize[3]
        if Height > self.closedWindowHeight and self.isResizing is False:
            print("set new Height", Height)
            NSUserDefaults.standardUserDefaults().setInteger_forKey_(Height, "ToucheWindowHeight")
            self.windowHeight = Height

    @objc.python_method
    def _resizeWindow(self, enlarge=True):
        posSize = self.w.getPosSize()
        if enlarge:
            self.w.results.show(True)
            self.w.outputList.show(True)
            targetHeight = self.windowHeight
            if targetHeight < 340:
                targetHeight = 340
        else:
            self.w.results.show(False)
            self.w.outputList.show(False)
            targetHeight = self.closedWindowHeight
        self.isResizing = True
        self.w.setPosSize((posSize[0], posSize[1], posSize[2], targetHeight))
        self.isResizing = False

    # ok let's do this
    @objc.python_method
    def checkFont(self, useSelection=False, excludeZeroWidth=True):
        f = Glyphs.font
        if f is not None:
            # initialize things
            self.w.options.progress.start()
            time0 = time.time()
            self.excludeZeroWidth = excludeZeroWidth
            self.f = f
            masterID = f.masters[f.masterIndex].id
            glyphs = f.selection if useSelection else f.keys()
            glyphList = [g.layers[masterID] for g in glyphs]
            glyphList = self._trimGlyphList(glyphList)
            self.touchingPairs = Touche(f, masterID).findTouchingPairs(glyphList)

            # display output
            self.w.results.stats.set("%d glyphs checked" % len(glyphList))
            self.w.results.result.set("%d touching pairs found" % len(self.touchingPairs))
            self.w.results.show(True)

            outputList = [{"left glyph": g1, "right glyph": g2} for (g1, g2) in self.touchingPairs]
            self.w.outputList.set(outputList)
            if len(self.touchingPairs) > 0:
                self.w.outputList.setSelection([0])

            #self.w.preview.setFont(f)
            self.w.options.progress.stop()
            self._resizeWindow(enlarge=True)

            time1 = time.time()
            print('Touché: finished checking %d glyphs in %.2f seconds' % (len(glyphList), time1-time0))

        else:
            Message('Touché: Can’t find a font to check')
