
<%
    def list2enum(lst):
        """convert items in python list to enumerated list"""
	return ''.join(['\n\t#. ' + x for x in lst if x.strip() != ''])	
%>

<%
    def list2bullet(lst):
        """convert items in python list to bullet list"""
	return ''.join(['\n\t- ' + x for x in lst if x.strip() != ''])	
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
${vals['Conclusions_Summary']}

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

    "**Access**", "${list2bullet([vals['Technical_Access 1'],vals['Technical_Access 2'],vals['Technical_Access 3'],vals['Technical_Access 4']])}"
    "**Catheters**", "${list2bullet([vals['Technical_Catheter 1'], vals['Technical_Catheter 2'],vals['Technical_Catheter 3'],vals['Technical_Catheter 4'],vals['Technical_Catheter 5']])}"

				     
.. csv-table:: Baseline Findings
   :widths: 3, 10

   "**Measurements**", "
                       - Rhythm: ${vals['Baseline_Rhythm']}
                       - AH: ${vals['Baseline_AH']} ms
		       - HV: ${vals['Baseline_HV']} ms
		       - CL: ${vals['Baseline_CL']} ms"
   "**ParaHisian pacing**", "${vals['Baseline_Parahisian']}"
    "**Incremental RV pace**", "
                                - VA conduction - ${vals['Incr V Pace_VA conduction']}
				- VAWB - ${vals['Incr V Pace_VAWB']} ms
				- Atrial activation - ${vals['Incr V Pace_Atrial Activation']}"
    "**Programmed RV pace**", "
         - VA conduction - ${vals['Prog V Pace_VA conduction']}
	 - VAERP - ${vals['Prog V Pace_VAERP']} ms
	 - Atrial activation - ${vals['Prog V Pace_Atrial Activation']}
	 - VERP - ${vals['Prog V Pace_VERP']} ms"
    "**Incremental A pace**", "
         - AVWB - ${vals['Incr A Pace_AVWB']} ms
	 - Level of block - ${vals['Incr A Pace_Level of block']}
	 - AH jump - ${vals['Incr A Pace_AH jump']}"
    "**Programmed A pace**", "
         - AH jump - ${vals['Prog A Pace_AH jump']}
	 - SPERP - ${vals['Prog A Pace_SPERP']} ms
	 - FPERP - ${vals['Prog A Pace_FPERP']} ms
	 - AERP - ${vals['Prog A Pace_AERP']}"



.. csv-table:: Tachycardia
   :widths: 3, 10

   "**Induced by**", "${vals['Tachycardia_Induction']}"
    "**Measurements**", "
         - QRS - ${vals['Tachycardia_QRS']}
         - Cycle length - ${vals['Tachycardia_CL']} ms
	 - AH - ${vals['Tachycardia_AH']} ms
	 - HV - ${vals['Tachycardia_HV']} ms
	 - VA - ${vals['Tachycardia_VA']} ms"
    "**VA relationship**", "${vals['Tachycardia_VA relationship']}"
    "**Atrial activation sequence**", "${vals['Tachycardia_Atrial activation']}"
    "**Ventricular overdrive pacing**", "${vals['Tachycardia_RV overdrive']}"
    "**Ventricular extrastimuli**", "${vals['Tachycardia_RV extra']}"
    "**Atrial overdrive pacing**", "${vals['Tachycardia_RA overdrive']}"
    "**Atrial extrastimuli**", "${vals['Tachycardia_RA extra']}"
    "**Terminated by**", "${vals['Tachycardia_Termination']}"
    "**Comment**", "${vals['Tachycardia_Comment']}"



.. csv-table:: RF ablation
    :widths: 3, 10

    "**Ablation catheter used**", "${vals['Ablation_Catheter']}"
    "**Target**", "${vals['Ablation_Target']}"
    "**Settings**", "${vals['Ablation_Settings']}"
    "**Ablation time**", "${vals['Ablation_Time']}"
    "**Endpoint**", "${vals['Ablation_Endpoint']}"


.. csv-table:: Post Ablation
   :widths: 3, 10

   "**Measurements**", "
                       - Rhythm: ${vals['Post Ablation_Rhythm']}
                       - AH: ${vals['Post Ablation_AH']} ms
		       - HV: ${vals['Post Ablation_HV']} ms
		       - CL: ${vals['Post Ablation_CL']} ms"
   "**ParaHisian pacing**", "${vals['Post Ablation_Parahisian']}"
   "**Incremental RV pace**", "${vals['Post Ablation_Incr V Pace']}"
    "**Programmed RV pace**", "${vals['Post Ablation_Prog V Pace']}"
    "**Incremental A pace**", "${vals['Post Ablation_Incr A Pace']}"
    "**Programmed A pace**", "${vals['Post Ablation_Prog A Pace']}"



Conclusions
'''''''''''
${list2bullet([vals['Conclusions_Conclusion 1'], vals['Conclusions_Conclusion 2'],
                vals['Conclusions_Conclusion 3'], vals['Conclusions_Conclusion 4']])}


Recommendations
'''''''''''''''
${list2bullet([vals['Recommendations_Recommendation 1'],
                vals['Recommendations_Recommendation 2'],
		vals['Recommendations_Recommendation 3'],
		vals['Recommendations_Recommendation 4']])}



.. raw:: pdf

       Spacer 0 40
     
    
| **Dr. Raja J. Selvaraj**
| **Assistant Professor of Cardiology**
| **JIPMER**

      

     
.. |jipmer| image:: jipmer_logo.png
              :height: 1in
    	      :width: 1in
	      :align: middle

