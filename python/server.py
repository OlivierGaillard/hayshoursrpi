from flask import Flask, request, render_template
from hayshours import HaysHours
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
    h.set_db(p)
    lastHourSaved = h.getLastSaved()
    if len(lastHourSaved) > 0:
        return render_template(
            "form.html", lastHourSaved=lastHourSaved, stateful_type=stateful_type
        )
    else:
        return render_template("form.html", stateful_type=stateful_type)


@app.route("/end/<elapsed>")
def end_hour(elapsed):
    h = HaysHours()
    h.set_db(p)
    endHour = h.getEnd(elapsed)
    return endHour


@app.route("/last")
def last():
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
            return render_template(
                "form.html", err_msg=err_msg, stateful_type=stateful_type
            )
        if lastHourSaved:
            return render_template(
                "form.html",
                endHour=endHour,
                elapsed=elapsed,
                lastHourSaved=lastHourSaved,
                stateful_type=stateful_type,
            )
        else:
            return render_template(
                "form.html",
                endHour=endHour,
                elapsed=elapsed,
                stateful_type=stateful_type,
            )
    else:
        lastHourSaved = p.readLast()
        if lastHourSaved:
            return render_template(
                "form.html", lastHourSaved=lastHourSaved, stateful_type=stateful_type
            )
        else:
            return render_template("form.html", stateful_type=stateful_type)


if __name__ == "__main__":
    STATEFUL_TYPE = os.getenv("STATEFUL_TYPE", "FILE")
    if STATEFUL_TYPE == "SQL":
        print("StateFule Type: SQL")
        from persistfactory import get_sqlpersist

        p = get_sqlpersist()
        stateful_type = p.get_stateful_type()
    else:
        print("StateFule Type: File")
        from persistfactory import get_filepersist

        p = get_filepersist()
        stateful_type = p.get_stateful_type()
    app.run(host="0.0.0.0")
