from config import clients
from config.settings import Settings
from pipeline import create_collection

def main(settings: Settings):
    create_collection.create_collections(settings=settings)

if __name__ == '__main__':
    projects_settings = Settings()
    main(projects_settings)