from app.schemas import Batch, OrderLine


def test_allocate_reduces_available_qty():
    orderline = OrderLine(orderid="abc", sku="test_sku", qty=2)
    batch = Batch(reference="testref", sku="test_sku", qty=10)
    batch.allocate(orderline)
    assert batch.available_qty == 8

def test_allocate_does_not_change_quantity_if_order_qty_more_than_available_qty():
    orderline = OrderLine(orderid="abc", sku="test_sku", qty=12)
    batch = Batch(reference="testref", sku="test_sku", qty=10)
    batch.allocate(orderline)
    assert batch.available_qty == 10

def test_allocate_the_same_order_again_does_not_change_available_qty():
    orderline = OrderLine(orderid="abc", sku="test_sku", qty=2)
    batch = Batch(reference="testref", sku="test_sku", qty=10)
    batch.allocate(orderline)
    batch.allocate(orderline)
    assert batch.available_qty == 8
