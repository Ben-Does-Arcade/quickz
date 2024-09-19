import quickz
from quickz import Value, Settings

Settings.auto_print_precision = True

voltage = Value("500 mV")
current = Value("134 uA")

resistance = voltage / current
resistance.add_base("Ω")
print(resistance)
