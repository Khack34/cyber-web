from flask import Flask, request
import os
import datetime

app = Flask(__name__)

LOG_FILE = "access.log"

def apache_log(req):
    ip = req.remote_addr
    time = datetime.datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
    method = req.method
    path = req.full_path
    status = 200
    return f'{ip} - - [{time}] "{method} {path} HTTP/1.1" {status} -\n'

@app.after_request
def log_request(response):
    with open(LOG_FILE, "a") as f:
        f.write(apache_log(request))
    return response

@app.route("/")
def home():
    return "Vulnerable Lab is LIVE"

@app.route("/search")
def search():
    q = request.args.get("q", "")
    return f"Search result: {q}"   # Reflected XSS

@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    os.system(f"ping -c 1 {host}")  # Command Injection
    return "Ping executed"

@app.route("/view")
def view():
    file = request.args.get("file", "")
    try:
        return open(file).read()    # LFI
    except:
        return "File not found"

@app.route("/admin")
def admin():
    return "Admin Panel - No Auth"

@app.route("/logs")
def logs():
    return "<pre>" + open(LOG_FILE).read() + "</pre"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
