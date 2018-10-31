#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import html
import os
import Cookie as cookies


form = cgi.FieldStorage()
view_mode = cgi.escape(form.getfirst("view_mode", ""))

tmp = """Content-type: text/html\n
<h1>IACT.PY</h1>
<b>view mode: {0}</b>""".format(view_mode)

print tmp
