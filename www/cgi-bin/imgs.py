#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import io
import cgi
import html
import Cookie as cookies

idir = "//home//hjk//www//static"
tmp2 = ""
tmp3 = ""

form = cgi.FieldStorage()
view_mode = cgi.escape(form.getfirst("view_mode", ""))
#if view_mode == None or view_mode == "":
#	view_mode = "0"

cookie = cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
cval = cookie.get("vmode")

if (view_mode == None or view_mode == "") and cval == None:
	tmp2 = "Set-cookie: vmode=0; expires=Wed May 18 03:33:20 2033; path=/cgi-bin/; httponly"
	tmp3 = "None"
elif (view_mode == None or view_mode == "") and cval != None:
	tmp2 = "Set-cookie: vmode={cv}; expires=Wed May 18 03:33:20 2033; path=/cgi-bin/; httponly".format(cv = cval.value)
	tmp3 = cval.value
elif view_mode == "S" and cval == None:
	tmp2 = "Set-cookie: vmode=0; expires=Wed May 18 03:33:20 2033; path=/cgi-bin/; httponly"
	tmp3 = "None"
elif view_mode == "S" and cval != None:
	tmp4 = { "0" : "1", "1" : "0" }[cval.value]
	tmp2 = "Set-cookie: vmode={cv}; expires=Wed May 18 03:33:20 2033; path=/cgi-bin/; httponly".format(cv = tmp4)
	tmp3 = cval.value

con_str = ""
Dirs = []
Files = []

pattern = ""
if tmp3 == "0":
	pattern = "<p>--------<a href=\"{0}\">{1}</a></p>"
else:
	pattern = "<p style=\"color: red; font-size: 14pt;\">{1}</p><p><a><img src = \"{0}\"\
id=\"Img\" onclick=\"iclick()\" style=\"width: 25%; height: 25%;\"></a></p>"
#	pattern = "<p>{1}</p><p><a href=\"{0}\"><img src = \"{0}\"\
#id=\"Img\" onclick=\"iclick()\"></a></p>"

for path, dirs, files in os.walk(idir):
	Dirs.append(path)
	Files.append(files)
	con_str += "<hr><b>{0}</b><br>".format(path)
	for f in files:
		tpath = path.split("www")[-1]
		con_str += pattern.format((tpath + "//" + f).replace("//", "/"), f)

"""/
con_str_l = "<hr>"
con_str_r = "<hr>"
tmp_ = con_str.split("<hr>")[1:-1]
for i in tmp_:
	_tmp = i.split("</p>")
	q0 = _tmp[0].split("<br>")
	con_str_l += q0[0] + "<br>"
	con_str_r += q0[0] + "<br>"
	_tmp[0] = q0[1]
	for j, v in enumerate(_tmp):
		if j % 2 == 0:
			con_str_l += v + "</p>"
		else:
			con_str_r += v + "</p>"
	if len(_tmp) % 2 != 0:
		con_str_r += "<p></p>"
	con_str_l += "<hr>"
	con_str_r += "<hr>"
con_str = "<hr>"
"""
con_str_l = ""
con_str_r = ""

#files = os.listdir(idir)
#afiles = [ idir +"//" + i for i in files ]
#dirs = [ i for i in afiles if os.path.isdir(i) ]

if False:
	tmp2 = ""
	tmp3 = ""
	if cval is None and view_mode != "1":
		tmp2 = """Set-cookie: vmode=0; expires=Wed May 18 03:33:20 2033; path=/cgi-bin/; httponly
			"""
		tmp3 = "None"
	else:
		if cval is not None:
			tmp3 = cval.value
		else:
			tmp3 = "0"
		tmp2 = """Set-cookie: vmode={cv}; expires=Wed May 18 03:33:20 2033; path=/cgi-bin/; httponly
		""".format(cv = view_mode)

	tmp = """<form action="/cgi-bin/imgs.py">
			<input type = "hidden" name = "view_mode" value = "1">
			<input type = "submit">
		</form>
	"""

tmp3 = { "0" : "links", "None" : "links",  "1" : "images" }[tmp3]

script_str = """\
function iclick() {
//	alert("ssdlkfskdf");
	var elem = document.getElementById("Img");
//	alert(str);
	if(elem.style.width === "25%") {
		elem.style.width = "100%";
		elem.style.height = "100%";
		return;
	}
	if(elem.style.width === "100%") {
		elem.style.width = "25%";
		elem.style.height = "25%";
		return;
	}
//	elem.style.border = "4px solid black";
}
"""

style_str = """\
	#left { position: absolute; left: 0; top: auto; width: 50%; }
	#right { position: absolute; right: 0; top: auto; width: 50%; }
"""



tmp = """{cookie_place}
Content-type: text/html\n
<!DOCTYPE HTML>
<html>
<head>
	<meta charset = "utf-8">
	<title>Images</title>
	<style type = "text/css">
	{style_code}
	</style>
	<script>
	{script_code}
	</script>
</head>
<body>
	<h1>Imgs:</h1>
	<b>view mode: {cookie_mode}</b>
	<form action="/cgi-bin/imgs.py">
		<input type = "hidden" name = "view_mode" value = "S">
		<input type = "submit">
	</form>
	<hr>

	{img_content}

	<div id = "left">
		{img_content_l}
	</div>


	<div id = "right">
		{img_content_r}
	</div>

</body>
</html>
""".format(cookie_place = tmp2, cookie_mode = tmp3, img_content = con_str,
script_code = script_str, style_code = style_str, img_content_l = con_str_l,
img_content_r = con_str_r)

print tmp

