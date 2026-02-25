import sys, importlib, inspect, os, traceback
print("cwd:", os.getcwd())
print("sys.path[0]:", sys.path[0])
print("top sys.path entries:", sys.path[:4])
try:
    m = importlib.import_module("Scripts.compute_metrics")
    print("Imported Scripts.compute_metrics ->", getattr(m, "__file__", "<no file>"))
except Exception:
    print("Import Scripts.compute_metrics failed:")
    traceback.print_exc()
try:
    m2 = importlib.import_module("scripts.compute_metrics")
    print("Imported scripts.compute_metrics ->", getattr(m2, "__file__", "<no file>"))
except Exception:
    print("Import scripts.compute_metrics failed:")
    traceback.print_exc()
print("\nExports (Scripts.compute_metrics):", [n for n in dir(m) if not n.startswith('_')] if 'm' in globals() else [])
