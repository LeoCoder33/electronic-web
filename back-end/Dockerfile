FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . /app
EXPOSE 5000
# CMD [ "python", "app.py" ]
# CMD ["python", "-m", "flask", "run", "--host=0.0,0,0"]
CMD ["flask", "run", "--host=0.0.0.0"]