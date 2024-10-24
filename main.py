"""
MIT License

Copyright (c) 2024 zperk
"""

from src.env.ctypes import *
from src.env.globales import *
from src.env.logger import *
from src.env.tools import *
from src.prolog_functions import *

assertz: GenericCallable = prolog_engine.assertz

# Family tree
assertz(f"{PARENT}(john, mary)")  # John is the parent of Mary
assertz(f"{PARENT}(john, paul)")  # John is the parent of Paul
assertz(f"{PARENT}(mary, susan)")  # Mary is the parent of Susan
assertz(f"{PARENT}(mary, james)")  # Mary is the parent of James
assertz(f"{PARENT}(paul, alice)")  # Paul is the parent of Alice

"""
Rules:
Grandparent: A person is a grandparent if they are the parent of someone who is also a parent.
Uncle: A person is an uncle if they are a sibling of someone's parent.
Sibling: Two people are siblings if they share *at least* one parent and *are not* the same person.
"""
assertz(f"{GRANDPARENT}(X, Y) :- {PARENT}(X, Z), {PARENT}(Z, Y)")
assertz(f"{UNCLE}(X, Y) :- {SIBLING}(X, Z), {PARENT}(Z, Y)")
assertz(f"{SIBLING}(X, Y) :- {PARENT}(Z, X), {PARENT}(Z, Y), X \\= Y")
assertz(f"{CHILDREN}(X, Y) :- {PARENT}(Y, X)")


def main() -> int:
    while True:
        valid_children: StringSet = get_main_value()  # Get all valid child names
        prt(
            "Valid child names are: "
            f"{', '.join(set_style(s.capitalize(), CHILD_COLOR) for s in valid_children)}",
            level=logging.DEBUG,
        )

        child_name: dict[str, str] = {"str": "", "html": ""}
        """
        Context for keys:
        - 'str': Is the *raw* name of the child. This string must always be in lowercase.
        - 'html': Is the formatted HTML copy of the 'str' key.
        """

        child_name["str"] = input("> ").lower()
        if not child_name["str"]:
            prt(
                set_style("Child name cannot be empty.", ERROR_COLOR, "<b>"),
                level=logging.WARN,
            )
            continue

        child_name["html"] = set_style(
            child_name["str"].capitalize(), START_COLOR, "<b>"
        )
        logger.debug(child_name)

        # Check if the child exists in the family tree
        if child_name["str"] not in valid_children:
            prt(
                set_style(f"{child_name['html']} is not a valid child.", ERROR_COLOR),
                level=logging.WARN,
            )
            continue

        # If the child exists, display the family tree
        prt(f"\nFamily tree of {child_name['html']}:")

        # Find parents
        x_of_child(PARENT, child_name)

        # Find grandparents
        x_of_child(GRANDPARENT, child_name)

        # Find uncles
        x_of_child(UNCLE, child_name)

        # Find siblings (if any)
        x_of_child(SIBLING, child_name)

        # Find children (if the inputted child is also a parent)
        x_of_child(CHILDREN, child_name)

        return 0


if __name__ == "__main__":
    function_handler(main)
