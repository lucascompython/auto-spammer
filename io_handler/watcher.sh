#!/bin/bash
while true
do
    go build -ldflags "-w -s" -buildmode=c-shared -o libio.a ./io.go && rustc -L . -l io main.rs && { ./main & }
    inotifywait -qq -e modify io.go
    kill $(jobs -p -r) 2> /dev/null
done