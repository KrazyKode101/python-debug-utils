import sys

resume = True
mode = ''
log_file = None

def input_command():
	if mode == 'replay':
		global log_file
		if not log_file:
			log_file = open("log.txt",'r')
		command = log_file.readline()
	else:
		command = raw_input("(enter command) ")
		log_file = open("log.txt",'a')
		log_file.write(command+'\n')
	return command

def process(command):
	global resume
	print repr(command)
	if command.startswith('q'):
		resume = False

def main():
	args = sys.argv[1:]
	global mode
	mode = args[0]
	while resume:
		command = input_command()
		process(command)

if __name__ == '__main__':
	main()