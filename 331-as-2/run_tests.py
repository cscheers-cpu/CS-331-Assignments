"""
Run the decipherMessage test cases against your a2p3.py.

Usage (from the folder that contains a2p3.py):
    python run_tests.py                 # reads tests.txt
    python run_tests.py my_cases.txt    # or give the test file name
    python run_tests.py tests.txt -v    # also print the details of passing tests

Test file format (what you were given): lines such as
    {'args': [[3, 2, 1], 'P 1MT3CU3'], 'result': 'CMPUT 331'}
Any other lines (file name, function name, blank lines) are ignored.
"""
import ast
import os
import sys
import time
import traceback

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from a2p3 import decipherMessage
except Exception:
    print("Could not import decipherMessage from a2p3.py. Run this script from the")
    print("folder that contains a2p3.py. The error was:\n")
    traceback.print_exc()
    sys.exit(2)


def load_cases(path):
    cases = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                case = ast.literal_eval(line)
            except (ValueError, SyntaxError):
                print(f"warning: line {lineno} could not be parsed, skipped")
                continue
            if isinstance(case, dict) and "args" in case and "result" in case:
                cases.append((lineno, case["args"], case["result"]))
    return cases


def short(s, limit=70):
    r = repr(s)
    return r if len(r) <= limit else r[: limit - 3] + "..."


def first_difference(got, want):
    for i, (a, b) in enumerate(zip(got, want)):
        if a != b:
            return i
    return min(len(got), len(want))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    verbose = "-v" in sys.argv[1:]
    path = args[0] if args else "tests.txt"
    if not os.path.exists(path):
        print(f"Test file '{path}' not found. Save the test cases next to this script")
        print("as tests.txt, or pass the file name: python run_tests.py <file>")
        return 2

    cases = load_cases(path)
    passed = 0
    failed_ids = []

    for n, (lineno, call_args, want) in enumerate(cases, 1):
        # pass copies so a function that modifies its arguments cannot affect other checks
        copied = [list(a) if isinstance(a, list) else a for a in call_args]
        start = time.perf_counter()
        try:
            got = decipherMessage(*copied)
            error = None
        except Exception:
            got, error = None, traceback.format_exc(limit=3)
        elapsed = time.perf_counter() - start

        ok = error is None and got == want
        label = f"Test {n:2d} (file line {lineno})"
        if ok:
            passed += 1
            print(f"PASS  {label}  [{elapsed:.3f}s]")
            if verbose:
                print(f"        key length {len(call_args[0])}, message length {len(call_args[1])}")
        else:
            failed_ids.append(n)
            print(f"FAIL  {label}  [{elapsed:.3f}s]")
            print(f"        key      : {short(call_args[0])}")
            print(f"        message  : {short(call_args[1])}")
            print(f"        expected : {short(want)}")
            if error:
                print("        raised an exception:")
                for l in error.rstrip().splitlines():
                    print("          " + l)
            else:
                print(f"        got      : {short(got)}")
                if not isinstance(got, str):
                    print(f"        note: returned {type(got).__name__}, expected str")
                else:
                    i = first_difference(got, want)
                    print(f"        first difference at index {i} "
                          f"(got length {len(got)}, expected length {len(want)})")

    print("\n" + "=" * 50)
    print(f"{passed} of {len(cases)} tests passed")
    if failed_ids:
        print("Failed tests:", ", ".join(map(str, failed_ids)))
    return 0 if not failed_ids else 1


if __name__ == "__main__":
    sys.exit(main())
