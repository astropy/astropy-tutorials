
{% extends 'rst.tpl' %}


{% macro insert_empty_lines(text) %}
{%- set before, after = text | get_empty_lines %}
{%- if before %}
    :empty-lines-before: {{ before }}
{%- endif %}
{%- if after %}
    :empty-lines-after: {{ after }}
{%- endif %}
{%- endmacro %}


{% block any_cell %}
{%- if cell.metadata.nbsphinx != 'hidden' %}
{{ super() }}
{% endif %}
{%- endblock any_cell %}


{% block input -%}
.. nbinput:: {% if cell.metadata.magics_language -%}
{{ cell.metadata.magics_language }}
{%- elif nb.metadata.language_info -%}
{{ nb.metadata.language_info.pygments_lexer or nb.metadata.language_info.name }}
{%- else -%}
{{ resources.codecell_lexer }}
{%- endif -%}
{{ insert_empty_lines(cell.source) }}
{%- if cell.execution_count %}
    :execution-count: {{ cell.execution_count }}
{%- endif %}
{%- if not cell.outputs %}
    :no-output:
{%- endif %}
{%- if cell.source.strip() %}

{{ cell.source.strip('
') | indent }}
{%- endif %}
{% endblock input %}


{% macro insert_nboutput(datatype, output, cell) -%}
.. nboutput::
{%- if datatype == 'text/plain' %}{# nothing #}
{%- else %} rst
{%- endif %}
{%- if output.output_type == 'execute_result' and cell.execution_count %}
    :execution-count: {{ cell.execution_count }}
{%- endif %}
{%- if output != cell.outputs[-1] %}
    :more-to-come:
{%- endif %}
{%- if output.name == 'stderr' %}
    :class: stderr
{%- endif %}
{%- if datatype == 'text/plain' -%}
{{ insert_empty_lines(output.data[datatype]) }}

{{ output.data[datatype].strip(
) | indent }}
{%- elif datatype in ['image/svg+xml', 'image/png', 'image/jpeg', 'application/pdf'] %}

    .. image:: {{ output.metadata.filenames[datatype] | posix_path }}
{%- elif datatype in ['text/markdown'] %}

{{ output.data['text/markdown'] | markdown2rst | indent }}
{%- elif datatype in ['text/latex'] %}

    .. math::
        :nowrap:

{{ output.data['text/latex'] | indent | indent }}
{%- elif datatype == 'text/html' %}

    .. raw:: html

{{ output.data['text/html'] | indent | indent }}
{%- elif datatype == 'application/javascript' %}
{% set div_id = uuid4() %}

    .. raw:: html

        <div id="{{ div_id }}"></div>
        <script type="text/javascript">
        var element = document.getElementById('{{ div_id }}');
{{ output.data['application/javascript'] | indent | indent }}
        </script>
{%- elif datatype.startswith('application') and datatype.endswith('+json') %}

    .. raw:: html

        <script type="{{ datatype }}">{{ output.data[datatype] | json_dumps }}</script>
{%- elif datatype == 'ansi' %}

    .. rst-class:: highlight

    .. raw:: html

        <pre>
{{ output.data[datatype] | ansi2html | indent | indent }}
        </pre>

    .. raw:: latex

        %
        \begin{OriginalVerbatim}[commandchars=\\\{\}]
{{ output.data[datatype] | ansi2latex | indent | indent }}
        \end{OriginalVerbatim}
        % The following \relax is needed to avoid problems with adjacent ANSI
        % cells and some other stuff (e.g. bullet lists) following ANSI cells.
        % See https://github.com/sphinx-doc/sphinx/issues/3594
        \relax
{% else %}

    .. nbwarning:: Data type cannot be displayed: {{ datatype }}
{%- endif %}
{% endmacro %}


{% block nboutput -%}
{%- set html_datatype, latex_datatype = output | get_output_type %}
{%- if html_datatype == latex_datatype %}
{{ insert_nboutput(html_datatype, output, cell) }}
{%- else %}
.. only:: html

{{ insert_nboutput(html_datatype, output, cell) | indent }}
.. only:: latex

{{ insert_nboutput(latex_datatype, output, cell) | indent }}
{%- endif %}
{% endblock nboutput %}


{% block execute_result %}{{ self.nboutput() }}{% endblock execute_result %}
{% block display_data %}{{ self.nboutput() }}{% endblock display_data %}
{% block stream %}{{ self.nboutput() }}{% endblock stream %}
{% block error %}{{ self.nboutput() }}{% endblock error %}


{% block markdowncell %}
{%- if 'nbsphinx-toctree' in cell.metadata %}
{{ cell | extract_toctree }}
{%- else %}
{{ super() }}
{% endif %}
{% endblock markdowncell %}


{% block rawcell %}
{%- set raw_mimetype = cell.metadata.get('raw_mimetype', '').lower() %}
{%- if raw_mimetype == '' %}
.. raw:: html

{{ cell.source | indent }}

.. raw:: latex

    %
{{ cell.source | indent }}
{%- elif raw_mimetype == 'text/html' %}
.. raw:: html

{{ cell.source | indent }}
{%- elif raw_mimetype == 'text/latex' %}
.. raw:: latex

    %
{{ cell.source | indent }}
{%- elif raw_mimetype == 'text/markdown' %}
{{ cell.source | markdown2rst }}
{%- elif raw_mimetype == 'text/restructuredtext' %}
{{ cell.source }}
{% endif %}
{% endblock rawcell %}


{% block footer %}

{% if 'application/vnd.jupyter.widget-state+json' in nb.metadata.widgets %}

.. raw:: html

    <script type="application/vnd.jupyter.widget-state+json">
    {{ nb.metadata.widgets['application/vnd.jupyter.widget-state+json'] | json_dumps }}
    </script>
{% endif %}

{# This is where the custom astropy-tutorials stuff begins: #}
.. raw:: html

    <hr width="75%" style="margin: 0 auto; padding: 16px;" />

{% set base_url = "https://github.com/astropy/astropy-tutorials/tree/master" %}
{% set nb_name = "{0}.ipynb".format("_".join(resources.unique_key.split('_')[2:])) %}
{{ "/".join([base_url] + resources.unique_key.split('_')[:2] + [nb_name]) }}

{{ super() }}
{% endblock footer %}
