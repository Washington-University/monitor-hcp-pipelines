#!/bin/bash

./batch01.sh
./batch02.sh
./batch03.sh
./batch04.sh
./batch05.sh
./batch06.sh
./batch07.sh
./batch08.sh
./batch09.sh
./batch10.sh
./batch11.sh

cat batch01.out batch02.out batch03.out batch04.out batch05.out batch06.out batch07.out batch08.out batch09.out batch10.out batch11.out > allbatches.out
