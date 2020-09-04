from app import create_app
from app.config import Config

config = Config()

app = create_app(config)

if __name__ == "__main__":
    app.run()