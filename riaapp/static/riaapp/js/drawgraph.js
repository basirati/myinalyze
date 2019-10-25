var width, height;
var radius = 8

function drawDJGraph(graph, svg) {
	var	node, link;
	
	width = parseInt($('svg').css("width"));
	height = parseInt($('svg').css("height"));
	
	simulation = d3.forceSimulation()
	.force("link", d3.forceLink().id(function (d) {return d.id;}).distance(100).strength(0.5))
	.force("charge", d3.forceManyBody())
	.force("center", d3.forceCenter(width / 2, height / 2));

	update(graph.links, graph.nodes, svg);
}

function update(links, nodes, svg) {
	var color = d3.scaleOrdinal(d3['schemeSet3']);
	
	simulation.alphaTarget(0.3).restart()

	svg
	.call(d3.zoom()
		.extent([[0, 0], [width, height]])
		.scaleExtent([0.5, 3])
		.translateExtent([[0, 0], [width, height]])
		.on("zoom", function () {
			k = d3.event.transform.k;
			svg.selectAll('g').attr("transform", d3.event.transform);
		})
		);

	link = svg.append('g').selectAll("line.link")
	.data(links)
	.enter().append("svg:line")
	.attr("class", "link")
	.attr("stroke", "black")
	.attr("stroke-width", "1")
	.attr('marker-end','url(#arrowhead)');

	svg.append('g').append('defs').append('marker')
	.attrs({'id':'arrowhead',
		'viewBox':'2 -5 10 10',
		'refX':25,
		'refY':0,
		'orient':'auto',
		'markerWidth':10,
		'markerHeight':10,
		'xoverflow':'visible'})
	.append('svg:path')
	.attr('d', 'M 0,-5 L 10 ,0 L 0,5')
	.attr('fill', '#999');


	link.append("title")
	.text(function (d) {return d.type;});

	edgepaths = svg.append('g').selectAll(".edgepath")
	.data(links)
	.enter()
	.append('path')
	.attrs({
		'class': 'edgepath',
		'fill-opacity': 0,
		'stroke-opacity': 0,
		'id': function (d, i) {return 'edgepath' + i}
	})
	.style("pointer-events", "none");

	edgelabels = svg.append('g').selectAll(".edgelabel")
	.data(links)
	.enter()
	.append('text')
	.style("pointer-events", "none")
	.attrs({
		'class': 'edgelabel',
		'id': function (d, i) {return 'edgelabel' + i},
		'font-size': 10,
		'fill': '#aaa'
	});

	edgelabels.append('textPath')
	.attr('xlink:href', function (d, i) {return '#edgepath' + i})
	.style("text-anchor", "middle")
	.style("pointer-events", "none")
	.attr("startOffset", "50%")
	.text(function (d) {return d.type});

	node = svg.append('g').selectAll(".node")
	.data(nodes)
	.enter()
	.append("g")
	.attr("class", "node")
	.call(d3.drag()
		.on("start", dragstarted)
		.on("drag", dragged)
		);

	node.append("circle")
	.attr("r", function(d) {return (Math.sqrt(d.outdeg + 1) * radius)})
	.style("fill", function (d, i) {return color(i);})
	.style("stroke", function(d, i) { return d3.color(color(i)).darker(); })

	node.append("title")
	.text(function (d) {return d.name;});


	node.append("text")
	.attr("dy", -3)
	.text(shortName)
	.style("opacity", 0.5);


	node.on("mouseover", function(d) {		
		d3.select(this)
		.select("text")
		.text(function (d) {return d.name;})
		.transition()
		.duration(200)
		.style("opacity", 1);

		d3.select(this).select("circle").style("opacity", 1);
	})
	.on("mouseout", function(d) {
		d3.select(this)
		.select("text")
		.text(shortName)
		.transition()
		.duration(200)
		.style("opacity", 0.5);

		d3.select(this).select("circle").style("opacity", 0.65);
	});

	simulation
	.nodes(nodes)
	.on("tick", ticked);

	simulation.force("link")
	.links(links);
}

function ticked() {
	link
	.attr("x1", function (d) {return d.source.x;})
	.attr("y1", function (d) {return d.source.y;})
	.attr("x2", function (d) {return d.target.x;})
	.attr("y2", function (d) {return d.target.y;});

	node.attr("cx", function(d) { return d.x = Math.max(radius, Math.min(width - radius, d.x)); })
	.attr("cy", function(d) { return d.y = Math.max(radius, Math.min(height - radius, d.y)); })
	.attr("transform", function (d) {return "translate(" + d.x + ", " + d.y + ")";});


	edgepaths.attr('d', function (d) {
		return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
	});

	edgelabels.attr('transform', function (d) {
		if (d.target.x < d.source.x) {
			var bbox = this.getBBox();

			rx = bbox.x + bbox.width / 2;
			ry = bbox.y + bbox.height / 2;
			return 'rotate(180 ' + rx + ' ' + ry + ')';
		}
		else {
			return 'rotate(0)';
		}
	});
}

function dragstarted(d) {
	if (!d3.event.active) simulation.alphaTarget(0.3).restart()
		d.fx = d.x;
	d.fy = d.y;
}

function dragged(d) {
	d.fx = d3.event.x;
	d.fy = d3.event.y;
}

function shortName (d) {
	if (d.name.length > 20)
		return d.name.substring(0,19) + "...";
	else
		return d.name;
}