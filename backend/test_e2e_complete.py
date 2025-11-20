"""
End-to-End Test Script - Simula interação completa do usuário
Testa o fluxo: Frontend → Backend → LLM → Response
"""
import sys
import os
import time
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app.main import app
from fastapi.testclient import TestClient

# Test data
TEST_URL = "https://www.linkedin.com/jobs/view/4341850331/?trk=mcm"
TEST_CV = """
JOÃO SILVA
São Paulo, SP | joao.silva@email.com | (11) 98765-4321
LinkedIn: linkedin.com/in/joaosilva | GitHub: github.com/joaosilva

RESUMO PROFISSIONAL
Senior Data Analyst com 8+ anos de experiência em análise de dados, engenharia de dados e business intelligence.
Especialista em construção de pipelines ETL, desenvolvimento de dashboards executivos e otimização de performance.
Domínio de Python, SQL, Tableau e plataformas cloud (AWS, GCP).

EXPERIÊNCIA PROFISSIONAL

SENIOR DATA ANALYST | Tech Solutions Brasil | Jan 2019 - Presente
• Liderei equipe de 5 analistas de dados, implementando best practices em visualização e análise
• Construí pipelines ETL robustos processando 10M+ registros diários com 99.9% de confiabilidade
• Desenvolvi dashboards executivos no Tableau utilizados pelo C-level para tomada de decisões estratégicas
• Otimizei queries SQL reduzindo tempo de processamento em 60% através de indexação e particionamento
• Implementei processos de governança de dados garantindo qualidade e consistência
• Colaborei com times de produto, engenharia e negócios em projetos de data-driven decision making

DATA ANALYST | Analytics Corp | Abr 2016 - Dez 2018
• Criei relatórios automatizados em Power BI reduzindo tempo de análise em 40%
• Desenvolvi modelos preditivos em Python para forecasting de vendas
• Realizei análises exploratórias identificando oportunidades de otimização de custos
• Mantive documentação técnica de processos e pipelines de dados

FORMAÇÃO ACADÊMICA
Bacharelado em Ciência da Computação | USP | 2012 - 2015
MBA em Data Science e Analytics | FGV | 2017 - 2019

HABILIDADES TÉCNICAS
• Linguagens: Python (Pandas, NumPy, Spark), SQL (PostgreSQL, MySQL)
• Visualização: Tableau, Power BI, Looker
• Cloud: AWS (Redshift, S3, Lambda), GCP (BigQuery, Cloud Functions)
• ETL/Orquestração: Airflow, dbt, Luigi
• Big Data: Spark, Hadoop
• Controle de Versão: Git, GitHub
• Banco de Dados: PostgreSQL, MySQL, MongoDB, Redshift, BigQuery

CERTIFICAÇÕES
• AWS Certified Data Analytics - Specialty
• Google Cloud Professional Data Engineer
• Tableau Desktop Specialist
"""

print("=" * 100)
print("TESTE END-TO-END COMPLETO - CV SOB MEDIDA")
print("=" * 100)

client = TestClient(app)

# Passo 1: Verificar saúde do backend
print("\n[ETAPA 1/4] Verificando saúde do backend...")
print("-" * 100)
health_response = client.get("/health")
assert health_response.status_code == 200, f"Health check failed: {health_response.status_code}"
print("✅ Backend está saudável e respondendo")

# Passo 2: Extrair detalhes da vaga
print("\n[ETAPA 2/4] Extraindo detalhes da vaga do LinkedIn...")
print(f"URL da vaga: {TEST_URL}")
print("-" * 100)

start_extraction = time.time()
extraction_response = client.post(
    "/extract-job-details",
    json={"url": TEST_URL},
    timeout=45.0
)
extraction_time = time.time() - start_extraction

assert extraction_response.status_code == 200, f"Extraction failed: {extraction_response.text}"
job_data = extraction_response.json()

print(f"✅ Extração concluída em {extraction_time:.2f}s")
print(f"\n📋 DETALHES DA VAGA EXTRAÍDA:")
print(f"   ID: {job_data['id']}")
print(f"   Título: {job_data['title']}")
print(f"   Empresa: {job_data['company']}")
print(f"   Skills identificadas: {len(job_data['skills'])}")
print(f"   Top 10 skills: {', '.join(job_data['skills'][:10])}")
print(f"   Descrição (primeiros 200 chars): {job_data['description'][:200]}...")

