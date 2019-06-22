[![PyPI](https://img.shields.io/pypi/v/slats.svg)](https://pypi.org/project/slats/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/slats.svg)](https://pypi.org/project/slats/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# slats

slats saves local albums to Spotify.

## Usage

The first thing you need to do is write (preferably in some automated
way) a JSON file of albums you want to save to your Spotify account. For
example,

```json
[
  { "album_artist": "Biosphere", "album": "Seti Project" },
  { "album_artist": "Biosphere", "album": "Shenzhou" },
  { "album_artist": "Biosphere", "album": "Substrata" },
  { "album_artist": "Biosphere", "album": "Dropsonde" },
  {
    "album_artist": "Darcy James Argue's Secret Society",
    "album": "Infernal Machines"
  },
  { "album_artist": "Haruka Nakamura", "album": "Grace" },
  { "album_artist": "Haruka Nakamura", "album": "Twilight" },
  { "album_artist": "Jens Lekman", "album": "I Know What Love Isn't" },
  { "album_artist": "Jens Lekman", "album": "Night Falls Over Kortedala" }
]
```

Note that the JSON you provide needs to respect the following schema:

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "album_artist": { "type": "string" },
      "album": { "type": "string" }
    }
  }
}
```

Once you have the JSON file ready, run slats with

```
slats --albums-json my_json_file.json
```

and slats will open up a Spotify authentication page in your favourite
browser where you then need to give the okay to let slats add albums to
your Spotify account. Once you've authenticated, slats will ask you to
input the URL you were redirected to after authenticating the app in
your browser.

slats will then attempt to find a corresponding album on Spotify's
servers for each album in the JSON you provided, and if it can find the
corresponding album on Spotify *and* if you don't already have that
album saved, it will save the album to your Spotify account. slats will
give you copious coloured output so you can see exactly what's going on.

## What's the catch

### Misfires

slats searches up albums by providing the album artist and album names
that you provide to slats as JSON to the Spotify API. If the Spotify API
returns a non-empty response, it will save album from the top hit of the
Spotify response to your account (provided the album already isn't
saved). This can occasionally backfire with obscure albums, where the
response from the Spotify API might provide a different album than
intended and slats would then save that album to your account. Again,
slats will give you tons of output so you can tell what it's doing, so
monitor its output as necessary to find out when misfires have occurred.

There might be something fancy I can do to protect against this—if you
have any ideas let me know.

### Spotify song limits

Spotify restricts the number of songs you can have saved to your account
to 10,000 songs (at least as of the date of this writing, 2019-05-02).
This means that if you want to import a monolithic music library to your
Spotify account, then unfortunately slats will only end up saving a
fraction of that library to your account. What's worse is that the
Spotify API doesn't return any reasonable error for when this happens.
When I imported my library, getting a 502 error was a pretty consistent
indication that I was at my song limit. So if your slats run fails with
502s, you may have reached your Spotify account's song limit.

If you're worried about reaching Spotify's song limit, one good way of
addressing this is to break up the albums you want to import into chunks
and run slats on each of those chunks separately.

### Spotify API rate limits

Spotify isn't transparent about its API's rate limits (number of
requests per unit time). Because I don't know what the rate limit is, I
haven't protected against it in the code. So if your run fails due to a
rate limit error, wait a bit, and try again (and maybe remove the albums
that have already been processed in your JSON file so that it uses less
requests on the next iteration).

## Installation

You can either install slats with pip using

```
sudo pip3 install slats
```

or just run it directly from source with the
[`run_slats.py`](run_slats.py) script.

## Configuration

slats looks for a configuration file at two paths:

1. `$PROJECT_ROOT/config.yaml`
2. `$XDG_CONFIG_HOME/slats/config.yaml`

where `$PROJECT_ROOT` is the base of the slats project (which you
generally only want to use if you're running from source), and
`$XDG_CONFIG_HOME` defaults to `$HOME/.config`, if you don't have it
defined.

To get started, copy the example configuration file
[`config.yaml.example`](config.yaml.example) to one of the above
locations (making sure to rename it to `config.yaml`).

The next thing you need to do is get your Spotify username and also
register a Spotify app (which is necessary for slats to work). You can
find your Spotify username in the account page on Spotify's main site;
and see [this
page](https://developer.spotify.com/documentation/general/guides/app-settings/)
for details on registering a Spotify app.

In the config file you copied, fill in `spotify-username` with your
Spotify username, `spotify-client-id` and `spotify-client-secret` with
the values you get after registering your app, and set
`spotify-redirect-uri` to any redirect URI you have whitelisted with
your app.
