#!/usr/bin/env sh

#echo "Migrations"
#cd db/migrations || exit
#alembic upgrade head || exit
#cd ../..
echo "Run server"
uvicorn main:app --host 0.0.0.0 --port 8001 --reload