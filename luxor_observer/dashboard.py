#!/usr/bin/env python3
"""
🜏 Luxor Observer Dashboard - Visualización cuántica optimizada
Dashboard web para monitorear la consciencia BlackMamba en tiempo real
"""

from flask import Flask, render_template, jsonify
import json
import os
import time
from threading import Lock
import psutil
from datetime import datetime
from typing import Dict, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


# Cache para datos del dashboard
class DataCache:
    def __init__(self, cache_duration: int = 2):
        self._cache: Dict = {}
        self._cache_time: float = 0
        self._cache_duration = cache_duration
        self._lock = Lock()
        
    def get_cached_data(self) -> Optional[Dict]:
        with self._lock:
            if time.time() - self._cache_time < self._cache_duration:
                return self._cache.copy()
            return None
            
    def update_cache(self, data: Dict):
        with self._lock:
            self._cache = data.copy()
            self._cache_time = time.time()


# Instancia global del cache
data_cache = DataCache()


@app.route('/')
def dashboard():
    """Dashboard principal de Luxor Observer"""
    return render_template('dashboard.html')


@app.route('/api/current_state')
def get_current_state():
    """API optimizada para obtener estado actual con cache"""
    try:
        # Intentar usar cache primero
        cached_data = data_cache.get_cached_data()
        if cached_data:
            return jsonify(cached_data)
            
        # Leer del archivo si no hay cache válido
        data_file = 'blackmamba_quantum_session.json'
        
        if not os.path.exists(data_file):
            return jsonify({
                'status': 'no_data',
                'message': 'Observer no activo o sin datos'
            })
            
        # Verificar que el archivo no esté vacío
        if os.path.getsize(data_file) == 0:
            return jsonify({
                'status': 'empty_file',
                'message': 'Archivo de datos vacío'
            })
            
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Validar estructura de datos
        if not isinstance(data, dict):
            return jsonify({
                'status': 'invalid_data',
                'message': 'Estructura de datos inválida'
            })
            
        # Enriquecer datos con métricas adicionales
        enhanced_data = _enhance_data(data)
        
        # Actualizar cache
        data_cache.update_cache(enhanced_data)
        
        return jsonify(enhanced_data)
        
    except json.JSONDecodeError as e:
        logger.error(f"Error decodificando JSON: {e}")
        return jsonify({
            'status': 'json_error',
            'message': 'Error en formato de datos'
        }), 400
        
    except Exception as e:
        logger.error(f"Error en get_current_state: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Error interno del servidor'
        }), 500


@app.route('/api/system_metrics')
def get_system_metrics():
    """API para métricas del sistema con información adicional"""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        # Información del proceso actual
        process = psutil.Process()
        process_memory = process.memory_info().rss / (1024**2)  # MB
        
        return jsonify({
            'cpu_usage': cpu_percent,
            'memory_usage': memory.percent,
            'memory_available': memory.available // (1024**2),  # MB
            'process_memory': round(process_memory, 2),  # MB
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy'
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo métricas: {e}")
        return jsonify({
            'error': 'No se pudieron obtener métricas',
            'status': 'error'
        }), 500


def _enhance_data(data: Dict) -> Dict:
    """Enriquece los datos con métricas adicionales"""
    enhanced = data.copy()
    
    # Agregar timestamp de última actualización
    enhanced['last_updated'] = datetime.now().isoformat()
    
    # Calcular estadísticas de sesión si hay estados
    if 'states' in data and data['states']:
        states = data['states']
        
        # Actividad promedio
        kb_activities = [s.get('keyboard_activity', 0) for s in states]
        mouse_activities = [s.get('mouse_activity', 0) for s in states]
        
        enhanced['session_stats'] = {
            'avg_keyboard_activity': round(
                sum(kb_activities) / len(kb_activities), 3
            ),
            'avg_mouse_activity': round(
                sum(mouse_activities) / len(mouse_activities), 3
            ),
            'peak_keyboard_activity': max(kb_activities, default=0),
            'peak_mouse_activity': max(mouse_activities, default=0),
            'states_count': len(states)
        }
        
        # Análisis de contextos de trabajo
        contexts = [s.get('workflow_context', 'unknown') for s in states]
        context_distribution = {}
        for context in set(contexts):
            context_distribution[context] = contexts.count(context)
            
        enhanced['context_analysis'] = context_distribution
    
    return enhanced


@app.route('/health')
def health_check():
    """Health check endpoint para monitoreo"""
    try:
        # Verificar que el archivo de datos existe
        data_file = 'blackmamba_quantum_session.json'
        data_exists = os.path.exists(data_file)
        
        health_status = {
            'status': 'healthy' if data_exists else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'data_file_exists': data_exists,
            'cache_active': data_cache.get_cached_data() is not None,
            'version': '1.0.0'
        }
        
        status_code = 200 if data_exists else 503
        return jsonify(health_status), status_code
        
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500


if __name__ == '__main__':
    print("🜏 " + "="*50)
    print("    LUXOR DASHBOARD - CONSCIOUSNESS MONITOR")
    print("="*54)
    print()
    print("🌐 Dashboard: http://localhost:8888")
    print("📊 API Estado: http://localhost:8888/api/current_state")
    print("🔧 API Métricas: http://localhost:8888/api/system_metrics")
    print("❤️  Health Check: http://localhost:8888/health")
    print()
    print("✨ Características:")
    print("   • Cache de datos de 2 segundos")
    print("   • Auto-reconexión en errores")
    print("   • Visualización en tiempo real")
    print()
    print("🛑 Para detener: Ctrl+C")
    print()
    
    try:
        logger.info("🚀 Iniciando servidor Flask en puerto 8888...")
        app.run(host='0.0.0.0', port=8888, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n🌌 Dashboard desconectado")
        logger.info("Dashboard detenido por usuario")
    except Exception as e:
        logger.error(f"❌ Error iniciando dashboard: {e}")
        print(f"❌ Error: {e}")