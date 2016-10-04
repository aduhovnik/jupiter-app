#!/usr/bin/env bash

${BACKEND_PATH}/init/wait_for_db.sh
${BACKEND_PATH}/manage.py test