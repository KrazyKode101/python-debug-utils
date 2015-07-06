import re
import random

def test(s):
	if re.search("<SELECT[^>]*>",s) >= 0:
		return "fail"
	else:
		return "pass"

#print test("<SELECT>")

def simplify(s):
	assert test(s) == 'fail'
	
	split = len(s)/2
	s1 = s[:split]
	s2 = s[split:]

	assert s == s1 + s2

	if test(s1) == 'fail':
		return simplify(s1)

	if test(s2) == 'fail':
		return simplify(s2)

	return s

#html_input = '<SELECT><OPTION VALUE="simplify"><OPTION ="beautify"></SELECT>'
#print simplify(html_input)

def ddmin(s,test):
	assert test(s) == 'fail'

	n = 2
	while len(s)>=2:
		print '*********'+s
		#assert s != '<SELECT>'
		len_of_each_subset = len(s)/n
		
		removing_subset_start = 0
		subset_failed = False

		for i in range(0,n):			
			removing_subset_end = removing_subset_start + len_of_each_subset
			subset_string = s[:removing_subset_start]+s[removing_subset_end:]
			removing_subset_start += len_of_each_subset
			if test(subset_string) == 'fail':
				subset_failed = True
				s = subset_string
				break

		if subset_failed:
			n = max(n-1,2)
		else:
			n = 2*n
			if n > len(s):
				break

	return s

#html_input = '<SELECT><OPTION VALUE="simplify"><OPTION ="beautify"></SELECT>'
#print ddmin(html_input,test)

def fuzzer():
	str_len = int(random.random()*1024)
	out = ''
	for i in range(0,str_len):
		c = chr(int(random.randon()*96+32))
		out = out + c
	return out

def test_mystery():
	ip = fuzzer()
	while True:
		if mystery(ip) == 'FAIL':
			min_input = ddmin(ip,mystery)
			print min_input			
			break
		else:
			ip = fuzzer()

