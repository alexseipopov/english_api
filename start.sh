export SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://postgres:postgres@localhost:5432/english"
flask --app=english_api db migrate
docker-compose down
docker-compose up --build -d