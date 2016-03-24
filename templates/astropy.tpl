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
	
	
	<!-- Author and Date Information & Edit on Github Link-->
	
	<div class="clearfix" style='margin-top:25px;margin-left:12%;'>
		<ul>
			<span style="float: left;"><b>Author: </b>{author}</span> 
			<span style="float: right"><a href="https://github.com/astropy/astropy-tutorials/tree/master/tutorials/{abspageurl}">Edit this tutorial on GitHub <img src="https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png" height="25px" width="25px" /></a></span>
			<br><span style="float: left;"><b>Date Created: </b> {date}</span>
		</ul>
	</div>
	
    {{ super() }}
	

  <!--Disqus Comment Section -->
	
	<div id="disqus_thread" style='margin-top:50px;'></div>
	<script type="text/javascript">
		/* * * CONFIGURATION VARIABLES * * */
		var disqus_shortname = 'astropytutorials'; //registered short name of astropy tutorials 
		var disqus_identifier= '{pageurl}';
		var disqus_url = 'http://www.astropy.org/astropy-tutorials/{pageurl}';
		/* * * DON'T EDIT BELOW THIS LINE * * */
		(function() {
			var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
			dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
			(document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
		})();
		(function () {
			var s = document.createElement('script'); s.async = true;
			s.type = 'text/javascript';
			s.src = 'http://' + disqus_shortname + '.disqus.com/count.js';
			(document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
		}());
	</script>
	<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>
	
	<!--End of comments section-->
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