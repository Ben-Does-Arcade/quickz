import quickz
from quickz import Value, Settings

Settings.auto_eng = True
Settings.auto_print_precision = True

# voltage = Value("500 mV")
# current = Value("134 uA")
#
# resistance = voltage / current
# resistance.add_base("Ω")
# print(resistance.base)
# print(resistance)

v = Value("5.07 mV")
a = Value("50 A")

print(v)
print(a)

v.to_std()
v.set_precision(5)
print(v)

v.convert_to("kA")
print(v)

v.convert_to("uA")
v.set_precision(10)
print(v)

v.to_eng()
print(v)