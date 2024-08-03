FROM continuumio/miniconda3:24.5.0-0

COPY environment.yml /tmp/environment.yml

WORKDIR /app

RUN conda env create -f /tmp/environment.yml

COPY bot /app

COPY .env /app

CMD ["conda", "run", "-n", "ticket-tortoise", "python", "bot.py"]
