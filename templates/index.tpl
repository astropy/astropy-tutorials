<!doctype html>
<html lang=en>
<head>
<meta charset=utf-8>
<title>Astropy tutorials</title>
</head>
<body>
<ul>
{% for notebook in notebooks %}
  <li><a href="{{ notebook['html_path'] }}">{{ notebook['name'] }}</a></li>
{% endfor %}
</ul>
</body>
</html>
