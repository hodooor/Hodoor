from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random
from getpass import getpass

REPO_URL = 'https://github.com/hodooor/Hodoor/'

def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _set_database_permissions(site_folder)

def input_password(text):
    while True:
        password = getpass(text)
        again = getpass("password (again): ")
        if (len(password) < 8):
            print("This password is too short. It must contain at least 9 characters.")
            continue
        if (password != again):
            print("Error: Your passwords didn't match.")
            continue
        return password
        
def create_superuser():
    source_folder = '/home/%s/sites/%s/source' % (env.user, env.host)
    run('cd %s && ../virtualenv/bin/python3 manage.py createsuperuser' % (source_folder))

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database','static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' %(source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture = True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/ticker/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path,
            'CSRF_COOKIE_SECURE = False',
            'CSRF_COOKIE_SECURE = True'
    )
    sed(settings_path,
            'SESSION_COOKIE_SECURE = False',
            'SESSION_COOKIE_SECURE = True'
    )
    sed(settings_path,
            'ALLOWED_HOSTS =.+$',
            'ALLOWED_HOSTS =["%s"]' % (site_name,)
    )
    settings_secret_file = source_folder + '/ticker/settings_secret.py'
    if not exists(settings_secret_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(settings_secret_file, "SECRET_KEY = '%s'" % (key, ))
        email_host_password = input_password("Enter the EMAIL_HOST_PASSWORD: ")
        append(settings_secret_file, "EMAIL_HOST_PASSWORD = '%s'" % (email_host_password, ))
    else:
        lines = open(os.path.join(source_folder, '/ticker/settings_secret.py'), "r").readlines()
        for line in lines:
            if "EMAIL_HOST_PASSWORD" in line:
                break
        else:
            email_host_password = input_password("Enter the EMAIL_HOST_PASSWORD: ")
            append(settings_secret_file, "EMAIL_HOST_PASSWORD = '%s'" % (email_host_password, ))
    append(settings_path, '\nfrom .settings_secret import SECRET_KEY, EMAIL_HOST_PASSWORD')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder, ))
    run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
    ))

def _update_static_files(source_folder):
    run('cd %s && npm install' % (
            source_folder,
    ))
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
            source_folder,
    ))

def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
            source_folder,
    ))
def _set_database_permissions(site_folder):
    database_folder = site_folder + "/database"
    static_folder = site_folder + "/static"

    run('sudo chgrp www-data %s' % (database_folder, )) #set group to folder
    run('sudo chgrp www-data %s/db.sqlite3' % (database_folder, )) #and file
    run('sudo chgrp www-data -R %s' % (static_folder, ))

    run('sudo chmod 770 %s' % (database_folder, ))
    run('sudo chmod 770 %s/db.sqlite3' % (database_folder, ))
    run('sudo chmod -R 770 %s' % (static_folder, ))
def _set_restart_apache():
    run('sudo systemctl restart apache2')
