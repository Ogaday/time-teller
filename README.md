# Time Teller

Long running process running in Docker on k8s demo.

## Python

`time_teller.py` is a simple python script intended to represent a long running
process. Every `n` seconds, it logs the current time to the console. The
message format and `n` itself can be configured by setting environment
variables. eg:

```bash
$ python -m time_teller
2020-03-23T11:33:15
2020-03-23T11:33:30
^C
$ TIME_TELLER__STEP=3 python -m time_teller 
2020-03-23T11:34:24
2020-03-23T11:34:27
2020-03-23T11:34:30
^C
$ export TIME_TELLER__LOG_TEMPLATE="It is %c"
$ python -m time_teller
It is Mon Mar 23 11:38:30 2020
It is Mon Mar 23 11:38:45 2020
^C
```

- `TIME_TELLER__STEP` should be between `1` and `60`. Otherwise it will be
  rounded up or down.
- `TIME_TELLER__LOG_TEMPLATE` gets treated as a python time format string. See
  the [docs](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)
  for more details.

## Docker

```bash
$ # Build the image, then run the container (with config)
$ docker build -t <tag> .
$ docker run <tag>
2020-03-23T11:22:15
2020-03-23T11:22:30
^C
$ docker run \
    -e TIME_TELLER__STEP=2 \
    -e TIME_TELLER__LOG_TEMPLATE="The time is: %H:%M:%S" \
    <tag>
The time is: 11:21:22
The time is: 11:21:24
^C
$ # Upload to the image to docker hub
$ docker image push repo/<tag>:<optional-version>
```

## Kubernetes

To deploy the container to kubernetes, there is a `deployment.yml` file.

I use [microk8s](https://microk8s.io/) for my kubernetes cluster, but it should
be similar for any distribution.

The behaviour is configured via the env vars in the deployment manifest.

```bash
$ kubectl apply -f deployment.yml
deployment.apps/time-teller-deployment created
$ kubectl get pods
NAME                                    READY  STATUS   RESTARTS  AGE 
time-teller-deployment-d87696944-wpncp  1/1    Running  0         39s
$ kubectl logs -f time-teller-deployment-d87696944-wpncp
It is Mon Mar 23 14:11:10 2020
It is Mon Mar 23 14:11:12 2020
...
```
