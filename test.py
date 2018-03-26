from svg import Element, Svg


svg = Svg()
bck = Element('rect').attr('fill', 'rgba(10,2,3,0.2)')
bck.css({
	'x': '0',
	'y': '0',
	'width': '100',
	'height': '100'
});
svg.add(bck)

g = Element('g')

circle = Element('circle').attr({'cx': '0', 'y': '0', 'r': 10, 'fill': 'transparent', 'stroke': '#000'})
cross = Element('g').add(Element('line').attr({'x1':-2, 'y1': 0, 'x2': 2, 'y2': 0, 'stroke': '#000'})).add(Element('line').attr({'x1':0, 'y1': -2, 'x2': 0, 'y2': 2, 'stroke': '#000'})).transform('translate', [0, -3])
minus = Element('g').add(Element('line').attr({'x1':-2, 'y1': 0, 'x2': 2, 'y2': 0, 'stroke': '#000'})).transform('translate', [0, 4])

g.add(cross).add(minus).add(circle)
g.transform('translate', ['50','50'])


svg.add(g)
svg.save('test.svg')