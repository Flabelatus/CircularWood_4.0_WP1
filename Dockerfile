FROM python:3.10
WORKDIR /app

RUN useradd -m -s /bin/bash robotlab
RUN chown -R robotlab:robotlab /app
USER robotlab

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]