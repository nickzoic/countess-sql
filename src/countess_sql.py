from typing import Optional, Mapping
import logging

from duckdb import DuckDBPyConnection, DuckDBPyRelation

from countess.core.plugins import DuckdbPlugin
from countess.core.parameters import TextParam, ArrayParam, StringParam

VERSION = '0.0.1'

logger = logging.getLogger(__name__)


class SqlStatementPlugin(DuckdbPlugin):
    name = "SQL Statement Plugin"
    description = "Run an SQL statement"
    version = VERSION

    subst = TextParam("Substitutions", read_only=True)
    code = TextParam("SQL Code")

    def execute_multi(
        self, ddbc: DuckDBPyConnection, sources: Mapping[str, DuckDBPyRelation], row_limit: Optional[int] = None
    ) -> Optional[DuckDBPyRelation]:

        self.subst.value = "\n".join("{%d} => %s" % (n, k) for n, k in enumerate(sources.keys()))
        sql = self.code.value.format(*[s.alias for s in sources.values()])

        return ddbc.sql(sql).limit(row_limit)
