<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<title>OpenStack Live Energy Monitoring</title>

	<script src="//code.jquery.com/jquery-1.11.3.min.js"></script>
	<script type="text/javascript">
	function reload_images() {
		var end = Math.floor(Date.now() / 1000);
		var start = end - 300;

		$('.container').find('img').each(function() {
			var url = $(this).attr('src');
			var new_url = url.replace(/\/\d+\/\d+\//, '/' + start + '/' + end + '/')
			console.log(url + ' -> ' + new_url);
			$(this).attr('src', new_url);
		});
	}

	$(document).ready(function() {
		setInterval(reload_images, 1000);
	});
	</script>
</head>

<body>
	<h1>Controllers</h1>
	<div class="container">
	%for node in controllers:
		<img class="graph"
		src="https://intranet.grid5000.fr/supervision/{{site}}/monitoring/energy/graph/{{site}}.{{node}}/{{start}}/{{end}}/"
		title="{{node}}" alt="" />
	%end
	</div>

	<h1>Compute</h1>
	<div class="container">
	%for node in computes:
		<img class="graph"
		src="https://intranet.grid5000.fr/supervision/{{site}}/monitoring/energy/graph/{{site}}.{{node}}/{{start}}/{{end}}/"
		title="{{node}}" alt="" />
	%end
	</div>
</body>
</html>
