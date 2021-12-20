import pathlib
import typer

from fanarttv_artist_art import gather_art

app = typer.Typer()


@app.command()
def command(
    path: pathlib.Path = typer.Option(
        None, help="The location of the music directory"
    )
) -> None:
    if path is None:
        print("File is required, exiting")

    gather_art(path=path)


def main():
    app()


if __name__ == "__main__":
    main()
