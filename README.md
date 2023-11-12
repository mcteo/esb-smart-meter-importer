# ESB Smart Meter Importer

A small utility to extract power comsumption data from Ireland's national electrical grid provider.

[![PyPI - Version](https://img.shields.io/pypi/v/esb-smart-meter-importer.svg)](https://pypi.org/project/esb-smart-meter-importer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/esb-smart-meter-importer.svg)](https://pypi.org/project/esb-smart-meter-importer)

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install esb-smart-meter-importer
```

## Usage

```python
from esb_smart_meter_importer import smart_meter_usage

username = "Your Email Address"
password = "Your Password"

# Your Electricity Meter Number
mprn_number = "100XXXXXXXXXXX"

# If you don't know this, you can use any date *since* the meter was
# installed. Any dates before, and an exception will be thrown.
start_date = "2023-06-01"

# Imports is how much energy you bought from the grid (in kWh)
# Exports is how much energy you sold to the grid (in kWh), but
# presumedly only populated if you have Solar PV panels, etc.
imports, exports = smart_meter_usage(username, password, mprn_number, start_date)

print(imports)
```

Both `imports` and `exports` are dictionaries of `datetime` -> `float`, representing your usage in kWh at a 30 minute granularity.

```
{
    datetime(2023, 11, 10, 17, 0, tzinfo=datetime.timezone.utc): 0.142,
    datetime(2023, 11, 10, 17, 30, tzinfo=datetime.timezone.utc): 0.1285
}
```

ESB collect the data, so this library cannot offer more than a 30 minute granularity. If you want near live data, you can investigate alternate methods of collection, via Shelly EM clamps.


## License

`esb-smart-meter-importer` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
