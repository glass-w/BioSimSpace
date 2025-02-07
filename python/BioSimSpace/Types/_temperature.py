######################################################################
# BioSimSpace: Making biomolecular simulation a breeze!
#
# Copyright: 2017-2021
#
# Authors: Lester Hedges <lester.hedges@gmail.com>
#
# BioSimSpace is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# BioSimSpace is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BioSimSpace. If not, see <http://www.gnu.org/licenses/>.
#####################################################################

"""
A temperature type.
"""

__author__ = "Lester Hedges"
__email__ = "lester.hedges@gmail.com"

__all__ = ["Temperature"]

from Sire import Units as _SireUnits

from ._type import Type as _Type

class Temperature(_Type):
    """A temperature type."""

    # Dictionary of allowed units.
    _supported_units = { "KELVIN"     : _SireUnits.kelvin,
                         "CELSIUS"    : _SireUnits.celsius,
                         "FAHRENHEIT" : _SireUnits.fahrenheit }

    # Map unit abbreviations to the full name.
    _abbreviations = { "K" : "KELVIN",
                       "C" : "CELSIUS",
                       "F" : "FAHRENHEIT" }

    # Print formatting.
    _print_format = { "KELVIN"     : "K",
                      "CELSIUS"    : "C",
                      "FAHRENHEIT" : "F" }

    # Documentation strings.
    _doc_strings = { "KELVIN"     : "A temperature in Kelvin.",
                     "CELSIUS"    : "A temperature in Celsius.",
                     "FAHRENHEIT" : "A temperature in Fahrenheit." }

    # Null type unit for avoiding issue printing configargparse help.
    _null_unit = "KELVIN"

    def __init__(self, *args):
        """Constructor.

           ``*args`` can be a magnitude and unit, or a string representation
           of the temperature, e.g. "298 K".

           Parameters
           ----------

           magnitude : float
               The magnitude.

           unit : str
               The unit.

           string : str
               A string representation of the temperature.

           Examples
           --------

           Create an object representing a temperature of 298 Kelvin then
           print the temperature in Celsius.

           >>> import BioSimSpace as BSS
           >>> temperature = BSS.Types.Temperature(298, "K")
           >>> print(temperature.celsius())

           The same as above, except passing a string representation of the
           temperature to the constructor.

           >>> import BioSimSpace as BSS
           >>> time = BSS.Types.Temperature("298 K")
           >>> print(temperature.celsius())

           The string matching is extremeley flexible, so all of the following
           would be valid arguments: "298 K", "298 kelvin", "2.98e2 k".
        """

        # Call the base class constructor.
        super().__init__(*args)

        # Check that the temperature is above absolute zero.
        if self._kelvin() < 0:
            raise ValueError("The temperature cannot be less than absolute zero (0 Kelvin).")

    def __add__(self, other):
        """Addition operator."""

        from ..Units import allow_offset

        # Addition of another object of the same type.
        if type(other) is type(self):
            # The temperatures have the same unit.
            if self._unit == other._unit:
                if self._unit != "KELVIN":
                    if not allow_offset:
                        raise ValueError("Ambiguous operation with offset unit: '%s'" % self._unit)
                    else:
                        # Add the magnitudes in the original unit.
                        mag = self._magnitude + other._magnitude

                        # Return a new object of the same type with the original unit.
                        return Temperature(mag, self._unit)
                else:
                    return super().__add__(other)
            else:
                if not allow_offset:
                    raise ValueError("Ambiguous operation with offset unit: '%s'" % self._unit)
                else:
                    # Left-hand operand takes precedence.
                    mag = self._magnitude + other._convert_to(self._unit).magnitude()

                    # Return a new object of the same type with the original unit.
                    return Temperature(mag, self._unit)

        # Addition of a string.
        elif type(other) is str:
            temp = self._from_string(other)
            return self + temp

        else:
            raise TypeError("unsupported operand type(s) for +: '%s' and '%s'"
                % (self.__class__.__qualname__, other.__class__.__qualname__))

    def __sub__(self, other):
        """Subtraction operator."""

        from ..Units import allow_offset

        # Subtraction of another object of the same type.
        if type(other) is type(self):
            # The temperatures have the same unit.
            if self._unit == other._unit:
                if self._unit != "KELVIN":
                    if not allow_offset:
                        raise ValueError("Ambiguous operation with offset unit: '%s'" % self._unit)
                    else:
                        # Subtract the magnitudes in the original unit.
                        mag = self._magnitude - other._magnitude

                        # Return a new object of the same type with the original unit.
                        return Temperature(mag, self._unit)
                else:
                    return super().__sub__(other)
            else:
                if not allow_offset:
                    raise ValueError("Ambiguous operation with offset unit: '%s'" % self._unit)
                else:
                    # Left-hand operand takes precedence.
                    mag = self._magnitude - other._convert_to(self._unit).magnitude()

                    # Return a new object of the same type with the original unit.
                    return Temperature(mag, self._unit)

        # Addition of a string.
        elif type(other) is str:
            temp = self._from_string(other)
            return self - temp

        else:
            raise TypeError("unsupported operand type(s) for -: '%s' and '%s'"
                % (self.__class__.__qualname__, other.__class__.__qualname__))

    def __mul__(self, other):
        """Multiplication operator."""

        if self._unit != "KELVIN":
            from ..Units import allow_offset
            if not allow_offset:
                raise ValueError("Ambiguous operation with offset unit: '%s'" % self._unit)

            else:
                # Convert int to float.
                if type(other) is int:
                    other = float(other)

                # Only support multiplication by float.
                if type(other) is float:
                    # Multiply magnitude.
                    mag = self._magnitude * other

                    # Return a new object of the same type with the original unit.
                    return Temperature(mag, self._unit)

                else:
                    raise TypeError("unsupported operand type(s) for *: '%s' and '%s'"
                        % (self.__class__.__qualname__, other.__class__.__qualname__))

        else:
            return super().__mul__(other)

    def __rmul__(self, other):
        """Multiplication operator."""

        # Multipliation is commutative: a*b = b*a
        return self.__mul__(other)

    def __truediv__(self, other):
        """Division operator."""

        if self._unit != "KELVIN":
            from ..Units import allow_offset
            if not allow_offset:
                raise ValueError("Ambiguous operation with offset unit: '%s'" % self._unit)

            else:
                # Convert int to float.
                if type(other) is int:
                    other = float(other)

                # Float division.
                if type(other) is float:
                    # Divide magnitude.
                    mag = self._magnitude / other

                    # Return a new object of the same type with the original unit.
                    return Temperature(mag, self._unit)

                # Division by another object of the same type.
                elif type(other) is type(self):
                    return self._magnitude / other._convert_to(self._unit).magnitude()

                # Division by a string.
                elif type(other) is str:
                    obj = self._from_string(other)
                    return self / obj

                else:
                    raise TypeError("unsupported operand type(s) for /: '%s' and '%s'"
                        % (self.__class__.__qualname__, other.__class__.__qualname__))
        else:
            return super().__truediv__(other)

    def _kelvin(self):
        """Return the magnitude of the temperature in Kelvin."""
        return (self._magnitude * self._supported_units[self._unit]).value()

    def kelvin(self):
        """Return the temperature in Kelvin.

           Returns
           -------

           temperature : :class:`Temperature <BioSimSpace.Types.Temperature>`
               The temperature in Kelvin.
        """
        return Temperature((self._magnitude * self._supported_units[self._unit]).value(), "KELVIN")

    def celsius(self):
        """Return the temperature in Celsius.

           Returns
           -------

           temperature : :class:`Temperature <BioSimSpace.Types.Temperature>`
               The temperature in Celsius.
        """
        return Temperature((self._magnitude * self._supported_units[self._unit]).to(_SireUnits.celsius), "CELSIUS")

    def fahrenheit(self):
        """Return the temperature in Fahrenheit.

           Returns
           -------

           temperature : :class:`Temperature <BioSimSpace.Types.Temperature>`
               The temperature in Fahrenheit.
        """
        return Temperature((self._magnitude * self._supported_units[self._unit]).to(_SireUnits.fahrenheit), "FAHRENHEIT")

    def _default_unit(self, mag=None):
        """Internal method to return an object of the same type in the default unit.

           Parameters
           ----------

           mag : float
               The magnitude (optional).

           Returns
           -------

           temperature : :class:`Temperature <BioSimSpace.Types.Temperature>`
               The temperature in the default unit of Kelvin.
        """
        if mag is None:
            return self.kelvin()
        else:
            return Temperature(mag, "KELVIN")

    def _convert_to(self, unit):
        """Return the temperature in a different unit.

           Parameters
           ----------

           unit : str
               The unit to convert to.

           Returns
           -------

           temperature : :class:`Temperature <BioSimSpace.Types.Temperature>`
               The temperature in the specified unit.
        """
        if unit == "KELVIN":
            return self.kelvin()
        elif unit == "CELSIUS":
            return self.celsius()
        elif unit == "FAHRENHEIT":
            return self.fahrenheit()
        else:
            raise ValueError("Supported units are: '%s'" % list(self._supported_units.keys()))

    def _validate_unit(self, unit):
        """Validate that the unit are supported."""

        # Strip whitespace and convert to upper case.
        unit = unit.replace(" ", "").upper()

        # Strip all instances of "DEGREES", "DEGREE", "DEGS", & "DEG".
        unit = unit.replace("DEGREES", "")
        unit = unit.replace("DEGREE", "")
        unit = unit.replace("DEGS", "")
        unit = unit.replace("DEG", "")

        # Check that the unit is supported.
        if unit in self._supported_units:
            return unit
        elif unit in self._abbreviations:
            return self._abbreviations[unit]
        else:
            raise ValueError("Supported units are: '%s'" % list(self._supported_units.keys()))
