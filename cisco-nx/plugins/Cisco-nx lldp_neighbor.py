"""
CLI Plugin for Cisco-style LLDP neighbors
Author: Shashi Sharma
Email: Shashi.Sharma@nokia.com
"""

from srlinux.mgmt.cli import CliPlugin
from srlinux.syntax import Syntax
from srlinux.location import build_path
from srlinux.data import Data, ColumnFormatter, Borders, Formatter
from srlinux.schema import FixedSchemaRoot
import sys
import logging

# Setup basic logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger("LLDPPlugin")

class Plugin(CliPlugin):
    def load(self, cli, **_kwargs):
        """Load the LLDP plugin and define the CLI command structure."""
        logger.debug("Loading LLDP plugin")
        lldp_cmd = cli.show_mode.add_command(Syntax('lldp', help='LLDP info'))
        lldp_cmd.add_command(
            Syntax('neighbor', help='Show LLDP neighbors Cisco-style'),
            callback=self._show_lldp_neighbor,
            schema=self._get_schema()
        )

    def _get_schema(self):
        """Define the schema for the LLDP neighbor data."""
        logger.debug("Setting up schema")
        root = FixedSchemaRoot()
        root.add_child('neighbors', key='Local_Intf', fields=['Device_ID', 'Hold_time', 'Capability', 'Port_ID'])
        return root

    def _show_lldp_neighbor(self, state, arguments, output, **_kwargs):
        """Handle the 'show lldp neighbor' command."""
        logger.debug("Running show lldp neighbor")
        lldp_data = self._get_lldp_data(state)
        if not lldp_data:
            sys.stdout.write("No LLDP neighbors found.\n")
            return

        result = Data(arguments.schema)
        self._set_formatters(result)
        self._populate_data(result, lldp_data, state)
        with output.stream_data(result):
            pass

    def _get_lldp_data(self, state):
        """Fetch LLDP neighbor data from the system."""
        path = build_path('/system/lldp/interface[name=*]/neighbor[id=*]')
        logger.debug(f"Grabbing LLDP data from: {path}")
        try:
            data = state.server_data_store.get_data(path, recursive=True)
            return data
        except Exception as e:
            logger.error(f"Couldn’t fetch LLDP data: {e}")
            return None

    def _get_hold_time(self, state):
        """Calculate the hold time, using defaults if configuration attributes are missing."""
        # Default values
        default_hello_timer = 3
        default_hold_multiplier = 40
        default_hold_time = default_hello_timer * default_hold_multiplier  # 120

        # Fetch LLDP configuration from /system/lldp
        config_path = build_path('/system/lldp')
        try:
            config = state.server_data_store.get_data(config_path, recursive=True)
            # Check if hello_timer and hold_multiplier exist
            if hasattr(config, 'hello_timer') and hasattr(config, 'hold_multiplier'):
                hello_timer = config.hello_timer
                hold_multiplier = config.hold_multiplier
                hold_time = hello_timer * hold_multiplier
                return str(hold_time)
            else:
                # use default hold time if attributes are missing
                return str(default_hold_time)
        except Exception:
            # use default hold time if fetching config fails
            return str(default_hold_time)

    def _populate_data(self, data_root, lldp_data, state):
        """Populate the LLDP neighbor data into the output structure."""
        logger.debug("Filling in neighbor data")
        hold_time = self._get_hold_time(state)  # Get dynamic hold_time
        interfaces = lldp_data.get_descendants('/system/lldp/interface')
        
        for iface in interfaces:
            local_intf = getattr(iface, 'name', 'Unknown')
            if not hasattr(iface, 'neighbor'):
                logger.debug(f"No neighbors on {local_intf}")
                continue

            for neighbor in iface.neighbor.items():
                device_id = getattr(neighbor, 'system_name', 'Unknown')
                capability = 'S'  # Default to Switch
                port_id = getattr(neighbor, 'port_id', 'Unknown')

                logger.debug(f"Adding {device_id} for {local_intf}")
                row = data_root.neighbors.create(local_intf)
                row.device_id = device_id
                row.hold_time = hold_time
                row.capability = capability
                row.port_id = port_id

    def _set_formatters(self, data):
        """Set up the table formatting for Cisco-style output."""
        logger.debug("Setting up table look")
        data.set_formatter('/neighbors', CiscoTableFormatter())
        data.set_formatter(
            '/neighbors',
            ColumnFormatter(
                widths={'Local_Intf': 18, 'Device_ID': 18, 'Hold_time': 12, 'Capability': 12, 'Port_ID': 18},
                borders=Borders.Nothing
            )
        )

class CiscoTableFormatter(Formatter):
    def iter_format(self, entry, max_width):
        """Format the LLDP neighbor data in a Cisco-style table."""
        yield "Capability codes: (R) Router, (B) Bridge, (W) WLAN AP, (S) Switch, (O) Other"
        yield ""
        yield "{:<18} {:<18} {:<12} {:<12} {:<18}".format("Device ID", "Local Intf", "Hold-time", "Capability", "Port ID")
        yield "-" * 78
        total = 0
        for row in entry.neighbors.values():
            yield "{:<18} {:<18} {:<12} {:<12} {:<18}".format(row.device_id, row.local_intf, row.hold_time, row.capability, row.port_id)
            total += 1
        yield ""
        yield f"Total entries: {total}"

if __name__ == '__main__':
    Plugin()