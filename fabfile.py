import os

from fabric.api import run, sudo
from fabric.api import prefix, warn, abort
from fabric.api import task, env
from fabric.contrib.files import exists
from fabric.context_managers import cd

env.hosts = ['smallweb1.openprescribing.net']
env.forward_agent = True
env.colorize_errors = True
env.repo = "thedatalab"
env.django_project = env.repo + "/thedatalab"

environments = {
    'live': 'thedatalab',
    'staging': 'thedatalab_staging',
}


def sudo_script(script):
    """Run script under `deploy/fab_scripts/` as sudo.

    We don't use the `fabric` `sudo()` command, because instead we
    expect the user that is running fabric to have passwordless sudo
    access.  In this configuration, that is achieved by the user being
    a member of the `fabric` group (see `setup_sudo()`, below).

    """
    return run('sudo ' +
        os.path.join(
            env.path,
            '%s/deploy/fab_scripts/%s' % (env.repo, script))
    )


def make_directory():
    if not exists(env.path):
        sudo("mkdir -p %s" % env.path)
        sudo("chown -R www-data:www-data %s" % env.path)
        sudo("chmod  g+w %s" % env.path)

def venv_init():
    run('[ -e venv ] || python3.5 -m venv venv')

def pip_install():
    with prefix('source venv/bin/activate'):
        run('pip install --upgrade pip setuptools')
        run('pip install -q -r %s/requirements.txt' % env.repo)

def update_from_git(branch):
    # clone or update code
    if not exists('%s/.git' % env.repo):
        run("git clone -q git@github.com:ebmdatalab/%s.git" % env.repo)
    with cd(env.repo):
        run("git fetch --all")
        run("git reset --hard origin/{}".format(branch))

def setup_nginx():
    sudo_script('setup_nginx.sh %s %s' % (env.path, env.app))


def setup_django():
    with prefix('source venv/bin/activate'):
        run('cd %s/ && python manage.py collectstatic --noinput --settings=thedatalab.settings' % env.django_project)
        run('cd %s/ && python manage.py migrate --settings=thedatalab.settings' % env.django_project)

def restart_gunicorn():
    sudo_script("restart.sh %s" % env.app)

def reload_nginx():
    sudo_script("reload_nginx.sh")

def setup(environment, branch='master'):
    if environment not in environments:
        abort("Specified environment must be one of %s" %
              ",".join(environments.keys()))
    env.app = environments[environment]
    env.environment = environment
    env.path = "/var/www/%s" % env.app
    env.branch = branch
    return env


@task
def deploy(environment, branch='master'):
    env = setup(environment, branch)
    make_directory()
    with cd(env.path):
        with prefix("source /etc/profile.d/%s.sh" % env.app):
            venv_init()
            update_from_git(branch)
            pip_install()
            setup_django()
            setup_nginx()
            restart_gunicorn()
            reload_nginx()
