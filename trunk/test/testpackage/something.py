# Copyright 2006  Peter Gebauer
# (see LICENSE.txt for licensing information)
"""
Just a test module.

Adding some more documentation to test the one-liner doc in the index page.
    Oh, we might as well test indentation.
"""

class ATestClass(int, str):
    """
    Just a test class that has multiple inheritance and that's about it.
    """

    class ANestedClass:
        """
        Ugly as this may be, it should be included in the documentation.
        """


def somefunc(a = {"a": [1, [2, {"b": (3, 4)}]]}, b = [None, AMestedClass]):
    """
    Some function.
    This tests the nested default arguments as well as the other things.

    Not indented.
        Indented 1
        Indented 2
            Indented 1-1
            Indented 1-2
    """
