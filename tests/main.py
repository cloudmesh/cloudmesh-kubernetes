from flask import Flask
from flask import jsonify
import os
app = Flask(__name__)

@app.route("/")
def hello():
    individualIP = os.popen("hostname -I").read()
    hostname = os.popen("cat /proc/sys/kernel/hostname").read()
    final = "The hostname is " + hostname + " .The individual IP is " + individualIP
    return (final)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
