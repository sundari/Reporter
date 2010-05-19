
<%
    def list2enum(lst):
        """convert items in python list to enumerated list"""
	return ''.join(['\n\t#. ' + x for x in lst])	
%>

<%
    def list2bullet(lst):
        """convert items in python list to bullet list"""
	return ''.join(['\n\t- ' + x for x in lst])	
%>

<%
    def csv2bullet(csv):
        """convert a line with comma separated values into
	a bullet list"""
	lst = csv.split(',')
	return list2bullet(lst)
%>

<%
    def csv2enum(csv):
        """convert a line with comma separated values into
	an eunumarated list"""
	lst = csv.split(',')
	return list2enum(lst)
%>



|jipmer|  Electrophysiology study and RF ablation
=================================================

Department of Cardiology
------------------------

Jawaharlal Institute of Postgraduate Medical Education and Research
--------------------------------------------------------------------

.. csv-table:: Demographics

          "**Name**", "${vals['Demographics_Name']}", "**Age**", "${vals['Demographics_Age']}", "**Sex**", "${vals['Demographics_Sex']}"
	  "**Date of Admission**", "${vals['Demographics_Date of Admission']}", "**Date of Procedure**", "${vals['Demographics_Date of Procedure']}", "**IP No.**", "${vals['Demographics_IP Number']}"

Summary
'''''''
"${vals['summary']}

.. csv-table:: Clinical
   :widths: 3, 10

    "**Presentation**", "${vals['Clinical_Presentation']}"
    "**ECG**", "${vals['Clinical_ECG']}"
    "**ECG during tachycardia**", "${vals['Clinical_ECG during tachycardia']}"
    "**Other investigations**", "${vals['Clinical_Other investigations']}"
    "**Drugs**", "${csv2enum(vals['Clinical_Drugs'])}"

.. csv-table:: Technical details
   :widths: 3, 10

    "**Lab**", "${vals['Technical_Lab']}"
    "**EP System**", "${vals['Technical_EP System']}"
    "**Stimulator**", "${vals['Technical_Stimulator']}"
    "**Operators**", "${list2bullet([vals['Technical_Operator 1'],
                                     vals['Technical_Operator 2']])}"
    "**Comment**", "${vals['Technical_Comment']}"


.. csv-table:: Access and catheters
   :widths: 3, 10

    "**Access**", "${list2bullet(vals['access'])}"
    "**Catheters**", "${list2bullet(vals['catheters'])}"


% for m in vals['pre_measurements']:
   <%include file="measurements.rst" args="mvals=m"/>
% endfor

% for m in vals['tachycardias']:
   <%include file="tachycardia.rst" args="mvals=m"/>
% endfor

.. csv-table:: RF ablation
    :widths: 3, 10

    "**Ablation catheter used**", "4 mm tip Webster Blue"
    "**Target**", "Anatomical - at level of CS os / Slow pathway potential"
    "**Settings**", "60 C / 30 W"
    "**Ablation time**", "2 / 60 seconds"
    "**Endpoint**", "No AH jump / Non inducible"

% for m in vals['post_measurements']:
   <%include file="measurements.rst" args="mvals=m"/>
% endfor



Conclusions
'''''''''''
"${list2bullet(vals['conclusions'])}"

Recommendations
'''''''''''''''
"${list2bullet(vals['recommendations'])}"


.. raw:: pdf

       Spacer 0 40
     
    
| **Dr. Raja J. Selvaraj**
| **Department of Cardiology**
| **JIPMER**

      

     
.. |jipmer| image:: jipmer_logo.png
              :height: 1in
    	      :width: 1in
	      :align: middle

.. footer::

   EP report  Pg.###Page###
	      
	     
