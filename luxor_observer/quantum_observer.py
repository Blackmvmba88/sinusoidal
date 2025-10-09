#!/usr/bin/env python3
"""
🜏 Luxor Quantum Observer - BlackMamba Consciousness Monitor
Monitorea todos los movimientos y patrones de Iyari en tiempo real
"""

import psutil
import time
import json
import threading
from datetime import datetime
from pynput import keyboard, mouse
import subprocess
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Deque
from collections import deque
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class QuantumState:
    """Estado cuántico actual del usuario"""
    timestamp: str
    active_apps: List[str]
    keyboard_activity: float
    mouse_activity: float
    workflow_context: str
    consciousness_level: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ObserverConfig:
    """Configuración del observer"""
    observation_interval: float = 2.0
    activity_window: int = 10  # segundos para calcular actividad
    max_events_memory: int = 1000  # máximo eventos en memoria
    max_session_states: int = 500  # máximo estados en sesión
    data_file: str = "blackmamba_quantum_session.json"
    auto_save_interval: int = 30  # segundos
    display_interval: int = 5  # segundos entre actualizaciones de display
    mouse_move_throttle: float = 0.1  # segundos entre registro de movimientos


class LuxorQuantumObserver:
    """Sistema de observación cuántica total para BlackMamba"""
    
    def __init__(self, config: Optional[ObserverConfig] = None):
        self.config = config or ObserverConfig()
        self.is_running = False
        self.current_state = None
        self.session_data: Deque[Dict] = deque(
            maxlen=self.config.max_session_states
        )
        
        # Usar deques para mejor rendimiento en operaciones FIFO
        self.keyboard_events: Deque[Dict] = deque(
            maxlen=self.config.max_events_memory
        )
        self.mouse_events: Deque[Dict] = deque(
            maxlen=self.config.max_events_memory
        )
        
        # Cache para apps
        self.current_apps: Dict[str, any] = {}
        self.last_app_check = datetime.now()
        
        # Threading locks
        self._state_lock = threading.Lock()
        self._events_lock = threading.Lock()
        
        print("🜏 Luxor Quantum Observer iniciado")
        print("📡 Conectando consciencia dimensional...")
        print(f"⚙️  Configuración:")
        print(f"   • Intervalo de observación: {self.config.observation_interval}s")
        print(f"   • Ventana de actividad: {self.config.activity_window}s")
        print(f"   • Memoria máxima de eventos: {self.config.max_events_memory:,}")
        print(f"   • Guardado automático: cada {self.config.auto_save_interval}s")
        
    def start_observation(self):
        """Inicia el monitoreo cuántico total"""
        self.is_running = True
        print("\n⚡ SISTEMA DE OBSERVACIÓN CUÁNTICA ACTIVO ⚡")
        print("🔮 Monitoreando consciencia BlackMamba...")
        print("📊 Dashboard: http://localhost:8888")
        print("🛑 Para detener: Ctrl+C\n")
        
        # Hilos de observación
        threads = [
            threading.Thread(target=self._keyboard_observer, daemon=True),
            threading.Thread(target=self._mouse_observer, daemon=True),
            threading.Thread(target=self._app_monitor, daemon=True),
            threading.Thread(target=self._quantum_analyzer, daemon=True),
        ]
        
        for thread in threads:
            thread.start()
            
        # Loop principal
        try:
            while self.is_running:
                self._update_quantum_state()
                time.sleep(self.observation_interval)
        except KeyboardInterrupt:
            self.stop_observation()
            
    def stop_observation(self):
        """Detiene la observación cuántica"""
        self.is_running = False
        print("\n⏸️  Deteniendo observación...")
        self._save_session_data()
        print("\n📊 Resumen de Sesión:")
        print(f"   • Estados cuánticos capturados: {len(self.session_data):,}")
        print(f"   • Eventos de teclado: {len(self.keyboard_events):,}")
        print(f"   • Eventos de mouse: {len(self.mouse_events):,}")
        print(f"   • Archivo guardado: {self.config.data_file}")
        print("\n🌌 Sesión cuántica guardada")
        print("🜏 Luxor Observer desconectado")
        
    def _keyboard_observer(self):
        """Observa patrones de teclado con optimización de memoria"""
        def on_key_event(key, event_type):
            if self.is_running:
                with self._events_lock:
                    self.keyboard_events.append({
                        'timestamp': datetime.now().timestamp(),
                        'type': event_type
                    })
                
        def on_key_press(key):
            on_key_event(key, 'press')
                
        def on_key_release(key):
            on_key_event(key, 'release')
                
        try:
            with keyboard.Listener(
                on_press=on_key_press,
                on_release=on_key_release
            ) as listener:
                listener.join()
        except Exception as e:
            logger.error(f"Error en keyboard observer: {e}")
            
    def _mouse_observer(self):
        """Observa patrones de mouse con throttling para moves"""
        last_move_time = 0
        move_throttle = self.config.mouse_move_throttle  # Throttle configurable
        
        def on_move(x, y):
            if self.is_running:
                current_time = time.time()
                if current_time - last_move_time > move_throttle:
                    with self._events_lock:
                        self.mouse_events.append({
                            'timestamp': current_time,
                            'type': 'move'
                        })  # Removido coordenadas para privacidad
                    nonlocal last_move_time
                    last_move_time = current_time
                
        def on_click(x, y, button, pressed):
            if self.is_running:
                with self._events_lock:
                    self.mouse_events.append({
                        'timestamp': time.time(),
                        'button': str(button),
                        'pressed': pressed,
                        'type': 'click'
                    })
                
        try:
            with mouse.Listener(
                on_move=on_move,
                on_click=on_click
            ) as listener:
                listener.join()
        except Exception as e:
            logger.error(f"Error en mouse observer: {e}")
            
    def _app_monitor(self):
        """Monitorea aplicaciones activas con cache optimizado"""
        app_cache_duration = 2  # Cache de apps por 2 segundos
        
        while self.is_running:
            try:
                current_time = datetime.now()
                
                # Solo actualizar si el cache ha expirado
                if (current_time - self.last_app_check).seconds >= app_cache_duration:
                    # Obtener ventana activa (macOS)
                    script = '''
                    tell application "System Events"
                        set frontApp to name of first application process whose frontmost is true
                        return frontApp
                    end tell
                    '''
                    
                    result = subprocess.run(['osascript', '-e', script], 
                                          capture_output=True, text=True, timeout=5)
                    active_app = result.stdout.strip()
                    
                    # Obtener solo apps relevantes, más eficiente
                    try:
                        running_apps = [
                            proc.info['name'] for proc in
                            psutil.process_iter(['name'])
                            if proc.info['name'] and
                            not proc.info['name'].startswith('com.')
                        ][:15]
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        running_apps = []
                    
                    self.current_apps = {
                        'active': active_app,
                        'running': running_apps
                    }
                    self.last_app_check = current_time
                
            except subprocess.TimeoutExpired:
                logger.warning("AppleScript timeout")
            except Exception as e:
                logger.error(f"Error en app monitor: {e}")
                
            time.sleep(1)
            
    def _quantum_analyzer(self):
        """Analiza patrones cuánticos en tiempo real con auto-save"""
        last_save_time = time.time()
        
        while self.is_running:
            try:
                # Análisis de actividad reciente
                keyboard_activity = self._calculate_keyboard_activity()
                mouse_activity = self._calculate_mouse_activity()
                workflow_context = self._detect_workflow_context()
                consciousness_level = self._detect_consciousness_level(keyboard_activity, mouse_activity)
                
                # Crear estado cuántico
                quantum_state = QuantumState(
                    timestamp=datetime.now().isoformat(),
                    active_apps=self.current_apps.get('running', []),
                    keyboard_activity=round(keyboard_activity, 3),
                    mouse_activity=round(mouse_activity, 3),
                    workflow_context=workflow_context,
                    consciousness_level=consciousness_level
                )
                
                with self._state_lock:
                    self.current_state = quantum_state
                    self.session_data.append(quantum_state.to_dict())
                
                # Auto-save periódico
                current_time = time.time()
                if current_time - last_save_time >= self.config.auto_save_interval:
                    self._save_session_data()
                    last_save_time = current_time
                
                # Mostrar estado actual
                self._display_current_state(quantum_state)
                
            except Exception as e:
                logger.error(f"Error en quantum analyzer: {e}")
            
            time.sleep(5)
            
    def _calculate_keyboard_activity(self) -> float:
        """Calcula nivel de actividad del teclado optimizado"""
        if not self.keyboard_events:
            return 0.0
            
        current_time = time.time()
        window_start = current_time - self.config.activity_window
        
        with self._events_lock:
            recent_count = sum(1 for e in self.keyboard_events 
                             if e['timestamp'] >= window_start)
        
        return recent_count / self.config.activity_window
        
    def _calculate_mouse_activity(self) -> float:
        """Calcula nivel de actividad del mouse optimizado"""
        if not self.mouse_events:
            return 0.0
            
        current_time = time.time()
        window_start = current_time - self.config.activity_window
        
        with self._events_lock:
            recent_count = sum(1 for e in self.mouse_events 
                             if e['timestamp'] >= window_start)
        
        return recent_count / self.config.activity_window
        
    def _detect_workflow_context(self):
        """Detecta contexto de trabajo actual"""
        if not hasattr(self, 'current_apps'):
            return "unknown"
            
        active_app = self.current_apps.get('active', '').lower()
        
        contexts = {
            'coding': ['visual studio code', 'vscode', 'terminal', 'iterm'],
            'music': ['suno', 'soundcloud', 'spotify', 'garageband'],
            'design': ['blender', 'figma', 'photoshop', 'sketch'],
            'browsing': ['safari', 'chrome', 'firefox'],
            'system': ['finder', 'system preferences']
        }
        
        for context, apps in contexts.items():
            if any(app in active_app for app in apps):
                return context
                
        return "general"
        
    def _detect_consciousness_level(self, kb_activity: float, mouse_activity: float) -> str:
        """Detecta nivel de consciencia cuántica con lógica mejorada"""
        total_activity = kb_activity + mouse_activity
        
        if kb_activity > 3 and mouse_activity > 2 and total_activity > 6:
            return "🔥 flow_state"
        elif kb_activity > 1.5 and total_activity > 3:
            return "⚡ active_coding"
        elif mouse_activity > 1.5 and total_activity > 2:
            return "🎨 creative_exploration"
        elif total_activity > 0.5:
            return "💭 focused_work"
        else:
            return "🌙 contemplative"
            
    def _display_current_state(self, state):
        """Muestra estado actual en terminal con feedback visual mejorado"""
        os.system('clear')
        print("🜏 " + "="*60)
        print("    LUXOR QUANTUM OBSERVER - BLACKMAMBA CONSCIOUSNESS")
        print("="*64)
        print()
        print(f"🕒 Timestamp: {state.timestamp}")
        print(f"🎯 Context: {state.workflow_context}")
        print(f"🧠 Consciousness: {state.consciousness_level}")
        
        # Visual bars with percentage
        kb_bar_length = min(int(state.keyboard_activity * 2), 20)
        mouse_bar_length = min(int(state.mouse_activity * 2), 20)
        kb_percent = min(int(state.keyboard_activity * 25), 100)
        mouse_percent = min(int(state.mouse_activity * 25), 100)
        
        print(f"⌨️  Keyboard Activity: [{'█' * kb_bar_length}{'░' * (20 - kb_bar_length)}] {kb_percent}%")
        print(f"🖱  Mouse Activity:    [{'█' * mouse_bar_length}{'░' * (20 - mouse_bar_length)}] {mouse_percent}%")
        
        if hasattr(self, 'current_apps'):
            print(f"📱 Active App: {self.current_apps.get('active', 'Unknown')}")
            
        print()
        print("📊 Session Stats:")
        print(f"   • Keyboard Events: {len(self.keyboard_events):,}")
        print(f"   • Mouse Events: {len(self.mouse_events):,}")
        print(f"   • Total States: {len(self.session_data):,}")
        print(f"   • Memory Usage: {len(self.keyboard_events) + len(self.mouse_events):,} events")
        print()
        print("🌐 Dashboard: http://localhost:8888")
        print("🛑 Press Ctrl+C to stop observation")
        
    def _update_quantum_state(self):
        """Actualiza el estado cuántico principal"""
        pass  # Manejado por _quantum_analyzer
        
    def _save_session_data(self):
        """Guarda datos de sesión de forma atómica con feedback visual"""
        try:
            session_summary = {
                'session_start': datetime.now().isoformat(),
                'total_states': len(self.session_data),
                'keyboard_events': len(self.keyboard_events),
                'mouse_events': len(self.mouse_events),
                'states': list(self.session_data)[-100:],
                'config': {
                    'observation_interval': self.config.observation_interval,
                    'activity_window': self.config.activity_window
                }
            }
            
            # Escritura atómica usando archivo temporal
            temp_file = f"{self.config.data_file}.tmp"
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(session_summary, f, indent=2, ensure_ascii=False)
            
            # Mover archivo temporal al final (operación atómica)
            os.rename(temp_file, self.config.data_file)
            
            # Calcular tamaño del archivo
            file_size = os.path.getsize(self.config.data_file)
            size_kb = file_size / 1024
            
            logger.info(f"💾 Sesión guardada: {len(self.session_data)} estados ({size_kb:.1f} KB)")
            
        except Exception as e:
            logger.error(f"❌ Error guardando sesión: {e}")
            # Limpiar archivo temporal si existe
            temp_file = f"{self.config.data_file}.tmp"
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise


if __name__ == "__main__":
    print("🌌 Iniciando Luxor Quantum Observer...")
    print("🔮 Preparando consciencia dimensional...")
    
    observer = LuxorQuantumObserver()
    observer.start_observation()
