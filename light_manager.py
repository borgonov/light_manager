#!/usr/bin/python

from datetime import datetime, timedelta
from threading import Timer
import RPi.GPIO as GPIO

class LightManager:
    # day_start_time and day_end_time are strings in format "HH:MM" (00:00 - 23:59).
    def __init__(self, gpio_address, light_start_time, light_end_time):
        GPIO.setmode(GPIO.BCM)
        self._gpio_address = gpio_address
        start_time_splitted = light_start_time.split(":")
        end_time_splitted = light_end_time.split(":")
        self._light_start_hour = int(start_time_splitted[0])
        self._light_start_minute = int(start_time_splitted[1])
        self._light_end_hour = int(end_time_splitted[0])
        self._light_end_minute = int(end_time_splitted[1])

    def run(self):
        if self._should_be_turned_on_now():
            self.turn_light_on()
        else:
            self.turn_light_off()

    def turn_light_on(self):
        print("Turning light on!")
        GPIO.setup(self._gpio_address, GPIO.OUT)
        turn_off_interval = self._get_turn_off_interval()
        print(f"Waiting for {turn_off_interval} seconds to turn off.")
        Timer(turn_off_interval, self.turn_light_off).start()

    def turn_light_off(self):
        print("Turning light off!")
        GPIO.setup(self._gpio_address, GPIO.IN)
        turn_on_interval = self._get_turn_on_interval()
        print(f"Waiting for {turn_on_interval} seconds to turn on.")
        Timer(turn_on_interval, self.turn_light_on).start()

    def _get_turn_off_date(self):
        today = datetime.today()
        turn_off_date = today.replace(hour=self._light_end_hour,
                                      minute=self._light_end_minute,
                                      second=0,
                                      microsecond=0)

        return turn_off_date

    def _get_turn_on_date(self):
        today = datetime.today()
        turn_on_date = today.replace(hour=self._light_start_hour,
                                     minute=self._light_start_minute,
                                     second=0,
                                     microsecond=0)

        return turn_on_date

    def _get_turn_on_interval(self):
        return abs((datetime.now() - self._get_turn_on_date()).total_seconds())

    def _get_turn_off_interval(self):
        return abs((datetime.now() - self._get_turn_off_date()).total_seconds())

    def _should_be_turned_on_now(self):
        # Return true if now is in the range of light time
        today = datetime.today()
        start_date = today.replace(hour=self._light_start_hour, minute=self._light_start_minute)

        if self._light_start_hour > self._light_end_hour:
            tomorrow = today + timedelta(days=1)
            end_date = today.replace(day= tomorrow.day, hour=self._light_end_hour, minute=self._light_end_minute)
        else:
            end_date = today.replace(hour=self._light_end_hour, minute=self._light_end_minute)

        return start_date < datetime.now() < end_date
