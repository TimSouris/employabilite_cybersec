FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1

WORKDIR /

COPY . .

RUN pip install --upgrade pip && pip install \
	beautifulsoup4 \
	jobspy \
	matplotlib \
	pandas \
	pyfiglet \
	python-dotenv \
	requests \
	selenium \
	webdriver-manager \
	wordcloud

CMD ["python", "Main.py"]
