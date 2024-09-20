class Settings:
    auto_eng = True
    auto_precision = False
    auto_print_precision = True
    precision = 3  # Set -1 to turn off

class Value:
    # Known units with their equivalent deviation from the base
    units = {
        "T": 1e12,
        "G": 1e9,
        "M": 1e6,
        "k": 1e3,
        # "h": 1e2,
        # "da": 1e1,
        "BASE": 1e0,
        # "d": 1e-1,
        # "c": 1e-2,
        "m": 1e-3,
        "u": 1e-6,
        "n": 1e-9,
        "p": 1e-12
    }

    # When the unit data contains exactly one of these, do not try to parse the prefix
    __known_ignores = ["Hz"]

    def __init__(self, value_str: str, no_conversion: bool = False) -> None:
        if value_str.count(" ") == 1:
            try:
                # Convert value and store entirety of unit data
                value = float(value_str.split(" ")[0])
                unit_data = value_str.split(" ")[1]
                prefix = None
                base = None

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
                    self.std = Value(f"{value * self.units[prefix]} {base}", True)
                else:
                    # No prefix found, the prefix must already be standard
                    base = unit_data
                    self.prefix = None
                    self.std = self

                # Store class fields
                self.value = value
                self.base = base
                self.prefix_base = unit_data
                self.precision = Settings.precision
            except Exception:
                raise ValueError("Cannot convert value")
        else:
            try:
                # Attempt to set the value as just a float by itself, useful for mathematical operations
                self.value = float(value_str)
                self.prefix = None
                self.base = None
                self.prefix_base = None
                self.std = self
                self.precision = Settings.precision
            except ValueError:
                raise SyntaxError("Value string does not match expected format of 'n.n PrefixUnit'")

        # Convert to engineering notation if automatic conversion is enabled
        if Settings.auto_eng and not no_conversion:
            self.to_eng()

        if Settings.auto_precision and not no_conversion:
            self.set_precision(self.precision)

    def to_eng(self) -> None:
        if self.prefix is None:
            # There is no prefix, so assign the BASE prefix offset of 10^0 = 1
            unit_index = list(self.units.keys()).index("BASE")
        else:
            # There is a prefix, so assign the corresponding prefix offset
            unit_index = list(self.units.keys()).index(self.prefix)

        # While the value is not within engineering notation range
        while abs(self.value) < 1 or abs(self.value) >= 1000:
            old_index = unit_index

            if self.value < 1:
                unit_index += 1

                if unit_index is len(self.units):
                    raise ValueError("Value out of range! Cannot shift units past upper bound")
            else:
                unit_index -= 1

                if unit_index < 0:
                    raise ValueError("Value out of range! Cannot shift units past lower bound")

            # Try new offset
            shift = self.units[list(self.units.keys())[unit_index]] / self.units[list(self.units.keys())[old_index]]
            self.prefix = list(self.units.keys())[unit_index]
            self.value /= shift

            # Only include the base in prefix_base if it is defined
            if self.base is not None:
                self.prefix_base = f"{self.prefix}{self.base}"
            else:
                self.prefix_base = self.prefix

        # Reset the std property so that references to .std and calls for to_std() work as expected
        if self.base is not None and self.prefix is not None:
            # Has base and prefix, convert the prefix and value to std and leave base
            self.std = Value(f"{self.value * self.units[self.prefix]} {self.base}", True)
        elif self.base is None and self.prefix is not None:
            # Does not have base but has prefix, convert the prefix and value to std and do not include base
            self.std = Value(f"{self.value * self.units[self.prefix]}", True)
        else:
            # Does not have base and does not have prefix, leave as-is
            self.std = self

    def to_std(self) -> None:
        self.value = self.std.value
        self.base = self.std.base
        self.prefix = self.std.prefix
        self.prefix_base = self.std.prefix_base

    def convert_to(self, prefix: str) -> None:
        flag = False

        # Find the right unit and associate the prefix
        for unit_attempt in self.units:
            if unit_attempt in prefix and prefix.index(unit_attempt) == 0:
                flag = True
                prefix = unit_attempt
                break

        if not flag:
            raise ValueError("Invalid prefix")

        self.to_std()
        self.value /= self.units[prefix]
        self.prefix = prefix

        if self.base is not None:
            self.prefix_base = f"{self.prefix}{self.base}"
        else:
            self.prefix_base = self.prefix

    def set_precision(self, precision: int) -> None:
        self.precision = precision

    def set_base(self, base: str) -> None:
        self.base = base
        self.std.base = base

        if self.prefix is None:
            self.prefix_base = base
            self.std.prefix_base = base
        else:
            self.prefix_base = f"{self.prefix}{self.base}"
            self.std.prefix_base = f"{self.base}"

    def __str__(self) -> str:
        if Settings.auto_print_precision:
            return f"{round(self.value, self.precision)} {self.prefix_base if self.prefix_base is not None else ''}"
        else:
            return f"{self.value} {self.prefix_base if self.prefix_base is not None else ''}"
    
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

    def __gt__(self, val2):
        return Value(str(self.std.value > val2.std.value))

    def __ge__(self, val2):
        return Value(str(self.std.value >= val2.std.value))

    def __lt__(self, val2):
        return Value(str(self.std.value < val2.std.value))

    def __le__(self, val2):
        return Value(str(self.std.value <= val2.std.value))

    def __eq__(self, val2):
        return Value(str(self.std.value == val2.std.value))

    def __ne__(self, val2):
        return Value(str(self.std.value != val2.std.value))

class Phasor:
    def __init__(self, value: str) -> None:
        if " < " in value:
            try:
                magnitude = float(value.split(" < ")[0])
                angle = float(value.split(" < ")[1])

                if Settings.auto_precision:
                    magnitude = round(magnitude, Settings.precision)
                    angle = round(angle, Settings.precision)

                self.magnitude = magnitude
                self.angle = angle
                self.precision = Settings.precision
            except Exception:
                raise ValueError("Cannot convert value")
        else:
            raise SyntaxError("Value string does not match the expected format of 'nn < 00")

    def set_precision(self, precision: int) -> None:
        self.precision = precision

    def __str__(self) -> str:
        if Settings.auto_print_precision:
            return f"{round(self.magnitude, Settings.precision)} ∠ {round(self.angle, Settings.precision)}°"
        else:
            return f"{self.magnitude} ∠ {self.angle}°"

    def __mul__(self, val2):
        return Phasor(f"{self.magnitude * val2.magnitude} < {self.angle + val2.angle}")

    def __truediv__(self, val2):
        return Phasor(f"{self.magnitude / val2.magnitude} < {self.angle - val2.angle}")
