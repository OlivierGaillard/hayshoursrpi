# Simple Flask App for microk8s Test on Rapsberry pi-4

## History

I wrote it to learn and both to get one little tool
to convert the decimal time of workous into a start
and quit hour when I worked for Hays.

## Tests

### Create a Virtualenv with Python3

Use the `requests.txt` and e.g. virtualenvwrapper.
Then `workon`.

### Testing  the pod created `hoursdata-pod`

- ` kubectl port-forward hoursdata-pod 5000:5000`
- `python test_server.py`

### Testing the Server Containerized

To test the server containerized execute:

- `python server.py` to run the flask server
- `python test_server.py`

## K8S Usages

### Versions of Image `gaillardo/hayshoursrpi`

- test and latest are stateless

- `datavol` uses an host volume on the node to store the last
  quitting hour. Just a singleton pod is created. This is not
  a deployment. To access the website:
  `kubectl port-forward <pod-name> localport:5000`

## Volume of Pod `hoursdata-pod` 

The `hostPath` of `pod_raspi.yaml` define a volume path `/home/ubuntu`
on the node running the pod. The `volumeMounts` set the mount
path to `/data` for the container image.

`kubectl exec hoursdata-pod ls /data` returns `db1`, which is the
fixed `dbname` defined in `server.py`.

`server.py` uses the environment variable `ROOTDIR` to use the
mount path set by the pod definition.

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

### `test_server.py`

```
class TestServer(unittest.TestCase):

    def test_calcformpage(self):
        r = requests.get('http://localhost:5000/calc')
        self.assertEqual(200, r.status_code)

    def test_end(self):
        r = requests.get('http://localhost:5000/end/8.5')
        self.assertEqual('16:30:00\n', r.text)

    def test_last(self):
        requests.get('http://localhost:5000/end/9')
        r = requests.get('http://localhost:5000/last')
        self.assertEqual('17:30:00\n', r.text)
```

### Flask template

- `api.html`

## Github

[Hayshours source](https://github.com/OlivierGaillard/hayshoursrpi)
