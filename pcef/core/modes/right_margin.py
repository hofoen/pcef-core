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
This module contains the right margin mode.
"""
from pcef.core import constants
from pcef.core.mode import Mode
from pcef.qt import QtGui


class RightMarginMode(Mode):
    """
    Display the right margin
    """
    #: Mode identifier
    IDENTIFIER = "rightMargin"
    DESCRIPTION = "Draw the right margin on the text document"

    def __init__(self):
        Mode.__init__(self)
        #: Defines the margin position. 80 is the default
        self.marginPos = constants.MARGIN_POS
        self.__pen = QtGui.QPen()

    def install(self, editor):
        """
        Installs the mode on the editor and setup drawing tools

        :param editor: The editor instance
        """
        Mode.install(self, editor)
        color = self.editor.style.addProperty("margin", "#FF0000")
        self.__pen = QtGui.QPen(QtGui.QColor(color))
        self.marginPos = int(self.editor.settings.addProperty(
            "marginPos", "80"))

    def onStyleChanged(self, section, key, value):
        """
        Changes the margin color

        :param section:
        :param key:
        :param value:
        """
        if key == "margin":
            self.__pen = QtGui.QPen(QtGui.QColor(value))
            self.editor.update()

    def onStateChanged(self, state):
        """
        Connects/Disconnects to the painted event of the editor

        :param state: Enable state
        """
        if state:
            self.editor.painted.connect(self.__paintMargin)
            self.editor.update()
        else:
            self.editor.painted.disconnect(self.__paintMargin)
            self.editor.update()

    def __paintMargin(self, event):
        """ Paints the right margin after editor paint event. """
        rect = event.rect()
        font = self.editor.currentCharFormat().font()
        fm = QtGui.QFontMetricsF(font)
        pos = self.marginPos
        offset = self.editor.contentOffset().x() + \
            self.editor.document().documentMargin()
        x80 = round(fm.width(' ') * pos) + offset
        p = QtGui.QPainter(self.editor.viewport())
        p.setPen(self.__pen)
        p.drawLine(x80, rect.top(), x80, rect.bottom())
