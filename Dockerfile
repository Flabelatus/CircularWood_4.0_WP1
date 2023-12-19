FROM python:3.10
EXPOSE 5000
WORKDIR /app

RUN useradd -m -s /bin/bash robotlab
RUN chown -R robotlab:robotlab /app
USER robotlab

COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY . .

CMD ["flask", "run", "--host", "0.0.0.0"]