from flask import Flask, request, render_template
from hayshours import HaysHours
from persist import FilePersist
import os


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG=True,
))

rootdir = os.getenv('ROOTDIR', './tmp')
dbname = 'db1'


@app.route('/')
def message():
    h = HaysHours()
    p = FilePersist(rootdir, dbname)
    h.set_db(p)
    lastHourSaved = h.getLastSaved()
    if len(lastHourSaved) > 0:
        return render_template('form.html', lastHourSaved=lastHourSaved)
    else:
        return render_template('form.html')


@app.route('/end/<elapsed>')
def end_hour(elapsed):
    h = HaysHours()
    p = FilePersist(rootdir, dbname)
    h.set_db(p)
    endHour = h.getEnd(elapsed) + '\n'
    return endHour


@app.route('/last')
def last():
    p = FilePersist(rootdir, dbname)
    return p.readLast()


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    if request.method == "POST":
        req = request.form
        h = HaysHours()
        p = FilePersist(rootdir, dbname)
        h.set_db(p)
        lastHourSaved = h.getLastSaved()
        elapsed = req.get('elapsed')
        endHour = h.getEnd(elapsed)
        if len(elapsed) == 0:
            err_msg = 'No end-time because no elapsed time given.'
            return render_template('form.html', err_msg=err_msg)
        if len(lastHourSaved) > 0:
            return render_template('form.html',
                endHour=endHour,
                elapsed=elapsed,
                lastHourSaved=lastHourSaved)
        else:
            return render_template('form.html', endHour=endHour, elapsed=elapsed)
    else:
        p = FilePersist(rootdir, dbname)
        lastHourSaved = p.readLast()
        if len(lastHourSaved) > 0:
            return render_template('form.html', lastHourSaved=lastHourSaved)
        else:
            return render_template('form.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
