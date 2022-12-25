from typing import Optional
from datetime import datetime
from dataclasses import dataclass

"""
A dataclass (or a namedtuple) is a Value Object since it is
identified by the data it holds. For example, if any of the
values in an OrderLine changes, then it is a new OrderLine.

A dataclass allows us to work with value equality, e.g.:
 line1 = OrderLine(orderid="abc", sku="sku1", qty=2)
 line2 = OrderLine(orderid="abc", sku="sku1", qty=2)
 assert line1 == line2 # True

Some mathematical operators like addition, subtraction and
multiplication by a number are also available.

Alternatively, objects (or entities) can have identity equality,
where changing a value does not change the identity of an object.
For instance, changing the available quantity of a Batch does
not make that another batch. We make that explict, by defining the
__eq__ method. 
"""

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

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference

    def __hash__(self):
        """
        The hash dunder method is used to control the 
        behavior of objects when added to sets or used
        as dict keys.
        See: https://docs.python.org/3/reference/datamodel.html?highlight=__hash__#object.__hash__

        Note: for value objects, hash should include all values
        and thus the objects should be immutable.

        Note 2: it is not recommended to modify __hash__ in
        isolation without modifying __eq__ accordingly.
        """
        return hash(self.reference)
    
    def allocate(self, orderline: OrderLine) -> None:
        if self._can_allocate(orderline):
            self._allocated_lines.add(orderline)

    def deallocate(self, orderline: OrderLine) -> None:
        if orderline in self._allocated_lines:
            self._allocated_lines.remove(orderline)
    
    def _can_allocate(self, orderline: OrderLine) -> bool:
        return (
            (self.available_quantity >= orderline.qty) 
            and orderline.sku == self.sku
        )

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocated_lines)
        
    @property
    def available_quantity(self) -> int:
        return self._purchased_qty - self.allocated_quantity

