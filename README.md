# Fluvial Metapop Persistance

This repository contains the data and code for the paper "A note on the role of seasonal expansions and contractions of the flowing fluvial network on metapopulation persistence" by J. Giezendanner, P. Benettin, Nicola Durighetto, G. Botter and A. Rinaldo.

## Setup
Clone the [repo](https://github.com/GieziJo/FluvialMetapopPersistance.git) with:
```shell
git clone https://github.com/GieziJo/FluvialMetapopPersistance.git
```
To get the same working coding environment used during the assessment (with all packages installed), pull the docker image with:
```shell
docker pull bobgiezi/meta-landscape
```
Then launch the docker image with (bash for windows)
```shell
docker run --rm -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v /$(cmd //c cd):/home/jovyan/work bobgiezi/meta-landscape
```
or by running
```shell
sh runJupyterDocker.sh
```
You can then open jupyter lab in your browser (link in the shell, usually `http://127.0.0.1:8888/?token=yourToken`).
The command "`-v /$(cmd //c cd):/home/jovyan/work/`" permits to mount the current folder to the docker container.
Once jupyter lab opened, navigate to `/home/jovyan/work/`, then open and run all cells `main.ipynb` to see the main results.