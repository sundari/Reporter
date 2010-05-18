"""Render the report template by supplying the values"""


from mako.template import Template
from mako.lookup import TemplateLookup

mylookup = TemplateLookup(directories=['/data/Dropbox/work/EP_reports_JIPMER/'])


baseline_measurements = {'name':'Baseline',
                         'AH':134,
                         'HV':34,
                         'CL':754,
                         'parahisian':'Nodal response',
                         'va_conduction_incr':'non-decremental',
                         'vawb':320,
                         'atrial_activation_incr':'concentric',
                         'va_conduction_prog':'non-decremental',
                         'vaerp':310,
                         'atrial_activation_prog':'concentric',
                         'verp':300,
                         'avwb':360,
                         'av_block_level':'Infra-His',
                         'ah_jump_incr':'present',
                         'ah_jump_prog':'present',
                         'sperp':360,
                         'fperp':320,
                         'aerp':300
                         }

isoprenaline_measurements = {'name':'Isoprenaline',
                         'AH':114,
                         'HV':34,
                         'CL':554,
                         'parahisian':'Nodal response',
                         'va_conduction_incr':'non-decremental',
                         'vawb':310,
                         'atrial_activation_incr':'concentric',
                         'va_conduction_prog':'non-decremental',
                         'vaerp':310,
                         'atrial_activation_prog':'concentric',
                         'verp':300,
                         'avwb':360,
                         'av_block_level':'Infra-His',
                         'ah_jump_incr':'present',
                         'ah_jump_prog':'present',
                         'sperp':360,
                         'fperp':320,
                         'aerp':300
                         }

postrf_measurements = {'name':'Post ablation',
                         'AH':134,
                         'HV':34,
                         'CL':714,
                         'parahisian':'Nodal response',
                         'va_conduction_incr':'non-decremental',
                         'vawb':320,
                         'atrial_activation_incr':'concentric',
                         'va_conduction_prog':'non-decremental',
                         'vaerp':310,
                         'atrial_activation_prog':'concentric',
                         'verp':300,
                         'avwb':360,
                         'av_block_level':'Infra-His',
                         'ah_jump_incr':'present',
                         'ah_jump_prog':'present',
                         'sperp':360,
                         'fperp':320,
                         'aerp':300
                         }


tachycardia1 = {'name': 'Tachycardia',
                'induction': 'Atrium 600/320',
                'CL': 310 ,
                'AH': 134,
                'HV': 34,
                'VA': 22,
                'va_relationship': '1:1',
                'atrial_activation': 'concentric',
                'ventricular_overdrive': 'VAV response',
                'ventricular_extra': 'unable to preexcite atrium',
                'atrial_overdrive': 'VA linking',
                'atrial_extra': 'advances V',
                'termination': 'RV burst 240',
                'comment': 'Findings consistent with AVNRT'}

demographics = {'patient_name':'John Doe',
                'patient_age': '34 years',
                'patient_sex': 'Male',
                'admission_date':'29-01-2009',
                'hospital_number':'123456',
                'ip_number':'654321'}

clinical = {'presentation':'Palpitations since the age of 2 years. History of tachycardia termination with Adenosine.',
            'ecg': 'Pre-excitation suggestive of Right posteroseptal AP during sinus rhythm',
            'ecg_tachycardia':'Narrow QRS, long RP tachycardia at rate of 220 bpm.',
            'other_investigations':'Echo - No structural abnormalities'}

summary = """34 year old male presented with palpitations, documented adenosine-sensitive tachycardia and ECG evidence of preexcitation. EP study showed evidence of a non-decremental accessory pathway with both antegrade and retrograde conduction. Tachycardia induced during programmed stimulation was identified as orthodromic AVRT based on eccentric atrial activation, atrial preexcitation by His refractory PAC and VAV response with ventricular overdrive pacing. Mapping showed earliest ventricular activation at right posteroseptal annulus. RF delivery at this location resulted in abolition of pathway conduction and made the tachycardia non-inducible. See procedure details below."""

technical = {'lab':'EMS',
            'ep_system':'Bard',
            'stimulator':'Micropace 2',
            'operators':["Dr. Raja Selvaraj", "Dr. S. Anandaraja", "Dr. J. Balachander"],
            'technical_comment':'System was changed',
            'access':["RFV: 5F x 2, 6F", "LFV: 7F"],
            'catheters':["5F Quadripolar x 2", "6F Deflectable decapolar", "7F Deflectable 4 mm tip ablation catheter"],}

procedure = {'summary': summary,
            'pre_measurements': [baseline_measurements,
                                 isoprenaline_measurements],
            'tachycardias': [tachycardia1],
            'post_measurements': [postrf_measurements],
            'conclusions': ['**Typical slow-fast AVNRT**',
                            '**Successful ablation of slow pathway**'],
            'recommendations': ['**Aspirin 150 mg OD x 6 weeks**',
                                '**Review after 1 month in Arrhythmia clinic (Cardiology OPD, Wednesday afternoon)**']}


dictlist = [demographics, clinical, technical, procedure]


def get_testvals():
    return {'patient_name':'John Doe',
            'patient_age': '34 years',
            'patient_sex': 'Male',
            'admission_date':'29-01-2009',
            'hospital_number':'123456',
            'ip_number':'654321',
            'presentation':'Palpitations since the age of 2 years. History of tachycardia termination with Adenosine.',
            'ecg': 'Pre-excitation suggestive of Right posteroseptal AP during sinus rhythm',
            'ecg_tachycardia':'Narrow QRS, long RP tachycardia at rate of 220 bpm.',
            'other_investigations':'Echo - No structural abnormalities',
            'drugs': ["Aspirin 81 mg OD", "Atorvastatin 20 mg OD"],
            'lab':'EMS',
            'ep_system':'Bard',
            'stimulator':'Micropace 2',
            'operators':["Dr. Raja Selvaraj", "Dr. S. Anandaraja", "Dr. J. Balachander"],
            'technical_comment':'System was changed',
            'access':["RFV: 5F x 2, 6F", "LFV: 7F"],
            'catheters':["5F Quadripolar x 2", "6F Deflectable decapolar", "7F Deflectable 4 mm tip ablation catheter"],
            'summary': summary,
            'pre_measurements': [baseline_measurements,
                                 isoprenaline_measurements],
            'tachycardias': [tachycardia1],
            'post_measurements': [postrf_measurements],
            'conclusions': ['**Typical slow-fast AVNRT**',
                            '**Successful ablation of slow pathway**'],
            'recommendations': ['**Aspirin 150 mg OD x 6 weeks**',
                                '**Review after 1 month in Arrhythmia clinic (Cardiology OPD, Wednesday afternoon)**']
}

        

mytemplate = Template(filename='ep_report_template.rst', lookup=mylookup)
print mytemplate.render(vals=get_testvals())
