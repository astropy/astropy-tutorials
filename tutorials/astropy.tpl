{%- extends 'display_priority.tpl' -%}

{% block header %}

{# Remove the exec_ prefix #}
{% set nb_name = resources.metadata.name[5:] %}

.. note::

    This tutorial was generated from an IPython notebook that can be downloaded `here
    <../_static/{{ nb_name }}/{{ nb_name }}.ipynb>`_.

    You can interact with a live version of the source notebook through binder:

    |binder{{ nb_name }}|

.. |binder{{ nb_name }}| image:: http://mybinder.org/badge.svg
   :target: https://beta.mybinder.org/v2/gh/astropy/astropy-tutorials/master?filepath=docs/_static/tutorials/{{ nb_name }}/{{ nb_name }}.ipynb

.. _{{nb_name}}:
{% endblock %}

{% block in_prompt %}
{% endblock in_prompt %}

{% block output_prompt %}
{% endblock output_prompt %}

{% block input %}
{%- if cell.source.strip() and not cell.source.startswith("%") -%}
.. code:: python

{{ cell.source | indent}}
{% endif -%}
{% endblock input %}

{% block error %}
::

{{ super() }}
{% endblock error %}

{% block traceback_line %}
{{ line | indent | strip_ansi }}
{% endblock traceback_line %}

{% block execute_result %}
{% block data_priority scoped %}
{{ super() }}
{% endblock %}
{% endblock execute_result %}

{% block stream %}
.. parsed-literal::

{{ output.text | indent }}
{% endblock stream %}

{% block data_svg %}
.. image:: {{ output.metadata.filenames['image/svg+xml'] | posix_path }}
{% endblock data_svg %}

{% block data_png %}
.. image:: {{ output.metadata.filenames['image/png'] | posix_path }}

{% endblock data_png %}

{% block data_jpg %}
.. image:: {{ output.metadata.filenames['image/jpeg'] | posix_path }}
{% endblock data_jpg %}

{% block data_latex %}
.. math::

{{ output.data['text/latex'] | strip_dollars | indent }}
{% endblock data_latex %}

{% block data_text scoped %}
.. parsed-literal::

{{ output.data['text/plain'] | indent }}
{% endblock data_text %}

{% block data_html scoped %}
.. raw:: html

{{ output.data['text/html'] | indent }}
{% endblock data_html %}

{% block markdowncell scoped %}
{{ cell.source | markdown2rst }}
{% endblock markdowncell %}

{%- block rawcell scoped -%}
{%- if cell.metadata.get('raw_mimetype', '').lower() in resources.get('raw_mimetypes', ['']) %}
{{cell.source}}
{% endif -%}
{%- endblock rawcell -%}

{% block headingcell scoped %}
{{ ("#" * cell.level + cell.source) | replace('\n', ' ') | markdown2rst }}
{% endblock headingcell %}

{% block unknowncell scoped %}
unknown type  {{cell.type}}
{% endblock unknowncell %}
