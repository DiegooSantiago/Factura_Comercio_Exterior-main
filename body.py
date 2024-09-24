from layout import Layout
from abc import abstractmethod

class Body(Layout):

	def __init__(self, xml_obj, filenametxt):
		super().__init__(xml_obj, filenametxt)

	@abstractmethod
	def GetLayout(self, file_object, c, filenametxt):
		self.GetStaticHeaderText(c)
		self.GetFolios(c)
		self.GetRectangles(c)
		self.GetDetalleHeader(c)
		self.PrintConceptos(c)
