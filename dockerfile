FROM python:3.9-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install fastapi openai slowapi python-dotenv requests uvicorn python-multipart
COPY ./ /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
