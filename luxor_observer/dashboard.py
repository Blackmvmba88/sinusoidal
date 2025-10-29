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
    data_file = 'blackmamba_quantum_session.json'
    
    try:
        # Intentar usar cache primero
        cached_data = data_cache.get_cached_data()
        if cached_data:
            return jsonify(cached_data)
            
        # Verificar que el archivo existe
        if not os.path.exists(data_file):
            return jsonify({
                'status': 'no_data',
                'message': 'Observer no activo o sin datos',
                'timestamp': datetime.now().isoformat()
            })
        
        # Verificar que el archivo no esté vacío
        try:
            file_size = os.path.getsize(data_file)
            if file_size == 0:
                return jsonify({
                    'status': 'empty_file',
                    'message': 'Archivo de datos vacío',
                    'timestamp': datetime.now().isoformat()
                })
        except OSError as e:
            logger.error(f"Error accediendo al archivo: {e}")
            return jsonify({
                'status': 'file_error',
                'message': 'Error accediendo al archivo de datos'
            }), 500
        
        # Leer archivo con timeout implícito y manejo de errores
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error decodificando JSON: {e}")
            return jsonify({
                'status': 'json_error',
                'message': 'Error en formato de datos'
            }), 400
        except IOError as e:
            logger.error(f"Error leyendo archivo: {e}")
            return jsonify({
                'status': 'io_error',
                'message': 'Error leyendo archivo de datos'
            }), 500
            
        # Validar estructura de datos
        if not isinstance(data, dict):
            logger.warning("Datos no son un diccionario")
            return jsonify({
                'status': 'invalid_data',
                'message': 'Estructura de datos inválida'
            }), 400
        
        # Enriquecer datos con métricas adicionales
        try:
            enhanced_data = _enhance_data(data)
        except Exception as e:
            logger.error(f"Error enriqueciendo datos: {e}")
            # Retornar datos básicos si el enriquecimiento falla
            enhanced_data = data
            enhanced_data['last_updated'] = datetime.now().isoformat()
        
        # Actualizar cache
        data_cache.update_cache(enhanced_data)
        
        return jsonify(enhanced_data)
        
    except Exception as e:
        logger.error(f"Error inesperado en get_current_state: {e}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'Error interno del servidor',
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/system_metrics')
def get_system_metrics():
    """API para métricas del sistema con información adicional"""
    try:
        # Obtener métricas de CPU con intervalo corto
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Obtener información de memoria
        try:
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available // (1024**2)  # MB
        except (AttributeError, psutil.Error) as e:
            logger.warning(f"Error obteniendo info de memoria: {e}")
            memory_percent = 0
            memory_available = 0
        
        # Información del proceso actual
        try:
            process = psutil.Process()
            process_memory = process.memory_info().rss / (1024**2)  # MB
            process_cpu = process.cpu_percent(interval=0.1)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.Error) as e:
            logger.warning(f"Error obteniendo info del proceso: {e}")
            process_memory = 0
            process_cpu = 0
        
        return jsonify({
            'cpu_usage': round(cpu_percent, 2),
            'memory_usage': round(memory_percent, 2),
            'memory_available': memory_available,
            'process_memory': round(process_memory, 2),
            'process_cpu': round(process_cpu, 2),
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy'
        })
        
    except Exception as e:
        logger.error(f"Error inesperado obteniendo métricas: {e}", exc_info=True)
        return jsonify({
            'error': 'No se pudieron obtener métricas',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


def _enhance_data(data: Dict) -> Dict:
    """Enriquece los datos con métricas adicionales"""
    try:
        enhanced = data.copy()
        
        # Agregar timestamp de última actualización
        enhanced['last_updated'] = datetime.now().isoformat()
        
        # Calcular estadísticas de sesión si hay estados
        if 'states' in data and data['states']:
            states = data['states']
            
            if not isinstance(states, list):
                logger.warning("states no es una lista, omitiendo estadísticas")
                return enhanced
            
            # Filtrar estados válidos
            valid_states = [s for s in states if isinstance(s, dict)]
            
            if not valid_states:
                return enhanced
            
            # Actividad promedio con validación
            kb_activities = []
            mouse_activities = []
            
            for s in valid_states:
                try:
                    kb = s.get('keyboard_activity', 0)
                    mv = s.get('mouse_activity', 0)
                    # Validar que sean números
                    kb_activities.append(float(kb) if kb is not None else 0.0)
                    mouse_activities.append(float(mv) if mv is not None else 0.0)
                except (ValueError, TypeError):
                    continue
            
            if kb_activities and mouse_activities:
                enhanced['session_stats'] = {
                    'avg_keyboard_activity': round(
                        sum(kb_activities) / len(kb_activities), 3
                    ),
                    'avg_mouse_activity': round(
                        sum(mouse_activities) / len(mouse_activities), 3
                    ),
                    'peak_keyboard_activity': round(max(kb_activities, default=0), 3),
                    'peak_mouse_activity': round(max(mouse_activities, default=0), 3),
                    'states_count': len(valid_states)
                }
            
            # Análisis de contextos de trabajo con Counter para eficiencia
            try:
                from collections import Counter
                contexts = [
                    s.get('workflow_context', 'unknown') 
                    for s in valid_states 
                    if 'workflow_context' in s
                ]
                context_distribution = dict(Counter(contexts))
                enhanced['context_analysis'] = context_distribution
            except Exception as e:
                logger.debug("Error analizando contextos: %s", e)
        
        return enhanced
    except Exception as e:
        logger.error("Error enriqueciendo datos: %s", e)
        # Retornar datos originales con timestamp si falla
        return {**data, 'last_updated': datetime.now().isoformat()}


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