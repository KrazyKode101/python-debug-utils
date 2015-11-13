import sys
import ntpath

calls = {}
op_file = None

def print_leaf(path):
	head,tail = ntpath.split(path)
	return tail or ntpath.basename(head)

def record_calls(frame,event,arg):
	func_name = frame.f_code.co_name
	file_name = frame.f_code.co_filename
	if event == 'call':
		args = frame.f_locals
		add_function_call(file_name,func_name,args)
	elif event == 'return':
		add_return_value(func_name,arg)
	return record_calls

def add_function_call(file_name,func_name,args):
	if func_name not in calls:
		calls[func_name] = { 'module_name':'','stack_call':[], 'stack_no':-1 }
	value = {'args':pretty_locals(args), 'ret':'' }		
	calls[func_name]['stack_call'].append(value)
	calls[func_name]['stack_no'] += 1
	calls[func_name]['module_name'] = file_name

def add_return_value(func_name,ret):
	index = calls[func_name]['stack_no']
	calls[func_name]['stack_call'][index]['ret'] = ret
	print_calls(func_name,index)

def pretty_locals(args):
	ret = ''
	for (name,value) in args.items():
		if ret != '':
			ret += ','
		ret = ret + str(name) + '=' + "'" + str(value) + "'"
	return ret

def print_calls(func_name,index):
	global op_file
	if not op_file:
		op_file = open('print_calls.txt','w')
	temp = calls[func_name]
	stack_f = temp["stack_call"][index]
	module_name = print_leaf(temp['module_name'])	
	res = module_name + ':' + func_name + ':' + stack_f['args'] + ':' + str(stack_f['ret'])
	op_file.write(res + '\n')
