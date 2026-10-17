"""Run the real Python suite; expose failure tracebacks in GitHub annotations."""
from pathlib import Path
import sys
import unittest

root = Path(__file__).resolve().parents[1]
suite = unittest.defaultTestLoader.discover(str(root / 'tests'), pattern='test_*.py')
result = unittest.TextTestRunner(verbosity=2).run(suite)
for test, trace in result.errors + result.failures:
    message = (str(test) + '\n' + trace).replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
    print('::error::' + message, flush=True)
if result.testsRun == 0:
    print('::error::No tests executed', flush=True)
raise SystemExit(0 if result.wasSuccessful() and result.testsRun else 1)
