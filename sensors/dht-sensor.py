"""
sensors/dht_sensor.py
Reads temperature (°C) and relative humidity (%) from a DHT22 sensor
using the adafruit_dht library.

Retries up to MAX_RETRIES times to handle the occasional checksum error
that is normal for DHT sensors.
"""

import logging
import time
import adafruit_dht

log = logging.getLogger(__name__)

MAX_RETRIES   = 5
RETRY_DELAY_S = 2


def read_dht(device: adafruit_dht.DHT22) -> tuple[float | None, float | None]:
    """
    Read temperature and humidity from an already-initialised DHT22 device.

    Args:
        device: An adafruit_dht.DHT22 (or DHT11) instance.

    Returns:
        (temperature_c, humidity_pct) — either value may be None on failure.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            temp = device.temperature   # degrees Celsius
            hum  = device.humidity      # percent
            if temp is not None and hum is not None:
                log.debug("DHT22 → %.1f °C  %.1f %%RH", temp, hum)
                return round(temp, 2), round(hum, 2)
        except RuntimeError as exc:
            # DHT sensors sometimes throw RuntimeError on bad reads — retry
            log.warning("DHT22 read attempt %d/%d failed: %s", attempt, MAX_RETRIES, exc)
            time.sleep(RETRY_DELAY_S)
        except Exception as exc:
            log.error("Unexpected DHT22 error: %s", exc)
            break

    log.error("DHT22 failed after %d attempts — returning None values", MAX_RETRIES)
    return None, None