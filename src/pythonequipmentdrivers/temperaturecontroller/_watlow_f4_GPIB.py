from typing import Union
from pythonequipmentdrivers.core import VisaResource 

class WatlowF4(VisaResource): 
    """
    Python driver for the SPX Tenney TUJR Temperature Chamber
    equipped with a Watlow F4 Controller and Tidal Engineering GPIB interface.
    """
    
    def __init__(self, address: str, **kwargs) -> None:
        """
        Initialize the connection to the temperature chamber.
        
        Args:
            address (str): The GPIB address (e.g., 'GPIB0::30::INSTR')
            **kwargs: Additional arguments passed up to the VisaResource
        """
        # Inject the required TE1643 connection settings into kwargs 
        # before passing them to the parent class
        kwargs.setdefault('write_termination', '\r\n')
        kwargs.setdefault('read_termination', None)
        kwargs.setdefault('timeout', 5)
        
        super().__init__(address, **kwargs)
        
        # Clear the hardware buffer
        #self.clear()

    def _query_float(self, command: str) -> float:
        """
        Helper to send a query and parse the return as a float.
        """

        response = self.query_resource(command).strip()
        
        clean_response = response.replace(command.replace('?', '').strip(), '').strip()
        try:
            return float(clean_response)
        except ValueError:
            raise ValueError(f"Could not parse float from chamber response: '{response}'")

    @property
    def temperature(self) -> float:
        """
        Read the current actual temperature of the chamber (Register 100).
        """
        raw_val = self._query_float("R? 100, 1")
        return raw_val / 10.0

    @property
    def setpoint(self) -> float:
        """
        Get the current temperature setpoint of the chamber (Register 300).
        """
        raw_val = self._query_float("R? 300, 1")
        return raw_val / 10.0

    @setpoint.setter
    def setpoint(self, value: Union[float, int]) -> None:
        """
        Set the target temperature setpoint using the Write (W) command.
        """
        register_value = int(float(value) * 10)
        
        self.write_resource(f"W 300, {register_value}")

    @property
    def output_state(self) -> bool:
        mode = self._query_float("R? 274, 1")

        return mode == 2.0
    
    @output_state.setter
    def output_state(self, state:bool) -> None:
        mode_val = 2 if state else 4

        self.write_resource(f"W 274, {mode_val}")

    def get_id(self) -> str:
        """
        Retrieve the identification string from the GPIB interface.
        """
        return self.query_resource("*IDN?")
