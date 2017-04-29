import sys
sys.path.append('.')
import code_coverage
import line_trace
import function_trace
from towerOfHanoi import towerOfHanoi

sys.settrace(code_coverage.trace_code)
towerOfHanoi(5, 'A', 'B', 'C')
sys.settrace(None)

sys.settrace(line_trace.trace_code)
towerOfHanoi(5, 'A', 'B', 'C')
sys.settrace(None)
line_trace.print_coverage()

sys.settrace(function_trace.record_calls)
towerOfHanoi(5, 'A', 'B', 'C')
sys.settrace(None)