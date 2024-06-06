import pandas as pd
import numpy as np

def read_IN8scan(Nscan, folder):
    '''
    Function to read IN8 scan files.
    Input:
        Nscan: scan number
        folder: folder where the scan is located

    Output:
        data: dictionary with the following keys:
            date: date of the scan
            time: time of the scan
            QM: Q modulus value
            E: energy value
            steps: number of steps
            command: command used to run the scan
            param: dictionary with the parameters used in the scan
            variab: dictionary with the variables used in the scan
            zeros: dictionary with the zeros used in the scan
            data: pandas dataframe with the data of the scan

    '''
    Nscan = str(Nscan)
    meas = {}
    meas['param'] = {}
    meas["variab"] = {}
    meas['zeros'] = {}

    with open(folder+Nscan) as f:
        lines = f.readlines()
        meas['date'] = lines[5].split()[2]
        meas['time'] = lines[5].split()[3]

        for line in lines:
            if "COMND:" in line:
                meas["command"] = line[7:]

            if "POSQE:" in line:
                l = line[6:].split(',')
                #meas['QH'] = float(l[0].split('=')[1])
                #meas['QK'] = float(l[1].split('=')[1])
                #meas['QL'] = float(l[2].split('=')[1])
                meas["QM"] =  (float(l[0].split('=')[1])**2 + float(l[1].split('=')[1])**2 + float(l[2].split('=')[1])**2)**0.5
                meas['E'] = float(l[3].split('=')[1])

            if "STEPS:" in line:
                meas["steps"] = line[7:-1]
            
            if "PARAM:" in line:
                el = line[6:].split(',')
                for i in el:
                    meas['param'][i.split('=')[0].strip()] = float(i.split('=')[1])
            

            if "VARIA:" in line:
                el = line[6:].split(',')
                for i in el:
                    meas['variab'][i.split('=')[0].strip()] = float(i.split('=')[1])
            if "ZEROS:" in line:
                el = line[6:].split(',')
                for i in el:
                    meas['zeros'][i.split('=')[0].strip()+"_zero"] = float(i.split('=')[1])
        
        skiprows = lines.index('DATA_:\n') + 1 
        
    meas['data'] = pd.read_csv(folder+Nscan, skiprows=skiprows, sep='\s+', index_col=0)
    try:
        meas['data']['dCNTS'] = np.sqrt(meas['data']['CNTS'])
    except:
        pass

    return meas

def gen_data_df(datasheet, folder):
    if type(datasheet) == str:
        datasheet = pd.read_csv(datasheet, index_col=0, comment='#', sep='\t')
    if type(datasheet) == pd.core.frame.DataFrame:
        datasheet = datasheet    

    data = []
    for i in datasheet.index:
        try:
            meas = read_IN8scan(i, folder)
            meas['Nscan'] = i
            meas['name'] = datasheet.loc[i]['name']
            meas['notes'] = datasheet.loc[i]['notes']
            data.append(meas)
        except:
            print ("Scan {} not found".format(i))
        
    data = pd.DataFrame(data)
    data.set_index('Nscan', inplace=True)
    data = data[['name', 'notes',  'date', 'time', 'QM', 'E', 'steps', 'command', 'param', 'variab', 'zeros', 'data']]

    return data




#####################################################################################################################

