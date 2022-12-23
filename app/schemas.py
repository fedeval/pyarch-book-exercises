from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class OrderLine:
    orderid: str
    sku: str
    qty: int

class Batch:
    def __init__ (
        self,
        reference: str,
        sku: str,
        qty: int,
        eta: Optional[datetime] = None
    ) -> None:
        self.reference = reference
        self.sku = sku
        self.available_qty = qty
        self.eta = eta
        self.allocated_lines: list[OrderLine] = []
    
    def allocate(self, orderline: OrderLine):
        if self._can_allocate(orderline):
            self.available_qty -= orderline.qty
            self._allocate_line(orderline)

    def deallocate(self, orderline: OrderLine):
        pass
    
    def _can_allocate(self, orderline: OrderLine) -> bool:
        return (self.available_qty >= orderline.qty) and not any(orderline.orderid == line.orderid for line in self.allocated_lines)

    def _allocate_line(self, orderline: OrderLine):
        self.allocated_lines.append(orderline)

