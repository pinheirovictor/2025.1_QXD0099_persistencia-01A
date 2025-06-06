# routers/advanced.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func, union_all, literal_column
from typing import List, Optional, Dict, Any
from models import User, Product, Order
from core.database import get_session
from datetime import date
from models.user import User, UserRead
from models.product import Product, ProductRead
from models.order import Order, OrderRead
from models.order_product import OrderProduct
from models.user import User
from models.profile import Profile


router = APIRouter(prefix="/advanced", tags=["Consultas Avançadas"])




@router.get("/usuarios-com-perfis-existentes", response_model=List[Dict[str, Any]])
def get_usuarios_com_perfis_existentes(
    session: Session = Depends(get_session)
):
    """
    Retorna uma lista de usuários que possuem um perfil associado,
    juntamente com seus dados de perfil.
    """
    # A declaração de SELECT e JOIN
    statement = (
        select(
            User.nome.label("nome_usuario"),
            User.email.label("email_usuario"),
            Profile.endereco.label("endereco_perfil"),
            Profile.telefone.label("telefone_perfil")
        )
        .join(Profile, Profile.user_id == User.id) # Isso é o INNER JOIN!
    )

    results = session.exec(statement).all()

    # Formatação dos resultados para uma melhor visualização
    formatted_results = []
    for user_nome, user_email, profile_endereco, profile_telefone in results:
        formatted_results.append({
            "nome_usuario": user_nome,
            "email_usuario": user_email,
            "perfil": {
                "endereco": profile_endereco,
                "telefone": profile_telefone
            }
        })
    
    return formatted_results


@router.get("/todos-os-produtos-com-detalhes-de-pedido", response_model=List[Dict[str, Any]])
def get_todos_os_produtos_com_detalhes_de_pedido(
    session: Session = Depends(get_session)
):
    """
    Retorna todos os produtos do marketplace e, para aqueles que fazem parte de um pedido,
    inclui os detalhes da quantidade comprada e do pedido.
    Produtos sem pedidos aparecerão, mas com os campos do pedido como NULL.
    """
    statement = (
        select(
            Product.id.label("produto_id"),
            Product.nome.label("nome_produto"),
            Product.preco.label("preco_produto"),
            OrderProduct.quantidade.label("quantidade_comprada"),
            Order.id.label("pedido_id"),
            Order.data.label("data_pedido")
        )
        # O LEFT JOIN é a chave aqui! A tabela da esquerda é 'Product'.
        .outerjoin(OrderProduct, OrderProduct.product_id == Product.id) # Usamos outerjoin para LEFT/RIGHT/FULL
        .outerjoin(Order, Order.id == OrderProduct.order_id)
        # NOTA: Em SQLModel/SQLAlchemy, 'outerjoin' é usado para LEFT e FULL OUTER JOIN.
        # Por padrão, outerjoin() faz um LEFT OUTER JOIN.
    )

    results = session.exec(statement).all()

    # Formatação dos resultados para uma melhor visualização
    # Agrupamos os detalhes dos pedidos para cada produto
    produtos_map: Dict[int, Dict[str, Any]] = {}

    for row in results:
        product_id = row.produto_id
        if product_id not in produtos_map:
            produtos_map[product_id] = {
                "id": row.produto_id,
                "nome": row.nome_produto,
                "preco": row.preco_produto,
                "pedidos_relacionados": []
            }
        
        # Adiciona detalhes do pedido apenas se o produto estiver em um pedido
        # Note que se Order.id for None, significa que o produto não tem pedido relacionado nesta linha
        if row.pedido_id is not None:
            produtos_map[product_id]["pedidos_relacionados"].append({
                "pedido_id": row.pedido_id,
                "quantidade_comprada": row.quantidade_comprada,
                "data_pedido": row.data_pedido
            })
    
    return list(produtos_map.values())


@router.get("/todos-os-perfis-com-detalhes-de-usuario", response_model=List[Dict[str, Any]])
def get_todos_os_perfis_com_detalhes_de_usuario(
    session: Session = Depends(get_session)
):
    """
    Retorna todos os perfis cadastrados no sistema e, para cada perfil,
    inclui os detalhes do usuário associado, se houver.
    Perfis sem usuário aparecerão, mas com os campos do usuário como NULL.
    """
    statement = (
        select(
            Profile.id.label("profile_id"),
            Profile.endereco.label("endereco_perfil"),
            Profile.telefone.label("telefone_perfil"),
            User.id.label("user_id"),
            User.nome.label("nome_usuario"),
            User.email.label("email_usuario")
        )
        # Em SQLModel/SQLAlchemy, como mencionado antes, 'outerjoin' é usado para LEFT e FULL OUTER JOIN.
        # Para simular um RIGHT JOIN, nós simplesmente invertemos a ordem das tabelas no join()
        # e usamos outerjoin() no 'Profile' (que agora é a tabela "esquerda" na perspectiva do join)
        # e o 'User' (que é a "direita" no join)
        .select_from(Profile) # Explicitamente define Profile como a tabela inicial
        .outerjoin(User, Profile.user_id == User.id) # Isso funciona como um LEFT JOIN de Profile para User
                                                     # mas se a sua intenção fosse um RIGHT JOIN SQL puro
                                                     # onde a 'direita' é o foco, a forma mais idiomática
                                                     # no SQLAlchemy é sempre usar LEFT JOIN e reordenar.
    )

    results = session.exec(statement).all()

    # Formatação dos resultados para uma melhor visualização
    formatted_results = []
    for row in results:
        formatted_results.append({
            "id_perfil": row.profile_id,
            "endereco": row.endereco_perfil,
            "telefone": row.telefone_perfil,
            "usuario": {
                "id": row.user_id,
                "nome": row.nome_usuario,
                "email": row.email_usuario
            } if row.user_id is not None else None # Retorna None se não houver usuário associado
        })
    
    return formatted_results


