#!/usr/bin/env python
# -*- coding= utf-8 -*-

"""Utility functions for retrieving main windows of DCC applications."""

# Built-in
import shiboken2
from typing import Optional, Any

# Third-party
from PySide2 import QtWidgets

# Metadatas
__author__ = "John Russel"
__email__ = "johndavidrussell@gmail.com"


###### CODE ####################################################################


def get_dcc_main_window() -> Optional[Any]:
    """This function attempts to import a series of modules and call a corresponding function in each.
    The first successful call is returned. If no calls are successful, the function returns `None`.

    Returns:
        Optional[Any]: The return value of the first successful function call, or `None` if no calls are successful.
    """

    dccs = [
        ("maya.OpenMayaUI", "get_maya_main_window"),
        ("hou", "get_houdini_main_window"),
        ("nuke", "get_nuke_main_window"),
    ]

    for module_name, function_name in dccs:
        try:
            module = __import__(module_name)
            function = getattr(module, function_name)
            return function()
        except ImportError:
            continue
    return None


def get_houdini_main_window() -> QtWidgets.QWidget:
    """Get the Houdini main window.

    Returns:
        PySide2.QtWidgets.QWidget: `QWidget` Houdini main window.
    """

    return hou.qt.mainWindow()  # type:ignore


def get_houdini_stylesheet() -> str:
    """Get the Houdini stylesheet.

    Returns:
        str: The Houdini stylesheet.
    """

    return hou.qt.styleSheet()  # type:ignore


def get_maya_main_window() -> QtWidgets.QWidget:
    """Get the Maya main window.

    Returns:
        PySide2.QtWidgets.QWidget: `TmainWindow` Maya main window.
    """

    window = apiUI.MQtUtil.mainWindow()  # type:ignore
    if window is not None:
        return shiboken2.wrapInstance(int(window), QtWidgets.QWidget)


def get_nuke_main_window() -> QtWidgets.QMainWindow:
    """Get the Nuke main window.

    Returns:
        PySide2.QtWidgets.QMainWindow: `DockMainWindow` Nuke main window.
    """

    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.inherits("QMainWindow") and widget.metaObject().className() == "Foundry::UI::DockMainWindow":
            return widget
