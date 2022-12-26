from .model import OrderLine, Batch

def allocate(line: OrderLine, batches: list[Batch]) -> None:
    """
    This is a domain service since it represents a business
    process. It could also be an object (e.g. AllocationService),
    but it is so simple that is more expressive and readable
    to simply define it as a function.
    """
    batch_to_allocate = sorted(batches)[0]
    batch_to_allocate.allocate(line)