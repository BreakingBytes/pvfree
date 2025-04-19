from pvfree import views


def test__datatables_helper():
    testdata = dict.fromkeys(TESTDATA)
    for k, v in TESTDATA.items():
        testdata[k] = v[-1]  # django gets the last item in the queryset
    columns, order = views._datatables_helper(testdata)
    assert columns == COL_EXPECTED
    assert order == ORDER_EXPECTED


# TODO: make these black
TESTDATA = {
  'draw': ['1'],
  'columns[0][data]': ['Name'], 'columns[0][name]': [''], 'columns[0][searchable]': ['true'], 'columns[0][orderable]': ['true'], 'columns[0][search][value]': [''], 'columns[0][search][regex]': ['false'], 
  'columns[1][data]': ['BIPV'], 'columns[1][name]': [''], 'columns[1][searchable]': ['true'], 'columns[1][orderable]': ['true'], 'columns[1][search][value]': [''], 'columns[1][search][regex]': ['false'], 
  'columns[2][data]': ['Date'], 'columns[2][name]': [''], 'columns[2][searchable]': ['true'], 'columns[2][orderable]': ['true'], 'columns[2][search][value]': [''], 'columns[2][search][regex]': ['false'], 
  'columns[3][data]': ['T_NOCT'], 'columns[3][name]': [''], 'columns[3][searchable]': ['true'], 'columns[3][orderable]': ['true'], 'columns[3][search][value]': [''], 'columns[3][search][regex]': ['false'], 
  'columns[4][data]': ['A_c'], 'columns[4][name]': [''], 'columns[4][searchable]': ['true'], 'columns[4][orderable]': ['true'], 'columns[4][search][value]': [''], 'columns[4][search][regex]': ['false'], 
  'columns[5][data]': ['N_s'], 'columns[5][name]': [''], 'columns[5][searchable]': ['true'], 'columns[5][orderable]': ['true'], 'columns[5][search][value]': [''], 'columns[5][search][regex]': ['false'], 
  'columns[6][data]': ['I_sc_ref'], 'columns[6][name]': [''], 'columns[6][searchable]': ['true'], 'columns[6][orderable]': ['true'], 'columns[6][search][value]': [''], 'columns[6][search][regex]': ['false'], 
  'columns[7][data]': ['V_oc_ref'], 'columns[7][name]': [''], 'columns[7][searchable]': ['true'], 'columns[7][orderable]': ['true'], 'columns[7][search][value]': [''], 'columns[7][search][regex]': ['false'], 
  'columns[8][data]': ['I_mp_ref'], 'columns[8][name]': [''], 'columns[8][searchable]': ['true'], 'columns[8][orderable]': ['true'], 'columns[8][search][value]': [''], 'columns[8][search][regex]': ['false'], 
  'columns[9][data]': ['V_mp_ref'], 'columns[9][name]': [''], 'columns[9][searchable]': ['true'], 'columns[9][orderable]': ['true'], 'columns[9][search][value]': [''], 'columns[9][search][regex]': ['false'], 
  'columns[10][data]': ['Technology'], 'columns[10][name]': [''], 'columns[10][searchable]': ['true'], 'columns[10][orderable]': ['true'], 'columns[10][search][value]': [''], 'columns[10][search][regex]': ['false'], 
  'columns[11][data]': ['STC'], 'columns[11][name]': [''], 'columns[11][searchable]': ['true'], 'columns[11][orderable]': ['true'], 'columns[11][search][value]': [''], 'columns[11][search][regex]': ['false'], 
  'order[0][column]': ['0'], 'order[0][dir]': ['asc'], 'order[0][name]': [''], 
  'start': ['0'], 'length': ['10'], 'search[value]': [''], 'search[regex]': ['false']
}
COL_EXPECTED = [
    {'[data]': 'Name', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'},
    {'[data]': 'BIPV', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'},
    {'[data]': 'Date', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'},
    {'[data]': 'T_NOCT', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'},
    {'[data]': 'A_c', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'},
    {'[data]': 'N_s', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'},
    {'[data]': 'I_sc_ref', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'},
    {'[data]': 'V_oc_ref', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'},
    {'[data]': 'I_mp_ref', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'},
    {'[data]': 'V_mp_ref', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'},
    {'[data]': 'Technology', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'},
    {'[data]': 'STC', '[name]': '', '[searchable]': 'true', '[orderable]': 'true', '[search][value]': '', '[search][regex]': 'false'}]
ORDER_EXPECTED = [{'[column]': '0', '[dir]': 'asc', '[name]': ''}]