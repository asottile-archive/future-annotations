[![Build Status](https://asottile.visualstudio.com/asottile/_apis/build/status/asottile.future-annotations?branchName=master)](https://asottile.visualstudio.com/asottile/_build/latest?definitionId=66&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/66/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=66&branchName=master)

future-annotations
==================

A backport of \_\_future\_\_ annotations to python<3.7.


## Installation

`pip install future-annotations`


## Usage

Include the following encoding cookie at the top of your file (this replaces
the utf-8 cookie if you already have it):

```python
# -*- coding: future_annotations -*-
```

And then write python3.7+ forward-annotation code as usual!

```python
# -*- coding: future_annotations -*-
class C:
    @classmethod
    def make(cls) -> C:
        return cls()

print(C.make())
```

```console
$ python3.6 main.py
<__main__.C object at 0x7fb50825dd90>
$ mypy main.py
Success: no issues found in 1 source file
```

## Showing transformed source

`future-annotations` also includes a cli to show transformed source.

```console
$ future-annotations-show main.py
# ****************************** -*-
class C:
    @classmethod
    def make(cls) -> 'C':
        return cls()

print(C.make())
```

## How does this work?

`future-annotations` has two parts:

1. A utf-8 compatible `codec` which performs source manipulation
    - The `codec` first decodes the source bytes using the UTF-8 codec
    - The `codec` then leverages
      [tokenize-rt](https://github.com/asottile/tokenize-rt) to rewrite
      annotations.
2. A `.pth` file which registers a codec on interpreter startup.

## when you aren't using normal `site` registration

in setups (such as aws lambda) where you utilize `PYTHONPATH` or `sys.path`
instead of truly installed packages, the `.pth` magic above will not take.

for those circumstances, you'll need to manually initialize `future-annotations`
in a non-annotations wrapper.  for instance:

```python
import future_annotations

future_annotations.register()

from actual_main import main

if __name__ == '__main__':
    exit(main())
```

## you may also like

- [future-breakpoint](https://github.com/asottile/future-breakpoint)
- [future-fstrings](https://github.com/asottile/future-fstrings)
