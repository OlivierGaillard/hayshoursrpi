from flask import Flask, request, render_template
from hayshours import HaysHours
from filepersist import FilePersist
from sqlpersist import SQLPersist

# import os


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(
    dict(
        DEBUG=True,
    )
)

host = "192.168.1.100"
user = "root"
password = "orionScanner103"
port = 30306
database = "worktime"
table = "hours"
p = SQLPersist(host, user, password, port, database, create=True)
id_query = "id MEDIUMINT NOT NULL AUTO_INCREMENT"
primary = "PRIMARY KEY(id)"
create_table_query = f"""CREATE TABLE {database}.{table}({id_query},
    leaving VARCHAR(10),
    {primary}
    )"""
p.create_table(create_table_query, table)


@app.route("/")
def message():
    h = HaysHours()
    p = SQLPersist(host, user, password, port, database, create=False)
    h.set_db(p)
    lastHourSaved = h.getLastSaved()
    if len(lastHourSaved) > 0:
        return render_template("form.html", lastHourSaved=lastHourSaved)
    else:
        return render_template("form.html")


@app.route("/end/<elapsed>")
def end_hour(elapsed):
    h = HaysHours()
    p = SQLPersist(host, user, password, port, database, create=False)
    h.set_db(p)
    endHour = h.getEnd(elapsed) + "\n"
    return endHour


@app.route("/last")
def last():
    p = SQLPersist(host, user, password, port, database, create=False)
    return p.readLast()


@app.route("/calc", methods=["GET", "POST"])
def calc():
    if request.method == "POST":
        req = request.form
        h = HaysHours()
        p = SQLPersist(host, user, password, port, database, create=False)
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
        p = SQLPersist(host, user, password, port, database, create=False)
        lastHourSaved = p.readLast()
        if lastHourSaved:
            return render_template("form.html", lastHourSaved=lastHourSaved)
        else:
            return render_template("form.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
