#!/usr/bin/env python
#
# thermometer.py: Driver for a one-off thermometer device
#
# @ 2026 Dan Douglas (dougl215@slac.stanford.edu)
#
# This file is a part of the InstrumentKit project.
# Licensed under the AGPL version 3.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
Driver for Dan's Special Thermometer

Originally contributed and copyright held by Dan Douglas
(dougl215@slac.stanford.edu)

An unrestricted license has been provided to the maintainers of the Instrument
Kit project.
"""

# IMPORTS #####################################################################
import time
from enum import Enum

from instruments.generic_scpi import SCPIMultimeter
from instruments.units import ureg as u

# CLASSES #####################################################################

class Thermometer(SCPIMultimeter):
    """
    """

    def __init__(self, filelike):
        """
        Initialize the instrument, and set the properties needed for communication.
        """
        super().__init__(filelike)
        self.timeout = 3 * u.second
        self.terminator = "\n"
        # self.terminator = "\r"
        # self.positions = {}
        # self.connect()
    
    # ENUMS ##

    class Mode(Enum):
        """
        Enum of valid measurement modes for this SCPI device
        """

        temperature_probe_0 = "TEMP0"
        temperature_probe_1 = "TEMP1"
        temperature_probe_2 = "TEMP2"
        temperature_probe_3 = "TEMP3"

    # METHODS ##

    def measure(self, mode=None):
        """
        Instruct the multimeter to perform a one time measurement. The
        instrument will use default parameters for the requested measurement.
        The measurement will immediately take place, and the results are
        directly sent to the instrument's output buffer.

        Method returns a Python quantity consisting of a numpy array with the
        instrument value and appropriate units. If no appropriate units exist,
        (for example, continuity), then return type is `float`.

        :param mode: Desired measurement mode. If set to `None`, will default
            to the current mode.
        :type mode: `~Thermometer.Mode`
        """
        if mode is None:
            mode = self.mode
        if not isinstance(mode, Thermometer.Mode):
            raise TypeError(
                "Mode must be specified as a Thermometer.Mode "
                "value, got {} instead.".format(type(mode))
            )
        # pylint: disable=no-member
        value = float(self.query(f"MEAS:{mode.value}?"))
        return u.Quantity(value, UNITS[mode])


# UNITS #############################################################

UNITS = {
    Thermometer.Mode.temperature_probe_0: u.celsius,
    Thermometer.Mode.temperature_probe_1: u.celsius,
    Thermometer.Mode.temperature_probe_2: u.celsius,
    Thermometer.Mode.temperature_probe_3: u.celsius,
}
