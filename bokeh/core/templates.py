#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2021, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
''' Provide Jinja2 templates used by Bokeh to embed Bokeh documents and
models in various ways.

.. bokeh-jinja:: bokeh.core.templates.AUTOLOAD_JS
.. bokeh-jinja:: bokeh.core.templates.AUTOLOAD_NB_JS
.. bokeh-jinja:: bokeh.core.templates.AUTOLOAD_REQUEST_TAG
.. bokeh-jinja:: bokeh.core.templates.AUTOLOAD_TAG
.. bokeh-jinja:: bokeh.core.templates.CSS_RESOURCES
.. bokeh-jinja:: bokeh.core.templates.DOC_JS
.. bokeh-jinja:: bokeh.core.templates.DOC_NB_JS
.. bokeh-jinja:: bokeh.core.templates.FILE
.. bokeh-jinja:: bokeh.core.templates.JS_RESOURCES
.. bokeh-jinja:: bokeh.core.templates.NOTEBOOK_LOAD
.. bokeh-jinja:: bokeh.core.templates.PLOT_DIV
.. bokeh-jinja:: bokeh.core.templates.ROOT_DIV
.. bokeh-jinja:: bokeh.core.templates.SCRIPT_TAG

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations

import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import sys
from functools import lru_cache
from os.path import dirname, join
from typing import Any

# External imports
from jinja2 import Environment, FileSystemLoader

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

@lru_cache(None)
def get_env():
    ''' Get the correct Jinja2 Environment, also for frozen scripts.
    '''
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller uses _MEIPASS and only works with jinja2.FileSystemLoader
        templates_path = join(sys._MEIPASS, 'bokeh', 'core', '_templates')
    else:
        # Non-frozen Python and cx_Freeze can use __file__ directly
        templates_path = join(dirname(__file__), '_templates')

    return Environment(loader=FileSystemLoader(templates_path))

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------

_templates = dict(
    JS_RESOURCES=lambda: get_env().get_template("js_resources.html"),
    CSS_RESOURCES=lambda: get_env().get_template("css_resources.html"),
    SCRIPT_TAG=lambda: get_env().get_template("script_tag.html"),
    PLOT_DIV=lambda: get_env().get_template("plot_div.html"),
    ROOT_DIV=lambda: get_env().get_template("root_div.html"),
    DOC_JS=lambda: get_env().get_template("doc_js.js"),
    DOC_NB_JS=lambda: get_env().get_template("doc_nb_js.js"),
    FILE=lambda: get_env().get_template("file.html"),
    MACROS=lambda: get_env().get_template("macros.html"),
    NOTEBOOK_LOAD=lambda: get_env().get_template("notebook_load.html"),
    AUTOLOAD_JS=lambda: get_env().get_template("autoload_js.js"),
    AUTOLOAD_NB_JS=lambda: get_env().get_template("autoload_nb_js.js"),
    AUTOLOAD_TAG=lambda: get_env().get_template("autoload_tag.html"),
    AUTOLOAD_REQUEST_TAG=lambda: get_env().get_template("autoload_request_tag.html"),
)

@lru_cache(None)
def __getattr__(name: str) -> Any:
    if name in _templates:
        return _templates[name]()
    raise AttributeError()
