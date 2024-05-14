__version__ = "0.0.5"
__author__ = "Antônio Roberto Júnior"


from fastapi import FastAPI
from placafipy import PlacaFipy


from .tokens import scraping_ant_tokens


app = FastAPI()
fipy = PlacaFipy(scraping_ant_tokens)


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
            "result": fipy.obter_estado(sigla)
        }


@app.get("/consulta/{placa}")
async def consulta(placa):
    return {
            "status": True,
            "result": fipy.consulta(placa)
        }


@app.get("/converter/{placa}")
async def converter(placa):
    return {
            "status": True,
            "result": fipy.converter_placa(placa)
        }


@app.get("/mercosul/{placa}")
async def mercosul(placa):
    return {
            "status": True,
            "result": fipy.verificar_placa_mercosul(placa)
        }