# Passo 3: Gerar materiais personalizados
print("\n[ETAPA 3/4] Gerando materiais personalizados com IA...")
print("-" * 100)

start_generation = time.time()
generation_response = client.post(
    "/generate-materials",
    json={
        "job": {
            "id": job_data["id"],
            "title": job_data["title"],
            "company": job_data["company"],
            "description": job_data["description"],
            "skills": job_data["skills"]
        },
        "profile": {
            "cvText": TEST_CV
        }
    },
    timeout=90.0
)
generation_time = time.time() - start_generation

assert generation_response.status_code == 200, f"Generation failed: {generation_response.text}"
assets = generation_response.json()

print(f"✅ Geração concluída em {generation_time:.2f}s")
print(f"\n📄 MATERIAIS GERADOS:")
print(f"   Match Score: {assets['matchScore']}/100")
print(f"   CV personalizado: {len(assets['cv'])} caracteres")
print(f"   Carta de apresentação: {len(assets['coverLetter'])} caracteres")
print(f"   Dicas de networking: {len(assets['networking'])} caracteres")

# Parse insights
try:
    insights = json.loads(assets['insights'])
    print(f"\n🎯 INSIGHTS DA ANÁLISE:")
    print(f"   Score: {insights['score']}/100")
    print(f"   Forças identificadas:")
    for i, strength in enumerate(insights['strengths'][:3], 1):
        print(f"      {i}. {strength[:100]}...")
    print(f"   Gap identificado: {insights['gap'][:150]}...")
except:
    print(f"   Insights: {assets['insights'][:200]}...")

# Passo 4: Validar qualidade dos outputs
print("\n[ETAPA 4/4] Validando qualidade dos outputs...")
print("-" * 100)

validations = []

# Validação 1: CV contém keywords da vaga
job_keywords = set(word.lower() for word in job_data['skills'][:20])
cv_text = assets['cv'].lower()
keywords_found = sum(1 for keyword in job_keywords if keyword.lower() in cv_text)
keywords_percentage = (keywords_found / len(job_keywords)) * 100 if job_keywords else 0
validations.append(("CV contém keywords da vaga", keywords_percentage >= 30, f"{keywords_percentage:.1f}%"))

# Validação 2: CV menciona a empresa
validations.append(("CV menciona a empresa", job_data['company'].lower() in cv_text, "Sim" if job_data['company'].lower() in cv_text else "Não"))

# Validação 3: Match score razoável
validations.append(("Match score razoável (>50)", assets['matchScore'] >= 50, f"{assets['matchScore']}/100"))

# Validação 4: Tamanho mínimo dos documentos
validations.append(("CV tem tamanho adequado", len(assets['cv']) >= 500, f"{len(assets['cv'])} chars"))
validations.append(("Cover letter tem tamanho adequado", len(assets['coverLetter']) >= 500, f"{len(assets['coverLetter'])} chars"))

# Validação 5: Tempo de resposta aceitável
total_time = extraction_time + generation_time
validations.append(("Tempo total aceitável (<120s)", total_time < 120, f"{total_time:.2f}s"))

print("\n📊 RESULTADOS DAS VALIDAÇÕES:")
all_passed = True
for validation_name, passed, detail in validations:
    status = "✅" if passed else "❌"
    print(f"   {status} {validation_name}: {detail}")
    all_passed = all_passed and passed

# Resumo final
print("\n" + "=" * 100)
print("RESUMO DA EXECUÇÃO")
print("=" * 100)
print(f"⏱️  Tempo de extração: {extraction_time:.2f}s")
print(f"⏱️  Tempo de geração: {generation_time:.2f}s")
print(f"⏱️  Tempo total: {total_time:.2f}s")
print(f"📊 Validações passadas: {sum(1 for _, p, _ in validations if p)}/{len(validations)}")
print(f"🎯 Score de compatibilidade: {assets['matchScore']}/100")

if all_passed:
    print("\n🎉 TODOS OS TESTES PASSARAM! Sistema funcionando perfeitamente end-to-end!")
    sys.exit(0)
else:
    print("\n⚠️  Algumas validações falharam. Revisar outputs acima.")
    sys.exit(1)
