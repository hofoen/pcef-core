#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PCEF - Python/Qt Code Editing Framework
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
This module contains the search and replace panel
"""
from pcef.qt import QtCore, QtGui
from pcef.core import constants
from pcef.core.decoration import TextDecoration
from pcef.core.panel import Panel
from pcef.core.system import DelayJobRunner
from pcef.core.ui import loadUi


class SearchAndReplacePanel(Panel, DelayJobRunner):
    """
    This panel allow the user to search and replace some text in the current
    editor.

    It uses the QTextDocument API to search for some text. Search operation is
    performed in a background thread.

    The search panel can also be used pragmatically. To do that, the client code
    must first request a search (**requestSearch**) and connect to the
    searchFinished signal. The results of the search can then be retrieved using
    the cptOccurrences attribute and the getOccurrences method. The client code
    may now navigates through occurrences (**selectNext**/**selectionPrevious**)
    or replace the occurences with their own text (
    **replaceOccurrence**/**replaceAll**).
    """
    IDENTIFIER = "searchPanel"
    DESCRIPTION = "Search and replace text in the editor"

    #: Stylesheet
    STYLESHEET = """QWidget
    {
        background-color: %(bck)s;
        color: %(color)s;
    }

    QLineEdit
    {
        background-color: %(txt_bck)s;
        border: 1px solid %(highlight)s;
        border-radius: 3px;
    }

    QLineEdit:hover, QLineEdit:focus
    {
        border: 1px solid %(color)s;
        border-radius: 3px;
    }

    QPushButton
    {
        background-color: transparent;
        padding: 5px;
        border: none;
    }

    QPushButton:hover
    {
        background-color: %(highlight)s;
        border: none;
        border-radius: 5px;
        color: %(color)s;
    }

    QPushButton:pressed, QCheckBox:pressed
    {
        border: 1px solid %(bck)s;
    }

    QPushButton:disabled
    {
        color: %(highlight)s;
    }

    QCheckBox
    {
        padding: 4px;
    }

    QCheckBox:hover
    {
            background-color: %(highlight)s;
            color: %(color)s;
            border-radius: 5px;
    }
    """
    _KEYS = ["panelBackground", "background", "foreground", "panelHighlight"]

    #: Signal emitted when a search operation finished
    searchFinished = QtCore.Signal()

    @property
    def background(self):
        return self.editor.style.value("searchOccurrenceBackground")

    @property
    def foreground(self):
        return self.editor.style.value("searchOccurrenceForeground")

    def __init__(self):
        Panel.__init__(self)
        DelayJobRunner.__init__(self, self, nbThreadsMax=1, delay=500)
        loadUi("search_panel.ui", self)
        #: Occurrences counter
        self.cptOccurrences = 0
        self.__separator = None
        self.__decorations = []
        self.__mutex = QtCore.QMutex()
        self.__occurrences = []
        self.__current_occurrence = -1
        self.__updateButtons(txt="")
        self.lineEditSearch.installEventFilter(self)
        self.lineEditReplace.installEventFilter(self)

    def install(self, editor):
        Panel.install(self, editor)
        self.__resetStylesheet()
        self.on_pushButtonClose_clicked()
        self.editor.style.addProperty("searchOccurrenceBackground",
                                      constants.SEARCH_OCCURRENCES_BACKGROUND)
        self.editor.style.addProperty("searchOccurrenceForeground",
                                      constants.SEARCH_OCCURRENCES_FOREGROUND)

    def onStyleChanged(self, section, key, value):
        if key in self._KEYS:
            self.__resetStylesheet()

    def onStateChanged(self, state):
        if state:
            # add menus
            self.__separator = self.editor.contextMenu.addSeparator()
            self.editor.contextMenu.addAction(self.actionSearch)
            self.editor.contextMenu.addAction(self.actionActionSearchAndReplace)
            self.editor.contextMenu.addAction(self.actionFindNext)
            self.editor.contextMenu.addAction(self.actionFindPrevious)
            # requestSearch slot
            self.editor.textChanged.connect(self.requestSearch)
            self.lineEditSearch.textChanged.connect(self.requestSearch)
            self.checkBoxCase.stateChanged.connect(self.requestSearch)
            self.checkBoxWholeWords.stateChanged.connect(self.requestSearch)
            # navigation slots
            self.pushButtonNext.clicked.connect(self.selectNext)
            self.actionFindNext.triggered.connect(self.selectNext)
            self.pushButtonPrevious.clicked.connect(self.selectPrevious)
            self.actionFindPrevious.triggered.connect(self.selectPrevious)
            # replace slots
            self.pushButtonReplace.clicked.connect(self.replaceCurrent)
            self.pushButtonReplaceAll.clicked.connect(self.replaceAll)
            # internal updates slots
            self.lineEditReplace.textChanged.connect(self.__updateButtons)
            self.searchFinished.connect(self.__onSearchFinished)
        else:
            # remove menus
            if self.__separator:
                self.editor.contextMenu.removeAction(self.__separator)
            self.editor.contextMenu.removeAction(self.actionSearch)
            self.editor.contextMenu.removeAction(
                self.actionActionSearchAndReplace)
            self.editor.contextMenu.removeAction(self.actionFindNext)
            self.editor.contextMenu.removeAction(self.actionFindPrevious)
            # requestSearch slot
            self.editor.textChanged.disconnect(self.requestSearch)
            self.lineEditSearch.textChanged.disconnect(self.requestSearch)
            self.checkBoxCase.stateChanged.disconnect(self.requestSearch)
            self.checkBoxWholeWords.stateChanged.disconnect(self.requestSearch)
            # navigation slots
            self.pushButtonNext.clicked.disconnect(self.selectNext)
            self.actionFindNext.triggered.disconnect(self.selectNext)
            self.pushButtonPrevious.clicked.disconnect(self.selectPrevious)
            # replace slots
            self.pushButtonReplace.clicked.disconnect(self.replaceCurrent)
            self.pushButtonReplaceAll.clicked.disconnect(self.replaceAll)
            # internal updates slots
            self.lineEditReplace.textChanged.disconnect(self.__updateButtons)
            self.searchFinished.connect(self.__onSearchFinished)

    @QtCore.Slot()
    def on_pushButtonClose_clicked(self):
        """
        Closes the panel
        :return:
        """
        self.hide()
        self.lineEditReplace.clear()
        self.lineEditSearch.clear()

    @QtCore.Slot()
    def on_actionSearch_triggered(self):
        """
        Executes the search action using the selected text of the editor
        (Ctrl+F).
        """
        self.widgetSearch.show()
        self.widgetReplace.hide()
        self.show()
        newText = self.editor.selectedText()
        oldText = self.lineEditSearch.text()
        textChanged = newText != oldText
        self.lineEditSearch.setText(newText)
        self.lineEditSearch.selectAll()
        self.lineEditSearch.setFocus()
        if not textChanged:
            self.requestSearch(newText)

    @QtCore.Slot()
    def on_actionActionSearchAndReplace_triggered(self):
        """
        Executes the search and replace action using the selected text of the
        editor (ctrl+r)
        """
        self.widgetSearch.show()
        self.widgetReplace.show()
        self.show()
        newText = self.editor.selectedText()
        oldText = self.lineEditSearch.text()
        textChanged = newText != oldText
        self.lineEditSearch.setText(newText)
        self.lineEditReplace.clear()
        self.lineEditReplace.setFocus()
        if not textChanged:
            self.requestSearch(newText)

    def focusOutEvent(self, event):
        """ Cancel jobs when leaving the widget """
        self.stopJob()
        self.cancelRequests()
        Panel.focusOutEvent(self, event)

    def requestSearch(self, txt=None):
        """
        Request a search operation.

        :param txt: The text to replace. If None, the content of lineEditSearch
        is used instead.
        """
        if txt is None or isinstance(txt, int):
            txt = self.lineEditSearch.text()
        if txt:
            self.requestJob(self.__execSearch, True,
                            txt, self.editor.document().clone(),
                            self.editor.textCursor(),
                            self.__getUserSearchFlag())
        else:
            self.cancelRequests()
            self.stopJob()
            self.__clearOccurrences()
            self.__onSearchFinished()

    def getOccurrences(self):
        """
        Returns the list of text occurrences.

        An occurrence is a tuple that contains start and end positions.

        :return: List of tuple(int, int)
        """
        self.__mutex.lock()
        retval = []
        for occ in self.__occurrences:
            retval.append(occ)
        self.__mutex.unlock()
        return retval

    def selectNext(self):
        """
        Selects the next occurrence.

        :return: True in case of success, false if no occurrence could be
        selected.
        """
        cr = self.__getCurrentOccurrence()
        occurrences = self.getOccurrences()
        if (cr == -1 or
                cr == len(occurrences) - 1):
            cr = 0
        else:
            cr += 1
        self.__setCurrentOccurrence(cr)
        try:
            tc = self.editor.textCursor()
            tc.setPosition(occurrences[cr][0])
            tc.setPosition(occurrences[cr][1], tc.KeepAnchor)
            self.editor.setTextCursor(tc)
            return True
        except IndexError:
            return False

    def selectPrevious(self):
        """
        Selects previous occurrence.

        :return: True in case of success, false if no occurrence could be
        selected.
        """
        cr = self.__getCurrentOccurrence()
        occurrences = self.getOccurrences()
        if (cr == -1 or
                cr == 0):
            cr = len(occurrences) - 1
        else:
            cr -= 1
        self.__setCurrentOccurrence(cr)
        try:
            tc = self.editor.textCursor()
            tc.setPosition(occurrences[cr][0])
            tc.setPosition(occurrences[cr][1], tc.KeepAnchor)
            self.editor.setTextCursor(tc)
            return True
        except IndexError:
            return False

    def replaceCurrent(self, text=None):
        """
        Replaces the selected occurrence.

        :param text: The replacement text. If it is None, the lineEditReplace's
        text is used instead.

        :return True if the text could be replace properly, False if there is
        no more occurrences to replace.
        """
        if text is None or isinstance(text, bool):
            text = self.lineEditReplace.text()
        cr = self.__getCurrentOccurrence()
        occurrences = self.getOccurrences()
        if cr == -1:
            self.selectNext()
        try:
            try:
                self.editor.textChanged.disconnect(self.requestSearch)
            except RuntimeError:
                pass
            occ = occurrences[cr]
            tc = self.editor.textCursor()
            tc.setPosition(occ[0])
            tc.setPosition(occ[1], tc.KeepAnchor)
            len_to_replace = len(tc.selectedText())
            len_replacement = len(text)
            offset = len_replacement - len_to_replace
            tc.insertText(text)
            self.editor.setTextCursor(tc)
            self.editor.textChanged.connect(self.requestSearch)
            # prevent search request due to editor textChanged
            self.__removeOccurrence(cr, offset)
            cr -= 1
            self.__setCurrentOccurrence(cr)
            self.selectNext()
            self.cptOccurrences = len(self.getOccurrences())
            self.__updateLabels()
            self.__updateButtons()
            return True
        except IndexError:
            return False

    def replaceAll(self, text=None):
        """
        Replaces all occurrences in the editor's document.

        :param text: The replacement text. If None, the content of the lineEdit
                     replace will be used instead
        """
        remains = self.replaceCurrent(text=text)
        while remains:
            remains = self.replaceCurrent(text=text)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if (event.key() == QtCore.Qt.Key_Tab or
                    event.key() == QtCore.Qt.Key_Backtab):
                return True
            elif (event.key() == QtCore.Qt.Key_Return or
                    event.key() == QtCore.Qt.Key_Enter):
                if obj == self.lineEditReplace:
                    if event.modifiers() & QtCore.Qt.ControlModifier:
                        self.replaceAll()
                    else:
                        self.replaceCurrent()
                elif obj == self.lineEditSearch:
                    self.selectNext()
                return True
            elif event.key() == QtCore.Qt.Key_Escape:
                self.on_pushButtonClose_clicked()
        return Panel.eventFilter(self, obj, event)

    def __getUserSearchFlag(self):
        """ Returns the user search flag """
        searchFlag = QtGui.QTextDocument.FindFlags(0)
        if self.checkBoxCase.isChecked():
            searchFlag |= QtGui.QTextDocument.FindCaseSensitively
        if self.checkBoxWholeWords.isChecked():
            searchFlag |= QtGui.QTextDocument.FindWholeWords
        return searchFlag

    def __execSearch(self, text, doc, originalCursor, flags):
        self.__mutex.lock()
        self.__occurrences[:] = []
        self.__current_occurrence = -1
        if text:
            cptMatches = 0
            cursor = doc.find(text, 0, flags)
            while not cursor.isNull():
                if self.__compareCursors(cursor, originalCursor):
                    self.__current_occurrence = cptMatches
                self.__occurrences.append((cursor.selectionStart(),
                                          cursor.selectionEnd()))
                cursor.setPosition(cursor.position() + 1)
                cursor = doc.find(text, cursor, flags)
                cptMatches += 1
        self.__mutex.unlock()
        self.searchFinished.emit()

    def __updateLabels(self):
        self.labelMatches.setText("{0} matches".format(self.cptOccurrences))
        color = "#DD0000"
        if self.cptOccurrences:
            color = "#00DD00"
        self.labelMatches.setStyleSheet("color: %s" % color)
        if self.lineEditSearch.text() == "":
            self.labelMatches.clear()

    def __onSearchFinished(self):
        self.__clearDecorations()
        occurrences = self.getOccurrences()
        for occurrence in occurrences:
            deco = self.__createDecoration(occurrence[0],
                                           occurrence[1])
            self.__decorations.append(deco)
            self.editor.addDecoration(deco)
        self.cptOccurrences = len(occurrences)
        if not self.cptOccurrences:
            self.__current_occurrence = -1
        elif self.__getCurrentOccurrence() == -1:
            self.selectNext()
        self.__updateLabels()
        self.__updateButtons(txt=self.lineEditReplace.text())

    def __resetStylesheet(self):
        stylesheet = self.STYLESHEET % {
            "bck": self.editor.style.value(self._KEYS[0]).name(),
            "txt_bck": self.editor.style.value(self._KEYS[1]).name(),
            "color": self.editor.style.value(self._KEYS[2]).name(),
            "highlight": self.editor.style.value(self._KEYS[3]).name()}
        self.setStyleSheet(stylesheet)

    def __getCurrentOccurrence(self):
        self.__mutex.lock()
        retVal = self.__current_occurrence
        self.__mutex.unlock()
        return retVal

    def __clearOccurrences(self):
        self.__mutex.lock()
        self.__occurrences[:] = []
        self.__mutex.unlock()

    def __createDecoration(self, selection_start, selection_end):
        """ Creates the text occurences decoration """
        deco = TextDecoration(self.editor.document(), selection_start,
                              selection_end)
        deco.setBackground(QtGui.QBrush(self.background))
        deco.setForeground(QtGui.QBrush(self.foreground))
        deco.draw_order = 1
        return deco

    def __clearDecorations(self):
        """ Remove all decorations """
        for deco in self.__decorations:
            self.editor.removeDecoration(deco)
        self.__decorations[:] = []

    def __setCurrentOccurrence(self, cr):
        self.__mutex.lock()
        self.__current_occurrence = cr
        self.__mutex.unlock()

    def __compareCursors(self, a, b):
        assert isinstance(a, QtGui.QTextCursor)
        assert isinstance(b, QtGui.QTextCursor)
        return (a.selectionStart() == b.selectionStart() and
                a.selectionEnd() == b.selectionEnd())

    def __removeOccurrence(self, i, offset=0):
        self.__mutex.lock()
        self.__occurrences.pop(i)
        if offset:
            updated_occurences = []
            for j, occ in enumerate(self.__occurrences):
                if j >= i:
                    updated_occurences.append(
                        (occ[0] + offset, occ[1] + offset))
                else:
                    updated_occurences.append((occ[0], occ[1]))
            self.__occurrences = updated_occurences
        self.__mutex.unlock()

    def __updateButtons(self, txt=""):
        enable = self.cptOccurrences > 1
        self.pushButtonNext.setEnabled(enable)
        self.pushButtonPrevious.setEnabled(enable)
        self.actionFindNext.setEnabled(enable)
        self.actionFindPrevious.setEnabled(enable)
        enable = txt != self.lineEditSearch.text() and bool(self.cptOccurrences)
        self.pushButtonReplace.setEnabled(enable)
        self.pushButtonReplaceAll.setEnabled(enable)
