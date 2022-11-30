"""
Shared utility functions used by many tests
"""

from unittest import main


def unittest_main():
    """Runs unittest.main if __main__"""
    if __name__ == "__main__":
        main()


__all__ = ["unittest_main"]
