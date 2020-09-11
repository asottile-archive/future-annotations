import os.path
import shutil


def main() -> int:
    pth = 'tests/__pycache__'
    if os.path.exists(pth):
        shutil.rmtree(pth)
    return 0


if __name__ == '__main__':
    exit(main())
