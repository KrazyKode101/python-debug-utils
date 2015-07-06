import sys

first_time = True
stepping = False
breakpoints = { }
watchpoints = { }
event_type_string = { 'step' : "step mode", 'break' : 'break point arrived', 'watch':"watch point has found a change" , 'first_time':"first time"}

def get_command():
	command = raw_input("(my-spider): ")
	return command

def print_help():
	print "p - to print info"
	print "s - to step through current function frame"
	print "c - to continue to next breakpoint/watchpoint"
	print "b [line no] - to set breakpoint"
	print "w [variable name] - to set watchpoint for a variable in current frame"
	print "d [b/w] [line no/var name] - to delete breakpoint or watchpoint"
	print "q - to quit debugger"

def add_to_watchlist(var,frame):
	global watchpoints
	f_locals = frame.f_locals
	filename = frame.f_code.co_filename
	func_name = frame.f_code.co_name
	f_code = filename+':'+func_name

	if f_code not in watchpoints:
		watchpoints[f_code] = {}
	
	if var not in watchpoints[f_code]:
		watchpoints[f_code][var] = f_locals[var]
	
	print "watch points in current frame"
	print watchpoints[f_code]

def has_changed_watchpoints(frame):
	global watchpoints
	f_locals = frame.f_locals
	filename = frame.f_code.co_filename
	func_name = frame.f_code.co_name
	f_code = filename+':'+func_name	

	if watchpoints.has_key(f_code):
		for var in f_locals:
			if var in watchpoints[f_code] and f_locals[var]!=watchpoints[f_code][var]:
				return True

	return False

def print_changed_watchpoints(frame):
	global watchpoints
	f_locals = frame.f_locals
	filename = frame.f_code.co_filename
	func_name = frame.f_code.co_name
	f_code = filename+':'+func_name

	if watchpoints.has_key(f_code):
		for var in f_locals:
			if var in watchpoints[f_code] and f_locals[var]!=watchpoints[f_code][var]:
				print "variable "+var+" has been changed from \n"
				print watchpoints[f_code][var]
				print " to "
				print f_locals[var]
				print "\n"

				watchpoints[f_code][var] = f_locals[var]

def remove_from_watchlist(var,frame):
	global watchpoints
	f_locals = frame.f_locals
	filename = frame.f_code.co_filename
	func_name = frame.f_code.co_name
	f_code = filename+':'+func_name

	if f_code not in watchpoints or var not in watchpoints[f_code]:
		print "enter correct var name"
		return

	temp = watchpoints[f_code]
	del temp[var]	
	if not temp:
		del watchpoints[f_code]

def add_to_breakpoints(no,frame):
	global breakpoints
	filename = frame.f_code.co_filename
	func_name = frame.f_code.co_name
	f_code = filename+':'+func_name	
	
	if f_code not in breakpoints:
		breakpoints[f_code] = []
	
	if no not in breakpoints[f_code]:
		breakpoints[f_code].append(no)
	
	print "break points in current frame"
	print breakpoints[f_code]

def remove_from_breakpoints(no,frame):
	global breakpoints
	filename = frame.f_code.co_filename
	func_name = frame.f_code.co_name
	f_code = filename+':'+func_name	
	
	if f_code not in breakpoints or no not in breakpoints[f_code]:
		print "improper line no"
		return

	temp = breakpoints[f_code]
	del temp[no]
	if not temp:
		del breakpoints[f_code]

def has_breakpoint_reached(frame):
	global breakpoints
	filename = frame.f_code.co_filename
	func_name = frame.f_code.co_name
	f_code = filename+':'+func_name	

	if f_code in breakpoints and frame.f_lineno in breakpoints[f_code]:
		return True
	else:
		return False

def debug(command,arg,frame):
	locals = frame.f_locals
	global stepping
	global breakpoints

	if not command:
		return True

	#seperate command and arguments
	if command.find(' ') > 0:
		cmd = command.split(' ')[0]
		args = command.split(' ')[1:]
	else:
		cmd = command
		args = None

	#handle each option seperately
	if cmd == 'h' or cmd == 'help':
		print_help()

	elif cmd == 's' or cmd == 'step':
		stepping = True
		return True

	elif cmd == 'c' or cmd == 'continue':
		stepping = False
		return True

	elif cmd == 'p' or cmd == 'print':
		if not arg:
			print "********locals********"
			print locals
			print "\n"
			print "********breakpoints********"
			print breakpoints
			print "\n"
			print '********watchpoints********'
			print watchpoints
			print "\n"
			return False	
		else:
			for e in args:
				print e+locals[e]
		return False

	elif cmd == 'b' or cmd == 'break':
		if not args:
			print "please enter break point line no"
			return False
		else:
			add_to_breakpoints(int(args[0]),frame)
		return False

	elif cmd == 'd' or cmd == 'remove':
		if not args or (args[0] != 'b' and args[0] != 'w'):	
			print "please enter 'b no' or 'w var'"
			return False

		if args[0] == 'b':
			if len(args) < 2:
				print "please enter break point no"
				return			
			remove_from_breakpoints(int(args[1]), frame)
		else:
			if len(args) < 2:
				print "please enter watch point var name"
				return
			remove_from_watchlist(args[1],frame)

		return False

	elif cmd == 'w' or cmd == 'watch':
		if not args or args[0] not in locals:
			print "please enter proper watch point variable name"
			return False
		else:
			add_to_watchlist(args[0],frame)
			return False

	elif cmd == 'q' or cmd == 'quit':
		sys.exit(0)

	else:
		print "no such command",repr(command)		

def traceit(frame,event,arg):

	global first_time
	global stepping
	global breakpoints
	
	if event == 'line':
		process_event = False
		event_type = ''

		if first_time:
			process_event = True
			first_time = False
			event_type = 'first_time'
		if stepping:
			process_event = True
			event_type = 'step'
		if has_breakpoint_reached(frame):
			process_event = True
			event_type = 'break'
		if has_changed_watchpoints(frame):
			process_event = True
			event_type = 'watch'

		if process_event == True:
			print "line no: "+str(frame.f_lineno)+" "+event_type_string[event_type]+"\n"

			if event_type == 'watch':
				print_changed_watchpoints(frame)

			resume = False
			while not resume:				
				command = get_command()
				resume = debug(command,arg,frame)

	return traceit
