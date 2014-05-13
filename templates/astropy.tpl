{%- extends 'full.tpl' -%}

{% block header %}
<meta name="viewport" content="width=device-width, initial-scale=1" />

<title></title>

{{ super() }}

<link href='http://fonts.googleapis.com/css?family=Open+Sans:200,300,400italic,400,700' rel='stylesheet' type='text/css' />
<link rel="stylesheet" type="text/css" href="css/docs.css" />
<link rel="stylesheet" type="text/css" href="css/style.css" />

{%- endblock header %}

{% block body %}

<div id="wrapper">
    <nav style="font-size: 140%; color: #fff; font-weight: 300;">
        <a href="http://www.astropy.org">
            <img src="images/astropy_word_32.png" style="vertical-align: middle;"/>
        </a>
        <li><a href="http://tutorials.astropy.org/">tutorials</a></li>
    </nav>

    {{ super() }}

</div>

<!-- This javascript hides tracebacks, but inserts a button to
     let the user toggle showing the full traceback. -->
<script type='text/javascript'>
    var parent = $('.output_pyerr');
    var b = $("<button></button><br>").appendTo(parent);
    b.attr('name', 'toggle_err');
    b.html('Show/hide full traceback');
    b.attr("class", "btn");

    $('button[name=toggle_err]').click(function() {
        $(this).parent().children('pre').toggle();
        $(this).parent().parent().children('.prompt').toggle();
        $(this).parent().parent().children('.prompt').toggle();
    });

    $('.output_pyerr pre').hide();

</script>

{%- endblock body %}