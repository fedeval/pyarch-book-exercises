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

@pytest.mark.parametrize("line_qty,final_available_quantity",[
    (2,8),
    (10,0)
])
def test_allocate_reduces_available_quantity_if_amount_available(
    line_qty: int,
    final_available_quantity: int,
    batch: Batch
):
    orderline = OrderLine(orderid="abc", sku="test_sku", qty=line_qty)
    batch.allocate(orderline)
    assert batch.available_quantity == final_available_quantity

def test_does_not_allocate_if_skus_do_not_match(
    batch: Batch,
):  
    wrong_orderline = OrderLine(orderid="abc", sku="wrong_sku", qty=2)
    batch.allocate(wrong_orderline)
    assert batch.available_quantity == 10 

def test_allocate_does_not_change_quantity_if_order_qty_more_than_available_quantity(
    batch: Batch,
    big_orderline: OrderLine
):
    batch.allocate(big_orderline)
    assert batch.available_quantity == 10

def test_allocate_the_same_order_again_does_not_change_available_quantity(
    batch: Batch,
    small_orderline: OrderLine
):
    batch.allocate(small_orderline)
    batch.allocate(small_orderline)
    assert batch.available_quantity == 8


def test_deallocate_increases_available_quantity(
    batch: Batch,
    small_orderline: OrderLine
):
    batch.allocate(small_orderline)
    assert batch.available_quantity == 8
    batch.deallocate(small_orderline)
    assert batch.available_quantity == 10

def test_deallocate_does_not_remove_unallocated_line(
    batch: Batch,
    small_orderline: OrderLine
):
    batch.deallocate(small_orderline)
    assert batch.available_quantity == 10
