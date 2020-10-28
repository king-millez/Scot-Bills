# Scot-Bills

A fork of [Aus-Bills](https://github.com/KipCrossing/Aus-Bills) which supports the [Scottish Parliament](https://www.parliament.scot).

---

To quote Ben:

> Bro, plz Scotland.

> Free my people.

And so it was done.

## Usage

### Setup

Use **pip3** to install the required modules in `requirements.txt`:

```pip3 install -r requirements.txt```

### Returning all bills

Each individual bill is returned as a **dict** in Python, then each **dict** is stored in a list, which can be accessed like this:

```python
from scotbills.scot_parliament import all_bills

# Print all the bills:
print(all_bills)

# Print the first bill:
print(all_bills[0])

# Print the first bill's URL:
print(all_bills[0]['url'])
```

## Todo

Add **scot_Bill** object to return more metadata for each bill.