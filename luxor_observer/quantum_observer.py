#!/usr/bin/env python3
"""
🜏 Luxor Quantum Observer - BlackMamba Consciousness Monitor
Monitorea movimientos y patrones en tiempo real (versión segura para pruebas).
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
import threading
import time
from collections import deque
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Deque, Dict, List, Optional

# Intentional optional imports
try:
    import psutil
except Exception:  # pragma: no cover - optional
    psutil = None

try:
    from pynput import keyboard as _keyboard, mouse as _mouse
except Exception:  # pragma: no cover - optional
    _keyboard = None
    _mouse = None

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s - %(levelname)s - %(message)s"),
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
    max_events_memory: int = 1000
    max_session_states: int = 500
    data_file: str = "blackmamba_quantum_session.json"
    auto_save_interval: int = 30
    display_interval: float = 2.0
    mouse_move_throttle: float = 0.25


class LuxorQuantumObserver:
    """Observer robusto y autocontenido para desarrollos locales.

    Las dependencias opcionales (psutil, pynput) se usan si están
    disponibles. Esta versión prioriza ser importable y ejecutable en
    entornos de desarrollo.
    """

    def __init__(self, config: Optional[ObserverConfig] = None) -> None:
        self.config = config or ObserverConfig()
        self.is_running: bool = False
        self.current_state: Optional[QuantumState] = None
        # Hilos lanzados por start_observation
        self._threads: List[threading.Thread] = []

        # Datos en memoria
        self.session_data: Deque[Dict] = deque(
            maxlen=self.config.max_session_states
        )
        self.keyboard_events: Deque[Dict] = deque(
            maxlen=self.config.max_events_memory
        )
        self.mouse_events: Deque[Dict] = deque(
            maxlen=self.config.max_events_memory
        )

        # Estado de apps
        self.current_apps: Dict[str, Any] = {}
        self.last_app_check = datetime.now()

        # Locks
        self._state_lock = threading.Lock()
        self._events_lock = threading.Lock()

        logger.info("🜏 Luxor Quantum Observer inicializado")
        logger.info(
            "   • observation_interval=%s", self.config.observation_interval
        )
        logger.info("   • activity_window=%s", self.config.activity_window)

    def start_observation(self) -> None:
        """Inicia los hilos y loop principal (bloqueante)."""
        self.is_running = True
        logger.info("⚡ SISTEMA DE OBSERVACIÓN CUÁNTICA ACTIVO ⚡")

        threads = [
            threading.Thread(target=self._keyboard_observer, daemon=True),
            threading.Thread(target=self._mouse_observer, daemon=True),
            threading.Thread(target=self._app_monitor, daemon=True),
            threading.Thread(target=self._quantum_analyzer, daemon=True),
        ]

        # Guardar referencias para poder join() al detener
        self._threads = threads
        for t in self._threads:
            t.start()

        try:
            while self.is_running:
                # El analizador actualiza el estado; aquí solo esperamos
                time.sleep(self.config.observation_interval)
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt recibido, deteniendo observer")
            self.stop_observation()

    def stop_observation(self) -> None:
        self.is_running = False
        logger.info("⏸️  Deteniendo observación...")
        try:
            self._save_session_data()
        except Exception as exc:
            logger.exception("Error guardando sesión al detener: %s", exc)
        # Intentar join de hilos para terminar limpiamente (timeout corto)
        for t in getattr(self, "_threads", []):
            try:
                if t.is_alive():
                    t.join(timeout=1.0)
            except Exception:
                logger.debug("Error uniendo hilo al detener")

    def _keyboard_observer(self) -> None:
        """Observador de teclado (opcional)."""
        if _keyboard is None:
            logger.debug(
                "pynput teclado no disponible; keyboard observer deshabilitado"
            )
            return

        def on_key_event(_key, event_type: str) -> None:
            if self.is_running:
                with self._events_lock:
                    self.keyboard_events.append(
                        {
                            "timestamp": datetime.now().timestamp(),
                            "type": event_type,
                        }
                    )

        def on_press(key) -> None:
            on_key_event(key, "press")

        def on_release(key) -> None:
            on_key_event(key, "release")

        try:
            with _keyboard.Listener(
                on_press=on_press, on_release=on_release
            ) as listener:
                listener.join()
        except Exception:
            logger.exception("Error en keyboard observer")

    def _mouse_observer(self) -> None:
        """Observador de ratón (opcional)."""
        if _mouse is None:
            logger.debug(
                "pynput mouse no disponible; mouse observer deshabilitado"
            )
            return

        last_move = 0.0
        throttle = self.config.mouse_move_throttle

        def on_move(_x, _y) -> None:
            nonlocal last_move
            if self.is_running:
                now = time.time()
                if now - last_move > throttle:
                    with self._events_lock:
                        self.mouse_events.append(
                            {"timestamp": now, "type": "move"}
                        )
                    last_move = now

        def on_click(_x, _y, button, pressed) -> None:
            if self.is_running:
                with self._events_lock:
                    self.mouse_events.append(
                        {
                            "timestamp": time.time(),
                            "button": str(button),
                            "pressed": pressed,
                            "type": "click",
                        }
                    )

        try:
            with _mouse.Listener(
                on_move=on_move, on_click=on_click
            ) as listener:
                listener.join()
        except Exception:
            logger.exception("Error en mouse observer")

    def _app_monitor(self) -> None:
        """Monitorea la aplicación activa (macOS via osascript).

        Si psutil está disponible, también lista procesos activos.
        """
        cache_seconds = 2
        while self.is_running:
            try:
                now = datetime.now()
                if (now - self.last_app_check).seconds >= cache_seconds:
                    script = (
                        'tell application "System Events"\n'
                        '    set frontApp to name of first application\n'
                        '    process whose frontmost is true\n'
                        '    return frontApp\n'
                        'end tell'
                    )
                    active_app = ""
                    try:
                        res = subprocess.run(
                            ["osascript", "-e", script],
                            capture_output=True,
                            text=True,
                            timeout=5,
                        )
                        active_app = res.stdout.strip()
                    except subprocess.TimeoutExpired:
                        logger.warning(
                            "AppleScript timeout obteniendo app activa"
                        )

                    running_apps: List[str] = []
                    if psutil is not None:
                        try:
                            tmp: List[str] = []
                            for p in psutil.process_iter(["name"]):
                                name = p.info.get("name")
                                if name:
                                    tmp.append(str(name))
                            running_apps = tmp[:15]
                        except Exception:
                            running_apps = []

                    self.current_apps = {
                        "active": active_app,
                        "running": running_apps,
                    }
                    self.last_app_check = now
            except Exception:
                logger.exception("Error en app monitor")

            time.sleep(1)

    def _quantum_analyzer(self) -> None:
        """Genera estados periódicos basados en eventos recientes."""
        last_save = time.time()
        while self.is_running:
            try:
                kb = self._calculate_keyboard_activity()
                mv = self._calculate_mouse_activity()
                ctx = self._detect_workflow_context()
                lvl = self._detect_consciousness_level(kb, mv)

                state = QuantumState(
                    timestamp=datetime.now().isoformat(),
                    active_apps=self.current_apps.get("running", []),
                    keyboard_activity=round(kb, 3),
                    mouse_activity=round(mv, 3),
                    workflow_context=ctx,
                    consciousness_level=lvl,
                )

                with self._state_lock:
                    self.current_state = state
                    self.session_data.append(state.to_dict())

                now_ts = time.time()
                if now_ts - last_save >= self.config.auto_save_interval:
                    self._save_session_data()
                    last_save = now_ts

                # En modo desarrollo imprimimos resumen compacto (debug)
                logger.debug(
                    "State: %s kb=%s mv=%s ctx=%s lvl=%s",
                    state.timestamp,
                    state.keyboard_activity,
                    state.mouse_activity,
                    state.workflow_context,
                    state.consciousness_level,
                )
            except Exception:
                logger.exception("Error en quantum analyzer")

            time.sleep(self.config.display_interval)

    def _calculate_keyboard_activity(self) -> float:
        if not self.keyboard_events:
            return 0.0
        now = time.time()
        window_start = now - self.config.activity_window
        with self._events_lock:
            recent = sum(
                1
                for e in self.keyboard_events
                if e.get("timestamp", 0) >= window_start
            )
        return recent / max(1, self.config.activity_window)

    def _calculate_mouse_activity(self) -> float:
        if not self.mouse_events:
            return 0.0
        now = time.time()
        window_start = now - self.config.activity_window
        with self._events_lock:
            recent = sum(
                1
                for e in self.mouse_events
                if e.get("timestamp", 0) >= window_start
            )
        return recent / max(1, self.config.activity_window)

    def _detect_workflow_context(self) -> str:
        active = (self.current_apps.get("active") or "").lower()
        mapping = {
            "coding": ["visual studio code", "vscode", "terminal", "iterm"],
            "music": ["suno", "spotify", "garageband"],
            "design": ["figma", "photoshop", "sketch", "blender"],
            "browsing": ["chrome", "safari", "firefox"],
        }
        for ctx, apps in mapping.items():
            if any(a in active for a in apps):
                return ctx
        return "general"

    def _detect_consciousness_level(self, kb: float, mv: float) -> str:
        total = kb + mv
        if kb > 3 and mv > 2 and total > 6:
            return "🔥 flow_state"
        if kb > 1.5 and total > 3:
            return "⚡ active_coding"
        if mv > 1.5 and total > 2:
            return "🎨 creative_exploration"
        if total > 0.5:
            return "💭 focused_work"
        return "🌙 contemplative"

    def _save_session_data(self) -> None:
        try:
            summary = {
                "session_start": datetime.now().isoformat(),
                "total_states": len(self.session_data),
                "keyboard_events": len(self.keyboard_events),
                "mouse_events": len(self.mouse_events),
                "states": list(self.session_data)[-100:],
                "config": {
                    "observation_interval": self.config.observation_interval,
                    "activity_window": self.config.activity_window,
                },
            }

            tmp = f"{self.config.data_file}.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)

            os.replace(tmp, self.config.data_file)
            size_kb = os.path.getsize(self.config.data_file) / 1024
            logger.info(
                "💾 Sesión guardada: %s estados (%.1f KB)",
                len(self.session_data),
                size_kb,
            )
        except Exception:
            logger.exception("Error guardando sesión")
            tmp = f"{self.config.data_file}.tmp"
            if os.path.exists(tmp):
                os.remove(tmp)
            raise
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


if __name__ == "__main__":
    logger.info("🌌 Iniciando Luxor Quantum Observer (diagnóstico)...")
    obs = LuxorQuantumObserver()
    try:
        obs.start_observation()
    except Exception:
        logger.exception("Observer fallo en ejecución principal")
