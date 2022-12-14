import asyncio
import os
import sys
from db import csv_log_reading
import time

from meross_iot.controller.mixins.electricity import ElectricityMixin
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

necessary_vars = [
    'MEROSS_EMAIL',
    'MEROSS_PASSWORD'
]

for var in necessary_vars:
    if var not in os.environ:
        print(f'{var} environment variable necessary')
        sys.exit(1)

EMAIL = os.environ.get('MEROSS_EMAIL')
PASSWORD = os.environ.get('MEROSS_PASSWORD')

async def main():
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the devices that implement the electricity mixin
    await manager.async_device_discovery()
    devs = manager.find_devices(device_class=ElectricityMixin)

    if len(devs) < 1:
        print("No electricity-capable device found...")
    else:
        dev = devs[0]

        while True:

            # Update device status: this is needed only the very first time we play with this device (or if the
            #  connection goes down)
            await dev.async_update()

            # Read the electricity power/voltage/current
            instant_consumption = await dev.async_get_instant_metrics()
            print(f"Current consumption data: {instant_consumption}")
            # instant_consumption.power
            # instant_consumption.current
            # instant_consumption.voltage
            # instant_consumption.sample_timestamp

            csv_log_reading(dev, instant_consumption)

            # TODO register device - type, uuid, name, hardware version, firmware version,
            # dev.type - str
            # dev.uuid  str
            # dev.name - str
            # dev.firmware_version - str
            # dev.hardware_version - str
            # dev.lan_ip

            time.sleep(60)

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()