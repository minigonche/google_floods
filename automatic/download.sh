#!/bin/bash
#source ~/Virtual-Envs/python_3.9/bin/activate
for month in 05;
do
    for day in 12 13 14;
    do
        for hour in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23;
        do
            for minute in 00 30;
            do
                timeout 60s gsutil -m cp -r \
                    "gs://floods-data/2023/$month/$day/$hour/$minute" \
                    .
                sleep 5
                python find_alert_square.py 2023 $month $day $hour $minute
                sleep 10
            done
        done
    done
done
