import sys
sys.path.append('.')
import code_trace
import line_coverage
import function_trace
from towerOfHanoi import towerOfHanoi

sys.settrace(code_trace.trace_code)
towerOfHanoi(5, 'A', 'B', 'C')
sys.settrace(None)

sys.settrace(line_coverage.line_coverage)
towerOfHanoi(5, 'A', 'B', 'C')
sys.settrace(None)
line_coverage.print_coverage()

sys.settrace(function_trace.record_calls)
towerOfHanoi(5, 'A', 'B', 'C')
sys.settrace(None)