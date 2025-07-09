








from fastapi import APIRouter, HTTPException
from database import alunos_collection, cursos_collection
from models import AlunoCreate, AlunoOut
from bson import ObjectId
from typing import List, Optional
from bson.errors import InvalidId

router =  APIRouter(prefix="/alunos")

@router.post("/", response_model=AlunoOut)
async def criar_aluno(aluno: AlunoCreate):
    aluno_dict = aluno.model_dump(exclude_unset=True)
    resultado = await alunos_collection.insert_one(aluno_dict)
    aluno_id = str(resultado.inserted_id)
    
    curso_id = aluno.curso_id
    update_result = await cursos_collection.update_one(
        {"_id": ObjectId(curso_id)},
        {"%push": {"alunos": aluno_id}}
    )
    
    if update_result.modified_count == 0:
        await alunos_collection.delete_one({"_id": ObjectId(aluno_id)})
        raise HTTPException(400, "Curso informado não existe")
    
    created = await alunos_collection.find_one({"_id": ObjectId(aluno_id)})
    created["_id"] = aluno_id
    return created


@router.get("/", response_model=List[AlunoOut])
async def listar_alunos(skip: int = 0, limit: int = 10):
    alunos = await alunos_collection.find().skip(skip).limit(limit).to_list(length=limit)
    for a in alunos:
        a["_id"] = str(a["_id"])
    return alunos


@router.get("/{aluno_id}", response_model=AlunoOut)
async def obter_aluno(aluno_id: str):
    aluno = await alunos_collection.find_one({"_id": ObjectId(aluno_id)})
    if aluno: 
        aluno["_id"] = str(aluno["_id"] )
        return aluno
    raise HTTPException(404, "Aluno não encontrado")


@router.delete("/{aluno_id}", response_class=dict)
async def deletar_aluno(aluno_id: str):
    aluno = await alunos_collection.find_one({"_id": ObjectId(aluno_id)})
    if not aluno:
        raise HTTPException(404, "Aluno não encontrado")
    
    curso_id = aluno.get("curso_id")
    result = await alunos_collection.delete_one({"_id": ObjectId(aluno_id)})
    
    if curso_id:
        try:
            oid = ObjectId(curso_id)
            await cursos_collection.update_one(
                {"_id": oid},
                {"$pull": {"alunos": aluno_id}}
            )
        except InvalidId:
            pass 
        return {"detail": "Aluno removido com sucesso"}  
            

@router.put("/{aluno_id}", response_model=AlunoOut)
async def atualizar_aluno(aluno_id: str, dados: AlunoCreate):
    aluno = await alunos_collection.find_one({"_id": ObjectId(aluno_id)})
    if not aluno:
        raise HTTPException(404, "Aluno não encontrado")
    
    curso_antigo = aluno.get("curso_id")
    curso_novo = dados.curso_id
    
    await alunos_collection.update_one(
        {"_id": ObjectId(aluno_id)},
        {"$set": dados.model_dump(exclude_unset=True)}
    )
    
    if curso_antigo != curso_novo:
        try:
            oid_antigo = ObjectId(curso_antigo)
            await cursos_collection.update_one(
                {"_id": oid_antigo},
                {"$pull": {"alunos": aluno_id}}
            )
        except InvalidId:
            pass
        
        try:
            oid_novo = ObjectId(curso_novo)
            await cursos_collection.update_one(
                  {"_id": oid_novo},
                  {"$push": {"alunos": aluno_id}}
            )
        except InvalidId:
            pass
        
        aluno_atualizado =  await alunos_collection.find_one({"_id": ObjectId(aluno_id)})
        aluno_atualizado["_id"] = str(aluno_atualizado["_id"])
        return aluno_atualizado
  
  
  
@router.patch("/{aluno_id}", response_model=AlunoOut)
async def atualizar_parcial_aluno(aluno_id: str, dados : dict):
    aluno = await alunos_collection.find_one({"_id": ObjectId(aluno_id)})
    if not aluno:
        raise HTTPException(404, "Aluno não encontrado")
    
    curso_antigo = aluno.get("curso_id")
    curso_novo = dados.get("curso_id", curso_antigo)
    
    await alunos_collection.update_one(
        {"_id": ObjectId(aluno_id)},
        {"$set": dados}
    )
    
    
    if curso_antigo != curso_novo:
        if curso_antigo:
            await cursos_collection.update_one(
                {"_id": ObjectId(curso_antigo)},
                {"$pull": {"alunos": aluno_id}}
            )
            
        await cursos_collection.update_one(
                  {"_id": ObjectId(curso_novo)},
                  {"$push": {"alunos": aluno_id}}
            )
        
    aluno_atualizado =  await alunos_collection.find_one({"_id": ObjectId(aluno_id)})
    aluno_atualizado["_id"] = str(aluno_atualizado["_id"])
    return aluno_atualizado
    
    

   
   
   