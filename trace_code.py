import sys

def trace_code(frame,event,arg):
	if event == 'line':
		filename = frame.f_code.co_filename
		lineno = frame.f_lineno
		code = open(filename,'r').readlines()[lineno-1]
		open('trace_file.txt','a').write(filename+'\t'+str(lineno)+'\t'+code)
	return trace_code