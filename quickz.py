class Value:
    # Known units with their equivalent deviation from the base
    units = {
        "T": 1e12,
        "G": 1e9,
        "M": 1e6,
        "k": 1e3,
        "h": 1e2,
        "da": 1e1,
        "BASE": 1e0,
        "d": 1e-1,
        "c": 1e-2,
        "m": 1e-3,
        "u": 1e-6,
        "n": 1e-9,
        "p": 1e-12
    }

    # When the unit data contains exactly one of these, do not try to parse the prefix
    __known_ignores = ["Hz"]

    def __init__(self, value_str: str, manual_unit: str = None) -> None:
        if value_str.count(" ") == 1:
            try:
                # Convert value and store entirety of unit data
                value = float(value_str.split(" ")[0])
                unit_data = value_str.split(" ")[1]
                prefix = ""
                base = ""

                flag = False

                # Find the right unit and associate the prefix
                if len(unit_data) > 1 and unit_data not in self.__known_ignores:  # Avoids wrongfully assuming that a value like "10 m" gets treated like "milli-None"
                    for unit_attempt in self.units:
                        if unit_attempt in unit_data and unit_data.index(unit_attempt) == 0:
                            flag = True
                            prefix = unit_attempt
                            break

                if flag:
                    # Prefix was found, store the adjusted value
                    base = unit_data.split(prefix)[1]
                    self.prefix = prefix
                    self.std = Value(f"{value * self.units[prefix]} {base}")
                else:
                    # No prefix found, the prefix must already be standard
                    self.prefix = None
                    self.std = self

                # Store class fields
                self.value = value
                self.base = base
                self.prefix_base = unit_data
            except Exception as e:
                raise ValueError(f"Cannot convert value: {e}")
        else:
            try:
                # Attempt to set the value as just a float by itself, useful for mathematical operations
                self.value = float(value_str)
                self.prefix = None
                self.base = None
                self.prefix_base = None
                self.std = self
            except ValueError:
                raise SyntaxError("Value string does not match expected format of 'n.n PrefixUnit'")
            
    def to_eng(self) -> None:
        if self.prefix is None:
            unit_index = list(self.units.keys()).index("BASE")
        else:
            unit_index = list(self.units.keys()).index(self.prefix)

        while self.value < 1 or self.value >= 1000:
            if self.value < 1:
                unit_index -= 1
            else:
                unit_index += 1

            # TODO: finish this later.
        
    def add_base(self, base: str) -> None:
        self.base = base

    def __str__(self) -> str:
        if self.prefix_base is not None:
            return f"{self.value} {self.prefix_base}"
        else:
            return str(self.value)
    
    def __float__(self) -> float:
        return self.std.value
    
    def __add__(self, val2):
        return Value(str(self.std.value + val2.std.value))
    
    def __sub__(self, val2):
        return Value(str(self.std.value - val2.std.value))
    
    def __mul__(self, val2):
        return Value(str(self.std.value * val2.std.value))
    
    def __truediv__(self, val2):
        return Value(str(self.std.value / val2.std.value))