# ------------------ IMPORTS AND SETUP ----------------- #

import typer
app = typer.Typer()

# ----------------------- DEFINES ---------------------- #

# ---------------------- FUNCTIONS --------------------- #

# --------------------- ENTRYPOINT --------------------- #


@app.command("add")
def add_data(data: str):
    print(f"data added: {data}")

@app.command("delete")
def del_data(data: str):
    print(f"data deleted: {data}")

def main(name: str = "name" ):
    print(f"hello {name}")

if __name__ == "__main__":
    app()