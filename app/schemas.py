from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
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
        self._purchased_qty = qty
        self.eta = eta
        self._allocated_lines: set[OrderLine] = set()
    
    def allocate(self, orderline: OrderLine):
        if self._can_allocate(orderline):
            self._allocated_lines.add(orderline)

    def deallocate(self, orderline: OrderLine):
        if orderline in self._allocated_lines:
            self._allocated_lines.remove(orderline)
    
    def _can_allocate(self, orderline: OrderLine) -> bool:
        return (
            (self.available_quantity >= orderline.qty) 
            and orderline.sku == self.sku
        )

    @property
    def allocated_quantity(self):
        return sum(line.qty for line in self._allocated_lines)
        
    @property
    def available_quantity(self):
        return self._purchased_qty - self.allocated_quantity

