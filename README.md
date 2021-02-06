# Simple Flask App for MicroK8s Test on Rapsberry pi-4

## History

I wrote it to learn and both to get one little tool
to convert the decimal time of workours e.g. 8.4 into a starting
and leaving times, what were required  by the accounting website of
Hays.

I wrote it first in Python, then in Go. This version for Kubernetes
is written with Python again.

## Home Cluster

The nodes are made of four raspberry-pi with 128 Gb cards.
I tried with two nodes of 32 Gb and two of 16 Gb but the
small ones often crashed.

The image used is an Ubuntu one: `ubuntu-20.04.1-preinstalled-server-arm64+raspi.img.xz`.
The setup is explained both on [MicroK8s](https://microk8s.io/)
and on [Ubuntu](https://ubuntu.com/tutorials/how-to-kubernetes-cluster-on-raspberry-pi#1-overview).

Her is a picture of the cluster.

![cluster](rpi-cluster.jpg)

Once `kubectl proxy` is running we can access the dashboard.

![cluster](dashboard.png)


### Note on Node `n3`

On this node the raspberry pi image is built. It could be
any another node.

## Create a Virtualenv with Python3

Use the `requests.txt` and e.g. with *virtualenvwrapper.*
`mkvirtualenv <your venv-name>`.
Then `workon` and select <your venv-name>`. See [virtualenvwrapper doc](https://virtualenvwrapper.readthedocs.io/en/latest/).

To install *MariaDB* client and `mysql-connector-python`
some special packages where required with debian.

# Tests

To run all tests: `python -m unittest`.

## Testing  the Service  `hours-service`

`test_server L|K`:

- `L' uses the `flask` server locally
- `K` uses the Kubernetes service

- `python test_server.py K`

## K8S Usages

# Versions of Image `gaillardo/hayshoursrpi`

- test and latest are stateless

- `datavol` uses an host volume on the node to store the last
  quitting hour. Just a singleton pod is created. This is not
  a deployment. To access the website:
  `kubectl port-forward <pod-name> localport:5000`

- Tag `sql` refers to... SQL version with MariaDB.

## Test the image

- `docker run -it <image> /bin/bash`. Then:
  - `python3 test_sql.py` to test MariaDB connection and
    usage of the PyMySQL client.

## Version with Volume of Pod `hoursdata-pod`

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

# Note: Future Version

- The next version will use `StateFulSets`

- Configmap for MariaDB to create the database and its unique table
  (Now when the flask server starts it initializes the database.)

- The starting time is fixed to 07:30.

### Flask template

- `form.html`

## API

It is also possible to use an API.

### `test_server.py`

Two modes for this test, *local* or *K8S*. To use the local
one you have to run the Flask server with `python server.py`
and then `python test_server.py L` with the *L* flag.

To use the Kubernetes Service set the URL to the variable
`K8S` to one of your node and `python test_server K`.
No specific node is required because a *NodePort* is
declared in `deployment_raspi_sql.yaml`:

``
metadata:
  name: hours-service
  labels:
    app: hayshours
spec:
  type: NodePort
  selector:
    app: hayshours
  ports:
    - protocol: "TCP"
      port: 8989
      targetPort: 5000
      nodePort: 30036
``

This test add entries in the table `hours` of the database
`worktime`.

When the server starts it initializes the database and the
table if they do not exist.


```
class TestServer(unittest.TestCase):

    def test_calcformpage(self):
        r = requests.get('http://localhost:5000/calc')
        self.assertEqual(200, r.status_code)

    def test_end(self):
        r = requests.get('http://localhost:5000/end/8.5')
        self.assertEqual('16:30:00', r.text)

    def test_last(self):
        requests.get('http://localhost:5000/end/9')
        r = requests.get('http://localhost:5000/last')
        self.assertEqual('17:30:00', r.text)
```

### Flask template

- `api.html`

## Github

[Hayshours source](https://github.com/OlivierGaillard/hayshoursrpi)
[Docker Hub](https://hub.docker.com/repository/docker/gaillardo/hayshoursrpi)
