from sqlalchemy.sql.dml import Insert
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.compiler import SQLCompiler


@compiles(Insert)
def _compile_insert(insert, compiler: SQLCompiler, **kw):
    if isinstance(insert._values, (list, tuple)) and len(insert._values) > 1:
        raise ValueError(f'Multi-row inserts are not allowed on {insert.table.name} ')
    return compiler.visit_insert(insert, **kw)
