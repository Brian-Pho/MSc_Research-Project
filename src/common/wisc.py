"""
Holds the constants for the Weschler Intelligence Scale for Children (WISC).
"""
# The ten WISC-V scaled subtests.
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

# The five WISC-V primary indices and full-scale IQ.
FSIQ = ['WISC_FSIQ']
PRIMARY_INDICES = [
    'WISC_VSI',
    'WISC_VCI',
    'WISC_FRI',
    'WISC_WMI',
    'WISC_PSI',
]

# The WISC-V level/granularity we want.
WISC_LEVEL = {
    0: FSIQ + PRIMARY_INDICES + SCALED_SUBTESTS,
    1: FSIQ,
    2: PRIMARY_INDICES,
    3: SCALED_SUBTESTS,
    4: RAW_SUBTESTS,
    5: FSIQ + PRIMARY_INDICES,
}
