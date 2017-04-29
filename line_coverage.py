import sys

coverage = {}

def line_coverage(frame,event,arg):
	if event == 'line':
		global coverage
		filename = frame.f_code.co_filename
		lineno = frame.f_lineno

		if filename not in coverage:
			coverage[filename] = set()

		coverage[filename].add(lineno)

	return line_coverage

def print_coverage():
	output = open('line_coverage.txt','w')
	for filename in coverage.keys():
		lines = open(filename,'r').readlines()
		count = 1
		for line in lines:
			if count in coverage[filename]:
				output.write('*'+line)
			else:
				output.write('  '+line)
			count += 1
