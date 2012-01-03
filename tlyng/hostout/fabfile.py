from collective.hostout.hostout import buildoutuser, asbuildoutuser
from fabric import api, contrib
from fabric.context_managers import cd
from pkg_resources import resource_filename

import os
import os.path
import time
import tempfile


def requireOwnership (file, user=None, group=None, recursive=False):

    if bool(user) !=  bool(group):  # logical xor
        signature = user or group
        sigFormat = (user and "%U") or "%G"
    else:
        signature = "%s:%s" % (user, group)
        sigFormat = "%U:%G"

    if recursive:
        opt = "-R"
    else:
        opt = ""

    getOwnerGroupCmd = "stat --format=%s '%s'" % (sigFormat, file)
    chownCmd = "chown %(opt)s %(signature)s '%(file)s'" % locals()

    api.env.hostout.sudo ('[ `%(getOwnerGroupCmd)s` == "%(signature)s" ] || %(chownCmd)s' % locals())


def bootstrap_users_ubuntu():
    api.env.hostout.bootstrap_users()

def bootstrap_buildout_ubuntu():
    path = api.env.path
    buildout = api.env['buildout-user']
    buildoutgroup = api.env['buildout-group']
    buildoutcache = api.env['buildout-cache']

    if path[0] == "/":
        save_path = api.env.path # the pwd may not yet exist
        api.env.path = "/"

    #api.sudo('mkdir -p -m ug+x %s' % path)
    api.sudo('mkdir -p %s' % path)
    api.sudo('mkdir -p %s' % os.path.join(buildoutcache, "eggs"))
    api.sudo('mkdir -p %s' % os.path.join(buildoutcache, "downloads/dist"))
    api.sudo('mkdir -p %s' % os.path.join(buildoutcache, "extends"))
    requireOwnership(buildoutcache, user=buildout, group=buildoutgroup, recursive=True)
    requireOwnership(path, user=buildout, group=buildoutgroup, recursive=True)
    if path[0] == "/":
        api.env.path = save_path # restore the pwd

    with asbuildoutuser():
        bootstrap = resource_filename(__name__, 'bootstrap.py')

        with cd(path):
            api.put(bootstrap, '%s/bootstrap.py' % path)
            api.run('echo "[buildout]" > buildout.cfg')

            # Get python
            version = api.env['python-version']
            major = '.'.join(version.split('.')[:2])
            python = 'python%s' % major

            # Bootstrap baby!
            api.run('%s bootstrap.py --distribute --version=1.4.4' % python)


def bootstrap():
    hostout = api.env.hostout
    path = api.env.path
    hostos = api.env.get('hostos','').lower()
    version = api.env['python-version']
    major = '.'.join(version.split('.')[:2])
    majorshort = major.replace('.','')
 
    d = api.run("lsb_release -rd")
    api.run('uname -r')

    api.sudo('apt-get -y update')
    api.sudo('apt-get -y upgrade ')
    api.sudo('apt-get -yq install '
             'build-essential '
             'ncurses-dev '
             'libncurses5-dev '
             'libz-dev '
             'libdb4.6 '
             'libxp-dev '
             'libreadline5 '
             'libreadline5-dev '
             'python%(major)s '
             'python%(major)s-dev '
             'libpcre3-dev '
             'libssl-dev '
             'python-imaging '
             'wv '
             'poppler-utils '
             'xsltproc '
             'xlhtml '
             'ppthtml '
             'unzip '
             'libxml2-dev '
             'libxslt1-dev '
             % locals())
    
    if not hostos:
        hostos = api.env.hostout.detecthostos().lower()
    
    bootstrap_users_ubuntu()
    bootstrap_buildout_ubuntu()


def buildout(*args):
    api.env.superfun(*args)
    with cd(api.env.path):
        api.env.hostout.sudo("find var -exec chmod g+w {} \; || true")
        api.env.hostout.sudo("find var -maxdepth 1 -type d -exec chmod 770 {} \; || true")

def predeploy():
    print "PREDEPLOY"
    api.env.superfun()

def postdeploy():
    print "POSTDEPLOY"
    api.env.superfun()
