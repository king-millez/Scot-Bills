from scotbills.scot_parliament import all_bills
import pytest
import random
import json

def test_scot():
    all_the_bills_lad = all_bills
    random_numbers = [int(random.random()*len(all_the_bills_lad)) for i in range(10)]
    bills_sample = [all_the_bills_lad[i] for i in random_numbers]
    for bill in bills_sample:
        print(json.dumps(bill, indent=2) + '\n')