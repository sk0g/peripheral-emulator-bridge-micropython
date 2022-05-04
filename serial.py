import re

uart_selected = 1
uart_baud_rate = 115200
uart_bits = 8
uart_parity_bits = None
uart_stop_bits = 1
uart_timeout = 2000

value_update = re.compile(r'(\d\d)\|(\d)')
set_port_input = re.compile(r'PI\|(\d\d)')
set_port_output = re.compile(r'PO\|(\d\d)')
