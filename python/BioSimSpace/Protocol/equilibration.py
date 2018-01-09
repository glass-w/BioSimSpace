"""
@package biosimspace
@author  Lester Hedges
@brief   A class for storing equilibration protocols.
"""

from .protocol import Protocol, ProtocolType

from warnings import warn

class Equilibration(Protocol):
    """A class for storing equilibration protocols."""

    def __init__(self, runtime=200, temperature_start=300, temperature_end=None, restrain_backbone=False):
        """Constructor.

           Keyword arguments:

           runtime           -- The running time (in picoseconds).
           temperature_start -- The starting temperature (in Kelvin).
           temperature_end   -- The final temperature (in Kelvin).
           restrain_backbone -- Whether the atoms in the backbone are fixed.
        """

        # Call the base class constructor.
        super().__init__(ProtocolType.EQUILIBRATION)

        # Set the start temeperature.
        self._temperature_start = temperature_start

        # Set the final temperature.
        if not temperature_end is None:
            self._temperature_end = temperature_end

            # Start and end temperature is the same.
            if (self._temperature_start == self._temperature_end):
                warn("Start and end temperatures are the same!")
                self._is_const_temp = True

        # Constant temperature simulation.
        else:
            self._is_const_temp = True

    @property
    def runtime(self):
        """Return the running time."""
        return self._runtime

    @runtime.setter
    def runtime(self, runtime):
        """Set the running time."""

        if runtime <= 0:
            warn("The running time must be positive. Using default (200 ps).")
            self._runtime = 200

        else:
            self._runtime = runtime

    @property
    def temperature_start(self):
        """Return the starting temperature."""
        return self._temperature_start

    @temperature_start.setter
    def temperature_start(self, temperature):
        """Set the starting temperature."""

        if temperature <= 0:
            warn("Starting temperature must be positive. Using default (300 K).")
            self._temperature_start = 300

        else:
            self._temperature_start = temperature

    @property
    def temperature_end(self):
        """Return the final temperature."""
        return self._temperature_end

    @temperature_end.setter
    def temperature_end(self, temperature):
        """Set the final temperature."""

        if temperature <= 0:
            warn("Final temperature must be positive. Using default (300 K).")
            self._temperature_end = 300

        else:
            self._temperature_end = temperature

    def type(self):
        """Return the protocol type."""
        return self._type