
from app.allocate import allocate
from app.model import Batch, OrderLine
from datetime import datetime, timedelta

def test_allocates_to_in_stock_first():
    in_stock_batch = Batch(reference="instock", sku="test-sku", qty=10)
    in_transit_batch = Batch(reference="in_transit", sku="test-sku", qty=10, eta=datetime.today() + timedelta(days=1))
    line = OrderLine(orderid="my-order", sku="test-sku", qty=2)
    allocate(line, [in_stock_batch, in_transit_batch])
    assert in_stock_batch.available_quantity == 8
    assert in_transit_batch.available_quantity == 10

def test_allocates_lowest_eta_batch_first():
    tomorrow_batch = Batch(reference="tomorrow", sku="test-sku", qty=10, eta=datetime.today() + timedelta(days=1))
    plus_two_batch = Batch(reference="plus_one", sku="test-sku", qty=10, eta=datetime.today() + timedelta(days=2))
    plus_three_batch = Batch(reference="plus_two", sku="test-sku", qty=10, eta=datetime.today() + timedelta(days=3))
    line = OrderLine(orderid="my-order", sku="test-sku", qty=2)
    allocate(line, [plus_two_batch, tomorrow_batch, plus_three_batch])
    assert tomorrow_batch.available_quantity == 8
    assert plus_two_batch.available_quantity == 10
    assert plus_three_batch.available_quantity == 10