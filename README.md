[![Build Status](https://travis-ci.com/josecelano/mandelbrot-api.svg?branch=master)](https://travis-ci.com/github/josecelano/mandelbrot-api)

# Mandelbrot API

Online demo: https://mandelbrot-set-periods.online/api

This service is an API to generate two types of Mandelbrot images:
* Image tiles: a tile of the Mandelbrot Set fractal.
* Orbit graphs: graph representing the iterations values for a given Mandelbrot Set point, calculating recursively the formula `f(z) = z² + c` where `z` and `c` are complex numbers.

Sample image tile:  
![Orbit with cycle of period 3](doc/img/mandelbrot-tile-colored-periods.png)

Sample point orbit for point (-0.1,0.7) with period 3:
![Orbit with cycle of period 3](doc/img/mandelbrot-point-orbit-period-3.png)

## Development

Setup (docker build)
```
./bin/dev-setup
```

Run API (dev mode):	
```	
./bin/dev-serve
```
And open http://0.0.0.0:5000/

## Usage

```
docker pull josecelano/mandelbrot-api
docker run -it --rm \
    -p 80:80 \
	-w /app \
    mandelbrot-api
```

## Deploy

The demo environment was deployed to [Digital Ocean Kubernetes](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nginx-ingress-on-digitalocean-kubernetes-using-helm).

You can see the `yaml` files in [deploy/k8s](deploy/k8s) folder.

Init cluster:
```shell
helm install nginx-ingress stable/nginx-ingress --set controller.publishService.enabled=true
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.14.1/cert-manager.crds.yaml
kubectl create namespace cert-manager
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager --version v0.14.1 --namespace cert-manager jetstack/cert-manager
kubectl create -f ./deploy/k8s/production-issuer.yaml
```

Deploy app:
```shell
kubectl create -f ./deploy/k8s/mandelbrot-api.yaml
kubectl create -f ./deploy/k8s/mandelbrot-api-ingress.yaml
```

Re-deploy app after changing docker image:
```
kubectl rollout restart deployment mandelbrot-api
```

## Related projects

This API uses these two command line applications:
* [Console command to generate tiles](https://github.com/josecelano/c-mandelbrot-arbitrary-precision)
* [Console command to generate orbits](https://github.com/josecelano/mandelbrot-orbit)
