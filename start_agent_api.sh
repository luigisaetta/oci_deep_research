# listen on all adresses
export HOST=0.0.0.0
export PORT=8080
uvicorn agent_api:app --host $HOST --port $PORT --reload