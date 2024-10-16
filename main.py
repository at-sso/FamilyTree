from src.env import tools
from src.functions import prolog_engine, get_family_tree

# Family tree
prolog_engine.assertz("parent(john, mary)")  # John is the parent of Mary
prolog_engine.assertz("parent(john, paul)")  # John is the parent of Paul
prolog_engine.assertz("parent(mary, susan)")  # Mary is the parent of Susan
prolog_engine.assertz("parent(mary, james)")  # Mary is the parent of James
prolog_engine.assertz("parent(paul, alice)")  # Paul is the parent of Alice

# - Grandparent
prolog_engine.assertz("grandparent(X, Y) :- parent(X, Z), parent(Z, Y)")
# - Uncle
prolog_engine.assertz("uncle(X, Y) :- sibling(X, Z), parent(Z, Y)")
# - Sibling
prolog_engine.assertz("sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y")


# Rules:
# Grandparent: A person is a grandparent if they are the parent of someone who is also a parent.
# Uncle: A person is an uncle if they are a sibling of someone's parent.
# Sibling: Two people are siblings if they share at least one parent and are not the same person.
def main() -> int:
    # Take user input for child's name
    child_name: str = input("Enter the name of the child: ").lower()

    # Call the function to retrieve and print the family tree
    get_family_tree(child_name)
    return 0


if __name__ == "__main__":
    tools.function_handler(main)
