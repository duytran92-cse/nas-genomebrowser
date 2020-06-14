
PAGE_KINDS = [
    {'id': 'page',         'label': 'Page'},
    {'id': 'variation',    'label': 'Variation'},
    {'id': 'gene',         'label': 'Gene'},
    {'id': 'trait',        'label': 'Trait'},
    {'id': 'disease',      'label': 'Disease'},
    {'id': 'treatment',    'label': 'Treatment'}
]


PAGE_BLOCK_POSITIONS = [
    {'id': 'main',                     'label': 'Main'},
    {'id': 'left',                     'label': 'Left'},
    {'id': 'right',                    'label': 'Right'},
]

PAGE_BLOCK_KINDS = [
    {'id': 'general_text',             'label': 'General - Text'},
    {'id': 'general_publications',     'label': 'General - Publications'},
    {'id': 'variation_effect',         'label': 'Variation - Effect'},
]


POPULATION_CODES_EFFECT = [
    {'id': 'Global',                   'label': 'Global'},
    {'id': 'AFR',                      'label': 'African'},
    {'id': 'AMR',                      'label': 'American'},
    {'id': 'EUR',                      'label': 'European'},
    {'id': 'EAS',                      'label': 'East Asian'},
    {'id': 'SAS',                      'label': 'South Asian'},
]

POPULATION_CODES = [
    {'id': 'AFR',                      'label': 'African'},
    {'id': 'AMR',                      'label': 'American'},
    {'id': 'EUR',                      'label': 'European'},
    {'id': 'EAS',                      'label': 'East Asian'},
    {'id': 'SAS',                      'label': 'South Asian'},

    {'id': 'ACB',                      'label': 'African Caribbean in Barbados'},
    {'id': 'TSI',                      'label': 'Toscani in Italy'},
    {'id': 'BEB',                      'label': 'Bengali in Bangladesh'},
    {'id': 'PEL',                      'label': 'Peruvian in Lima, Peru'},
    {'id': 'LWK',                      'label': 'Luhya in Webuye, Kenya'},
    {'id': 'MSL',                      'label': 'Mende in Sierra Leone'},
    {'id': 'GBR',                      'label': 'British in England and Scotland'},
    {'id': 'IBS',                      'label': 'Iberian populations in Spain'},
    {'id': 'ASW',                      'label': 'African Ancestry in Southwest US'},
    {'id': 'KHV',                      'label': 'Kinh in Ho Chi Minh City, Vietnam'},
    {'id': 'CEU',                      'label': 'Utah residents with Northern and Western European ancestry'},
    {'id': 'YRI',                      'label': 'Yoruba in Ibadan, Nigeria'},
    {'id': 'CHB',                      'label': 'Han Chinese in Bejing, China'},
    {'id': 'GWD',                      'label': 'Gambian in Western Division, The Gambia'},
    {'id': 'STU',                      'label': 'Sri Lankan Tamil in the UK'},
    {'id': 'CHS',                      'label': 'Southern Han Chinese, China'},
    {'id': 'ESN',                      'label': 'Esan in Nigeria'},
    {'id': 'FIN',                      'label': 'Finnish in Finland'},
    {'id': 'GIH',                      'label': 'Gujarati Indian in Houston, Texas'},
    {'id': 'PJL',                      'label': 'Punjabi in Lahore, Pakistan'},
    {'id': 'MXL',                      'label': 'Mexican Ancestry in Los Angeles, California'},
    {'id': 'PUR',                      'label': 'Puerto Rican in Puerto Rico'},
    {'id': 'ITU',                      'label': 'Indian Telugu in the UK'},
    {'id': 'CDX',                      'label': 'Chinese Dai in Xishuangbanna, China'},
    {'id': 'JPT',                      'label': 'Japanese in Tokyo, Japan'},
    {'id': 'CLM',                      'label': 'Colombian in Medellin, Colombia'}

]
SUB_POPULATION_CODES = {
    'EAS' : [
        {'id': 'CHB',                      'label': 'Han Chinese in Bejing, China'},
        {'id': 'JPT',                      'label': 'Japanese in Tokyo, Japan'},
        {'id': 'CHS',                      'label': 'Southern Han Chinese, China'},
        {'id': 'CDX',                      'label': 'Chinese Dai in Xishuangbanna, China'},
        {'id': 'KHV',                      'label': 'Kinh in Ho Chi Minh City, Vietnam'},
    ],
    'SAS' : [
        {'id': 'GIH',                      'label': 'Gujarati Indian in Houston, Texas'},
        {'id': 'PJL',                      'label': 'Punjabi in Lahore, Pakistan'},
        {'id': 'BEB',                      'label': 'Bengali in Bangladesh'},
        {'id': 'STU',                      'label': 'Sri Lankan Tamil in the UK'},
        {'id': 'ITU',                      'label': 'Indian Telugu in the UK'},

    ],
    'AMR': [
        {'id': 'MXL',                      'label': 'Mexican Ancestry in Los Angeles, California'},
        {'id': 'PUR',                      'label': 'Puerto Rican in Puerto Rico'},
        {'id': 'CLM',                      'label': 'Colombian in Medellin, Colombia'},
        {'id': 'PEL',                      'label': 'Peruvian in Lima, Peru'},
    ],
    'AFR': [
        {'id': 'ACB',                      'label': 'African Caribbean in Barbados'},
        {'id': 'YRI',                      'label': 'Yoruba in Ibadan, Nigeria'},
        {'id': 'LWK',                      'label': 'Luhya in Webuye, Kenya'},
        {'id': 'GWD',                      'label': 'Gambian in Western Division, The Gambia'},
        {'id': 'MSL',                      'label': 'Mende in Sierra Leone'},
        {'id': 'ESN',                      'label': 'Esan in Nigeria'},
        {'id': 'ASW',                      'label': 'African Ancestry in Southwest US'},
    ],
    'EUR': [
        {'id': 'CEU',                      'label': 'Utah residents with Northern and Western European ancestry'},
        {'id': 'TSI',                      'label': 'Toscani in Italy'},
        {'id': 'FIN',                      'label': 'Finnish in Finland'},
        {'id': 'GBR',                      'label': 'British in England and Scotland'},
        {'id': 'IBS',                      'label': 'Iberian populations in Spain'},
    ]
}

PAGE_BLOCK_EFFECT_COLOR = [
    {'id': '#011460',                      'label': 'Dark Blue'},
    {'id': '#00B0F0',                      'label': 'Light Blue'},
    {'id': '#95C709',                      'label': 'Green'},
]

PAGE_BLOCK_VERSION_STATUS = [
    {'id': 'pending', 'label': 'Pending'},
    {'id': 'approved', 'label': 'Approved'},
    {'id': 'denied', 'label': 'Denied'},
]

GENE_EFFECT_TYPE = [
    {'id': 'conditions',    'label': 'Conditions'},
    {'id': 'reactions',     'label': 'Reactions'},
    {'id': 'traits',        'label': 'Traits'}
]
