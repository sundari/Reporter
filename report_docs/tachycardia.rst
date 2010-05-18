<%page args="mvals"/> 

.. csv-table:: ${mvals['name']}
   :widths: 3, 10

   "**Induced by**", "${mvals['induction']}"
    "**Measurements**", "
         - Cycle length - ${mvals['CL']} ms
	 - AH - ${mvals['AH']} ms
	 - HV - ${mvals['HV']} ms
	 - VA - ${mvals['VA']} ms"
    "**VA relationship**", "${mvals['va_relationship']}"
    "**Atrial activation sequence**", "${mvals['atrial_activation']}"
    "**Ventricular overdrive pacing**", "${mvals['ventricular_overdrive']}"
    "**Ventricular extrastimuli**", "${mvals['ventricular_extra']}"
    "**Atrial overdrive pacing**", "${mvals['atrial_overdrive']}"
    "**Atrial extrastimuli**", "${mvals['atrial_extra']}"
    "**Terminated by**", "${mvals['termination']}"
    "**Comment**", "${mvals['comment']}"


