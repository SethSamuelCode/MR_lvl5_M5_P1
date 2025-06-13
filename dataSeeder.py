# ------------------ IMPORTS AND SETUP ----------------- #

import typer

# ----------------------- DEFINES ---------------------- #

# ---------------------- FUNCTIONS --------------------- #

# --------------------- ENTRYPOINT --------------------- #


def main(name: str = "name" ):
    print(f"hello {name}")

if __name__ == "__main__":
    typer.run(main)