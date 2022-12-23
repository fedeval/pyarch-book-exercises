import pytest
from app.schemas import Batch, OrderLine

@pytest.fixture
def batch() -> Batch:
    return Batch(reference="testref", sku="test_sku", qty=10)

@pytest.fixture
def small_orderline() -> OrderLine:
    return OrderLine(orderid="abc", sku="test_sku", qty=2)

@pytest.fixture
def big_orderline() -> OrderLine:
    return OrderLine(orderid="abc", sku="test_sku", qty=12)

@pytest.mark.parametrize("line_qty,final_available_qty",[
    (2,8),
    (10,0)
])
def test_allocate_reduces_available_qty_if_amount_available(
    line_qty: int,
    final_available_qty: int,
    batch: Batch
):
    orderline = OrderLine(orderid="abc", sku="test_sku", qty=line_qty)
    batch.allocate(orderline)
    assert batch.available_qty == final_available_qty

def test_does_not_allocate_if_skus_do_not_match(
    batch: Batch,
    small_orderline: OrderLine
):  
    small_orderline.sku = "wrong_sku"
    batch.allocate(small_orderline)
    assert batch.available_qty == 10 

def test_allocate_does_not_change_quantity_if_order_qty_more_than_available_qty(
    batch: Batch,
    big_orderline: OrderLine
):
    batch.allocate(big_orderline)
    assert batch.available_qty == 10

def test_allocate_the_same_order_again_does_not_change_available_qty(
    batch: Batch,
    small_orderline: OrderLine
):
    batch.allocate(small_orderline)
    batch.allocate(small_orderline)
    assert batch.available_qty == 8
