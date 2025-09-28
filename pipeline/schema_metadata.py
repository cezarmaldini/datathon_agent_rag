from pydantic import BaseModel, Field

class ResumeCurriculum(BaseModel):
    name: str = Field(description='Nome do candidato')
    email: str = Field(description='Endereço de email do candidato')
    phone: str = Field(description='Telefone de contato do candidato')
    location: str = Field(description='Cidade e Estado do candidato (Exemplo: São Paulo/SP)')
    summary: str = Field(description='Resumo do currículo do candidato')
    academic_level: str = Field(description='Nível acadêmico do candidato')
    areas_of_expertise: list[str] = Field(description='Áreas de atuação do candidato')
    technical_skills: list[str] = Field(description='Competências técnicas e tecnologias do candidato')
    behavioral_skills: list[str] = Field(description='Habilidades comportamentais do candidato')
    pcd: bool = Field(description='Candidato com deficiência (PCD)')