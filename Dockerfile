FROM python:3.13-slim

WORKDIR /app


COPY ./src ./src
COPY ./config ./config
COPY model.onnx ./model.onnx
COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD ["python", "-m", "src.main"]