__version__ = "0.0.3"
__author__ = "Antônio Roberto Júnior"


from fastapi import FastAPI
from tabelaFipe import TabelaFipe


app = FastAPI()
fipe = TabelaFipe()


@app.get("/")
async def root():
    return {
                "author": __author__,
                "version": __version__,
                "message": "Placa FIPE API Online!",
                "git": "https://github.com/juniorkrz/placa-fipe-api"
            }


@app.get("/estado/{sigla}")
async def estado(sigla):
    return {
            "status": True,
            "result": fipe.obter_estado(sigla)
        }


@app.get("/consulta/{placa}")
async def consulta(placa):
    return {
            "status": True,
            "result": fipe.consulta(placa)
        }


@app.get("/converter/{placa}")
async def converter(placa):
    return {
            "status": True,
            "result": fipe.converter_placa(placa)
        }


@app.get("/mercosul/{placa}")
async def mercosul(placa):
    return {
            "status": True,
            "result": fipe.verificar_placa_mercosul(placa)
        }