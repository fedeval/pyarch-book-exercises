from .model import OrderLine, Batch

def allocate(line: OrderLine, batches: list[Batch]) -> None:
    batch_to_allocate = sorted(batches)[0]
    batch_to_allocate.allocate(line)