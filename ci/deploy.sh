#!/usr/bin/env bash

echo -e "\033[34mEncrypting ssh identity file...\033[0m"
openssl enc -d -aes-256-cbc -k ${DECRYPT_KEY_PASSWORD} -in ${SSH_IDENTITY_FILE} -out jupiter_key
chmod 600 jupiter_key

echo -e "\033[34mCopying docker-compose.yml configuration file...\033[0m"
scp -i jupiter_key docker-compose.build.yml ${SSH_USER}@${HOST}:docker-compose.yml

echo -e "\033[34mStopping containers...\033[0m";
ssh -i jupiter_key ${SSH_USER}@${HOST} docker-compose stop

echo -e "\033[34mRemoving backend and frontend containers...\033[0m";
ssh -i jupiter_key ${SSH_USER}@${HOST} docker-compose rm -f backend frontend

echo -e "\033[34mPulling newer images...\033[0m";
ssh -i jupiter_key ${SSH_USER}@${HOST} docker-compose pull

echo -e "\033[34mRunning containers...\033[0m";
ssh -i jupiter_key ${SSH_USER}@${HOST} docker-compose up -d