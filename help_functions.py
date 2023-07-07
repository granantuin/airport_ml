def Hss(cm):
     """
     obtain de Heidke skill score from a 3x3 confusion matrix (margins=on)

     Returns: Heidke skill score
     """
     if cm.shape == (3,3):
          a = cm.values[0,0]
          b = cm.values[1,0]
          c = cm.values[0,1]
          d = cm.values[1,1]
          HSS = round(2*(a*d-b*c)/((a+c)*(c+d)+(a+b)*(b+d)),2)
     else:
          HSS = 0
     return HSS


def get_metar(oaci,control):
     """
     get metar from IOWA university database

     in: OACI airport code
     Returns
      -------
     dataframe with raw metar.
     """
     #today metar control =True
     if control:
       today = pd.to_datetime("today")+timedelta(1)
       yes = today-timedelta(1)
     else:
        today = pd.to_datetime("today")+timedelta(1)
        yes = today-timedelta(2)

     #url string
     s1="https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station="
     s2="&data=all"
     s3="&year1="+yes.strftime("%Y")+"&month1="+yes.strftime("%m")+"&day1="+yes.strftime("%d")
     s4="&year2="+today.strftime("%Y")+"&month2="+today.strftime("%m")+"&day2="+today.strftime("%d")
     s5="&tz=Etc%2FUTC&format=onlycomma&latlon=no&missing=M&trace=T&direct=no&report_type=1&report_type=2"
     url=s1+oaci+s2+s3+s4+s5
     df_metar_global=pd.read_csv(url,parse_dates=["valid"],).rename({"valid":"time"},axis=1)
     df_metar = df_metar_global[["time",'tmpf', 'dwpf','drct', 'sknt', 'alti','vsby',
                                 'gust', 'skyc1', 'skyc2', 'skyl1', 'skyl2','wxcodes',
                                 "metar"]].set_index("time")

     #temperature dry a dew point to celsius
     df_metar["temp_o"] = np.rint((df_metar.tmpf - 32)*5/9)
     df_metar["tempd_o"] = np.rint((df_metar.dwpf - 32)*5/9)

     #QNH to mb
     df_metar["mslp_o"] = np.rint(df_metar.alti*33.8638)

     #visibility SM to meters
     df_metar["visibility_o"] =np.rint(df_metar.vsby/0.00062137)

     #wind direction, intensity and gust
     df_metar["spd_o"] = df_metar["sknt"]
     df_metar["dir_o"] = df_metar["drct"]
     df_metar['gust_o'] = df_metar['gust']

     #Add suffix cloud cover and cloud height, present weather, and metar
     df_metar['skyc1_o'] = df_metar['skyc1']
     df_metar["skyl1_o"] = df_metar["skyl1"]
     df_metar['skyc2_o'] = df_metar['skyc2']
     df_metar["skyl2_o"] = df_metar["skyl2"]
     df_metar["wxcodes_o"] = df_metar["wxcodes"]
     df_metar["metar_o"] = df_metar["metar"]

     # Select all columns that do not start with "_o"
     columns_to_keep = [col for col in df_metar.columns if col.endswith("_o")]
     df_metar = df_metar[columns_to_keep]

     return df_metar

