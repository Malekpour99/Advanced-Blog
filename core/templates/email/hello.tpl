{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account Activation
{% endblock %}

{% block html %}
Please click on the link below to activate your account:
{{ token }}
{% endblock %}
