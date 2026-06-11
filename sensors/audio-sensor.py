"""
sensors/audio_sensor.py
Reads a digital sound/audio detection module via a GPIO pin.
These modules (e.g. KY-038, LM393-based) output LOW when sound
exceeds the on-board threshold potentiometer setting.

Returns True if sound/audio is detected, False otherwise.
"""

import logging
import RPi.GPIO as GPIO

log = logging.getLogger(__name__)


def read_audio(pin: int) -> bool:
    """
    Read the digital output of a sound detection module.

    Many common modules are active-LOW: the pin goes LOW (0) when
    sound is detected. This function normalises that to True = detected.

    Args:
        pin: BCM GPIO pin number connected to the module's DO (digital out) pin.

    Returns:
        True if audio/sound threshold exceeded, False if quiet.
    """
    try:
        raw = GPIO.input(pin)
        # Active-LOW logic: 0 → sound detected, 1 → quiet
        detected = (raw == GPIO.LOW)
        log.debug("Audio pin %d → raw=%d  %s", pin, raw, "DETECTED" if detected else "quiet")
        return detected
    except Exception as exc:
        log.error("Audio sensor read error on pin %d: %s", pin, exc)
        return False