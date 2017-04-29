import sys
import os

op_file = None

def record_calls(frame,event,arg):
	func_name = frame.f_code.co_name
	file_name = frame.f_code.co_filename

	if event == 'call':
		args = frame.f_locals
		add_function_call(file_name,func_name,args)
	elif event == 'return':
		add_return_call(file_name,func_name,arg)

	return record_calls

def add_function_call(file_name,func_name,args):
	global op_file
	if not op_file:
		op_file = open('function_trace.txt','w')
	
	res = file_name + ':' + 'call :' + func_name + ':' + pretty_locals(args)
	op_file.write(res + '\n')

def pretty_locals(args):
	ret = ''
	for (name,value) in args.items():
		if ret != '':
			ret += ','
		ret = ret + str(name) + '=' + "'" + str(value) + "'"
	return ret

def add_return_call(file_name,func_name,ret_val):
	res = file_name + ':' + 'return :' + func_name
	if ret_val:
		res += ':' + ret_val
	else:
		res += ': None'
	op_file.write(res + '\n')
