#!/usr/bin/env python3
"""
🔒 Script de Validación de Seguridad
Verifica las mejoras de seguridad implementadas
"""

import sys
from pathlib import Path

# Agregar el directorio luxor_observer al path
sys.path.insert(0, str(Path(__file__).parent / "luxor_observer"))


def test_config_validation():
    """Test de validación de configuración"""
    print("🧪 Test 1: Validación de ObserverConfig")
    print("=" * 60)
    
    try:
        from quantum_observer import ObserverConfig
        
        # Test 1: Configuración válida
        print("  ✓ Test 1.1: Configuración válida por defecto")
        config = ObserverConfig()
        print(f"    - observation_interval: {config.observation_interval}")
        print(f"    - max_events_memory: {config.max_events_memory}")
        print("    ✅ PASADO")
        
        # Test 2: Intervalo negativo (debe fallar)
        print("\n  ✓ Test 1.2: Rechazar intervalo negativo")
        try:
            config = ObserverConfig(observation_interval=-1)
            print("    ❌ FALLADO - No rechazó valor negativo")
            return False
        except ValueError as e:
            print(f"    ✅ PASADO - Rechazado correctamente: {e}")
        
        # Test 3: Memoria excesiva (debe fallar)
        print("\n  ✓ Test 1.3: Rechazar memoria excesiva")
        try:
            config = ObserverConfig(max_events_memory=1000000)
            print("    ❌ FALLADO - No rechazó valor excesivo")
            return False
        except ValueError as e:
            print(f"    ✅ PASADO - Rechazado correctamente: {e}")
        
        # Test 4: Path traversal (debe fallar)
        print("\n  ✓ Test 1.4: Prevenir path traversal")
        try:
            config = ObserverConfig(data_file="../../../etc/passwd")
            print("    ❌ FALLADO - No previno path traversal")
            return False
        except ValueError as e:
            print(f"    ✅ PASADO - Prevenido correctamente: {e}")
        
        # Test 5: Path con slash (debe fallar)
        print("\n  ✓ Test 1.5: Prevenir rutas absolutas")
        try:
            config = ObserverConfig(data_file="/tmp/malicious.json")
            print("    ❌ FALLADO - No previno ruta absoluta")
            return False
        except ValueError as e:
            print(f"    ✅ PASADO - Prevenido correctamente: {e}")
        
        print("\n✅ Todos los tests de configuración pasaron")
        return True
        
    except ImportError as e:
        print(f"❌ Error importando módulo: {e}")
        return False


def test_rate_limiter():
    """Test de rate limiter"""
    print("\n🧪 Test 2: Rate Limiter")
    print("=" * 60)
    
    try:
        # Importar directamente la clase
        import sys
        sys.path.insert(0, 'luxor_observer')
        
        # Crear rate limiter con límites bajos para testing
        from dashboard import SimpleRateLimiter
        
        limiter = SimpleRateLimiter(max_requests=5, window_seconds=10)
        
        # Test 1: Permitir peticiones dentro del límite
        print("  ✓ Test 2.1: Permitir peticiones dentro del límite")
        allowed_count = 0
        for i in range(5):
            if limiter.is_allowed('test_client'):
                allowed_count += 1
        
        if allowed_count == 5:
            print(f"    ✅ PASADO - {allowed_count}/5 peticiones permitidas")
        else:
            print(f"    ❌ FALLADO - {allowed_count}/5 peticiones permitidas")
            return False
        
        # Test 2: Bloquear peticiones sobre el límite
        print("\n  ✓ Test 2.2: Bloquear peticiones sobre el límite")
        blocked = not limiter.is_allowed('test_client')
        if blocked:
            print("    ✅ PASADO - Petición 6 bloqueada correctamente")
        else:
            print("    ❌ FALLADO - Petición 6 no fue bloqueada")
            return False
        
        # Test 3: Permitir otro cliente
        print("\n  ✓ Test 2.3: Limitar por cliente independientemente")
        if limiter.is_allowed('other_client'):
            print("    ✅ PASADO - Otro cliente puede hacer peticiones")
        else:
            print("    ❌ FALLADO - Otro cliente bloqueado incorrectamente")
            return False
        
        print("\n✅ Todos los tests de rate limiter pasaron")
        return True
        
    except ImportError as e:
        print(f"❌ Error importando módulo: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False


def test_security_headers():
    """Test de headers de seguridad"""
    print("\n🧪 Test 3: Headers de Seguridad")
    print("=" * 60)
    
    try:
        from dashboard import app, add_security_headers
        
        # Crear contexto de aplicación
        with app.test_client() as client:
            # Hacer petición al dashboard
            response = client.get('/')
            
            # Verificar headers de seguridad
            print("  ✓ Verificando headers de seguridad:")
            
            headers_to_check = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Content-Security-Policy': "default-src 'self' 'unsafe-inline'"
            }
            
            all_passed = True
            for header, expected_value in headers_to_check.items():
                actual_value = response.headers.get(header)
                if actual_value == expected_value:
                    print(f"    ✅ {header}: {actual_value}")
                else:
                    print(f"    ❌ {header}: esperado '{expected_value}', obtenido '{actual_value}'")
                    all_passed = False
            
            if all_passed:
                print("\n✅ Todos los headers de seguridad están configurados")
                return True
            else:
                print("\n❌ Algunos headers de seguridad faltan o son incorrectos")
                return False
        
    except ImportError as e:
        print(f"❌ Error importando módulo: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecutar todos los tests"""
    print("\n" + "=" * 60)
    print("🔒 VALIDACIÓN DE SEGURIDAD - LUXOR QUANTUM OBSERVER")
    print("=" * 60 + "\n")
    
    results = []
    
    # Test 1: Validación de configuración
    results.append(("Config Validation", test_config_validation()))
    
    # Test 2: Rate limiter
    results.append(("Rate Limiter", test_rate_limiter()))
    
    # Test 3: Security headers
    results.append(("Security Headers", test_security_headers()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASADO" if result else "❌ FALLADO"
        print(f"  {name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests pasados")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS VALIDACIONES DE SEGURIDAD PASARON!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
