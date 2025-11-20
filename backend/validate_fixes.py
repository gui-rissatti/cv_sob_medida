#!/usr/bin/env python
"""
Quick Validation Script - Verifica que todas as correções estão aplicadas
Execute antes de fazer commit para garantir que tudo está funcionando.
"""
import sys
import os
from pathlib import Path

BACKEND_ROOT = Path(__file__).parent
SRC_ROOT = BACKEND_ROOT / "src"

print("=" * 80)
print("🔍 VALIDAÇÃO DE CORREÇÕES - CV SOB MEDIDA")
print("=" * 80)

validations = []

# Validação 1: .env existe
print("\n[1/5] Verificando arquivo .env...")
env_file = BACKEND_ROOT / ".env"
if env_file.exists():
    print("✅ Arquivo .env encontrado")
    validations.append(True)
else:
    print("❌ Arquivo .env não encontrado!")
    print("   Execute: cp .env.example .env")
    validations.append(False)

# Validação 2: GOOGLE_API_KEY está configurada
print("\n[2/5] Verificando GOOGLE_API_KEY...")
if env_file.exists():
    with open(env_file) as f:
        content = f.read()
        if "GOOGLE_API_KEY=" in content and "your_gemini_api_key_here" not in content:
            print("✅ GOOGLE_API_KEY configurada")
            validations.append(True)
        else:
            print("❌ GOOGLE_API_KEY não configurada ou usando valor padrão")
            print("   Edite .env e adicione sua chave do Google AI Studio")
            validations.append(False)
else:
    validations.append(False)

# Validação 3: Modelo correto nos agentes
print("\n[3/5] Verificando modelo Gemini nos agentes...")
errors = []

extraction_agent = SRC_ROOT / "agents" / "extraction_agent.py"
with open(extraction_agent) as f:
    content = f.read()
    if 'model: str = "gemini-2.5-flash"' in content or 'model: str = "gemini-2.0-flash"' in content:
        print("✅ extraction_agent.py usando modelo correto")
    else:
        print("❌ extraction_agent.py NÃO atualizado!")
        errors.append("extraction_agent.py")

generation_agent = SRC_ROOT / "agents" / "generation_agent.py"
with open(generation_agent) as f:
    content = f.read()
    if 'model: str = "gemini-2.5-flash"' in content or 'model: str = "gemini-2.0-flash"' in content:
        print("✅ generation_agent.py usando modelo correto")
    else:
        print("❌ generation_agent.py NÃO atualizado!")
        errors.append("generation_agent.py")

validations.append(len(errors) == 0)
if errors:
    print(f"   Arquivos a corrigir: {', '.join(errors)}")

# Validação 4: API key sendo passada aos agentes
print("\n[4/5] Verificando se API key é passada aos agentes...")
errors = []

with open(extraction_agent) as f:
    content = f.read()
    if "google_api_key=settings.google_api_key" in content:
        print("✅ extraction_agent.py passa API key corretamente")
    else:
        print("❌ extraction_agent.py NÃO passa API key!")
        errors.append("extraction_agent.py")

with open(generation_agent) as f:
    content = f.read()
    if "google_api_key=settings.google_api_key" in content:
        print("✅ generation_agent.py passa API key corretamente")
    else:
        print("❌ generation_agent.py NÃO passa API key!")
        errors.append("generation_agent.py")

validations.append(len(errors) == 0)

# Validação 5: Config usa caminho absoluto para .env
print("\n[5/5] Verificando configuração de .env path...")
config_file = SRC_ROOT / "core" / "config.py"
with open(config_file) as f:
    content = f.read()
    if "_BACKEND_ROOT" in content and "_ENV_FILE" in content:
        print("✅ config.py usa caminho absoluto para .env")
        validations.append(True)
    else:
        print("❌ config.py ainda usa caminho relativo!")
        print("   A correção em config.py não foi aplicada")
        validations.append(False)

# Resumo
print("\n" + "=" * 80)
passed = sum(validations)
total = len(validations)
print(f"RESULTADO: {passed}/{total} validações passadas")
print("=" * 80)

if all(validations):
    print("\n✅ TODAS AS CORREÇÕES ESTÃO APLICADAS!")
    print("   Sistema pronto para commit e deploy.")
    sys.exit(0)
else:
    print("\n❌ ALGUMAS CORREÇÕES ESTÃO FALTANDO!")
    print("   Revise os erros acima antes de fazer commit.")
    sys.exit(1)
