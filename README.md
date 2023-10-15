# OpenTracksViewer

## Install
### Python requirements
`pip install -r requirements.txt`
### Gunicorn
If you intend to use Gunicorn as a WSGI server (recommended), please check [the following documentation](https://docs.gunicorn.org/en/stable/run.html)
### CSS/JS resources (optional)
If you intend to locally serve the CSS and JS resources instead of using a CDN, you will need to run the following command: `npm --prefix otv/static install`

## Configure
### OpenTracks GPX file path
You need to specify OpenTracksViewer the path of the folder containing all your GPX tracks, you can do it either via:
- Setting the `TRACKS_FOLDER_PATH` in the `config.py` file
- Setting `OTV_TRACKS_FOLDER_PATH` environment variable
### Gunicorn
## Run
### Gunicorn (recommended)
`gunicorn -w 4 'otv.wsgi:create_app()'`

### Flask development server
`flask -A 'otv.wsgi:create_app()' run`