@router.get("/usuarios-e-produtos-completos", response_model=List[Dict[str, Any]])
def get_usuarios_e_produtos_completos(
    session: Session = Depends(get_session)
):
    """
    Simula um FULL OUTER JOIN entre Users e Products.
    Retorna todos os usuários (com seus produtos se forem vendedores)
    E todos os produtos (com seus vendedores se existirem),
    incluindo casos onde não há correspondência.
    """
    # Consulta 1: LEFT JOIN de User para Product (Todos os usuários e seus produtos, se forem vendedores)
    # Produtos sem vendedor aparecerão com campos de produto NULL
    query_left = (
        select(
            User.id.label("user_id"),
            User.nome.label("user_nome"),
            User.email.label("user_email"),
            Product.id.label("product_id"),
            Product.nome.label("product_nome"),
            Product.preco.label("product_preco"),
            literal_column("'User'").label("source") # Para identificar a origem
        )
        .outerjoin(Product, User.id == Product.vendedor_id)
    )

    # Consulta 2: LEFT JOIN de Product para User (Todos os produtos e seus vendedores)
    # Usuários sem produtos aparecerão com campos de usuário NULL
    # Excluímos aqui os registros que já foram pegos na primeira consulta (onde User.id não é NULL)
    # para evitar duplicatas antes do UNION, embora UNION ALL seja mais comum para ver todas as linhas
    query_right = (
        select(
            User.id.label("user_id"),
            User.nome.label("user_nome"),
            User.email.label("user_email"),
            Product.id.label("product_id"),
            Product.nome.label("product_nome"),
            Product.preco.label("product_preco"),
            literal_column("'Product'").label("source") # Para identificar a origem
        )
        .outerjoin(User, Product.vendedor_id == User.id)
        .where(User.id.is_(None)) # Apenas produtos sem um vendedor correspondente já listado acima.
                                  # Isso é para simular FULL OUTER JOIN ao juntar os sets
    )

    # Combinando as duas consultas com UNION ALL
    # UNION ALL inclui duplicatas se houver, o que é o comportamento do FULL OUTER JOIN.
    # Se usássemos UNION (sem ALL), ele removeria duplicatas, o que nem sempre é o desejado para FULL JOIN.
    full_outer_statement = union_all(query_left, query_right)

    results = session.exec(full_outer_statement).all()

    # Formatação dos resultados para uma melhor visualização
    # É preciso uma lógica para agrupar e remover duplicatas conceituais
    # pois o UNION ALL pode listar o mesmo par (user, product) duas vezes se houver correspondência
    # O objetivo aqui é ter uma lista de entidades (usuários ou produtos) e suas associações
    
    unique_entries: Dict[str, Dict[str, Any]] = {}
    
    for row in results:
        # Gerar uma chave única para identificar a entrada combinada
        # Tentamos identificar o usuário e/ou o produto para agrupar
        key = None
        if row.user_id is not None and row.product_id is not None:
            key = f"user_{row.user_id}_product_{row.product_id}"
        elif row.user_id is not None:
            key = f"user_{row.user_id}_no_product"
        elif row.product_id is not None:
            key = f"product_{row.product_id}_no_user"
        
        if key not in unique_entries:
            unique_entries[key] = {
                "user": {
                    "id": row.user_id,
                    "nome": row.user_nome,
                    "email": row.user_email
                } if row.user_id is not None else None,
                "product": {
                    "id": row.product_id,
                    "nome": row.product_nome,
                    "preco": row.product_preco
                } if row.product_id is not None else None,
                "relationship_type": "correspondence" if row.user_id and row.product_id else "no_product" if row.user_id else "no_user"
            }
    
    return list(unique_entries.values())








# 3. Busca por texto parcial (nome do produto)
@router.get("/produtos-busca")
def busca_produtos(nome: Optional[str] = None, session: Session = Depends(get_session)):
    statement = select(Product)
    if nome:
        statement = statement.where(Product.nome.contains(nome))
    produtos = session.exec(statement).all()
    return produtos


