from bs4 import BeautifulSoup
from unidecode import unidecode
from string import ascii_lowercase
from requests import get as requests_get
from random import choice as random_choice
from urllib.parse import urlencode as urllib_url_encode


from .tokens import scraping_ant_tokens


class TabelaFipe():


    ESTADOS = {
        "AC": "ACRE",
        "AL": "ALAGOAS",
        "AP": "AMAPÁ",
        "AM": "AMAZONAS",
        "BA": "BAHIA",
        "CE": "CEARÁ",
        "DF": "DISTRITO FEDERAL",
        "ES": "ESPÍRITO SANTO",
        "GO": "GOIÁS",
        "MA": "MARANHÃO",
        "MT": "MATO GROSSO",
        "MS": "MATO GROSSO DO SUL",
        "MG": "MINAS GERAIS",
        "PA": "PARÁ",
        "PB": "PARAÍBA",
        "PR": "PARANÁ",
        "PE": "PERNAMBUCO",
        "PI": "PIAUÍ",
        "RJ": "RIO DE JANEIRO",
        "RN": "RIO GRANDE DO NORTE",
        "RS": "RIO GRANDE DO SUL",
        "RO": "RONDÔNIA",
        "RR": "RORAIMA",
        "SC": "SANTA CATARINA",
        "SP": "SÃO PAULO",
        "SE": "SERGIPE",
        "TO": "TOCANTINS"
    }


    def __init__(self) -> None:
        self.__sa_api_url = 'https://api.scrapingant.com/v2/general'
        self.__placa_fipe_url = "https://placafipe.com/placa/%s"


    def __preparar_consulta(self, placa):
        self.__soup = None
        self.__placa = placa
        self.__html = None
        self.__consulta = {
                            "tabela_fipe": {},
                            "detalhes": {}
                        }


    def __obter_placa_fipe_html(self):
        fipe_url = self.__placa_fipe_url % self.__placa
        params = {'url': fipe_url, 'x-api-key': random_choice(scraping_ant_tokens)}
        url = f'{self.__sa_api_url}?{urllib_url_encode(params)}'
        resposta = requests_get(url)
        if resposta.status_code != 200:
            return False
        self.__html = resposta.text
        return True


    def __verificar_consulta(self):
        frases_erro = [
                        "tem um formato inválido",
                        "não foi encontrada informação para a placa",
                        ]
        for frase in frases_erro:
            if frase in self.__html.lower():
                return False
        return True


    def __obter_soup(self):
        self.__soup = BeautifulSoup(self.__html, "html.parser")
        return True


    def __obter_imagem_logo_url(self):
        imagem_logo = self.__soup.find("img", {"class": "fipeLogoDIV"})
        if imagem_logo:
            imagem_logo_url = imagem_logo.attrs["data-src"]
            self.__consulta["imagem_logo_url"] = imagem_logo_url
            return True
        self.__consulta["imagem_logo_url"] = False
        return False


    def __obter_imagem_placa_url(self):
        imagem_placa = self.__soup.find("img", {"class": "fipe-placa"})
        if imagem_placa:
            imagem_placa_url = imagem_placa.attrs["data-src"]
            self.__consulta["imagem_placa_url"] = imagem_placa_url
            return True
        self.__consulta["imagem_placa_url"] = False
        return False


    def __obter_detalhes(self):
        tabela_detalhes = self.__soup.find("table", {"class": "fipeTablePriceDetail"})
        linhas_tabela = tabela_detalhes.find_all("tr")

        for linha in linhas_tabela:
            parametro = unidecode(linha.find("td").get_text().replace(":", "").replace(" ", "_").strip().lower())
            valor = linha.find("td").find_next("td").get_text()
            self.__consulta["detalhes"][parametro] = valor
        return True


    def __tratar_parametros(self):
        importado = self.__consulta["detalhes"].get("importado")
        if importado:
            if importado == "Sim":
                importado = True
            else:
                importado = False
            self.__consulta["detalhes"]["importado"] = importado

        parametros = ["ano", "ano_modelo", "passageiros"]
        for p in parametros:
            parametro = self.__consulta["detalhes"].get(p)
            if parametro:
                self.__consulta["detalhes"][p] = int(self.__consulta["detalhes"][p])


    def __obter_tipo_veiculo(self):
        self.__consulta["detalhes"]["tipo_veiculo"] = self.__soup.find("h2").get_text().split(" ")[2].strip().lower()
        return True


    def __obter_orgao_emissor(self, texto):
        orgao_emissor = texto.split("pelo ")
        if len(orgao_emissor) > 1:
            orgao_emissor = orgao_emissor[1].replace(".", "").upper()
            return orgao_emissor
        return False


    def __obter_veiculos_registrados(self, texto):
        try:
            return float(texto.split("registrados ")[1].split(" ")[0])
        except:
            return False


    def __obter_data_tabela_fipe(self, texto):
        return texto.split("fipe de ")[1].split(",")[0].strip().capitalize()


    def __obter_outros_detalhes(self):
        for p in self.__soup.find_all("p"):
            texto = p.get_text().lower()
            if "emitida pelo" in texto:
                self.__consulta["orgao_emissor"] = self.__obter_orgao_emissor(texto)
            elif "registrados" in texto:
                self.__consulta["veiculos_registrados"] = self.__obter_veiculos_registrados(texto)
            elif "tabela fipe de" in texto:
                self.__consulta["tabela_fipe"]["data"] = self.__obter_data_tabela_fipe(texto)
                self.__consulta["tabela_fipe"]["descricao"] = p.get_text()
        return True


    def __tratar_tabela(self, tabela, converter_em_dict=False):
        linhas_tabela = tabela.find_all("tr")
        resultado = {} if converter_em_dict else []
        cabecalho_tabela = linhas_tabela[0]
        parametros = [unidecode(parametro.get_text().replace(" ", "_").strip().lower()) for parametro in cabecalho_tabela.find_all("td")]
        linhas_tabela.pop(0)
        for linha in linhas_tabela:
            item = {}
            for i, parametro in enumerate(parametros):
                valor = linha.find("td")
                if i > 0:
                    for ii in range(i):
                        valor = valor.find_next()
                valor = valor.get_text()
                item[parametro] = valor
                if converter_em_dict and len(item) == 1:
                    chave = valor
            if converter_em_dict:
                resultado[chave] = item
            else:
                resultado.append(item)
        return resultado


    def __obter_valores_fipe(self):
        tabela = self.__soup.find("table", {"class": "fipe-desktop"})
        if not tabela:
            return False
        self.__consulta["tabela_fipe"]["valores"] = self.__tratar_tabela(tabela)
        return True


    def __obter_valores_ipva(self):
        tabela = self.__soup.find("table", {"class": "placa-ipva"})
        if not tabela:
            return False
        self.__consulta["tabela_fipe"]["valores_ipva"] = self.__tratar_tabela(tabela, converter_em_dict=True)
        return True


    def obter_estado(self, sigla):
        return TabelaFipe.ESTADOS.get(sigla.upper())


    def verificar_placa_mercosul(self, placa):
        return placa[4].isalpha() or placa[5].isalpha() 


    def converter_placa(self, placa):
        p = placa.lower()
        if self.verificar_placa_mercosul(p):
            return f"{placa[:-3]}{str(ascii_lowercase.find(p[4]))}{placa[-2:]}".upper()
        else:
            return f"{placa[:-3]}{ascii_lowercase[int(p[4])]}{placa[-2:]}".upper()


    def consulta(self, placa):
        self.__preparar_consulta(placa)
        if self.__obter_placa_fipe_html() and self.__verificar_consulta():
            self.__obter_soup()
            self.__obter_imagem_logo_url()
            self.__obter_imagem_placa_url()
            self.__obter_detalhes()
            self.__tratar_parametros()
            self.__obter_valores_fipe()
            self.__obter_valores_ipva()
            self.__obter_tipo_veiculo()
            self.__obter_outros_detalhes()
            return self.__consulta
        return False