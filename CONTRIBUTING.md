# Guia de Contribuição

Obrigado por considerar contribuir com o ABNT Formatador!

## Como Contribuir

1. **Fork o repositório**
2. **Clone seu fork**: `git clone https://github.com/seu-usuario/ABNT.git`
3. **Crie uma branch**: `git checkout -b feature/minha-feature`
4. **Faça suas alterações**
5. **Commit**: `git commit -m "feat: adiciona nova funcionalidade"`
6. **Push**: `git push origin feature/minha-feature`
7. **Abra um Pull Request**

## Padrões de Código

### Backend (Python)

- Siga PEP 8
- Use type hints
- Docstrings em todas as funções públicas
- Testes para novas funcionalidades

### Frontend (TypeScript/React)

- Use TypeScript estrito
- Componentes funcionais com hooks
- Props tipadas
- CSS modular

## Commits

Use commits semânticos:

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

## Testes

Execute os testes antes de submeter PR:

```bash
make test
```

## Dúvidas?

Abra uma issue para discussão!
