# placa-fipe-api
Consulta de veículos na Tabela FIPE usando a placa do veículo.

## Instalação do uvicorn

```
pip install "uvicorn[standard]"

```

## Iniciar o servidor

```
uvicorn main:app --host 0.0.0.0 --port 80
```

## Descrição
Este projeto permite realizar consultas na FIPE utilizando a placa do veículo. Ele oferece as seguintes funcionalidades:

- Obter informações de um veículo específico com base na placa.
- Converter placas do antigo padrão para o padrão Mercosul e vice-versa.
- Verificar se uma placa é do padrão Mercosul ou não.

## Endpoints

## /consulta/{placa}

Realiza a consulta de um veículo com base na placa informada.

## /mercosul/{placa}

Verifica se a placa informada é do padrão Mercosul.

## /converter/{placa}

Converte a placa informada para o padrão Mercosul ou vice-versa.

## Autor
- Júnior Krz

## Licença

Este projeto está licenciado sob a [MIT License][license].

[license]: https://github.com/juniorkrz/placa-fipe-api/blob/master/LICENSE
