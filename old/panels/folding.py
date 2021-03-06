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
Contains the generic panels (used by the generic code editor widget)
"""
import logging
from PySide.QtCore import Qt
from PySide.QtCore import QRect
from PySide.QtCore import QSize
from PySide.QtGui import QFont
from PySide.QtGui import QColor
from PySide.QtGui import QFontMetricsF
from PySide.QtGui import QPainter
from PySide.QtGui import QPen
from PySide.QtGui import QBrush
from pygments.token import Text
from pcef.core import Panel


class FoldIndicator(object):
    """
    A fold marker is used by the FoldPanel to display code folding indicators.

    A fold marker is defined by two line number (start and end) and a boolean
    property that tells whether the code block is folded or not.
    """
    def __init__(self, start, end):
        #: Start line
        self.start = start
        #: End line
        self.end = end
        #: Is folded ?
        self.folded = False
        #: Is hover ?
        self.hover = False


class FoldPanel(Panel):
    """ This Panel display folding indicators and manage folding/unfolding a text


    The panel also handles line added/removed and update the indicators position automatically.

    .. note:: It does not parse the code to put fold indicators, this is the task of a code folder mode. Instead it
              provides an easy way for other modes to put fold indicators on the left margin.
    """
    #: Panel identifier
    IDENTIFIER = "Folding"
    DESCRIPTION = "Display code folding indicators"

    def __init__(self, parent=None):
        Panel.__init__(
            self, self.IDENTIFIER, self.DESCRIPTION, parent)
        self.fold_indicators = []
        self.setMouseTracking(True)
        self.logger = logging.getLogger(
            __name__ + "." + self.__class__.__name__)

    def addIndicator(self, start, end):
        """
        Adds a fold indicator
        :param start: Start line (1 based)
        :param end: End line
        """
        self.fold_indicators.append(FoldIndicator(start, end))
        self.update()

    def removeIndicator(self, indicator):
        """
        Remove a fold indicator
        :param indicator: Indicator to remove
        """
        self.fold_indicators.remove(indicator)
        self.update()

    def clearIndicators(self):
        """ Remove all indicators """
        self.fold_indicators[:] = []
        self.update()

    def install(self, editor):
        """ Install the Panel on the editor """
        Panel.install(self, editor)
        self.bc = self.editor.codeEdit.blockCount()
        self.__updateCursorPos()

    def _onStateChanged(self, state):
        Panel._onStateChanged(self, state)
        if state is True:
            self.editor.codeEdit.visibleBlocksChanged.connect(self.update)
            self.editor.codeEdit.blockCountChanged.connect(self.__onBlockCountChanged)
            self.editor.codeEdit.newTextSet.connect(self.__onNewTextSet)
            self.editor.codeEdit.keyPressed.connect(self.__updateCursorPos)
        else:
            self.editor.codeEdit.visibleBlocksChanged.disconnect(self.update)
            self.editor.codeEdit.blockCountChanged.disconnect(self.__onBlockCountChanged)
            self.editor.codeEdit.newTextSet.disconnect(self.__onNewTextSet)
            self.editor.codeEdit.keyPressed.disconnect(self.__updateCursorPos)

    def _onStyleChanged(self):
        """ Updates brushes and pens """
        style = self.currentStyle
        self.font = QFont(self.currentStyle.fontName, 7)
        self.font.setBold(True)
        fm = QFontMetricsF(self.editor.codeEdit.font())
        self.size_hint = QSize(16, 16)
        self.back_brush = QBrush(QColor(style.panelsBackgroundColor))
        self.active_line_brush = QBrush(QColor(style.activeLineColor))
        self.separator_pen = QPen(QColor(style.panelSeparatorColor))
        self.normal_pen = QPen(QColor(style.lineNbrColor))
        self.highlight_pen = QPen(QColor(style.tokenColor(Text)))
        self.repaint()

    def sizeHint(self):
        """ Returns a fixed size hint (16x16) """
        self.size_hint = QSize(16, 16)
        return self.size_hint

    def __onNewTextSet(self):
        self.clearIndicators()

    def getIndicatorForLine(self, line):
        """ Returns the fold indicator whose start position equals the line
        :param line: Line nbr of the start position of the indicator to get.
        :return: FoldIndicator or None
        """
        for m in self.fold_indicators:
            if m.start == line:
                return m
        return None

    def __updateCursorPos(self):
        """
        Update tcPos and tcPosInBlock
        :return:
        """
        self.tcPos = self.editor.codeEdit.textCursor().blockNumber() + 1
        self.tcPosInBlock = self.editor.codeEdit.textCursor().positionInBlock()

    def __onBlockCountChanged(self, num=-1):
        """ Handles line added/removed event """
        # a line has been inserted or removed
        tcPos = self.editor.codeEdit.textCursor().blockNumber() + 1
        tcPosInBlock = self.editor.codeEdit.textCursor().positionInBlock()
        bc = self.bc
        if bc < num:
            self.__onLinesAdded(num - bc, tcPos, tcPosInBlock)
        else:
            self.__onLinesRemoved(bc - num, tcPos, tcPosInBlock)
        self.tcPosInBlock = self.tcPosInBlock
        self.bc = num

    def __onLinesAdded(self, nbLines, tcPos, tcPosInBlock):
        """ Offsets markers positions with the number of line added """
        if self.tcPosInBlock > 0:
            self.tcPos += 1
        # offset each line after the tcPos by nbLines
        for marker in self.fold_indicators:
            if marker.start >= self.tcPos:
                marker.start += nbLines
            if marker.end >= self.tcPos:
                marker.end += nbLines
        self.tcPos = tcPos
        self.tcPosInBlock = tcPosInBlock
        self.update()

    def __onLinesRemoved(self, nbLines, tcPos, tcPosInBlock):
        """ Offsets markers positions with the number of line removed """
        for marker in self.fold_indicators:
            if marker.start >= self.tcPos:
                marker.start -= nbLines
                if marker.start < 1:
                    self.removeIndicator(marker)
            if marker.end >= self.tcPos:
                marker.end -= nbLines
            if marker.end == marker.start:
                self.removeIndicator(marker)
        self.tcPos = tcPos
        self.tcPosInBlock = tcPosInBlock
        self.update()

    def paintEvent(self, event):
        """ Paints the widget """
        if self.enabled is False:
            return
        Panel.paintEvent(self, event)
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.back_brush)

        for vb in self.editor.codeEdit.visible_blocks:
            line = vb.row
            # paint marker for line
            marker = self.getIndicatorForLine(line)
            if marker is None:
                continue
                # use the normal pen to draw the fold indicator
            drawLines = False
            pen = self.normal_pen
            if marker.hover is True:
                pen = self.highlight_pen
                drawLines = True
            painter.setPen(pen)
            # get the text to draw
            txt = '-'
            if marker.folded is True:
                drawLines = False
                txt = '+'
            offset = 4
            h = self.size_hint.height()
            fm = QFontMetricsF(self.editor.codeEdit.font())
            hoffset = (fm.height() - h) / 2.0
            r = QRect(vb.rect.x(), vb.rect.y() + hoffset, self.size_hint.width(), self.size_hint.height())
            painter.setFont(self.font)
            painter.drawText(r, Qt.AlignVCenter | Qt.AlignHCenter, txt)
            w = self.size_hint.width() - 2 * offset
            h = self.size_hint.width() - 2 * offset
            hoffset = (fm.height() - h) / 2.0
            r.setX(vb.rect.x() + offset)
            r.setY(vb.rect.y() + hoffset)
            r.setWidth(w)
            r.setHeight(h)
            painter.drawRect(r)
            if drawLines is True:
                top = (vb.rect.x() + self.size_hint.width() / 2.0,
                       vb.rect.y() + hoffset + offset * 2)
                delta = ((marker.end - marker.start) * vb.height)  # - (vb.rect.height() / 2.0)
                bottom = (top[0], top[1] + delta)
                painter.drawLine(top[0], top[1], bottom[0], bottom[1])
                painter.drawLine(bottom[0], bottom[1], bottom[0] + self.size_hint.width() / 2.0, bottom[1])

        return

    def leaveEvent(self, event):
        """ Clears indicator hover states and repaint """
        for m in self.fold_indicators:
            m.hover = False
        self.repaint()

    def mouseMoveEvent(self, event):
        """ Detects indicator hover states """
        if self.enabled is False:
            return
        pos = event.pos()
        y = pos.y()
        repaint = False
        for m in self.fold_indicators:
            if m.hover is True:
                m.hover = False
                repaint = True
        for vb in self.editor.codeEdit.visible_blocks:
            top = vb.top
            height = vb.height
            if top < y < top + height:
                marker = self.getIndicatorForLine(vb.row)
                if marker is not None:
                    # mark it as hover and repaint
                    marker.hover = True
                    repaint = True
        if repaint is True:
            self.repaint()

    def mouseReleaseEvent(self, event):
        """
        Folds/Unfolds code blocks
        """
        if self.enabled is False:
            return
        pos = event.pos()
        y = pos.y()
        for vb in self.editor.codeEdit.visible_blocks:
            top = vb.top
            height = vb.height
            if top < y < top + height:
                marker = self.getIndicatorForLine(vb.row)
                if marker is not None:
                    marker.folded = not marker.folded
                    self.editor.codeEdit.fold(marker.start - 1, marker.end, marker.folded)
                    self.repaint()