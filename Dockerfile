FROM python:3.8-slim-buster

ENV PIPENV_NOSPIN true
ENV PYTHONUNBUFFERED 1

# install packages
RUN apt-get -y update \
    && apt-get install -y build-essential gettext libpq-dev\
    && apt-get install -y wkhtmltopdf\
    && apt-get install -y gdal-bin\
    && apt-get install -y libgdal-dev\
    && apt-get install -y --no-install-recommends software-properties-common\
    && apt-add-repository contrib\
    && apt-get update

# If you want to use Microsoft fonts in reports, you must install the fonts
# Andale Mono, Arial Black, Arial, Comic Sans MS, Courier New, Georgia, Impact,
# Times New Roman, Trebuchet, Verdana,Webdings)
# RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections
# RUN apt-get install -y --no-install-recommends fontconfig ttf-mscorefonts-installer
# ADD localfonts.conf /etc/fonts/local.conf
# RUN fc-cache -f -v

# Install chromium
# RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
# RUN apt-get update -y && apt-get install -y google-chrome-stable

RUN pip install --upgrade pip pipenv

# Set volume for database and static files.
RUN mkdir -p /static /media

WORKDIR /app

# install requirements
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
# get env or set default
ARG STATIC_ROOT
ENV STATIC_ROOT ${STATIC_ROOT:-/static/}

ARG MEDIA_ROOT
ENV MEDIA_ROOT ${MEDIA_ROOT:-/media/}

ARG PORT
ENV PORT ${PORT:-8000}

ARG PROCESSES_NUM
ENV PROCESSES_NUM ${PROCESSES_NUM:-4}

COPY . /app

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

RUN python manage.py collectstatic --noinput

CMD ["/docker-entrypoint.sh"]
