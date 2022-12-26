from .model import OrderLine, Batch

def allocate(line: OrderLine, batches: list[Batch]) -> None:
    print([b.reference for b in sorted(batches)])
    batch_to_allocate = sorted(batches)[0]
    batch_to_allocate.allocate(line)