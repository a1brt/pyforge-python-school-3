FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src ./src
EXPOSE 8000
ENTRYPOINT ["uvicorn", "src.main:app"] 
CMD ["--host", "0.0.0.0", "--port", "8000"]