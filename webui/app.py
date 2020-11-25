from typing import List
from flask import Flask, render_template, url_for, request, redirect, flash
from format.blt import load_blt, BLT, Ballot
import pickle
import fcntl

app = Flask(__name__)
app.config.from_object("config")


blt: BLT = None

# Lists of form element IDs for each candidate. Each candidate's elements are
# ordered from first to last preference.
candidate_options: List[List[int]] = list()


@app.before_first_request
def initialize():
    # Load BLT
    global blt
    with open(app.config["BLT_PATH"], "r") as blt_file:
        blt = load_blt(blt_file)

    # TODO: omit withdrawn candidates
    # Compute form options
    global candidate_options
    for _ in range(len(blt.candidate_names)):
        candidate_ranking = list()
        candidate_options.append(candidate_ranking)
        for ranking_number in range(1, len(blt.candidate_names) + 1):
            candidate_ranking.append(ranking_number)

    # Write the BLT pickle if it does not already exist
    try:
        with open(app.config["PICKLE_PATH"], "xb") as pickle_file:
            pickle.dump(blt, pickle_file, pickle.HIGHEST_PROTOCOL)
    except FileExistsError:
        pass


@app.route("/")
def vote_form():
    return render_template(
        "vote_form.html",
        form_target=url_for("submit_vote"),
        candidate_options=candidate_options,
        blt=blt,
    )


@app.route("/vote", methods=["POST"])
def submit_vote():
    choices = list()
    for ranking in range(1, len(blt.candidate_names) + 1):
        for candidate_index, candidate_name in enumerate(blt.candidate_names):
            if candidate_name in request.form:
                choice = int(request.form[candidate_name])
                if choice == ranking:
                    choices.append(candidate_index + 1)
                    break

    ballot = Ballot(choices)
    description = ', '.join(map(lambda n: blt.candidate_names[n - 1], choices))
    flash(f"Your ballot for {description} has been received.")

    with open(app.config["PICKLE_PATH"], "r+b") as pickle_file:
        fcntl.flock(pickle_file, fcntl.LOCK_EX)

        running_results: BLT = pickle.load(pickle_file)

        running_results.add_ballot(ballot)
        pickle_file.seek(0)
        pickle.dump(running_results, pickle_file, pickle.HIGHEST_PROTOCOL)

        return redirect(url_for("receipt"))


@app.route("/receipt")
def receipt():
    return render_template("receipt.html")
