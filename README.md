# Image service

## Sobre o Projeto

O **Image service** é um serviço que processa imagens de vídeo e retorna para uma fila no RabbitMQ. Ele é responsável por extrair frames de vídeo, criar um ZIP com esses frames e enviar o ZIP para uma fila no RabbitMQ.

## Comandos Básicos

Este projeto utiliza um `Makefile` para facilitar a execução de tarefas comuns. Abaixo estão os comandos disponíveis:

### Execução

```bash
make install-hooks  # Instala os hooks de pré-commit para garantir a qualidade do código
make test           # Executa os testes da aplicação
make run            # Inicia o servidor de desenvolvimento
make ruff           # Verifica o código com o linter Ruff
make fix            # Corrige problemas detectados pelo linter Ruff
make format         # Formata o código automaticamente com o Ruff
make coverage       # Gera uma cobertura de testes
```

### Exemplo de Uso

Para iniciar o projeto, execute:

```bash
make install-hooks
make run
```

Para executar os testes:

```bash
make test
```

Para verificar e corrigir problemas no código:

```bash
make ruff
make fix
```

Consulte o `Makefile` para detalhes adicionais sobre cada comando.
