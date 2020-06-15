## install
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
```
## Uso

```bash
python main.py appname
```

## configuracion cfg.json
Un ejemplo de fichero de configuración podría ser este:
```json
{
    "mrproverb": {
        "server": {
            "host": "",
            "user": "",
            "password": ""
        },
        "before_install": [
            "git clone https://github.com/OpenComunCas/proverbs.git",
            "docker build -t mrproverb -f proverbs/proverbs/Dockerfile proverbs/proverbs",
            "docker save -o mrproverb.tar mrproverb:latest"
        ],
        "install": {
            "copy": [
                {
                    "src": "mrproverb.tar",
                    "dest": "/tmp/mrproverb.tar"
                }
            ],
            "steps": [
                "docker load /tmp/mrproverb.tar",
                "docker kill mrproverb",
                "docker container rm mrproverb",
                "docker run -p 5555:5555 --name mrproverb -d mrproverb",
                "rm /tmp/mrproverb.tar"
            ]
        },
        "after_install": [
            "cd proverbs/proverbs && sh discord_webhook.sh",
            "rm mrproverb.tar && rm -rf proverbs"
        ]
    }
}
```
## .env
Si se crea un fichero .env se incluirán los valores en el fichero .json, debe tener el mismo formato que el fichero
de configuración.

```json
{
    "mrproverb": {
        "server": {
            "host": "",
            "password": "",
            "user": ""
        }
    }
}
```