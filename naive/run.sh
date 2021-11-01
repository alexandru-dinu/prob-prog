#!/bin/bash

SCRIPT=naive
NUM=100000

echo "Haskell"
ghc --make -dynamic -O2 ${SCRIPT}.hs -i ~/workspace/git/probe.git/haskell/randomness.hs
time ./${SCRIPT} ${NUM} >/dev/null

echo '---'

echo "Python"
time python ${SCRIPT}.py --num_samples ${NUM} --s 1 --f 5 >/dev/null

rm -v ${SCRIPT} *.hi *.o
