# ng-openstv

OpenSTV went closed source and
[became OpaVote](https://www.opavote.com/openstv). This implements STV
but is intended for demo usage instead of actual elections. It supports
(partially) the BTL file format, also used by OpaVote.

## Requirements

* Python 3
* Flask

## Running

It will load the ballot from the configured BLT_PATH, and save and load the
running ballot box to and from PICKLE_PATH.

### Development

If you have [pipenv](https://pipenv.pypa.io/en/latest/) installed:

```bash
pipenv shell
env FLASK_ENV=development FLASK_APP=webui/app.py flask run
```

### Deploying

TODO: see aaata-buspage readme

### TODOs

* Add web UI for adding ballots
* Create template for consistent styling with header and whatnot.
    * See https://flask.palletsprojects.com/en/1.1.x/patterns/templateinheritance/#template-inheritance
* Support ignoring withdrawn candidates during tabulation.
* Add undervote and overvote support (just represent as `None`s?) Or don't bother.
* detect non- https://electionscience.org/library/monotonicity/
* Maybe a less-dumb BLT variant? BLT could be load-only. Use YAML - https://pypi.org/project/strictyaml/
    * oh wait just pickle the BLT class
    * Title
    * Candidate names
    * number of seats, then any subsequents numbers are withdrawn candidate numbers
    * List of ballots: weight; ordered choices
