#!/bin/bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use node

cd ../

git pull;

SRC=/work/secondproject/node-backend
DEST=/$HOME/deploy

rm -rf $DEST
mkdir -p $DEST
cp -rf $SRC $DEST

cd $DEST

source ~/.bashrc

npm install

if pm2 list | grep -q 'online'; then
    pm2 restart all
else
    pm2 start npm --name "app" -- run start
fi