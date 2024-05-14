# Obtenha o seu em https://scrapingant.com
# 1.000 consultas gratuitas por mês.
from os import getenv

sa_tokens = getenv('SA_TOKENS')

if not sa_tokens:
    raise ValueError("Token não encontrado. Certifique-se de definir a variável de ambiente SA_TOKENS. Obtenha o seu em https://scrapingant.com")

scraping_ant_tokens = [token for token in sa_tokens.strip().split(",") if token]