def get_meteogalicia_model_4Km(coorde):
    """
    get meteogalicia model (4Km)from algo coordenates
    Returns
    -------
    dataframe with meteeorological variables forecasted.
    """

    #defining url to get model from Meteogalicia server
    var1 = "var=dir&var=mod&var=wind_gust&var=mslp&var=temp&var=rh&var=visibility&var=lhflx"
    var2 = "&var=lwflx&var=conv_prec&var=prec&var=swflx&var=shflx&var=cape&var=cin&var=cfh&var=T850"
    var3 = "&var=cfl&var=cfm&var=cft&var=HGT500&var=HGT850&var=T500&var=snow_prec&var=snowlevel"
    var = var1+var2+var3
    head1="https://mandeo.meteogalicia.es/thredds/ncss/modelos/WRF_HIST/d03"


    #url12="http://mandeo.meteogalicia.es/thredds/ncss/modelos/WRF_HIST/d02/2016/09/wrf_arw_det_history_d02_20160927_0000.nc4?var=mod&disableLLSubset=on&dis
    try:

      today = pd.to_datetime("today")
      head2 = today.strftime("/%Y/%m/wrf_arw_det_history_d03")
      head3 = today.strftime("_%Y%m%d_0000.nc4?")
      head = head1+head2+head3

      f_day=(today+timedelta(days=2)).strftime("%Y-%m-%d")
      tail="&time_start="+today.strftime("%Y-%m-%d")+"T01%3A00%3A00Z&time_end="+f_day+"T23%3A00%3A00Z&accept=csv"

      dffinal=pd.DataFrame()
      for coor in list(zip(coorde.lat.tolist(),coorde.lon.tolist(),np.arange(0,len(coorde.lat.tolist())).astype(str))):
          dffinal=pd.concat([dffinal,pd.read_csv(head+var+"&latitude="+str(coor[0])+"&longitude="+str(coor[1])+tail,).add_suffix(str(coor[2]))],axis=1)

      #filter all columns with lat lon and date
      dffinal=dffinal.filter(regex='^(?!(lat|lon|date).*?)')

      #remove column string between brakets
      new_col=[c.split("[")[0]+c.split("]")[-1] for c in dffinal.columns]
      for col in zip(dffinal.columns,new_col):
          dffinal=dffinal.rename(columns = {col[0]:col[1]})

      dffinal=dffinal.set_index(pd.date_range(start=today.strftime("%Y-%m-%d"), end=(today+timedelta(days=3)).strftime("%Y-%m-%d"), freq="H")[1:-1])
      control = True

    except:

      today = pd.to_datetime("today")-timedelta(1)
      head2 = today.strftime("/%Y/%m/wrf_arw_det_history_d03")
      head3 = today.strftime("_%Y%m%d_0000.nc4?")
      head = head1+head2+head3

      f_day=(today+timedelta(days=2)).strftime("%Y-%m-%d")
      tail="&time_start="+today.strftime("%Y-%m-%d")+"T01%3A00%3A00Z&time_end="+f_day+"T23%3A00%3A00Z&accept=csv"

      dffinal=pd.DataFrame()
      for coor in list(zip(coorde.lat.tolist(),coorde.lon.tolist(),np.arange(0,len(coorde.lat.tolist())).astype(str))):
          dffinal=pd.concat([dffinal,pd.read_csv(head+var+"&latitude="+str(coor[0])+"&longitude="+str(coor[1])+tail,).add_suffix(str(coor[2]))],axis=1)


      #filter all columns with lat lon and date
      dffinal=dffinal.filter(regex='^(?!(lat|lon|date).*?)')

      #remove column string between brakets
      new_col=[c.split("[")[0]+c.split("]")[-1] for c in dffinal.columns]
      for col in zip(dffinal.columns,new_col):
          dffinal=dffinal.rename(columns = {col[0]:col[1]})

      dffinal=dffinal.set_index(pd.date_range(start=today.strftime("%Y-%m-%d"), end=(today+timedelta(days=3)).strftime("%Y-%m-%d"), freq="H")[1:-1])
      control= False


    return dffinal , control

