#!/bin/bash
echo '*** SERIOT1:'
ssh seriot1 "$@"
echo '*** SERIOT2:'
ssh seriot2 "$@"
echo '*** SERIOT3:'
ssh seriot3 "$@"
echo '*** SERIOT4:'
ssh seriot4 "$@"
echo '*** SERIOT5:'
ssh seriot5 "$@"
echo '*** SERIOT6:'
ssh seriot6 "$@"


