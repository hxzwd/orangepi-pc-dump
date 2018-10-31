#!/usr/bin/env python
# -*- coding: utf-8 -*-

F_DEBUG = False


import os
import io
import re
import sys

from pprint import pformat
from datetime import datetime

HtmlTemplateFile = "//home//hjk//www//html//gallery.template.html"
CssTemplateFile = "//home//hjk//www//css//gallery.template.css"
LogFile = "//home//hjk//www//log//gallery.log"

content_header = "Content-type: text/html"
debug_header = "Content-type: text"

template_pattern = r"([^\{]*[\{]{1})([^\{^\}]*)([\}]{1}[^\}]*)"


def f_get_page_content(html_file, css_file = ""):
	Handle = io.open(html_file, "r", encoding = "utf-8")
	page_content = Handle.read()
	Handle.close()
	style_pattern = ""
	replace_style_pattern = ""
	if css_file is not "":
		Handle = io.open(css_file, "r", encoding = "utf-8")
		style_content = Handle.read()
#		style_content = Handle.readlines()
		Handle.close()
#		style_content = "\t\t\n".join(style_content)
		if re.match(style_pattern, page_content):
			replace_style_pattern = "\\1\n{template_style_block}\n\t\\3"
			style_pattern = r"(\<style[^\>]*\>)([\s\n\t^\<]*)(\</style\>)"

		else:
			style_pattern = r"(\<title\>)([^\<]*)([\</title\>)"
			replace_style_pattern = "\\1\\2\\3\n<style type = \"text/css\">\n\t\{template_style_block}\n</style>\n"
		page_content = re.sub(style_pattern, replace_style_pattern, page_content)
		template_style_block = "template_style_block"
		style_template = [(template_style_block, style_content)]
	else:
		style_template = None
	return page_content, style_template

def f_apply_style_to_page(template_dict, style_template = None):
	if style_template is not None:
		template_dict.update(style_template)
	return template_dict

def f_get_template_list(data, pattern):
	regexp = re.compile(pattern)
	data_lines = data.splitlines()
	templates = list(map(lambda item: item[0][1], filter(None, map(regexp.findall, data_lines))))
	return templates

def f_make_template_dict(names, values):
	if len(values) < len(names):
		values += [ "" ]*(len(names) - len(values))
	dict_items = [ (name, values[i]) for i, name in enumerate(names) ]
	template_dict = dict(dict_items)
	return template_dict

def f_error_page(data, errors, values):
	if data == None:
		data = "\n{template_error_messages_block}\n"
	data_lines = data.splitlines()
	pos = data_lines.index("{template_error_messages_block}")
	data_lines = data_lines[:pos - 1] + errors
	error_page = "\n".join(data_lines)
	matches = re.findall(r"([\}]{0, 1}[^\}]*[^\{]*[\{]{1})([^\{^\}]*)", "".join(errors))
	errors_dict = dict(map(lambda item: (item[-1][-1], values[item[0]]), enumerate(matches)))
	error_page_content = error_page
#	error_page_content = error_page.format(error_dict)
	return error_page_content, errors_dict

def f_log(message):
	message = message.strip() + "\n"
	Handle = io.open(LogFile, "a+", encoding = "utf-8")
	Handle.write(message)
	Handle.close()

def f_debug_print(debug_data, description = None):
	debug_content_list = [ debug_header + "\n" ]
	if description == None:
		description = [ "\n" ] * len(debug_content_list)
	for index, data in enumerate(debug_data):
		debug_content_list.append(description[index])
		if type(data) is unicode or type(data) is str:
			debug_content_list.append(data)
		else:
			debug_content_list.append(pformat(data))
	for debug_message in debug_content_list:
		print debug_message

templates = None
template_dict = None
page_content = None
style_template = None
error_page_content = None
error_messages_block = []
error_messages = []
templates_values = []

img0_href = "../static/i_img_0.png"
img0_src = "../static/i_img_0.png"
img0_desc = "name: i_img_0; format: png"


img1_href = "../static/i_img_1.jpg"
img1_src = "../static/i_img_1.jpg"
img1_desc = "name: i_img_1; format: jpg"


img2_href = "../static/get_img_image.jpg"
img2_src = "../static/get_img_image.jpg"
img2_desc = "name: get_img_image1; format: jpg"


try:
	page_content, style_template = f_get_page_content(html_file = HtmlTemplateFile, css_file = CssTemplateFile)
except Exception as err:
	f_debug_print([err])
	error_messages.append(" ".join(["ERROR[f_get_page_content]:"] + list(err.args)))
	error_messages_block.append("<h1>{template_error_1}</h1>")


template_gallery_image = """\
	<div class = "image_div">
		<a target = "_blank" href = {0}>
			<img src = {1} width = "300" height = "200">
		</a>
		<div class = "image_desc_div">
			{2}
		</div>
	</div>
"""

for i in map(str, range(1, 10)):
	tmp_ = template_gallery_image
	tmp_ = tmp_.replace("{0}", "{template_img_href_" + i + "}")
	tmp_ = tmp_.replace("{1}", "{template_img_src_" + i + "}")
	tmp_ = tmp_.replace("{2}", "{template_img_desc_" + i + "}")
	page_content = re.sub(r"(\</body\>)", tmp_ + "\n\\1", page_content)


if error_messages_block:
	error_page_content, errors_dict = f_error_page(page_content, error_messages_block, error_messages)
	page_content = error_page_content
	template_dict = errors_dict
else:
	templates_values = [
		""
	]
	templates_img0 = [
		img0_href,
		img0_src,
		img0_desc
	]
	templates_img1 = [
		img1_href,
		img1_src,
		img1_desc
	]
	templates_img2 = [
		img2_href,
		img2_src,
		img2_desc
	]
	templates_values = [ "" ]
	templates_values += templates_img0 + templates_img1 + templates_img2
	templates_values += templates_img1 + templates_img0 + templates_img2
	templates_values += templates_img2 + templates_img1 + templates_img0
	templates_values += templates_img2
#	templates_values = [ "" ] + (templates_values*5)
	templates = f_get_template_list(page_content, template_pattern)
	templates.reverse()
	templates_values.reverse()
	template_dict = f_make_template_dict(templates, templates_values)
	template_dict = f_apply_style_to_page(template_dict, style_template)


if F_DEBUG:
	debug_description = [
		"page_content",
		"templates",
		"template_dict"
	]
	debug_data = [
		page_content,
		templates,
		template_dict
	]
	f_debug_print(debug_data, debug_description)



html_content = page_content.format(**template_dict)


print content_header
print
print html_content