# 5. Agregação e contagem (quantos produtos por vendedor)
@router.get("/conta-produtos-por-vendedor")
def conta_produtos_por_vendedor(session: Session = Depends(get_session)):
    statement = (
        select(Product.vendedor_id, func.count(Product.id).label("total_produtos"))
        .group_by(Product.vendedor_id)
    )
    result = session.exec(statement).all()
    return [{"vendedor_id": v_id, "total_produtos": total} for v_id, total in result]


# 6. Classificação/Ordenação (produtos ordenados por preço desc)
@router.get("/produtos-ordenados", response_model=List[ProductRead])
def produtos_ordenados(session: Session = Depends(get_session)):
    statement = select(Product).order_by(Product.preco.desc())
    produtos = session.exec(statement).all()
    return produtos




# Filtragem Avançada (WHERE)
@router.get("/produtos-filtrados", response_model=List[ProductRead], summary="Filtragem avançada de produtos")
def get_produtos_filtrados(
    nome: Optional[str] = Query(None, description="Busca parcial pelo nome do produto"),
    preco_min: Optional[float] = Query(None, ge=0, description="Preço mínimo do produto"),
    preco_max: Optional[float] = Query(None, ge=0, description="Preço máximo do produto"),
    descricao_like: Optional[str] = Query(None, description="Busca parcial na descrição (case-insensitive)"),
    vendedor_id: Optional[List[int]] = Query(None, description="Filtrar por IDs de vendedor (use múltiplos para IN)"),
    sem_descricao: Optional[bool] = Query(None, description="Filtrar produtos sem descrição (True) ou com descrição (False)"),
    session: Session = Depends(get_session)
):
    """
    Realiza uma busca avançada de produtos combinando diversas condições de filtragem.
    """
    statement = select(Product)

    # Combinação de múltiplas condições usando AND
    if nome:
        statement = statement.where(Product.nome.contains(nome)) # LIKE %nome%
    if preco_min is not None:
        statement = statement.where(Product.preco >= preco_min) # Operador de comparação >=
    if preco_max is not None:
        statement = statement.where(Product.preco <= preco_max) # Operador de comparação <=

    # Uso de LIKE para strings (ou ILIKE para case-insensitive, que é comum no SQL, mas .contains()
    # do SQLModel geralmente já é case-insensitive em SQLite/PostgreSQL para buscas parciais)
    if descricao_like:
        # Para case-insensitive em SQLModel/SQLAlchemy, você pode usar .ilike() ou .lower()
        # Em SQLite, .contains() e .like() já são case-insensitive por padrão para ASCII
        statement = statement.where(Product.descricao.ilike(f"%{descricao_like}%")) # ILIKE (case-insensitive)

    # Operadores de conjunto (IN)
    if vendedor_id:
        statement = statement.where(Product.vendedor_id.in_(vendedor_id))

    # Verificação de nulidade (IS NULL / IS NOT NULL)
    if sem_descricao is not None:
        if sem_descricao:
            statement = statement.where(Product.descricao.is_(None)) # IS NULL
        else:
            statement = statement.where(Product.descricao.is_not(None)) # IS NOT NULL

    produtos = session.exec(statement).all()
    return produtos


@router.get("/vendedores-com-mais-de-x-reais-vendidos", summary="Vendedores com total de vendas acima de um valor")
def get_vendedores_com_total_vendas(
    min_vendas_total: float = Query(0, ge=0, description="Valor mínimo total de vendas que um vendedor deve ter"),
    session: Session = Depends(get_session)
):
    """
    Retorna vendedores cujo total de vendas (soma do preço * quantidade dos produtos em pedidos)
    excede um valor mínimo.
    Demonstra GROUP BY, SUM e HAVING.
    """
    statement = (
        select(
            User.id.label("vendedor_id"),
            User.nome.label("nome_vendedor"),
            func.sum(Product.preco * OrderProduct.quantidade).label("total_vendas") # SUM()
        )
        .join(Product, Product.vendedor_id == User.id) # Junta User e Product para pegar o vendedor
        .join(OrderProduct, OrderProduct.product_id == Product.id) # Junta com OrderProduct para quantidades
        .group_by(User.id, User.nome) # GROUP BY
        .having(func.sum(Product.preco * OrderProduct.quantidade) >= min_vendas_total) # HAVING
        .order_by(func.sum(Product.preco * OrderProduct.quantidade).desc()) # Ordena para ver os maiores
    )

    results = session.exec(statement).all()

    # Formatar os resultados
    formatted_results = [
        {
            "vendedor_id": r.vendedor_id,
            "nome_vendedor": r.nome_vendedor,
            "total_vendas": float(r.total_vendas) # Converter para float se necessário
        }
        for r in results
    ]
    return formatted_results