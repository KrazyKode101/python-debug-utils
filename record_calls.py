import sys
from permutations_of_a_string import get_perms

calls = []

def record_calls(frame,event,arg):
	if event == 'call':
		pretty_call(frame,frame.f_locals)
	return record_calls
		
def pretty_call(frame,arg):
	func_name = frame.f_code.co_name
	calls.append(func_name+'('+pretty_locals(arg)+')')

def pretty_locals(arg):
	ret = ''
	for name,value in arg.iteritems():
		if ret != '':
			ret += ','
		ret = ret + name + '=' + "'" + value + "'"
	return ret

def print_calls():
	for call in calls:
		ret = eval(call)
		temp = call + "=" + repr(ret)
		open('print_calls.txt','a').write(temp + '\n')
