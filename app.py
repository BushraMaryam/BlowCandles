from flask import Flask, render_template
from flask_socketio import SocketIO
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('audio_data')
def handle_audio(data):
    """Receives audio levels from frontend and determines if candles should blow out."""
    volume_levels = np.array(data)
    avg_volume = np.mean(volume_levels)
    
    print(f"Received Volume: {avg_volume}")  # Debugging
    
    if avg_volume > 20:  # Threshold for blowing out candles
        socketio.emit('blow_out_candles')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=10000, debug=True)

