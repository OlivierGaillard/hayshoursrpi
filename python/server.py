from flask import Flask, request, render_template
from hayshours import HaysHours
from persistfactory import get_sqlpersist, get_filepersist
import os

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
    dict(
        DEBUG=True,
    )
)

@app.route("/")
def message():
    h = HaysHours()
    # p = SQLPersist(host, user, password, port, database, create=False)
    h.set_db(p)
    lastHourSaved = h.getLastSaved()
    if len(lastHourSaved) > 0:
        return render_template("form.html", lastHourSaved=lastHourSaved)
    else:
        return render_template("form.html")


@app.route("/end/<elapsed>")
def end_hour(elapsed):
    h = HaysHours()
    # p = SQLPersist(host, user, password, port, database, create=False)
    h.set_db(p)
    endHour = h.getEnd(elapsed)
    return endHour


@app.route("/last")
def last():
    # p = SQLPersist(host, user, password, port, database, create=False)
    return p.readLast()


@app.route("/calc", methods=["GET", "POST"])
def calc():
    if request.method == "POST":
        req = request.form
        h = HaysHours()
        h.set_db(p)
        lastHourSaved = h.getLastSaved()
        elapsed = req.get("elapsed")
        endHour = h.getEnd(elapsed)
        if len(elapsed) == 0:
            err_msg = "No end-time because no elapsed time given."
            return render_template("form.html", err_msg=err_msg)
        if lastHourSaved:
            return render_template(
                "form.html",
                endHour=endHour,
                elapsed=elapsed,
                lastHourSaved=lastHourSaved,
            )
        else:
            return render_template("form.html", endHour=endHour, elapsed=elapsed)
    else:
        lastHourSaved = p.readLast()
        if lastHourSaved:
            return render_template("form.html", lastHourSaved=lastHourSaved)
        else:
            return render_template("form.html")


if __name__ == "__main__":
    STATEFUL_TYPE = os.getenv('STATEFUL_TYPE', 'FILE')
    if STATEFUL_TYPE == 'SQL':
        p = get_sqlpersist()
    else:
        p = get_filepersist()
    app.run(host="0.0.0.0")
