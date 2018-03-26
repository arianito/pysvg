class Element(object):
	def __init__(self, type='none', id=None):
		
		self.type = type
		self.children = []
		self.attributes = {}
		if id:
			self.attr('id', id)

	def add(self, element):
		self.children.append(element)
		return self

	def attr(self, *args):
		if len(args) == 1:
			if isinstance(args[0], dict):
				for key, value in args[0].iteritems():
					self.attributes[key] = value
				return self
			else:
				return self.attributes[args[0]] if args[0] in self.attributes else None
		elif len(args) > 1:
			self.attributes[args[0]] = args[1]
			return self


	def css(self, *args):
		styles = self.__parseStyle(self.attr('style'))
		if len(args) == 1:
			if isinstance(args[0], dict):
				for key, value in args[0].iteritems():
					styles[key] = value
				self.attr('style', self.__renderStyle(styles))
				return self
			else:
				return styles[args[0]] if args[0] in styles else None
		elif len(args) > 1:
			styles[args[0]] = args[1]
			self.attr('style', self.__renderStyle(styles))
			return self


	def __getitem__(self, index):
		return self.attr(index)

	def __setitem__(self, index, value):
		return self.attr(index, value)


	def transform(self, *args):
		trs = self.__parseTransform(self.attr('transform'))
		if len(args) == 1:
			if isinstance(args[0], dict):
				for key, value in args[0].iteritems():
					trs[key] = value
				self.attr('transform', self.__renderTransform(trs))
				return self
			else:
				return trs[args[0]] if args[0] in trs else None
		elif len(args) > 1:
			trs[args[0]] = args[1]
			self.attr('transform', self.__renderTransform(trs))
			return self


	def addClass(self, *args):
		classes = self.__parseClass(self.attr('class'))
		for x in args:
			classes.append(x)
		self.attr('class', self.__renderClass(classes))


	def removeClass(self, *args):
		classes = self.__parseClass(self.attr('class'))
		for x in args:
			classes.remove(x)
		self.attr('class', self.__renderClass(classes))


	def hasClass(self, *args):
		classes = self.__parseClass(self.attr('class'))
		for x in args:
			if x in args:
				return True
		return False


	def styles(self):
		return self.__parseStyle(self.attr('style'))

	def classes(self):
		return self.__parseClass(self.attr('class'))


	def tranformation(self):
		return self.__parseTransform(self.attr('transform'))

	def __parseStyle(self, styles):
		if styles:
			items = styles.split(';')
			obj = {};
			for x in items:
				spl = x.split(':')
				obj[spl[0]] = spl[1]
			return obj
		else:
			return {}

	def __renderStyle(self, styles):
		plain = ''
		for key, value in styles.iteritems():
			plain = plain + str(key)+':'+str(value)+';'
		return plain[:-1]


	def __parseClass(self, classes):
		if classes:
			items = classes.split(' ')
			obj = [];
			for x in items: 
				obj.append(x)
			return obj
		else:
			return []

	def __renderClass(self, classes):
		plain = ''
		for x in classes:
			plain = plain + x + ' '
		return plain[:-1]



	def __parseTransform(self, trs):
		if trs:
			items = trs.split(') ')
			obj = {};
			for x in items:
				spl = x.split('(')
				nm = spl[0]
				dt = spl[1][:-1].split(',')
				obj[nm] = dt
			return obj
		else:
			return {}

	def __renderTransform(self, trs):
		plain = ''
		for key, value in trs.iteritems():
			dt = ''
			if isinstance(value, list):
				for x in value:
					dt = dt + str(x) + ' '
			else:
				dt = str(value)+' '
			plain = plain + str(key)+'('+ dt[:-1] +') '
		return plain[:-1]


	def select(self, id):
		if id == self.attr('id'):
			return self
		for x in self.children:
			a = x.select(id)
			if a:
				return a
		return Element()


	def render(self):
		plain_children = ''
		plain_attributes = ''
		for x in self.children:
			if hasattr(x, 'render'):
				plain_children = plain_children + x.render()


		for key, value in self.attributes.iteritems():
			plain_attributes = plain_attributes+' '+str(key)+'="'+str(value)+'"'

		return '<'+self.type+''+plain_attributes+'>'+plain_children+'</'+self.type+'>'


class Svg(Element):
	def __init__(self):
		super(Svg, self).__init__('svg')

		self.attr('version','1.2')
		self.attr('viewBox','0 0 100 100')
		self.attr('width','100%')
		self.attr('height','100%')
		self.attr('xmlns','http://www.w3.org/2000/svg')

	def save(self, path):
		file = open(path, 'w')
		file.write(self.render())
		file.close()

	def render(self):
		return '<?xml version="1.0" encoding="utf-8" ?>' + super(Svg, self).render()
