import os
import subprocess
import json
import collections
import click 
import paramiko


def dict_merge(dct, merge_dct):
    """ 
    https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def run_remote_step(client, command):
    client.invoke_shell()
    stdin, stdout, stderr = client.exec_command(command) 
    print(f"stdin: {stdin}, stdout: {stdout}, stderr: {stderr}")


def copy_remote(client, resources):
    ftp_client=client.open_sftp()
    for resource in resources:
        filename = resource["src"]
        ftp_client.put(
            resource["src"],
            resource["dest"],
            callback=lambda current, total: print(f"\r {filename} transfered: {(current/total) * 100:2f}", end=""))
    ftp_client.close()

def read_cfg():
    with open('cfg.json') as fh:
        data = json.loads(fh.read())
        if os.path.exists(".env"):
            with open(".env") as fhs:
                secrets = json.loads(fhs.read())
                dict_merge(data, secrets)
        return data

@click.command()
@click.option('--name', prompt='App name',
              help='App name will be deployed')
def deploy_app(name):
    apps = read_cfg()

    if name not in apps.keys():
        raise ValueError(f"app not found in configuration: '{name}'")
    cfg = apps[name] 

    for step in cfg["before_install"]:
        print(step)
        subprocess.call(step, shell=True)
    
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    client.connect(cfg["server"]["host"], 22, cfg["server"]["user"], cfg["server"]["password"])

    copy_remote(client, cfg["install"]["copy"])
    
    for step in cfg["install"]["steps"]:
        run_remote_step(client, step)
         
    for step in cfg["after_install"]:
        print(step)
        subprocess.call(step, shell=True)

if __name__ == '__main__':
    deploy_app()