# LAB 8 — FastAPI, GitHub Actions, Docker Hub, EC2 e Elastic IP

Projeto-base resolvido para os PDFs **08.2 GitHub Actions Projeto** e **08.3 Desafio ElasticIP**.

## O que foi implementado

- API FastAPI com `GET /`, `GET /health` e `POST /items`.
- Testes automatizados com pytest.
- Imagem Docker executada por usuário sem privilégios.
- Workflow `docker-hub.yml`: testa em push/PR; publica `latest` e o SHA do commit somente em push para `main`.
- Workflow `ec2-deploy.yml`: roda depois que o workflow de publicação termina com sucesso, acessa a EC2 por SSH, atualiza o container e verifica `/health`.

## 1. Preparar o GitHub e o Docker Hub

1. Crie no Docker Hub um repositório chamado `senai_fastapi`.
2. Crie um Access Token no Docker Hub.
3. Coloque esta pasta em um repositório GitHub e envie os arquivos para a branch `main`.
4. Em **Settings → Secrets and variables → Actions**, crie os secrets:

| Secret | Valor |
| --- | --- |
| `DOCKERHUB_USERNAME` | Seu usuário do Docker Hub |
| `DOCKERHUB_TOKEN` | Access Token do Docker Hub |
| `EC2_HOST` | Elastic IP associado à instância |
| `EC2_USERNAME` | `ec2-user` (Amazon Linux) ou `ubuntu` (Ubuntu) |
| `EC2_SSH_KEY` | Conteúdo completo da chave privada `.pem` |

Não coloque tokens, chave privada ou IP diretamente nos arquivos do projeto. O nome `senai_fastapi` pode ser alterado nos dois workflows, mas deve ser o mesmo em ambos.

## 2. Preparar a instância EC2

A instância precisa estar em execução, aceitar SSH (porta 22) e HTTP da API (porta 8080) no Security Group, e ter Docker instalado. O usuário SSH precisa poder executar `sudo docker`. Instale e inicie o Docker conforme o sistema da instância antes do primeiro deploy.

Teste o acesso usando o Elastic IP e o usuário corretos:

```bash
ssh -i "sua-chave.pem" ec2-user@SEU_ELASTIC_IP
```

Para Ubuntu, substitua `ec2-user` por `ubuntu`. No Git Bash/Linux/macOS pode ser necessário `chmod 400 sua-chave.pem` antes da conexão.

## 3. Desafio Elastic IP

No console AWS, abra **EC2 → Elastic IPs → Allocate Elastic IP address**. Selecione o endereço criado e use **Actions → Associate Elastic IP address**, escolhendo **Instance** e sua instância. Copie o IPv4 alocado para o secret `EC2_HOST` no GitHub.

Depois, pare e inicie a instância e confirme que o IPv4 público continua igual. Esse é o teste solicitado no desafio. O pipeline não precisa conter o IP: ele lê `EC2_HOST` do secret a cada execução.

Ao terminar o laboratório, desassocie e libere o Elastic IP se não for mais usá-lo. No AWS Academy, confira as regras e o tempo restante do Learner Lab.

## 4. Executar localmente

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest tests/ -v
python -m uvicorn app.main:app --reload --port 8080
```

Linux/macOS:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest tests/ -v
python -m uvicorn app.main:app --reload --port 8080
```

A API ficará em `http://localhost:8080`; a documentação interativa fica em `/docs`.

## 5. Fluxo de entrega

Faça push para `main`. O primeiro workflow executa os testes; se todos passarem, cria e publica a imagem. O segundo workflow observa a conclusão do primeiro e só faz deploy quando a publicação termina com sucesso. Ao final, o health check consulta `http://localhost:8080/health` na EC2.

## Observação sobre o material do exercício

No PDF, `needs: Build/Imagem` aparece em arquivos YAML diferentes, mas `needs` só conecta jobs dentro do mesmo workflow. Aqui a ligação entre os dois arquivos é feita por `workflow_run`. Também substituí as aspas tipográficas em `python-version`, usei o usuário do Docker Hub via secret e corrigi o caminho de inicialização da aplicação.
