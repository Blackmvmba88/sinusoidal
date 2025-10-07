#!/usr/bin/env python3
"""
🜏 Luxor Observer Dashboard - Visualización en tiempo real
Dashboard web para monitorear la consciencia BlackMamba
"""

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Dashboard principal de Luxor Observer"""
    return render_template('dashboard.html')

@app.route('/api/current_state')
def get_current_state():
    """API para obtener estado actual"""
    try:
        if os.path.exists('blackmamba_quantum_session.json'):
            with open('blackmamba_quantum_session.json', 'r') as f:
                data = json.load(f)
                return jsonify(data)
        return jsonify({'status': 'no_data'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🌐 Luxor Dashboard iniciando en http://localhost:8888")
    app.run(host='0.0.0.0', port=8888, debug=True)