#!/bin/bash

cd /var/www/git/Plants/NLP/word2vec/features/embed_import/;
wget https://doc-0g-8s-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/o2tin09msf2l8dqq8qqfl8cuth1r0vun/1491688800000/06848720943842814915/*/0B7XkCwpI5KDYNlNUTTlSS21pQmM;
gunzip -k 0B7XkCwpI5KDYNlNUTTlSS21pQmM;
mv 0B7XkCwpI5KDYNlNUTTlSS21pQmM GoogleNews-vectors-negative300.bin;
python convert.py;
cp GoogleNews-vectors-negative300.csv /var/www/git/Plants/NLP/word2vec/classify/0_data_source/GoogleNews-vectors-negative300.csv;