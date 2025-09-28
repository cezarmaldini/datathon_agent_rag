CREATE TABLE vagas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    data_requisicao DATE NOT NULL,
    titulo_vaga VARCHAR(200) NOT NULL,
    tipo_contratacao VARCHAR(50) NOT NULL,
    vaga_pcd BOOLEAN DEFAULT FALSE,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    pais VARCHAR(50) DEFAULT 'Brasil',
    nivel_profissional VARCHAR(50) NOT NULL,
    nivel_academico VARCHAR(50) NOT NULL,
    areas_atuacao TEXT[] NOT NULL,
    principais_atividades TEXT NOT NULL,
    competencias_tecnicas TEXT[] NOT NULL,
    habilidades_comportamentais TEXT[] NOT NULL,
    modalidade VARCHAR(50) NOT NULL,
    ativa BOOLEAN DEFAULT TRUE,
    criada_em TIMESTAMPTZ DEFAULT NOW(),
    atualizada_em TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para otimização
CREATE INDEX idx_vagas_ativa ON vagas(ativa);
CREATE INDEX idx_vagas_data_requisicao ON vagas(data_requisicao);
CREATE INDEX idx_vagas_cidade ON vagas(cidade);
CREATE INDEX idx_vagas_nivel_profissional ON vagas(nivel_profissional);

-- Trigger para atualizar automaticamente o campo atualizada_em
CREATE OR REPLACE FUNCTION update_atualizada_em()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizada_em = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_atualizada_em
    BEFORE UPDATE ON vagas
    FOR EACH ROW
    EXECUTE FUNCTION update_atualizada_em();