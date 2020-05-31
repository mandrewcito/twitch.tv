import logging
import time
import psutil
from signalrcore.hub_connection_builder import HubConnectionBuilder  


server_url = "https://localhost:5001/chatHub"


hub_connection = HubConnectionBuilder()\
    .with_url(server_url, options={"verify_ssl": False}) \
    .configure_logging(logging.DEBUG, socket_trace=True).build()


hub_connection.start()


message =""
max = 10
i = 0
while i < 100:
    time.sleep(3)
    hub_connection.send("SendMessage", 
    ["andresito", {
        "cpu": psutil.cpu_percent(),
        "disk": psutil.disk_usage('/').percent,
        "ram": psutil.virtual_memory().percent
    }])
    i += 1

