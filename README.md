# Simple Flask App for microk8s Test on Rapsberry pi-4

## History

I wrote it to learn and both to get one little tool
to convert the decimal time of workous into a start
and quit hour when I worked for Hays.

## Form Usage

- The starting time is fixed to 07:30.

- Once started `http://localhost:5000` allows to enter
  the decimal elapsed time in a form.

The submit will call the "backend" method `getEnd`
of `HaysHours` object.

### Flask template

- `form.html`

## API

It is also possible to use an API.

For sample
`http://localhost:5000/calc/8.5`

### Flask template

- `api.html`
