FROM docker.artifactory.ccta.dk/centos/python-36-centos7

# RUN yum install epel-release \
#                 python3-pip python3-devel gcc -y

# WORKDIR /opt/minitower
# COPY ./test/requirements.txt ./
# RUN pip3 install -r requirements.txt

# RUN django-admin startproject minitower /opt/minitower/ && \
#     python3 manage.py makemigrations && \
#     python3 manage.py migrate && \
#     python3 manage.py startapp inventory
# COPY ./unittest/AppSettingsfile.py ./minitower/settings.py
# COPY ./unittest/AppUrlsFile.py ./minitower/urls.py
# COPY ./unittest/main.css ./static/main/css/
# COPY ./unittest/base.html ./templates/base.html
# COPY . ./inventory/


# RUN  python3 manage.py migrate && python3 manage.py collectstatic 
# EXPOSE 8000
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
