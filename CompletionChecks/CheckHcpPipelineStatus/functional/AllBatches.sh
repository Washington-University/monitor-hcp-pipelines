#!/bin/bash

./Batch01.sh
./Batch02.sh
./Batch03.sh
./Batch04.sh
./Batch05.sh
./Batch06.sh
./Batch07.sh
./Batch08.sh
./Batch09.sh
./Batch10.sh
./Batch11.sh

cat Batch01.out Batch02.out Batch03.out Batch04.out Batch05.out Batch06.out Batch07.out Batch08.out Batch09.out Batch10.out Batch11.out > AllBatches.out
