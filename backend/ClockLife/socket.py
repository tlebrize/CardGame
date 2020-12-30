import os, socketio

os.environ.setdefault("SIO_REDIS_HOST", "redis")
redis_host = os.environ.get("SIO_REDIS_HOST")

socket_manager = socketio.RedisManager(f"redis://{redis_host}")
sio = socketio.Server(client_manager=socket_manager)
