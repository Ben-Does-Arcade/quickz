import quickz
from quickz import *

Settings.auto_eng = True
Settings.auto_print_precision = True

# voltage = Value("500 mV")
# current = Value("134 uA")
#
# resistance = voltage / current
# resistance.add_base("Ω")
# print(resistance.base)
# print(resistance)

# v = Value("5.07 mV")
# a = Value("50 nA")
#
# print(v)
# print(a)
#
# r = v / a
# r.set_base("Ω")
# print(r)
#
# r.to_std()
# print(r)

p = Phasor("34 < 50")
q = Phasor("2 < 15")

print(p * q)
