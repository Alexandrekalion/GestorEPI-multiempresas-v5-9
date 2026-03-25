"""
Script para criar dados de demonstração:
- 2 Empresas
- 5 Colaboradores com fotos
- 15 EPIs
- 5 Kits
- Entregas de EPI (5 para maioria, 15 para um)
"""
import asyncio
from datetime import datetime, timezone, timedelta
from database import connect_db, get_db
from bson import ObjectId
import random

async def create_demo_data():
    await connect_db()
    db = await get_db()
    
    print("="*60)
    print("CRIANDO DADOS DE DEMONSTRAÇÃO")
    print("="*60)
    
    # Obter empresa_id do admin
    admin = await db.users.find_one({"username": "admin"})
    if not admin:
        print("❌ Usuário admin não encontrado. Execute seed.py primeiro.")
        return
    
    empresa_id = admin.get('empresa_id')
    if not empresa_id:
        # Criar empresa se não existir
        empresa = await db.empresas.find_one({"cnpj": "00.000.000/0001-00"})
        if empresa:
            empresa_id = str(empresa['_id'])
        else:
            print("❌ Empresa não encontrada.")
            return
    
    print(f"✅ Usando empresa_id: {empresa_id}")
    
    # ===================== CRIAR 2 EMPRESAS (FILIAIS) =====================
    print("\n📦 Criando Empresas...")
    
    empresas_data = [
        {
            "nome": "TechCorp Indústria LTDA",
            "cnpj": "12.345.678/0001-90",
            "status": "ativo",
            "plano": "250",
            "limite_colaboradores": 250,
            "endereco": "Rua das Indústrias, 500 - Distrito Industrial, São Paulo/SP",
            "telefone": "(11) 4000-5000",
            "email": "contato@techcorp.com.br",
            "responsavel": "Roberto Mendes",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        },
        {
            "nome": "Construtora Horizonte S.A.",
            "cnpj": "98.765.432/0001-10",
            "status": "ativo",
            "plano": "350",
            "limite_colaboradores": 350,
            "endereco": "Av. Brasil, 2000 - Centro, Rio de Janeiro/RJ",
            "telefone": "(21) 3000-4000",
            "email": "rh@horizonteconstrucao.com.br",
            "responsavel": "Mariana Santos",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ]
    
    for emp_data in empresas_data:
        existing = await db.empresas.find_one({"cnpj": emp_data["cnpj"]})
        if not existing:
            await db.empresas.insert_one(emp_data)
            print(f"  ✅ Empresa criada: {emp_data['nome']}")
        else:
            print(f"  ⏭️ Empresa já existe: {emp_data['nome']}")
    
    # ===================== CRIAR 5 COLABORADORES =====================
    print("\n👥 Criando Colaboradores...")
    
    colaboradores_data = [
        {
            "full_name": "Maria Oliveira Santos",
            "cpf": "151.049.165-10",
            "rg": "23.456.789-0",
            "registration_number": "FUNC001",
            "department": "Produção",
            "position": "Operadora de Máquinas",
            "blood_type": "A+",
            "contact_phone": "(11) 98765-0001",
            "emergency_contact": "José Santos - (11) 91234-0001",
            "admission_date": "2023-03-15",
            "status": "active",
            "photo_path": "/uploads/employees/foto_1.png",
            "facial_consent": True,
            "empresa_id": empresa_id
        },
        {
            "full_name": "Ricardo Ferreira Lima",
            "cpf": "526.950.645-94",
            "rg": "34.567.890-1",
            "registration_number": "FUNC002",
            "department": "Manutenção",
            "position": "Técnico de Manutenção",
            "blood_type": "O+",
            "contact_phone": "(11) 98765-0002",
            "emergency_contact": "Ana Lima - (11) 91234-0002",
            "admission_date": "2022-08-20",
            "status": "active",
            "photo_path": "/uploads/employees/foto_2.png",
            "facial_consent": True,
            "empresa_id": empresa_id
        },
        {
            "full_name": "Pedro Henrique Costa",
            "cpf": "796.286.168-11",
            "rg": "45.678.901-2",
            "registration_number": "FUNC003",
            "department": "Almoxarifado",
            "position": "Auxiliar de Almoxarifado",
            "blood_type": "B+",
            "contact_phone": "(11) 98765-0003",
            "emergency_contact": "Lucia Costa - (11) 91234-0003",
            "admission_date": "2024-01-10",
            "status": "active",
            "photo_path": "/uploads/employees/foto_3.png",
            "facial_consent": True,
            "empresa_id": empresa_id
        },
        {
            "full_name": "Juliana Mendes Alves",
            "cpf": "446.749.997-07",
            "rg": "56.789.012-3",
            "registration_number": "FUNC004",
            "department": "Segurança",
            "position": "Técnica de Segurança do Trabalho",
            "blood_type": "AB+",
            "contact_phone": "(11) 98765-0004",
            "emergency_contact": "Carlos Alves - (11) 91234-0004",
            "admission_date": "2021-05-12",
            "status": "active",
            "photo_path": "/uploads/employees/foto_4.png",
            "facial_consent": True,
            "empresa_id": empresa_id
        },
        {
            "full_name": "Carla Regina Souza",
            "cpf": "705.154.725-90",
            "rg": "67.890.123-4",
            "registration_number": "FUNC005",
            "department": "Produção",
            "position": "Supervisora de Produção",
            "blood_type": "O-",
            "contact_phone": "(11) 98765-0005",
            "emergency_contact": "Paulo Souza - (11) 91234-0005",
            "admission_date": "2020-02-28",
            "status": "active",
            "photo_path": "/uploads/employees/foto_5.png",
            "facial_consent": True,
            "empresa_id": empresa_id
        }
    ]
    
    employee_ids = []
    for colab in colaboradores_data:
        colab["created_at"] = datetime.now(timezone.utc)
        colab["updated_at"] = datetime.now(timezone.utc)
        
        existing = await db.employees.find_one({"cpf": colab["cpf"], "empresa_id": empresa_id})
        if not existing:
            result = await db.employees.insert_one(colab)
            employee_ids.append(str(result.inserted_id))
            print(f"  ✅ Colaborador criado: {colab['full_name']} - CPF: {colab['cpf']}")
        else:
            employee_ids.append(str(existing['_id']))
            print(f"  ⏭️ Colaborador já existe: {colab['full_name']}")
    
    # ===================== CRIAR 15 EPIs =====================
    print("\n🦺 Criando EPIs...")
    
    epis_data = [
        {"name": "Capacete de Segurança Classe A", "ca_number": "CA-12345", "category": "Proteção da Cabeça", "validity_months": 60, "stock": 100, "minimum_stock": 20, "unit_price": 45.90},
        {"name": "Óculos de Proteção Transparente", "ca_number": "CA-23456", "category": "Proteção dos Olhos", "validity_months": 24, "stock": 150, "minimum_stock": 30, "unit_price": 15.50},
        {"name": "Protetor Auricular Plug", "ca_number": "CA-34567", "category": "Proteção Auditiva", "validity_months": 6, "stock": 500, "minimum_stock": 100, "unit_price": 3.20},
        {"name": "Luva de Vaqueta", "ca_number": "CA-45678", "category": "Proteção das Mãos", "validity_months": 12, "stock": 200, "minimum_stock": 50, "unit_price": 28.00},
        {"name": "Luva Nitrílica", "ca_number": "CA-56789", "category": "Proteção das Mãos", "validity_months": 6, "stock": 300, "minimum_stock": 60, "unit_price": 12.50},
        {"name": "Botina de Segurança", "ca_number": "CA-67890", "category": "Proteção dos Pés", "validity_months": 12, "stock": 80, "minimum_stock": 20, "unit_price": 120.00},
        {"name": "Máscara PFF2", "ca_number": "CA-78901", "category": "Proteção Respiratória", "validity_months": 3, "stock": 400, "minimum_stock": 100, "unit_price": 8.50},
        {"name": "Avental de Raspa", "ca_number": "CA-89012", "category": "Proteção do Tronco", "validity_months": 24, "stock": 50, "minimum_stock": 10, "unit_price": 85.00},
        {"name": "Cinto de Segurança Tipo Paraquedista", "ca_number": "CA-90123", "category": "Proteção Contra Quedas", "validity_months": 36, "stock": 30, "minimum_stock": 5, "unit_price": 350.00},
        {"name": "Mangote de Raspa", "ca_number": "CA-01234", "category": "Proteção dos Braços", "validity_months": 18, "stock": 60, "minimum_stock": 15, "unit_price": 45.00},
        {"name": "Perneira de Segurança", "ca_number": "CA-11111", "category": "Proteção das Pernas", "validity_months": 24, "stock": 40, "minimum_stock": 10, "unit_price": 55.00},
        {"name": "Máscara de Solda", "ca_number": "CA-22222", "category": "Proteção dos Olhos", "validity_months": 36, "stock": 25, "minimum_stock": 5, "unit_price": 180.00},
        {"name": "Protetor Facial Incolor", "ca_number": "CA-33333", "category": "Proteção da Face", "validity_months": 24, "stock": 45, "minimum_stock": 10, "unit_price": 42.00},
        {"name": "Colete Refletivo", "ca_number": "CA-44444", "category": "Sinalização", "validity_months": 24, "stock": 70, "minimum_stock": 15, "unit_price": 35.00},
        {"name": "Touca Árabe", "ca_number": "CA-55555", "category": "Proteção da Cabeça", "validity_months": 12, "stock": 90, "minimum_stock": 20, "unit_price": 18.00}
    ]
    
    epi_ids = []
    for i, epi in enumerate(epis_data):
        epi["internal_code"] = f"EPI{str(i+1).zfill(3)}"
        epi["qr_code"] = f"QR-EPI-{str(i+1).zfill(3)}"
        epi["empresa_id"] = empresa_id
        epi["expiry_date"] = (datetime.now(timezone.utc) + timedelta(days=365)).isoformat()
        epi["created_at"] = datetime.now(timezone.utc)
        epi["updated_at"] = datetime.now(timezone.utc)
        
        existing = await db.epis.find_one({"ca_number": epi["ca_number"], "empresa_id": empresa_id})
        if not existing:
            result = await db.epis.insert_one(epi)
            epi_ids.append({"id": str(result.inserted_id), "name": epi["name"]})
            print(f"  ✅ EPI criado: {epi['name']} - CA: {epi['ca_number']}")
        else:
            epi_ids.append({"id": str(existing['_id']), "name": epi["name"]})
            print(f"  ⏭️ EPI já existe: {epi['name']}")
    
    # ===================== CRIAR 5 KITS =====================
    print("\n📦 Criando Kits de EPI...")
    
    kits_data = [
        {
            "name": "Kit Básico Produção",
            "description": "Kit essencial para operadores de produção",
            "items": [
                {"epi_id": epi_ids[0]["id"], "epi_name": epi_ids[0]["name"], "quantity": 1},
                {"epi_id": epi_ids[1]["id"], "epi_name": epi_ids[1]["name"], "quantity": 1},
                {"epi_id": epi_ids[2]["id"], "epi_name": epi_ids[2]["name"], "quantity": 2},
                {"epi_id": epi_ids[5]["id"], "epi_name": epi_ids[5]["name"], "quantity": 1}
            ]
        },
        {
            "name": "Kit Soldador",
            "description": "Equipamentos completos para soldagem",
            "items": [
                {"epi_id": epi_ids[0]["id"], "epi_name": epi_ids[0]["name"], "quantity": 1},
                {"epi_id": epi_ids[11]["id"], "epi_name": epi_ids[11]["name"], "quantity": 1},
                {"epi_id": epi_ids[7]["id"], "epi_name": epi_ids[7]["name"], "quantity": 1},
                {"epi_id": epi_ids[9]["id"], "epi_name": epi_ids[9]["name"], "quantity": 1},
                {"epi_id": epi_ids[3]["id"], "epi_name": epi_ids[3]["name"], "quantity": 1}
            ]
        },
        {
            "name": "Kit Trabalho em Altura",
            "description": "Equipamentos para trabalho em altura",
            "items": [
                {"epi_id": epi_ids[0]["id"], "epi_name": epi_ids[0]["name"], "quantity": 1},
                {"epi_id": epi_ids[8]["id"], "epi_name": epi_ids[8]["name"], "quantity": 1},
                {"epi_id": epi_ids[5]["id"], "epi_name": epi_ids[5]["name"], "quantity": 1}
            ]
        },
        {
            "name": "Kit Químico",
            "description": "Proteção para manuseio de produtos químicos",
            "items": [
                {"epi_id": epi_ids[1]["id"], "epi_name": epi_ids[1]["name"], "quantity": 1},
                {"epi_id": epi_ids[4]["id"], "epi_name": epi_ids[4]["name"], "quantity": 2},
                {"epi_id": epi_ids[6]["id"], "epi_name": epi_ids[6]["name"], "quantity": 5},
                {"epi_id": epi_ids[7]["id"], "epi_name": epi_ids[7]["name"], "quantity": 1}
            ]
        },
        {
            "name": "Kit Visitante",
            "description": "Equipamentos básicos para visitantes",
            "items": [
                {"epi_id": epi_ids[0]["id"], "epi_name": epi_ids[0]["name"], "quantity": 1},
                {"epi_id": epi_ids[1]["id"], "epi_name": epi_ids[1]["name"], "quantity": 1},
                {"epi_id": epi_ids[2]["id"], "epi_name": epi_ids[2]["name"], "quantity": 1},
                {"epi_id": epi_ids[13]["id"], "epi_name": epi_ids[13]["name"], "quantity": 1}
            ]
        }
    ]
    
    kit_ids = []
    for kit in kits_data:
        kit["empresa_id"] = empresa_id
        kit["created_at"] = datetime.now(timezone.utc)
        kit["updated_at"] = datetime.now(timezone.utc)
        
        existing = await db.kits.find_one({"name": kit["name"], "empresa_id": empresa_id})
        if not existing:
            result = await db.kits.insert_one(kit)
            kit_ids.append({"id": str(result.inserted_id), "name": kit["name"], "items": kit["items"]})
            print(f"  ✅ Kit criado: {kit['name']}")
        else:
            kit_ids.append({"id": str(existing['_id']), "name": kit["name"], "items": kit["items"]})
            print(f"  ⏭️ Kit já existe: {kit['name']}")
    
    # ===================== CRIAR ENTREGAS =====================
    print("\n📋 Criando Entregas de EPI...")
    
    # Buscar colaboradores
    colaboradores = await db.employees.find({"empresa_id": empresa_id}).to_list(100)
    colab_map = {str(c['_id']): c for c in colaboradores}
    
    # Definir entregas por colaborador
    entregas_config = [
        {"colab_idx": 0, "num_entregas": 5},   # Maria - 5 entregas
        {"colab_idx": 1, "num_entregas": 5},   # Ricardo - 5 entregas
        {"colab_idx": 2, "num_entregas": 15},  # Pedro - 15 entregas
        {"colab_idx": 3, "num_entregas": 5},   # Juliana - 5 entregas
        {"colab_idx": 4, "num_entregas": 5},   # Carla - 5 entregas
    ]
    
    total_entregas = 0
    for config in entregas_config:
        if config["colab_idx"] >= len(employee_ids):
            continue
            
        emp_id = employee_ids[config["colab_idx"]]
        colab = colab_map.get(emp_id)
        if not colab:
            continue
        
        for i in range(config["num_entregas"]):
            # Selecionar EPIs aleatórios
            num_items = random.randint(1, 4)
            selected_epis = random.sample(epi_ids, min(num_items, len(epi_ids)))
            
            items = []
            for epi in selected_epis:
                items.append({
                    "epi_id": epi["id"],
                    "epi_name": epi["name"],
                    "quantity": random.randint(1, 3)
                })
            
            # Criar data aleatória nos últimos 90 dias
            days_ago = random.randint(0, 90)
            delivery_date = datetime.now(timezone.utc) - timedelta(days=days_ago)
            
            delivery = {
                "employee_id": emp_id,
                "employee_name": colab["full_name"],
                "employee_cpf": colab["cpf"],
                "employee_registration": colab.get("registration_number", ""),
                "items": items,
                "is_return": random.random() < 0.1,  # 10% são devoluções
                "notes": f"Entrega de rotina #{i+1}",
                "delivered_by": "admin",
                "delivered_by_name": "Administrador",
                "facial_match_score": round(random.uniform(0.85, 0.99), 2) if random.random() > 0.2 else None,
                "empresa_id": empresa_id,
                "created_at": delivery_date,
                "updated_at": delivery_date
            }
            
            await db.deliveries.insert_one(delivery)
            total_entregas += 1
        
        print(f"  ✅ {config['num_entregas']} entregas criadas para: {colab['full_name']}")
    
    # ===================== RESUMO =====================
    print("\n" + "="*60)
    print("RESUMO DOS DADOS CRIADOS")
    print("="*60)
    
    total_empresas = await db.empresas.count_documents({})
    total_colaboradores = await db.employees.count_documents({"empresa_id": empresa_id})
    total_epis = await db.epis.count_documents({"empresa_id": empresa_id})
    total_kits = await db.kits.count_documents({"empresa_id": empresa_id})
    total_deliveries = await db.deliveries.count_documents({"empresa_id": empresa_id})
    
    print(f"📊 Empresas: {total_empresas}")
    print(f"👥 Colaboradores: {total_colaboradores}")
    print(f"🦺 EPIs: {total_epis}")
    print(f"📦 Kits: {total_kits}")
    print(f"📋 Entregas: {total_deliveries}")
    print("="*60)
    
    print("\n✅ Dados de demonstração criados com sucesso!")

if __name__ == "__main__":
    asyncio.run(create_demo_data())
