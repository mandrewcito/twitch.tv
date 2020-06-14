import click 
import json
import paramiko
import subprocess


def run_remote_step(client, command):
    client.invoke_shell()
    stdin, stdout, stderr = client.exec_command(command) 
    print(stdout)

def copy_remote(client, resources):
    ftp_client=client.open_sftp()
    for resource in resources:
        filename = resource["src"]
        ftp_client.put(resource["src"], resource["dest"], callback=lambda current, pending: print(f"\r {filename} transfered: {current} // pending: {pending}", end=""))
    ftp_client.close()

def read_cfg():
    with open('cfg.json') as fh:
        return json.loads(fh.read())    

@click.command()
@click.option('--name', prompt='App name',
              help='App name will be deployed')
def deploy_app(name):
    apps = read_cfg()
    if name not in apps.keys():
        raise ValueError(f"app not found in configuration: '{name}'")
    cfg = apps[name] 

    for step in cfg["before_install"]:
        subprocess.call(step, shell=True) 
    
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    client.connect(cfg["server"]["host"], 22, cfg["server"]["user"], cfg["server"]["password"])

    copy_remote(client, cfg["install"]["copy"])
    
    for step in cfg["install"]["steps"]:
        run_remote_step(client, step)
         
    for step in cfg["after_install"]:
        subprocess.call(step, shell=True) 

if __name__ == '__main__':
    deploy_app()