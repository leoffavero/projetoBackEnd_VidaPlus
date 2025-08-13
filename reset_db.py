from app.database import Base, engine

#resetar o database (utilizar só se necessário)
print("Apagando todas as tabelas...")
Base.metadata.drop_all(bind=engine)

print("Criando todas as tabelas...")
Base.metadata.create_all(bind=engine)

print("Banco de dados resetado com sucesso!")
