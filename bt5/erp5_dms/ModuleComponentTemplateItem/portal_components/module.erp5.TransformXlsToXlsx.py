from Products.PortalTransforms.interfaces import itransform
from zope.interface import implements
from Products.ERP5OOo.transforms.oood_commandtransform import OOOdCommandTransform, OOoDocumentDataStream

class XlsToXlsx:
  """Transforms xls to xlsx by using Cloudooo"""

  implements(itransform)

  __name__ = 'xls_to_xlsx'
  inputs   = ('application/vnd.ms-excel',)
  output = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

  tranform_engine = OOOdCommandTransform.__module__

  def name(self):
    return self.__name__

  def __getattr__(self, attr):
    if attr == 'inputs':
      return self.config['inputs']
    if attr == 'output':
      return self.config['output']
    raise AttributeError(attr)

  def convert(self, orig, data, cache=None, filename=None, context=None, **kwargs):
    data = str(orig)
    xls = OOOdCommandTransform(context, filename, data, self.inputs[0])
    xlsx = xls.convertTo('xlsx')
    if cache is not None:
      cache.setData(xlsx)
      return cache
    else:
      stream = OOoDocumentDataStream()
      stream.setData(xlsx)
      return stream

def register():
  return XlsToXlsx()
