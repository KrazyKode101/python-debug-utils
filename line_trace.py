import sys

coverage = {}

def trace_code(frame,event,arg):
	if event == 'line':
		global coverage
		filename = frame.f_code.co_filename
		lineno = frame.f_lineno

		if filename not in coverage:
			coverage[filename] = set()

		coverage[filename].add(lineno)

	return trace_code

def print_coverage():
	output = open('line_trace.txt','w')
	for filename in coverage.keys():
		lines = open(filename,'r').readlines()
		count = 1
		for line in lines:
			if count in coverage[filename]:
				output.write('*'+line)
			else:
				output.write('  '+line)
			count += 1
