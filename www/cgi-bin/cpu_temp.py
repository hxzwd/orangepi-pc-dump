#!/usr/bin/env python
# -*- coding: utf-8 -*-

F_DEBUG = False


import os
import io
import re
import sys

from pprint import pformat
from datetime import datetime

CpuThermalSysFile = "//sys//class//thermal//thermal_zone0//temp"
HtmlTemplateFile = "//home//hjk//www//html//cpu_temp.template.html"
CssTemplateFile = "//home//hjk//www//css//cpu_temp.template.css"
LogFile = "//home//hjk//www//log//cpu_temp.log"

content_header = "Content-type: text/html"
debug_header = "Content-type: text"

template_pattern = r"([^\{]*[\{]{1})([^\{^\}]*)([\}]{1}[^\}]*)"

def f_get_cpu_temp():
	Handle = io.open(CpuThermalSysFile, "r")
	cpu_thermal = float(Handle.read().strip())/1000.0
	Handle.close()
	return cpu_thermal

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
header0_text = "CPU TEMPERATURE"
header1_text = "[ " + str(datetime.now()).split(".")[0] + " ]"
cpu_thermal = None
error_messages_block = []
error_messages = []
templates_values = []


try:
	page_content, style_template = f_get_page_content(html_file = HtmlTemplateFile, css_file = CssTemplateFile)
except Exception as err:
	f_debug_print([err])
	error_messages.append(" ".join(["ERROR[f_get_page_content]:"] + list(err.args)))
	error_messages_block.append("<h1>{template_error_1}</h1>")



try:
	cpu_thermal = f_get_cpu_temp()
except Exception as err:
	error_messages.append(" ".join(["ERROR[f_get_cpu_temp]:"] + list(err.args)))
	error_messages_block.append("<h1>{template_error_2}</h1>")

if error_messages_block:
	error_page_content, errors_dict = f_error_page(page_content, error_messages_block, error_messages)
	page_content = error_page_content
	template_dict = errors_dict
else:
	templates_values = [
		"",
		header0_text,
		header1_text,
		cpu_thermal
	]
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


