__all__ = ['N_CLASS', 'dataset_cfg']

N_CLASS={'mitbih_arr'   :6 ,
         'mitbih_id'    :20,
         'mitbih_auth'  :2,
         'mitbih_gender':2 ,
         'keti'         :2 ,
         'motion'       :4 ,
         'pamap2'       :7 ,
         'seizure'      :2 ,
         'wifi'         :7}

motion_cfg  = {'n_channel' : 45 ,
               'n_axis'    : 3  ,
               'input_size': 256}

pamap2_cfg  = {'n_channel' : 9  ,
               'n_axis'    : 3  ,
               'input_size': 256}

mitarr_cfg  = {'n_channel' : 1  ,
               'n_axis'    : 1  ,
               'input_size': 1800}

mitid_cfg   = {'n_channel' : 1  ,
               'n_axis'    : 1  ,
               'input_size': 1024}

seizure_cfg = {'n_channel' : 18 ,
               'n_axis'    : 1  ,
               'input_size': 256}

wifi_cfg    = {'n_channel' : 180 ,
               'n_axis'    : 1  ,
               'input_size': 256}

keti_cfg    = {'n_channel' : 4 ,
               'n_axis'    : 1  ,
               'input_size': 256}


dataset_cfg = {'motion'       : motion_cfg ,
               'pamap2'       : pamap2_cfg ,
               'mitbih_arr'   : mitarr_cfg ,
               'mitbih_id'    : mitid_cfg  ,
               'mitbih_auth'  : mitid_cfg  ,
               'mitbih_gender': mitid_cfg  ,
               'seizure'      : seizure_cfg,
               'wifi'         : wifi_cfg   ,
               'keti'         : keti_cfg   ,}