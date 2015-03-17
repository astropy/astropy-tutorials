{%- extends 'full.tpl' -%}

{% block header %}
<meta name="viewport" content="width=device-width, initial-scale=1" />

<title>{title}</title>

{{ super() }}

<link href='http://fonts.googleapis.com/css?family=Open+Sans:200,300,400italic,400,700' rel='stylesheet' type='text/css' />
<link rel="stylesheet" type="text/css" href="css/docs.css" />
<link rel="stylesheet" type="text/css" href="css/style.css" />

{%- endblock header %}

{% block body %}

<div id="wrapper">
    <nav>
        <a href="http://www.astropy.org"><img src="images/astropy_word_32.png"/></a>
        <div id="navigation">
            <ul>
                <li style="margin-top: 7px"><a href="http://tutorials.astropy.org">Tutorials</a></li>
            </ul>
        </div>
    </nav>

    {{ super() }}
	<div style="top:0px; border:1px">
    <table border="1" align="center">
     <tr height="100%">
      <td height="100%" width="100%" valign="middle" align="center">
	  <a href="https://github.com/astropy/astropy-tutorials/tree/master/tutorials/{pageurl}">Edit on Github  <img src="images/gitlogo.png" height=40px width=40px/></a>
      </td>
     </tr>
    </table>
  </div>
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