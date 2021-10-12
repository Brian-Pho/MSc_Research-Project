SCALED_SUBTESTS = [
    'WISC_BD_Scaled',
    'WISC_Similarities_Scaled',
    'WISC_MR_Scaled',
    'WISC_DS_Scaled',
    'WISC_Coding_Scaled',
    'WISC_Vocab_Scaled',
    'WISC_FW_Scaled',
    'WISC_VP_Scaled',
    'WISC_PS_Scaled',
    'WISC_SS_Scaled',
]

RAW_SUBTESTS = [subtest.replace("Scaled", "Raw") for subtest in SCALED_SUBTESTS]

PRIMARY_INDICES = [
    'WISC_VSI',
    'WISC_VCI',
    'WISC_FRI',
    'WISC_WMI',
    'WISC_PSI',
]

FSIQ = ['WISC_FSIQ']

WISC_LEVEL = {
    0: FSIQ + PRIMARY_INDICES + SCALED_SUBTESTS,
    1: FSIQ,
    2: PRIMARY_INDICES,
    3: SCALED_SUBTESTS,
    4: RAW_SUBTESTS,
}
