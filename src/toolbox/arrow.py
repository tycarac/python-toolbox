import pyarrow as pa
import pyarrow.compute as pc
from typing import cast, Any


# _____________________________________________________________________________
def select_by_key(table: pa.Table, column: str, key: Any) -> pa.Table:
    return cast(pa.Table, table.filter(pc.field(column) == key))
