import logging
import time
from signalrcore.hub_connection_builder import HubConnectionBuilder  

server_url = "https://localhost:5001/chatHub"

end = False

def bye(error, x):
    global end
    end = True
    if error:
        print("error {0}".format(x))
    else:
        print("complete! ")
    global hub_connection

hub_connection = HubConnectionBuilder()\
    .with_url(server_url, options={"verify_ssl": False}) \
    .configure_logging(logging.DEBUG, socket_trace=True).build()


hub_connection.start()

hub_connection.stream(
    "Counter",
    [10, 500]).subscribe({
        "next": lambda x: print("next callback: ", x),
        "complete": lambda x: bye(False, x),
        "error": lambda x: bye(True, x)
    })


hub_connection.on("ReceiveMessage", print)


while not end:
    time.sleep(1)
    hub_connection.send("SendMessage", ["mandrewcito", "andresito"])

hub_connection.stop()
