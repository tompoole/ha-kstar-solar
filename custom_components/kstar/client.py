"""The KStar Client."""

import socket

class KStarClient:
    """Client to extract data from Inverter."""

    _BUFFER_SIZE = 1024
    _PORT = 8899
    _REQUEST_MESSAGE = bytes.fromhex("aa55b07f0106000235")

    def __init__(self, host) -> None:
        """Create a new KStarClient."""
        self._host = host
        self._server_address_port = (host, self._PORT)

    def get_latest_data(self):
        """Fetch latest data from inverter."""

        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        sock.settimeout(10)
        sock.sendto(self._REQUEST_MESSAGE, self._server_address_port)

        msg = sock.recvfrom(self._BUFFER_SIZE)

        hex_data = msg[0].hex("-").split("-")

        return {
            "grid": self._get_grid_data(hex_data),
            "battery": self._get_battery_data(hex_data),
            "pv": self._get_pv_data(hex_data),
            "load": self._get_load_data(hex_data),
            "stats": self._get_stats_data(hex_data),
        }

    def _get_grid_data(self, hex_data: list[str]):
        return {
            "voltage": int(hex_data[41] + hex_data[42], base=16) / 10,
            "current": int(hex_data[43] + hex_data[44], base=16) / 10,
            "power": int(hex_data[45] + hex_data[46], base=16) / 1000,
            "frequency": int(hex_data[47] + hex_data[48], base=16) / 100,
            "mode": int(hex_data[87], base=16),
        }

    def _get_battery_data(self, hex_data: list[str]):
        return {
            "voltage": int(hex_data[17] + hex_data[18], base=16) / 10,
            "current": int(hex_data[25] + hex_data[26], base=16) / 10,
            "charge": int(hex_data[33], base=16),
            "mode": int(hex_data[37], base=16),
        }

    def _get_pv_data(self, hex_data: list[str]):
        data = {
            "pv1_voltage": int(hex_data[7] + hex_data[8], base=16) / 10,
            "pv1_current": int(hex_data[9] + hex_data[10], base=16) / 10,
            "pv2_voltage": int(hex_data[12] + hex_data[13], base=16) / 10,
            "pv2_current": int(hex_data[14] + hex_data[15], base=16) / 10,
        }

        data["power"] = (data["pv1_current"] * data["pv1_voltage"]) + (
            data["pv2_current"] * data["pv2_voltage"]
        )

        return data

    def _get_load_data(self, hex_data: list[str]):
        return {
            "voltage": int(hex_data[50] + hex_data[51], base=16) / 10,
            "current": int(hex_data[52] + hex_data[53], base=16) / 10,
            "power": int(hex_data[54] + hex_data[55], base=16) / 1000,
            "frequency": int(hex_data[56] + hex_data[57], base=16) / 100,
        }

    def _get_stats_data(self, hex_data: list[str]):
        return {
            "temperature": int(hex_data[60] + hex_data[61], base=16) / 10,
            "energy_total": int(
                hex_data[66] + hex_data[67] + hex_data[68] + hex_data[69], base=16
            )
            / 10,
            "energy_today": int(hex_data[74] + hex_data[75], base=16) / 10,
            "lifetime_hours": int(
                hex_data[70] + hex_data[71] + hex_data[72] + hex_data[73], base=16
            ),
        }
