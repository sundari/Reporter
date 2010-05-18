
<%page args="mvals"/> 

.. csv-table:: ${mvals['name']}
   :widths: 3, 10

   "**Measurements**", "
                       - AH: ${mvals['AH']} ms
		       - HV: ${mvals['HV']} ms
		       - CL: ${mvals['CL']} ms"
   "**ParaHisian pacing**", "${mvals['parahisian']}"
    "**Incremental RV pace**", "
                                - VA conduction - ${mvals['va_conduction_incr']}
				- VAWB - ${mvals['vawb']} ms
				- Atrial activation - ${mvals['atrial_activation_incr']}"
    "**Programmed RV pace**", "
         - VA conduction - ${mvals['va_conduction_prog']}
	 - VAERP - ${mvals['verp']} ms
	 - Atrial activation - ${mvals['atrial_activation_prog']}
	 - VERP - ${mvals['verp']} ms"
    "**Incremental A pace**", "
         - AVWB - ${mvals['avwb']} ms
	 - Level of block - ${mvals['av_block_level']}
	 - AH jump - ${mvals['ah_jump_incr']}"
    "**Programmed A pace**", "
         - AH jump - ${mvals['ah_jump_prog']}
	 - SPERP - ${mvals['sperp']} ms
	 - FPERP - ${mvals['fperp']} ms
	 - AERP - ${mvals['aerp']} ms"

