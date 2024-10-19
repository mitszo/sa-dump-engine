import sys

from sqlalchemy import (
    create_mock_engine,
    Engine,
    URL,
)


class Executor:

    def __init__(self, dialect_cls, output=sys.stdout, suffix=";", literal_binds=False):
        self.dialect_cls = dialect_cls
        self.output = output
        self.suffix = suffix
        self.literal_binds = literal_binds

    def dump(self, sql, *multiparams, **params):
        """create_mock_engine で指定する executor
        """
        print(
            str(
                sql.compile(
                    dialect=self.dialect_cls(),
                    compile_kwargs={
                        "literal_binds": self.literal_binds,
                    },
                )
            ).strip(),
            file=self.output,
        )
        print(self.suffix, file=self.output)


def create_dump_engine(dialect_name: str, output=sys.stdout, suffix=";", literal_binds=False) -> Engine:
    """create_mock_engine で指定する executor でdialectを指定可能にするための関数
    """
    url = URL.create(
        drivername=dialect_name,  # SQLを出力するだけなら、`dialect+driver` ではなくてもよい。
    )
    executor = Executor(
        dialect_cls=url.get_dialect(),
        output=output,
        suffix=suffix,
        literal_binds=literal_binds,
    )
    return create_mock_engine(url, executor=executor.dump)
