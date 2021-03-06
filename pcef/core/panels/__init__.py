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
This package contains the core panels (language independant)
"""
from pcef.core.panels.line_number import LineNumberPanel
from pcef.core.panels.search_and_replace import SearchAndReplacePanel

__all__ = ["LineNumberPanel", "SearchAndReplacePanel"]


