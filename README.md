# Sistema de Gerenciamento de Eventos

Um sistema web desenvolvido em Django para gerenciamento completo de eventos, permitindo criação, organização e participação em eventos diversos.


## LINK DO VIDEO:

### No Youtube 
- 



## Funcionalidades

### Para Organizadores (Palestrantes)
- Criação e edição de eventos
- Gerenciamento de categorias
- Configuração de locais
- Criação de tipos de ingressos
- Organização de atividades
- Painel administrativo com estatísticas

### Para Participantes (Clientes)
- Visualização e busca de eventos
- Inscrição em eventos
- Compra de ingressos
- Gerenciamento de inscrições
- Cancelamento de ingressos

### Funcionalidades Gerais
- Sistema de autenticação completo
- Perfis de usuário personalizados
- Sistema de permissões baseado em grupos
- Interface responsiva e moderna
- Paginação e filtros de busca

## Tecnologias Utilizadas

- **Backend**: Django 5.2.1
- **Frontend**: HTML5, CSS3, Bootstrap
- **Banco de Dados**: SQLite (desenvolvimento)
- **Autenticação**: Sistema nativo do Django
- **Permissões**: Django Groups e Permissions

## Estrutura do Projeto

```
sistema-eventos/
├── usuario/          # App de gerenciamento de usuários
├── eventos/          # App principal de eventos
├── categoria/        # Gerenciamento de categorias
├── atividade/        # Gerenciamento de atividades
├── local/           # Gerenciamento de locais
├── ingresso/        # Gerenciamento de ingressos
├── templates/       # Templates HTML
├── static/          # Arquivos estáticos
└── eventospsw/      # Configurações do projeto
```

## Configuração Inicial

### Criação de Grupos e Permissões

O sistema criará automaticamente os grupos "Palestrante" e "Participante" com as permissões adequadas. Para configurar manualmente:

1. Acesse o Django Admin
2. Vá em "Grupos" e verifique se os grupos foram criados
3. Atribua usuários aos grupos conforme necessário

### Configuração de Perfis

Todos os usuários devem completar seu perfil após o registro:
1. Faça login no sistema
2. Acesse "Perfil" no menu
3. Complete as informações obrigatórias
4. Selecione o tipo de usuário (Cliente ou Palestrante)

## Uso do Sistema

### Para Organizadores
1. Registre-se e configure seu perfil como "Palestrante"
2. Acesse o painel do palestrante
3. Crie categorias, locais e tipos de ingressos
4. Crie seus eventos
5. Gerencie inscrições e atividades

### Para Participantes
1. Registre-se e configure seu perfil como "Cliente"
2. Navegue pelos eventos disponíveis
3. Inscreva-se nos eventos de interesse
4. Gerencie suas inscrições na área "Meus Ingressos"



## Roadmap

- [ ] Sistema de notificações por email
- [ ] Integração com sistemas de pagamento
- [ ] API REST para integração externa
- [ ] Aplicativo mobile
- [ ] Sistema de avaliações e comentários
- [ ] Relatórios avançados
- [ ] Integração com redes sociais
