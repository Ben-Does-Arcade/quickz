from quickz import Value

voltage = Value("5 V")
current = Value("134 uA")

resistance = voltage / current
resistance.add_base("Ω")
print(resistance)
