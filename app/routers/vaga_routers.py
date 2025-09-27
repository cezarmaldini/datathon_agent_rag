from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from app.models.vaga_models import (
    VagaCreate, 
    VagaUpdate, 
    VagaResponse, 
    VagasListResponse
)
from app.services.vaga_crud import VagaCRUD
from config.clients import get_db

router = APIRouter(prefix="/vagas", tags=["vagas"])


def get_vaga_crud(db: Session = Depends(get_db)) -> VagaCRUD:
    return VagaCRUD(db)


@router.post(
    "/", 
    response_model=VagaResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova vaga",
    description="Cria uma nova vaga de emprego no sistema"
)
async def criar_vaga(
    vaga: VagaCreate,
    crud: VagaCRUD = Depends(get_vaga_crud)
):
    """
    Cria uma nova vaga de emprego com todos os dados necessários.
    """
    try:
        return crud.criar_vaga(vaga)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar vaga: {str(e)}"
        )


@router.get(
    "/", 
    response_model=VagasListResponse,
    summary="Listar vagas",
    description="Retorna uma lista paginada de todas as vagas"
)
async def listar_vagas(
    pagina: int = Query(1, ge=1, description="Número da página"),
    por_pagina: int = Query(100, ge=1, le=1000, description="Itens por página"),
    ativa: Optional[bool] = Query(None, description="Filtrar por status da vaga"),
    crud: VagaCRUD = Depends(get_vaga_crud)
):
    """
    Retorna uma lista paginada de vagas. Pode ser filtrada por status (ativa/inativa).
    """
    try:
        skip = (pagina - 1) * por_pagina
        vagas, total = crud.listar_vagas(skip=skip, limit=por_pagina, ativa=ativa)
        
        return VagasListResponse(
            vagas=vagas,
            total=total,
            pagina=pagina,
            por_pagina=por_pagina
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar vagas: {str(e)}"
        )


@router.get(
    "/{vaga_id}", 
    response_model=VagaResponse,
    summary="Obter vaga específica",
    description="Retorna os detalhes de uma vaga específica pelo ID"
)
async def obter_vaga(
    vaga_id: UUID,
    crud: VagaCRUD = Depends(get_vaga_crud)
):
    """
    Retorna os detalhes completos de uma vaga específica.
    """
    vaga = crud.obter_vaga(vaga_id)
    if not vaga:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vaga não encontrada"
        )
    return vaga


@router.put(
    "/{vaga_id}", 
    response_model=VagaResponse,
    summary="Atualizar vaga",
    description="Atualiza os dados de uma vaga existente"
)
async def atualizar_vaga(
    vaga_id: UUID,
    vaga_update: VagaUpdate,
    crud: VagaCRUD = Depends(get_vaga_crud)
):
    """
    Atualiza os dados de uma vaga existente. Apenas os campos fornecidos serão atualizados.
    """
    vaga_atualizada = crud.atualizar_vaga(vaga_id, vaga_update)
    if not vaga_atualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vaga não encontrada"
        )
    return vaga_atualizada


@router.delete(
    "/{vaga_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir vaga",
    description="Exclui permanentemente uma vaga do sistema"
)
async def excluir_vaga(
    vaga_id: UUID,
    crud: VagaCRUD = Depends(get_vaga_crud)
):
    """
    Exclui permanentemente uma vaga do sistema.
    """
    sucesso = crud.excluir_vaga(vaga_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vaga não encontrada"
        )
    return None