FROM python:3.8

# set work directory
WORKDIR /usr/scr/app

#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE "insurance_company_assignment.settings.local"

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements/base.txt ./requirements/base.txt
COPY ./requirements/local.txt ./requirements/local.txt
RUN pip install -r ./requirements/local.txt

# copy project
COPY . .