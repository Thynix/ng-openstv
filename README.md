# ng-openstv

OpenSTV went closed source and
[became OpaVote](https://www.opavote.com/openstv). This implements STV
but is intended for demo usage instead of actual elections. It supports
(partially) the BTL file format, also used by OpaVote.

## Requirements

* Python 3
* Flask, probably

### TODOs

* Add STV result computation
* Add web UI for adding ballots
* Add undervote and overvote support (just represent as `None`s?)
* detect non- https://electionscience.org/library/monotonicity/
