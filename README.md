# Simple Flask App for microk8s Test on Rapsberry pi-4

## History

I wrote it to learn and both to get one little tool
to convert the decimal time of workous into a start
and quit hour when I worked for Hays.

The nodes are made of four raspberry-pi with 128 Gb cards.
I tried with two nodes of 32 Gb and two of 16 Gb but the
small ones often crashed.

## Note on Node `n3`

On this node the raspberry pi image is built. It could be
any another node.

## Tests

### Create a Virtualenv with Python3

Use the `requests.txt` and e.g. with *virtualenvwrapper.*
`mkvirtualenv <your venv-name>`.
Then `workon` and select <your venv-name>`. See [virtualenvwrapper doc](https://virtualenvwrapper.readthedocs.io/en/latest/).

To install *MariaDB* client and `mysql-connector-python`
some special packages where required with debian.

### Testing  the Service  `hours-service`

`test_server L|K`:

- `L' uses the `flask` server locally
- `K` uses the Kubernetes service

- `python test_server.py K`

## K8S Usages

### Versions of Image `gaillardo/hayshoursrpi`

- test and latest are stateless

- `datavol` uses an host volume on the node to store the last
  quitting hour. Just a singleton pod is created. This is not
  a deployment. To access the website:
  `kubectl port-forward <pod-name> localport:5000`

- Tag `sql` refers to... SQL version with MariaDB.

#### Test the image



## Volume of Pod `hoursdata-pod`

The `hostPath` of `pod_raspi.yaml` defines a volume path `/home/ubuntu`
on the node running the pod. The `volumeMounts` set the mount
path to `/data` for the container image.

`kubectl exec hoursdata-pod ls /data` returns `db1`, which is the
fixed `dbname` defined in `server.py`.

`server.py` uses the environment variable `ROOTDIR` to use the
mount path set by the pod definition.

## Volume for MariaDB

The node `n3` is an nfs server whose exported directory is used as
Kubernetes volume. See the definitions here:
- `nfs-volume.yaml`
- `nfs-volume-claim.yaml`

I followed the setup from the book *Kubernetes Up & Running* from chapter
15 about storage solutions. In place of MySQL I used MariaDB to build
a *singleton* pod.

In the present implementation the test `test_stateful_withsql.py` will
connect to the MariaDB, create a database and one table, store leaving
hour as text. After the test the database is deleted.

### Note: Future Version

The next version will use `StateFulSets`

### Configmap for MariaDB

To create the database and its unique table I will use a configmap.

#### Temporary Solution

Once the flask server starts it initialize the database.

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
