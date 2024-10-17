from src.env.ctypes import *
from src.env.globales import *
from src.env.logger import logging, logger
from src.env.tools import *
from src.functions import *
from src.functions import prolog_engine

# Family tree
prolog_engine.assertz(f"{PARENT}(john, mary)")  # John is the parent of Mary
prolog_engine.assertz(f"{PARENT}(john, paul)")  # John is the parent of Paul
prolog_engine.assertz(f"{PARENT}(mary, susan)")  # Mary is the parent of Susan
prolog_engine.assertz(f"{PARENT}(mary, james)")  # Mary is the parent of James
prolog_engine.assertz(f"{PARENT}(paul, alice)")  # Paul is the parent of Alice

prolog_engine.assertz(f"{GRANDPARENT}(X, Y) :- parent(X, Z), parent(Z, Y)")
prolog_engine.assertz(f"{UNCLE}(X, Y) :- sibling(X, Z), parent(Z, Y)")
prolog_engine.assertz(f"{SIBLING}(X, Y) :- parent(Z, X), parent(Z, Y), X \\= Y")
prolog_engine.assertz(f"{CHILDREN}(X, Y) :- parent(Y, X)")


# Rules:
# Grandparent: A person is a grandparent if they are the parent of someone who is also a parent.
# Uncle: A person is an uncle if they are a sibling of someone's parent.
# Sibling: Two people are siblings if they share at least one parent and are not the same person.
def main() -> int:
    global capital_child
    while True:
        valid_children: StringSet = get_main_value()  # Get all valid child names
        prt(
            "Valid child names are: "
            f"{', '.join(set_style(s.capitalize(), CHILD_COLOR) for s in valid_children)}",
            level=logging.DEBUG,
        )

        child_name: Dict[str, str] = {"str": "", "html": ""}

        child_name["str"] = input()
        child_name["html"] = set_style(
            child_name["str"].capitalize(), START_COLOR, "<b>"
        )

        logger.debug(child_name)

        # Check if the child exists in the family tree
        if child_name["str"] not in valid_children:
            prt(
                set_style(
                    f"{child_name['html']} does not exist in the family tree.",
                    ERROR_COLOR,
                ),
                level=logging.WARN,
            )
            continue

        # clear_terminal()

        # If the child exists, display the family tree
        prt(f"\nFamily tree of {child_name['html']}:")

        # Find parents
        show_child_of_x(PARENT, child_name)

        # Find grandparents
        show_child_of_x(GRANDPARENT, child_name)

        # Find uncles
        show_child_of_x(UNCLE, child_name)

        # Find siblings (if any)
        show_child_of_x(SIBLING, child_name)

        # Find children (if the inputted child is also a parent)
        show_child_of_x(CHILDREN, child_name)

        return 0


if __name__ == "__main__":
    function_handler(main)
