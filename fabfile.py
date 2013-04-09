from fabric.api import task, env
from parcel.deploy import Deployment
from parcel import distro
from parcel import tools


env.app_name = 'pypiserver'
env.user = 'root'

upstart_conf = '''start on runlevel [12345]
stop on runlevel [0]
respawn
script
    mkdir -p /var/pypi/packages
    export APP_HOME={app_home}
    cd $APP_HOME
    . vp/bin/activate
    gunicorn -w4 'pypiserver:app("/var/pypi/packages")'
end script
'''

restart_service = '''if [ $(pgrep {app_name}) ]; then
        restart {app_name};
    else
        start {app_name};
    fi
'''


@task
def deb():
    deploy = Deployment(
        env.app_name,
        build_deps=['python-virtualenv', 'python-pip'],
        base='/opt/pypiserver',
        arch=distro.Ubuntu(),
        version="0.0.1"
    )

    deploy.add_postinst(['service %s start' % env.app_name])
    deploy.prepare_app()

    conf = upstart_conf.format(app_name=env.app_name, app_home=deploy.app_path)
    path = deploy.root_path + '/etc/init/%s.conf' % env.app_name

    tools.write_contents_to_remote(conf, path)
    #this should be built into parcel, or needs an Upstart(Depployment)
    #tools.rsync([deploy.path+'/debian/'],deploy.root_path,rsync_ignore='.rsync-ignore')
    deploy.build_package()
