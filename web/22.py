import time
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from alist_sdk import AlistClient
from aria2p import Aria2RPC

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_file():
    file_id = request.json['file_id']
    client = AlistClient()
    file_url = client.get_file_url(file_id)
    aria2 = Aria2RPC()
    download = aria2.add_uris([file_url])
    while True:
        status = aria2.tell_status(download.gid)
        if status['status'] == 'complete':
            return jsonify({'status': 'complete', 'time': str(datetime.now())})
        else:
            return jsonify({'status': 'in progress', 'time': str(datetime.now())})
        time.sleep(10)

if __name__ == '__main__':
    app.run(debug=True)