def read_IN8scan_specJun24(Nscan, folder):

    Nscan = str(Nscan)
    meas = {}
    meas['param'] = {}
    meas["variab"] = {}
    meas['zeros'] = {}

    with open(folder+Nscan) as f:
        lines = f.readlines()
        meas['date'] = lines[5][18:].split()[0]
        meas['time'] = lines[5][18:].split()[1]

        for line in lines:
            if "COMND:" in line:
                meas["command"] = line[7:]

            if "POSQE:" in line:
                l = line[6:].split(',')
                meas["QM"] =  (float(l[0].split('=')[1])**2 + float(l[1].split('=')[1])**2 + float(l[2].split('=')[1])**2)**0.5
                meas['E'] = float(l[3].split('=')[1])

            if "STEPS:" in line:
                meas["steps"] = line[7:-1]
            
            if "PARAM:" in line:
                el = line[6:].split(',')
                for i in el:
                    if i.split('=')[0].strip() not in ('Plexi1', 'Plexi2'):
                            meas['param'][i.split('=')[0].strip()] = float(i.split('=')[1])

            if "VARIA:" in line:
                el = line[6:].split(',')
                for i in el:
                    meas['variab'][i.split('=')[0].strip()] = float(i.split('=')[1])
            if "ZEROS:" in line:
                el = line[6:].split(',')
                for i in el:
                    meas['zeros'][i.split('=')[0].strip()+"_zero"] = float(i.split('=')[1])
        
        skiprows = lines.index('DATA_:\n') + 1 
        
    meas['data'] = pd.read_csv(folder+Nscan, skiprows=skiprows, sep='\s+', index_col=0)
    try:
        meas['data']['dCNTS'] = np.sqrt(meas['data']['CNTS'])
    except:
        pass

    return meas



def sum_meas(data, A, B):
        temp = data.loc[A].data.copy()
        temp.CNTS += data.loc[B].data.CNTS
        temp.dCNTS = np.sqrt(temp.CNTS)
        temp.M1 += data.loc[B].data.M1
        temp.M2 += data.loc[B].data.M2
        temp.TIME += data.loc[B].data.TIME
        temp.TT = np.NaN
        temp.TRT = np.NaN

        out =  {'QM': data.loc[A].QM,
                'steps': data.loc[A].steps,
                'data': temp,
                }
        return out

def gen_data_df_specJun24(datasheet, folder):
    if type(datasheet) == str:
        datasheet = pd.read_csv(datasheet, index_col=0, comment='#', sep='\t')
    if type(datasheet) == pd.core.frame.DataFrame:
        datasheet = datasheet    

    data = []
    for i in datasheet.index:
        try:
            meas = read_IN8scan_specJun24('0'+str(i), folder)
            meas['Nscan'] = i
            meas['name'] = datasheet.loc[i]['name']
            meas['notes'] = datasheet.loc[i]['notes']
            data.append(meas)
        except:
            print ("Scan {} not found".format(i))
        
    data = pd.DataFrame(data)
    data.set_index('Nscan', inplace=True)
    data = data[['name', 'notes',  'date', 'time', 'QM', 'E', 'steps', 'command', 'param', 'variab', 'zeros', 'data']]

#################################################################################################################################################################

#### SUM the empty cell sampled at 1 deg step with the second part (three points)
    data.loc['050321+050322'] =    {'name': np.nan,
                                    'QM': data.loc[50321].QM,
                                    'E': data.loc[50321].E,
                                    'steps': data.loc[50321].steps,
                                    'command': data.loc[50321].command,
                                    'data': pd.concat([data.loc[50321].data, data.loc[50322].data], axis=0).reset_index(drop=True),
                                    }
    data.loc['050321+050322'].data.index +=1
    data.loc['050321+050322'].data.index.name = 'PNT'


#### SUM the S(Q) of glycerol 300K sampled at different theta
    A = data.loc[50325].data.copy()
    B = data.loc[50327].data.copy()
    A.index = 2*A.index -1
    B.index = 2*B.index
    data.loc['050325+050327'] =    {'data': pd.concat([A,B], axis=0).sort_index()}
    data.loc['050325+050327+050328'] = sum_meas(data, '050325+050327', 50328)

#### SUM the empty cells at different temperatures

    data.loc['050312+050316'] = sum_meas(data, 50312, 50316)
    data.loc['050313+050317'] = sum_meas(data, 50313, 50317)
    data.loc['050314+050318'] = sum_meas(data, 50314, 50318)
    data.loc['050315+050319'] = sum_meas(data, 50315, 50319)
    data.loc['050331+050332'] = sum_meas(data, 50331, 50332)


    return data




