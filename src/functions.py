__all__ = ["prolog_engine"]

from pyswip import Prolog

from .env.ctypes import *

prolog_engine = Prolog()


# Function to get valid child names
def get_valid_children() -> GenericSet:
    children = set()  # Use a set to avoid duplicates
    for result in prolog_engine.query("parent(_, X)"):
        children.add(result["X"])
    return children


# Define a function to get the family tree of a specific child
def get_family_tree(child_name: str) -> None:
    valid_children: GenericSet = get_valid_children()  # Get all valid child names

    # Check if the child exists in the family tree
    if child_name not in valid_children:
        print(f"\nError: '{child_name}' does not exist in the family tree.")
        print("Valid child names are:", ", ".join(valid_children))
        return

    # If the child exists, display the family tree
    print(f"\nFamily tree of {child_name}:")

    # Find parents
    print("\nParents:")
    for result in prolog_engine.query(f"parent(X, {child_name})"):
        print(f"{result['X']} is the parent of {child_name}")

    # Find grandparents
    print("\nGrandparents:")
    for result in prolog_engine.query(f"grandparent(X, {child_name})"):
        print(f"{result['X']} is the grandparent of {child_name}")

    # Find uncles
    print("\nUncles:")
    for result in prolog_engine.query(f"uncle(X, {child_name})"):
        print(f"{result['X']} is the uncle of {child_name}")

    # Find siblings (if any)
    print("\nSiblings:")
    for result in prolog_engine.query(f"sibling(X, {child_name})"):
        print(f"{result['X']} is the sibling of {child_name}")

    # Find children (if the inputted child is also a parent)
    print("\nChildren:")
    for result in prolog_engine.query(f"child(X, {child_name})"):
        print(f"{result['X']} is the child of {child_name}")
