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
This package contains the core classes of pcef and an example of a generic
code editor widget
"""
#
# exposes public core api
#
import os
from pcef.core import constants
from pcef.core.constants import PanelPosition
from pcef.core.decoration import TextDecoration
from pcef.core.editor import QCodeEdit
from pcef.core.mode import Mode
from pcef.core.modes import AutoIndentMode
from pcef.core.modes import CaretLineHighlighterMode
from pcef.core.panel import Panel
from pcef.core.modes import PygmentsHighlighterMode
from pcef.core.modes import RightMarginMode
from pcef.core.modes import ZoomMode
from pcef.core.panels import LineNumberPanel
from pcef.core.panels import SearchAndReplacePanel
from pcef.core.properties import PropertyRegistry
from pcef.core.system import TextStyle
from pcef.core.system import JobRunner
from pcef.core.system import DelayJobRunner
from pcef.qt.ui import importRc

#: pcef-core version
__version__ = "1.0.0-dev"


def getUiDirectory():
    """
    Gets the pcef-core ui directory
    """
    return os.path.join(os.path.abspath(os.path.join(__file__, "..")), "ui")


def getRcDirectory():
    """
    Gets the pcef-core rc directory
    """
    return os.path.join(os.path.abspath(os.path.join(__file__, "..")), "ui",
                        "rc")

# import the core rc modules
importRc(os.path.join(getUiDirectory(), "pcef_icons.qrc"))


#
# Example of a generic code editor widgey
#
class QGenericCodeEdit(QCodeEdit):
    """
    Extends QCodeEdit with a hardcoded set of modes and panels.

    **Panels:**
        * line number panel
        * search and replace panel

    **Modes:**
        * document word completion
        * generic syntax highlighter (pygments)
    """
    def __init__(self, parent=None):
        QCodeEdit.__init__(self, parent)
        self.setLineWrapMode(self.NoWrap)
        self.setWindowTitle("PCEF - Generic Editor")
        self.installPanel(LineNumberPanel(), PanelPosition.LEFT)
        self.installPanel(SearchAndReplacePanel(), PanelPosition.BOTTOM)
        self.installMode(CaretLineHighlighterMode())
        self.installMode(RightMarginMode())
        self.installMode(PygmentsHighlighterMode())
        self.installMode(ZoomMode())
        self.installMode(AutoIndentMode())

__all__ = ["__version__", "constants", "Mode", "Panel", "QCodeEdit",
           "LineNumberPanel", "SearchAndReplacePanel",
           "CaretLineHighlighterMode", "RightMarginMode", "ZoomMode",
           "PygmentsHighlighterMode", "AutoIndentMode", "PanelPosition",
           "TextDecoration", "PropertyRegistry", "TextStyle",
           "QGenericCodeEdit", "JobRunner", "DelayJobRunner",
           "getUiDirectory", "getRcDirectory"]
