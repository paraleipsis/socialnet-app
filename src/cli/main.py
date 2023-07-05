from typing import Annotated

import typer
import dotenv

from auth.schemas.schemas_auth import auth_conf_dir
from conf.config import BASE_DIR
from cli.utils import generate_secret_key


cli = typer.Typer()


@cli.command()
def secret_key(
        write: Annotated[
            bool,
            typer.Option(
                help="Write generated secret key to configuration file."
            )
        ] = False
):
    """
    Generate Secret Key for Authentication purposes.
    """
    key = generate_secret_key()
    if write:
        file = BASE_DIR / auth_conf_dir
        dotenv.set_key(file, "SECRET_KEY", key)
        print(f"Secret key was successfully written to file {file}: {key}")
    else:
        print(f"Secret key: {key}")


if __name__ == "__main__":
    cli()
