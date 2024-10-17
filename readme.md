# Family Tree Prolog-Based Application

This repository contains a Python-based application that uses Prolog logic to manage and query family tree relationships. The program allows users to interactively input names and retrieve various relationships within the family, such as parents, grandparents, siblings, uncles, and children.

## Features

- **Family Tree Representation**: The program uses Prolog assertions to represent family relationships, including parents, siblings, grandparents, and uncles.
- **Interactive Mode**: Users can input a child's name and get information about their family tree.
- **Prolog Integration**: Prolog rules and facts are asserted in the program, allowing logical queries for relationships.

## How It Works

1. **Family Tree Setup**:

   - Prolog facts are asserted to represent parent-child relationships.
   - Logical rules define relationships like grandparents, uncles, and siblings.

2. **Interactive Console**:

   - The program continuously prompts for a child's name and provides the family tree, listing relationships like parents, siblings, grandparents, uncles, and children (if applicable).

3. **Prolog Queries**:
   - Uses Prolog logic to derive relationships by querying the family tree.

## Dependencies

- **Python** (recommended version: 3.10.12)
- **Prolog Engine**: The program utilizes a Prolog engine integrated into the Python environment to handle logical assertions and queries.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/at-sso/FamilyTree.git
   cd FamilyTree
   ```

2. Install the required dependencies (assuming Prolog engine support is included in your environment):

   ```bash
   pip install -r ./config/requirements.txt
   ```

3. Ensure that Prolog support is correctly set up in your environment: [SWI-Prolog](https://www.swi-prolog.org/download/stable).

## How to Run

To start the application, run the `main.py` file:

```bash
python3 ./main.py
```

The program will prompt you to input the name of a child from the family tree.

### Example Interaction:

```
Valid child names are: Mary, Susan, Paul, James, Alice
> Mary
```

Output:

```txt
Family tree of Mary:

Parent of Mary:
John is the parent of Mary

Grandparent of Mary:
Mary doesn't have any grandparent.

...
```

## Family Tree Representation

The family tree is represented using Prolog rules. Here are the key relationships:

1. **Parent**: Direct parent-child relationship.

   ```prolog
   parent(john, mary).
   parent(john, paul).
   parent(mary, susan).
   parent(mary, james).
   parent(paul, alice).
   ```

2. **Grandparent**: A person is a grandparent if they are the parent of someone who is also a parent.

   ```prolog
   grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
   ```

3. **Sibling**: Two people are siblings if they share at least one parent and are not the same person.

   ```prolog
   sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.
   ```

4. **Uncle**: A person is an uncle if they are a sibling of someone's parent.
   ```prolog
   uncle(X, Y) :- sibling(X, Z), parent(Z, Y).
   ```

## File Structure

```
.
├── config
│   └── requirements.txt
├── main.py # Main script that runs the family tree logic
└── src
    ├── env
    │   ├── ctypes.py   # Defines necessary types for the program
    │   ├── globales.py # Global variables and constants
    │   ├── logger.py   # Logging utilities
    │   └── tools.py    # Helper functions for formatting and styling output
    └── functions.py    # Core Prolog engine integration and function handling
```

## Customization

To customize the family tree, you can modify the Prolog facts in `main.py`. For example, to add a new child or define new relationships, modify the following section:

```python
assertz(f"{PARENT}(john, mary)")
assertz(f"{PARENT}(john, paul)")
# Add more family relationships here...
```

## License

This project is licensed under the MIT [License](license).