def get_meteogalicia_model_12Km(coorde):
    """
    get meteogalicia model (12Km)from algo coordenates
    Returns
    -------
    dataframe with meteeorological variables forecasted.
    """
    
    #defining url to get model from Meteogalicia server
    var1 = "var=dir&var=mod&var=wind_gust&var=mslp&var=temp&var=rh&var=visibility&var=lhflx"
    var2 = "&var=lwflx&var=conv_prec&var=prec&var=swflx&var=shflx&var=cape&var=cin&var=cfh&var=T850"
    var3 = "&var=cfl&var=cfm&var=cft&var=HGT500&var=HGT850&var=T500&var=snow_prec&var=snowlevel"
    var = var1+var2+var3 
    head1="https://mandeo.meteogalicia.es/thredds/ncss/modelos/WRF_HIST/d02"
    
    
    #url12="http://mandeo.meteogalicia.es/thredds/ncss/modelos/WRF_HIST/d02/2016/09/wrf_arw_det_history_d02_20160927_0000.nc4?var=mod&disableLLSubset=on&dis
    try:
          
      today = pd.to_datetime("today")    
      head2 = today.strftime("/%Y/%m/wrf_arw_det_history_d02")
      head3 = today.strftime("_%Y%m%d_0000.nc4?")
      head = head1+head2+head3
       
      f_day=(today+timedelta(days=2)).strftime("%Y-%m-%d") 
      tail="&time_start="+today.strftime("%Y-%m-%d")+"T01%3A00%3A00Z&time_end="+f_day+"T23%3A00%3A00Z&accept=csv"
  
      dffinal=pd.DataFrame() 
      for coor in list(zip(coorde.lat.tolist(),coorde.lon.tolist(),np.arange(0,len(coorde.lat.tolist())).astype(str))):
          dffinal=pd.concat([dffinal,pd.read_csv(head+var+"&latitude="+str(coor[0])+"&longitude="+str(coor[1])+tail,).add_suffix(str(coor[2]))],axis=1)    
  
      #filter all columns with lat lon and date
      dffinal=dffinal.filter(regex='^(?!(lat|lon|date).*?)')
  
      #remove column string between brakets
      new_col=[c.split("[")[0]+c.split("]")[-1] for c in dffinal.columns]
      for col in zip(dffinal.columns,new_col):
          dffinal=dffinal.rename(columns = {col[0]:col[1]})
  
      dffinal=dffinal.set_index(pd.date_range(start=today.strftime("%Y-%m-%d"), end=(today+timedelta(days=3)).strftime("%Y-%m-%d"), freq="H")[1:-1])  
      control = True
          
    except:

      today = pd.to_datetime("today")-timedelta(1)
      head2 = today.strftime("/%Y/%m/wrf_arw_det_history_d02")
      head3 = today.strftime("_%Y%m%d_0000.nc4?")
      head = head1+head2+head3
        
      f_day=(today+timedelta(days=2)).strftime("%Y-%m-%d") 
      tail="&time_start="+today.strftime("%Y-%m-%d")+"T01%3A00%3A00Z&time_end="+f_day+"T23%3A00%3A00Z&accept=csv"
  
      dffinal=pd.DataFrame() 
      for coor in list(zip(coorde.lat.tolist(),coorde.lon.tolist(),np.arange(0,len(coorde.lat.tolist())).astype(str))):
          dffinal=pd.concat([dffinal,pd.read_csv(head+var+"&latitude="+str(coor[0])+"&longitude="+str(coor[1])+tail,).add_suffix(str(coor[2]))],axis=1)    
  
      
      #filter all columns with lat lon and date
      dffinal=dffinal.filter(regex='^(?!(lat|lon|date).*?)')
  
      #remove column string between brakets
      new_col=[c.split("[")[0]+c.split("]")[-1] for c in dffinal.columns]
      for col in zip(dffinal.columns,new_col):
          dffinal=dffinal.rename(columns = {col[0]:col[1]})
  
      dffinal=dffinal.set_index(pd.date_range(start=today.strftime("%Y-%m-%d"), end=(today+timedelta(days=3)).strftime("%Y-%m-%d"), freq="H")[1:-1])  
      control= False  

     
    return dffinal , control

