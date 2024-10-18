from sqlalchemy import (
    create_mock_engine,
    Engine,
    URL,
)


class Executor:
    """create_mock_engine で指定する executor でdialectを指定可能にするためのクラス
    """

    def __init__(self, dialect_cls, literal_binds=False):
        self.dialect_cls = dialect_cls
        self.literal_binds = literal_binds

    def dump(self, sql, *multiparams, **params):
        """create_mock_engine で指定する executor
        """
        print('{};\n'.format(
            str(
                sql.compile(
                    dialect=self.dialect_cls(),
                    compile_kwargs={
                        "literal_binds": self.literal_binds,
                    },
                )
            ).strip()
        ))


def create_dump_engine(dialect_name: str, literal_binds=False) -> Engine:
    """create_mock_engine で指定する executor でdialectを指定可能にするための関数
    """
    url = URL.create(
        drivername=dialect_name,  # SQLを出力するだけなら、`dialect+driver` ではなくてもよい。
    )
    executor = Executor(
        dialect_cls=url.get_dialect(),
        literal_binds=literal_binds,
    )
    return create_mock_engine(url, executor=executor.dump)
