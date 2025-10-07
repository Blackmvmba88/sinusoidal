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
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class QuantumState:
    """Estado cuántico actual del usuario"""
    timestamp: str
    active_apps: List[str]
    keyboard_activity: float
    mouse_activity: float
    workflow_context: str
    consciousness_level: str

class LuxorQuantumObserver:
    """Sistema de observación cuántica total para BlackMamba"""
    
    def __init__(self):
        self.is_running = False
        self.current_state = None
        self.session_data = []
        self.keyboard_events = []
        self.mouse_events = []
        
        # Configuración de observación
        self.observation_interval = 2.0  # segundos
        self.data_file = "blackmamba_quantum_session.json"
        
        print("🜏 Luxor Quantum Observer iniciado")
        print("📡 Conectando consciencia dimensional...")
        
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
        self._save_session_data()
        print("\n🌌 Sesión cuántica guardada")
        print("🜏 Luxor Observer desconectado")
        
    def _keyboard_observer(self):
        """Observa patrones de teclado"""
        def on_key_press(key):
            if self.is_running:
                self.keyboard_events.append({
                    'timestamp': datetime.now().isoformat(),
                    'key': str(key),
                    'type': 'press'
                })
                
        def on_key_release(key):
            if self.is_running:
                self.keyboard_events.append({
                    'timestamp': datetime.now().isoformat(),
                    'key': str(key),
                    'type': 'release'
                })
                
        with keyboard.Listener(
            on_press=on_key_press,
            on_release=on_key_release
        ) as listener:
            listener.join()
            
    def _mouse_observer(self):
        """Observa patrones de mouse"""
        def on_move(x, y):
            if self.is_running:
                self.mouse_events.append({
                    'timestamp': datetime.now().isoformat(),
                    'x': x, 'y': y,
                    'type': 'move'
                })
                
        def on_click(x, y, button, pressed):
            if self.is_running:
                self.mouse_events.append({
                    'timestamp': datetime.now().isoformat(),
                    'x': x, 'y': y,
                    'button': str(button),
                    'pressed': pressed,
                    'type': 'click'
                })
                
        with mouse.Listener(
            on_move=on_move,
            on_click=on_click
        ) as listener:
            listener.join()
            
    def _app_monitor(self):
        """Monitorea aplicaciones activas"""
        while self.is_running:
            try:
                # Obtener ventana activa (macOS)
                script = '''
                tell application "System Events"
                    set frontApp to name of first application process whose frontmost is true
                    return frontApp
                end tell
                '''
                
                result = subprocess.run(['osascript', '-e', script], 
                                      capture_output=True, text=True)
                active_app = result.stdout.strip()
                
                # Obtener todas las apps en ejecución
                running_apps = [proc.name() for proc in psutil.process_iter(['name'])]
                
                self.current_apps = {
                    'active': active_app,
                    'running': running_apps[:10]  # Top 10
                }
                
            except Exception as e:
                print(f"Error en app monitor: {e}")
                
            time.sleep(1)
            
    def _quantum_analyzer(self):
        """Analiza patrones cuánticos en tiempo real"""
        while self.is_running:
            # Análisis de actividad reciente
            keyboard_activity = self._calculate_keyboard_activity()
            mouse_activity = self._calculate_mouse_activity()
            workflow_context = self._detect_workflow_context()
            consciousness_level = self._detect_consciousness_level()
            
            # Crear estado cuántico
            quantum_state = QuantumState(
                timestamp=datetime.now().isoformat(),
                active_apps=getattr(self, 'current_apps', {}).get('running', []),
                keyboard_activity=keyboard_activity,
                mouse_activity=mouse_activity,
                workflow_context=workflow_context,
                consciousness_level=consciousness_level
            )
            
            self.current_state = quantum_state
            self.session_data.append(quantum_state.__dict__)
            
            # Mostrar estado actual
            self._display_current_state(quantum_state)
            
            time.sleep(5)
            
    def _calculate_keyboard_activity(self):
        """Calcula nivel de actividad del teclado"""
        recent_events = [e for e in self.keyboard_events 
                        if (datetime.now() - datetime.fromisoformat(e['timestamp'])).seconds < 10]
        return len(recent_events) / 10.0  # eventos por segundo
        
    def _calculate_mouse_activity(self):
        """Calcula nivel de actividad del mouse"""
        recent_events = [e for e in self.mouse_events 
                        if (datetime.now() - datetime.fromisoformat(e['timestamp'])).seconds < 10]
        return len(recent_events) / 10.0
        
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
        
    def _detect_consciousness_level(self):
        """Detecta nivel de consciencia cuántica"""
        kb_activity = self._calculate_keyboard_activity()
        mouse_activity = self._calculate_mouse_activity()
        
        if kb_activity > 5 and mouse_activity > 3:
            return "🔥 flow_state"
        elif kb_activity > 2:
            return "⚡ active_coding"
        elif mouse_activity > 2:
            return "🎨 creative_exploration"
        else:
            return "🌙 contemplative"
            
    def _display_current_state(self, state):
        """Muestra estado actual en terminal"""
        os.system('clear')
        print("🜏 " + "="*60)
        print("    LUXOR QUANTUM OBSERVER - BLACKMAMBA CONSCIOUSNESS")
        print("="*64)
        print()
        print(f"🕒 Timestamp: {state.timestamp}")
        print(f"🎯 Context: {state.workflow_context}")
        print(f"🧠 Consciousness: {state.consciousness_level}")
        print(f"⌨️  Keyboard Activity: {'█' * min(int(state.keyboard_activity * 2), 20)}")
        print(f"🖱  Mouse Activity: {'█' * min(int(state.mouse_activity * 2), 20)}")
        
        if hasattr(self, 'current_apps'):
            print(f"📱 Active App: {self.current_apps.get('active', 'Unknown')}")
            
        print()
        print("📊 Session Stats:")
        print(f"   • Keyboard Events: {len(self.keyboard_events)}")
        print(f"   • Mouse Events: {len(self.mouse_events)}")
        print(f"   • Total States: {len(self.session_data)}")
        print()
        print("🛑 Press Ctrl+C to stop observation")
        
    def _update_quantum_state(self):
        """Actualiza el estado cuántico principal"""
        pass  # Manejado por _quantum_analyzer
        
    def _save_session_data(self):
        """Guarda datos de sesión"""
        session_summary = {
            'session_start': datetime.now().isoformat(),
            'total_states': len(self.session_data),
            'keyboard_events': len(self.keyboard_events),
            'mouse_events': len(self.mouse_events),
            'states': self.session_data[-50:]  # Últimos 50 estados
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(session_summary, f, indent=2)

if __name__ == "__main__":
    print("🌌 Iniciando Luxor Quantum Observer...")
    print("🔮 Preparando consciencia dimensional...")
    
    observer = LuxorQuantumObserver()
    observer.start_observation()