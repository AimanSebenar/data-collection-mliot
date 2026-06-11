"""
main.py
Raspberry Pi 4 - Multi-Sensor Data Logger
Sensors: Motion (PIR), Temperature/Humidity (DHT22), Audio
Sample rate: 30 minutes
Output: CSV file auto-pushed to GitHub on completion
"""

import time
import csv
import logging
import os
from datetime import datetime
from pathlib import Path

import RPi.GPIO as GPIO
import adafruit_dht
import board

from config.settings import (
    MOTION_PIN,
    AUDIO_PIN,
    DHT_PIN,
    SAMPLE_INTERVAL_SEC,
    TOTAL_SAMPLES,
    DATA_DIR,
    LOG_DIR,
)
from sensors.motion_sensor import read_motion
from sensors.audio_sensor import read_audio
from sensors.dht_sensor import read_dht
from utils.csv_writer import init_csv, write_row
from utils.github_push import push_to_github


# ── Logging setup ─────────────────────────────────────────────────────────────
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "sensor_log.txt"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def setup_gpio(dht_sensor):
    """Initialise GPIO and return the DHT device handle."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTION_PIN, GPIO.IN)
    GPIO.setup(AUDIO_PIN, GPIO.IN)
    log.info("GPIO initialised (BCM mode). Motion PIN=%d  Audio PIN=%d", MOTION_PIN, AUDIO_PIN)
    return dht_sensor


def collect_sample(dht_device):
    """Read all three sensors and return a result dict."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    motion   = read_motion(MOTION_PIN)
    temp, hum = read_dht(dht_device)
    audio    = read_audio(AUDIO_PIN)

    sample = {
        "timestamp":         timestamp,
        "motion_detected":   motion,
        "temperature_c":     temp,
        "humidity_pct":      hum,
        "audio_detected":    audio,
    }
    log.info("Sample → %s", sample)
    return sample


def run():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # One CSV file per run, named by start time
    csv_path = DATA_DIR / f"sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Initialise DHT device once (reused across samples)
    dht_device = adafruit_dht.DHT22(getattr(board, f"D{DHT_PIN}"))

    try:
        setup_gpio(dht_device)
        init_csv(csv_path)
        log.info("Logging %d samples every %d s → %s", TOTAL_SAMPLES, SAMPLE_INTERVAL_SEC, csv_path)

        for sample_num in range(1, TOTAL_SAMPLES + 1):
            log.info("── Sample %d / %d ──", sample_num, TOTAL_SAMPLES)
            sample = collect_sample(dht_device)
            write_row(csv_path, sample)

            if sample_num < TOTAL_SAMPLES:
                log.info("Sleeping %d s until next sample…", SAMPLE_INTERVAL_SEC)
                time.sleep(SAMPLE_INTERVAL_SEC)

        log.info("Data collection complete. Pushing to GitHub…")
        push_to_github(csv_path)

    except KeyboardInterrupt:
        log.warning("Interrupted by user — pushing partial data to GitHub…")
        push_to_github(csv_path)

    finally:
        dht_device.exit()
        GPIO.cleanup()
        log.info("GPIO cleaned up.")


if __name__ == "__main__":
    run()