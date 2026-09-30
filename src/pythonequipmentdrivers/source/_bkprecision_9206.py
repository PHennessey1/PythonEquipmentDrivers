from ..core import VisaResource


class BKPrecision_9206(VisaResource):
    """
    Programmers Manual
    https://www.tme.com/Document/c998692908083f3dde755c398b5b07de/BK9201.pdf
    """

    def set_state(self, state: bool) -> None:
        """
        set_state(state)

        Enables/disables the output of the supply.
        A delay of 1 second is required after changing the relay state before
        any program command is sent

        Args:
            state (bool): Supply state (True == enabled, False == disabled)

        """

        self.write_resource(f"OUTP {1 if state else 0}")

    def get_state(self) -> bool:
        """
        get_state()

        Retrives the current state of the output of the supply.

        Returns:
            bool: Supply state (True == enabled, False == disabled)
        """ 

        response = self.query_resource("OUTP?")
        return int(response) == 1

    def toggle(self) -> None:
        """
        toggle(return_state=False)

        Reverses the current state of the Supply's output
        """

        self.set_state(self.get_state() ^ True)

    def on(self) -> None:
        """
        on()

        Enables the relay for the power supply's output equivalent to
        set_state(True).
        """

        self.set_state(True)

    def off(self) -> None:
        """
        off()

        Disables the relay for the power supply's output equivalent to
        set_state(False).
        """

        self.set_state(False)


    def set_voltage(self, voltage: float) -> None:
        self.write_resource(f"VOLT {voltage}")

    def get_voltage(self) -> float:
        return float(self.query_resource("VOLT?"))

    def set_current(self, current: float) -> None:
        self.write_resource(f"CURR {current}")

    def get_current(self) -> float:
        return float(self.query_resource("CURR?"))

    def measure_voltage(self) -> float:
        """
        Measures the actual output voltage as if it was a DMM
        """
        return float(self.query_resource("MEAS:VOLT?"))
    
    def measure_current(self) -> float:
        """
        Measures the actual output current as if it was a DMM
        """
        return float(self.query_resource("MEAS:CURR?"))
    
    def measure_power(self) -> float:
        """
        Measures the actual output power as if it was a DMM
        """
        return float(self.query_resource("MEAS:POW?"))