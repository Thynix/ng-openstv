# ng-openstv

OpenSTV went closed source and
[became OpaVote](https://www.opavote.com/openstv). This implements STV
but is intended for demo usage instead of actual elections. It partially
supports loading the BTL file format used by OpaVote.

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

TODO; see [aaata-buspage](https://github.com/Thynix/aaata-buspage#setup) readme
for reference with setup on Apache 2. 

### TODOs

* Create template for consistent styling with header and whatnot.
    * See https://flask.palletsprojects.com/en/1.1.x/patterns/templateinheritance/#template-inheritance
* Add JS to highlight and disallow submission of:
    * Multiple votes for the same candidate.
    * Skipped rankings. (Such as ranking #3 but skipping #2.)
* Maybe do something to discourage multiple votes?
  Anything added to the clientside session can be easily cleared, but keeping IPs is a privacy risk.
  Likely not particularly worth it to bother.
* Ignore withdrawn candidates during tabulation.
* Support tabulating elections for multiple seats.
* Detect non- https://electionscience.org/library/monotonicity/
* Add BLT undervote and overvote support (just represent as `None`s?) Or don't bother.
