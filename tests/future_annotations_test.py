# -*- coding: future_annotations -*-
import importlib
import io
import tokenize
from typing import Optional
from typing import TYPE_CHECKING

import pytest

import future_annotations

if TYPE_CHECKING:
    from typing import Protocol
else:
    Protocol = object


@pytest.mark.parametrize(
    ('s', 'expected'),
    (
        ('# coding: wat', '# ***********'),
        ('  # coding: wat', '  # ***********'),
    ),
)
def test_new_coding_cookie(s, expected):
    matched = tokenize.cookie_re.match(s)
    assert matched
    replaced = tokenize.cookie_re.sub(future_annotations._new_coding_cookie, s)
    assert replaced == expected


def test_empty_file():
    assert future_annotations.decode(b'') == ('', 0)


def test_multiple_tokens_until_stopping():
    b_src = b'''\
def f(x: str  # ohai
    ,): ...
'''
    expected = '''\
def f(x: 'str'  # ohai
    ,): ...
'''
    src, _ = future_annotations.decode(b_src)
    assert src == expected


def test_streamreader_read():
    reader = future_annotations.StreamReader(io.BytesIO(b'def f(x: str): ...'))
    assert reader.read() == "def f(x: 'str'): ..."


class C(Protocol):
    c: C  # noqa: F821
    def make_arg(self, a: C) -> C: ...  # noqa: F821
    def make_stararg(self, *a: C) -> C: ...  # noqa: F821
    def make_namedonlyarg(self, *, a: C) -> C: ...  # noqa: F821
    def make_starstararg(self, **a: C) -> C: ...  # noqa: F821
    def make_opt(self, a: Optional[C]) -> C: ...  # noqa: F821


def test_it_works():
    assert C.__annotations__ == {'c': 'C'}
    assert C.make_arg.__annotations__ == {'a': 'C', 'return': 'C'}
    assert C.make_stararg.__annotations__ == {'a': 'C', 'return': 'C'}
    assert C.make_namedonlyarg.__annotations__ == {'a': 'C', 'return': 'C'}
    assert C.make_starstararg.__annotations__ == {'a': 'C', 'return': 'C'}
    assert C.make_opt.__annotations__ == {'a': 'Optional[C]', 'return': 'C'}


def test_main(tmpdir, capsys):
    f = tmpdir.join('f.py')
    f.write(
        '# -*- coding: future-annotations -*-\n'
        'class C:\n'
        '    c: C\n'
    )
    assert not future_annotations.main((str(f),))
    out, _ = capsys.readouterr()
    assert out == (
        '# ****************************** -*-\n'
        'class C:\n'
        "    c: 'C'\n"
    )


def test_fix_coverage():
    """Because our module is loaded so early in python startup, coverage
    doesn't have a chance to instrument the module-level scope.

    Run this last so it doesn't interfere with tests in any way.
    """
    importlib.reload(future_annotations)
