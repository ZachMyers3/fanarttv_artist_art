# FanartTV Arist Art

A simple python script to gather artist art for a music directory.

## Environment Variables

A valid API key to [FanartTV](https://fanart.tv) is required to run this application.

```bash
export FANARTTV_API_KEY="my_api_key"
```

## Usage

### With Poetry

```bash
# install dependencies
poetry install
# run cli help dialog
poetry run python ./src/cli.py --help
# run application
poetry run python ./src/cli.py --path /path/to/Music
```

