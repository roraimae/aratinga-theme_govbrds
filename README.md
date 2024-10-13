# Descrição do projeto

django-govbrds

Design System do Governo Federal Brasileiro para Django

## Objetivo

O objetivo deste projeto é combinar perfeitamente o Django e o Design System do Governo Brasileiro.

## A instalação

1. Instale usando o pip:

    ```console
    pip install django-govbrds
    ```

2. Adicionar ao INSTALLED_APPS nas suas settings.py:

    ```python
    INSTALLED_APPS = (
        # ...
        "django-govbrds",
        # ...
    )
    ```

    3. Em seus modelos, carregue a biblioteca django-govbrds e use as tags br_. Veja o exemplo abaixo.

## Exemplo de modelo

```jinja2
{% load django-govbrds %}
   
<form action="/url/to/submit/" method="post" class="form">
    {% csrf_token %}

    {% br_form form %}

    {% br_button button_type="submit" content="OK" %}
    {% br_button button_type="reset" content="Cancel" %}
</form>
    
```

## Licença

Você pode usar isso sob BSD-3-Clause. Consulte o arquivo LICENSE para mais detalhes.

## Autor

Desenvolvido e mantido por [Roraimae](https://github.com/roraimae).

Autor original: [Fábio Santos](https://github.com/f4biosa).