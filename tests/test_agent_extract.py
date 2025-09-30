from llama_cloud_services import LlamaExtract
from config.settings import Settings
from pipeline.schema_metadata import ResumeCurriculum


settings = Settings()

extractor = LlamaExtract(api_key=settings.llama_cloud_api_key)

agent = extractor.create_agent(name='test', data_schema=ResumeCurriculum)

result = agent.extract(files='data/teste.pdf')

print(result.data)