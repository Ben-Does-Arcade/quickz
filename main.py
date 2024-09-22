from quickz import *

Settings.auto_eng = True
Settings.auto_print_precision = True

a = Value("3 A")
b = Phasor("5 < -30")

print(f"a / b: {a / b}")
print(f"b / a: {b / a}")
print(f"a * b: {a * b}")
print(f"b * a: {b * a}")
print(f"a + b: {a + b}")
print(f"b + a: {b + a}")

