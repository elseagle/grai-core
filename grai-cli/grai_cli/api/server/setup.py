import typer
from grai_cli.api.entrypoint import app


client_app = typer.Typer(no_args_is_help=True, help="Interact with the grai server")
app.add_typer(client_app, name="client")


client_get_app = typer.Typer(no_args_is_help=True, help="Get objects from the server")
client_app.add_typer(client_get_app, name="get")
