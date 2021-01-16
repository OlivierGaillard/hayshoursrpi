from flask import Flask, request, render_template, redirect
from flask import escape
from hayshours import HaysHours

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG=True,
))

@app.route('/')
def message():
    return render_template('form.html', )

@app.route('/end/<elapsed>')
def end_hour(elapsed):
    h = HaysHours()
    endHour = h.getEnd(elapsed)
    s = 'Start hour: 07:30 and quit at {}'.format(endHour)
    return render_template('api.html', endHour=endHour, elapsed=elapsed)

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    if request.method == "POST":
        req = request.form
        print(req)
        h = HaysHours()
        elapsed = req.get('elapsed')
        endHour = h.getEnd(elapsed)
        print('endHour: ', endHour)
        if len(elapsed) == 0:
            err_msg = 'No end-time because no elapsed time given.'
            return render_template('form.html', err_msg=err_msg)
        return render_template('form.html', endHour=endHour, elapsed=elapsed)
    else:
        return render_template('form.html', )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
