import quickz
from quickz import Value, Settings

Settings.auto_eng = False
Settings.auto_print_precision = True

# voltage = Value("500 mV")
# current = Value("134 uA")
#
# resistance = voltage / current
# resistance.add_base("Ω")
# print(resistance.base)
# print(resistance)

v = Value("5.07 mV")
print(v)
v_std = v.std
v_std.set_precision(6)
print(v_std)
