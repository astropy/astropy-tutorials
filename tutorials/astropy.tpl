{%- extends 'display_priority.tpl' -%}

{% block header %}

{# Remove the exec_ prefix #}
{% set nb_name = resources.metadata.name[5:] %}

.. raw:: html

    <a href="../_static/{{ nb_name }}/{{ nb_name }}.ipynb"><button id="download">Download tutorial notebook</button></a>
    <a href="https://beta.mybinder.org/v2/gh/astropy/astropy-tutorials/master?filepath=/tutorials/notebooks/{{ nb_name }}/{{ nb_name }}.ipynb"><button id="binder">Interactive tutorial notebook</button></a>

    <div id="spacer"></div>

.. role:: inputnumrole
.. role:: outputnumrole

.. _{{nb_name}}:
{% endblock %}

{% block footer %}

.. raw:: html

    <div id="spacer"></div>

    <a href="../_static/{{ nb_name }}/{{ nb_name }}.ipynb"><button id="download">Download tutorial notebook</button></a>
    <a href="https://beta.mybinder.org/v2/gh/astropy/astropy-tutorials/master?filepath=/tutorials/notebooks/{{ nb_name }}/{{ nb_name }}.ipynb"><button id="binder">Interactive tutorial notebook</button></a>

{% endblock %}

{% block in_prompt %}

:inputnumrole:`In[{{  cell['execution_count'] }}]:`


{% endblock in_prompt %}

{% block output_prompt %}

:outputnumrole:`Out[{{  cell['execution_count'] }}]:`

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
