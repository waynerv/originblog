#!/usr/bin/env bash
echo "Creating mongo users..."
mongo admin --host localhost -u root -p example --eval "db = db.getSiblingDB('originblog'); db.createUser({user: 'originblog', pwd: 'PASSWORD', roles: [{role: 'dbOwner', db: 'originblog'}]});"
echo "Mongo users created."