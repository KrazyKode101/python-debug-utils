import sys

from permutations_of_a_string import get_perms
from remove_tags import remove_tags

from debug_utils import debugger as d
from debug_utils import trace_code as t
from debug_utils import record_calls as r

'''
sys.settrace(r.record_calls)
ret = get_perms('abcd')
print len(ret), repr(ret)
sys.settrace(None)
r.print_calls()
'''

sys.settrace(d.traceit)
print remove_tags("<br len='hi'>hello</br>")
sys.settrace(None)
