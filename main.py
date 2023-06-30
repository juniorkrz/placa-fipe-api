__version__ = "0.0.1"


from fastapi import FastAPI
from tabelaFipe import TabelaFipe


app = FastAPI()
fipe = TabelaFipe()


@app.get("/")
async def root():
    return {
                "message": "Placa FIPE API Online!",
                "author": "Júnior Krz",
                "version": __version__
            }


@app.get("/consulta/{placa}")
async def consulta(placa):
    return {
            "status": True,
            "result": fipe.consulta(placa)
        }


@app.get("/mercosul/{placa}")
async def consulta(placa):
    return {
            "status": True,
            "result": fipe.verificarPlacaMercosul(placa)
        }


@app.get("/converter/{placa}")
async def consulta(placa):
    return {
            "status": True,
            "result": fipe.converterPlaca(placa)
        }