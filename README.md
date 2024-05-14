# placa-fipe-api
Consulta de veículos na tabela FIPE com base na placa do veículo.

## Obtenha um API Token em ScrapingAnt
Crie uma conta em [ScrapingAnt][scrapingant] e obtenha um Token (1.000 consultas gratuitas por mês).

## Instalação das dependências

```
pip install -r requirements.txt
```

## Iniciar o servidor

```
uvicorn fipe.main:app --host 0.0.0.0 --port 8000
```

## Via Docker

```
docker run --name placa-fipe-api -e SA_TOKENS="token1,token2,token3" -p 8000:8000 juniorkrz/placa-fipe-api
```

Lembre-se de substituir `"token1,token2,token3"` pelos seus tokens reais, separados por vírgula. Você pode adicionar quantos tokens forem necessários.

## Descrição
Este projeto permite realizar consultas na FIPE utilizando a placa do veículo. Ele oferece as seguintes funcionalidades:

- Obter informações de um veículo específico com base na placa.
- Converter placas do antigo padrão para o padrão Mercosul e vice-versa.
- Verificar se uma placa é do padrão Mercosul ou não.
- Obter o nome de um estado brasileiro a partir de sua sigla.

## Endpoints

## /estado/{sigla}

Obtém o nome de um estado brasileiro com base na sigla informada.

## /consulta/{placa}

Realiza a consulta de um veículo com base na placa informada.

## /converter/{placa}

Converte a placa informada para o padrão Mercosul ou vice-versa.

## /mercosul/{placa}

Verifica se a placa informada é do padrão Mercosul.

## Autor
- [Antônio Roberto Júnior][krz]

## Licença

Este projeto está licenciado sob a [MIT License][license].

[krz]: https://github.com/juniorkrz
[license]: https://github.com/juniorkrz/placa-fipe-api/blob/master/LICENSE
[scrapingant]: https://scrapingant.com