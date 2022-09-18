import csv
import os.path

import meross_iot

## CSV
fields = ['timestamp', 'power', 'voltage', 'current']
def csv_get_fn(dev):
    # prepare dev name
    name = dev.name
    name = name.replace(' ', '')
    return f'meross_{name}.csv'

def csv_new_device(fn):
    with open(fn, 'w') as f:
        csvwriter=csv.writer(f)
        csvwriter.writerow(fields)

def csv_log_reading(dev,
                    reading):#: meross_iot.model.plugin.power.PowerInfo):
    dev_fn = csv_get_fn(dev)
    if not os.path.exists(dev_fn):
        csv_new_device(dev_fn)
    with open(dev_fn, 'a') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow([reading.sample_timestamp,
                            reading.power,
                            reading.voltage,
                            reading.current])
