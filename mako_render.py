"""Render the report template by supplying the values"""


from mako.template import Template
#from mako.lookup import TemplateLookup

#mylookup = TemplateLookup(directories=['/data/Dropbox/work/EP_reports_JIPMER/'])


mytemplate = Template(filename='report_docs/ep_report_template.rst')
print mytemplate.render(vals=get_testvals())
