#!/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="install.sh"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

pip install --upgrade pip && pip install -r requirements.txt