def get_meteogalicia_model_1Km(coorde):
    """
    get meteogalicia model (1Km)from algo coordenates
    Returns
    -------
    dataframe with meteeorological variables forecasted.
    """
    
    #defining url to get model from Meteogalicia server
    var1 = "var=dir&var=mod&var=wind_gust&var=mslp&var=temp&var=rh&var=visibility&var=lhflx"
    var2 = "&var=lwflx&var=conv_prec&var=prec&var=swflx&var=shflx&var=cape&var=cin&var=cfh&var=T850"
    var3 = "&var=cfl&var=cfm&var=cft&var=HGT500&var=HGT850&var=T500&var=snow_prec&var=snowlevel"
    var = var1+var2+var3 
    head1 = "https://mandeo.meteogalicia.es/thredds/ncss/wrf_1km_baixas/fmrc/files/" 

    try:
          
      today = pd.to_datetime("today")    
      head2 = today.strftime("/%Y%m%d/wrf_arw_det1km_history_d05")
      head3 = today.strftime("_%Y%m%d_0000.nc4?")
      head = head1+head2+head3
       
      f_day=(today+timedelta(days=2)).strftime("%Y-%m-%d") 
      tail="&time_start="+today.strftime("%Y-%m-%d")+"T01%3A00%3A00Z&time_end="+f_day+"T23%3A00%3A00Z&accept=csv"
  
      dffinal=pd.DataFrame() 
      for coor in list(zip(coorde.lat.tolist(),coorde.lon.tolist(),np.arange(0,len(coorde.lat.tolist())).astype(str))):
          dffinal=pd.concat([dffinal,pd.read_csv(head+var+"&latitude="+str(coor[0])+"&longitude="+str(coor[1])+tail,).add_suffix(str(coor[2]))],axis=1)    
  
      #filter all columns with lat lon and date
      dffinal=dffinal.filter(regex='^(?!(lat|lon|date).*?)')
  
      #remove column string between brakets
      new_col=[c.split("[")[0]+c.split("]")[-1] for c in dffinal.columns]
      for col in zip(dffinal.columns,new_col):
          dffinal=dffinal.rename(columns = {col[0]:col[1]})
  
      dffinal=dffinal.set_index(pd.date_range(start=today.strftime("%Y-%m-%d"), end=(today+timedelta(days=3)).strftime("%Y-%m-%d"), freq="H")[1:-1])  
      control = True
          
    except:

      today = pd.to_datetime("today")-timedelta(1)
      head2 = today.strftime("/%Y%m%d/wrf_arw_det1km_history_d05")
      head3 = today.strftime("_%Y%m%d_0000.nc4?")
      head = head1+head2+head3
        
      f_day=(today+timedelta(days=2)).strftime("%Y-%m-%d") 
      tail="&time_start="+today.strftime("%Y-%m-%d")+"T01%3A00%3A00Z&time_end="+f_day+"T23%3A00%3A00Z&accept=csv"
  
      dffinal=pd.DataFrame() 
      for coor in list(zip(coorde.lat.tolist(),coorde.lon.tolist(),np.arange(0,len(coorde.lat.tolist())).astype(str))):
          dffinal=pd.concat([dffinal,pd.read_csv(head+var+"&latitude="+str(coor[0])+"&longitude="+str(coor[1])+tail,).add_suffix(str(coor[2]))],axis=1)    
  
      
      #filter all columns with lat lon and date
      dffinal=dffinal.filter(regex='^(?!(lat|lon|date).*?)')
  
      #remove column string between brakets
      new_col=[c.split("[")[0]+c.split("]")[-1] for c in dffinal.columns]
      for col in zip(dffinal.columns,new_col):
          dffinal=dffinal.rename(columns = {col[0]:col[1]})
  
      dffinal=dffinal.set_index(pd.date_range(start=today.strftime("%Y-%m-%d"), end=(today+timedelta(days=3)).strftime("%Y-%m-%d"), freq="H")[1:-1])  
      control= False  

     
    return dffinal , control
