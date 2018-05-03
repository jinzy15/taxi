
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

plate = pd.read_csv('plate2.csv')
order = pd.read_csv('order.csv')
speed = pd.read_csv('speed_online_time.csv')


# In[3]:


import datetime
speed['plate'] = np.array(plate)
timehour = []
for day,hour in zip(speed['timeR_1'],speed['timeR_2']):
    if(day<31):
        timehour.append(datetime.datetime(2018,4,day,hour))
    else:
        timehour.append(datetime.datetime(2018,3,day,hour))


# In[4]:


speed['timehour'] = timehour
speed = speed.drop_duplicates()

# In[5]:


df = pd.DataFrame()


# In[6]:


for plate_name,car in speed.groupby(speed.plate):
    col_timestamp = []
    col_frame = []
    for timestamp, frame in car.groupby(car.timehour):
        col_timestamp.append(timestamp)
        col_frame.append(len(frame)*10/3600)
    out = pd.Series(col_frame ,index = col_timestamp)
    df[plate_name] = out



# In[7]:


df = df.fillna(0)



# In[8]:


df = df.stack()


# In[9]:


ans = pd.DataFrame()
online_frame = df
ans['online_frame'] = online_frame


# In[10]:


ans['value'] = pd.Series(np.zeros(len(online_frame)),index = online_frame.index)
ans['driver_id'] = pd.Series(-np.ones(len(online_frame)),index = online_frame.index)


# In[11]:


# In[12]:


def to_hour(in_time):
    time = datetime.datetime.strptime(in_time, "%m-%d %H:%M:%S")
    return time.strftime("%m-%d %H")


# In[13]:


# In[19]:


for item in range(len(order)):
    if(type(order.iloc[item]['request_time'])!=str):
        print(item)
        print(order.iloc[item]['request_time'])


# In[14]:


for item in range(len(order)):
    if(type(order.iloc[item]['pickup_time'])==str):
        time = '2018-'+to_hour(order.iloc[item]['pickup_time'])+':00:00'
        driver_id = order.iloc[item]['driver_id']
        price = order.iloc[item]['price']
        plate = order.iloc[item]['plate']
        try:
            ans.value[time][plate] += price
            ans.driver_id[time][plate] = driver_id
        except:
            print(time,plate)
            pass

ans.to_csv('mydataset.csv')
# In[2]:


import pandas as pd
ans = pd.read_csv('mydataset.csv')

# In[3]:


ans.columns= ['time', 'plate', 'online_frame', 'value', 'driver_id']
ans = ans.drop('plate',1)


# In[10]:


import numpy as np
ans = ans[ans['driver_id']!=-1]
ans.index = np.arange(len(ans))
ans['month'] = pd.Series(list(map(lambda time:datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S').month,ans.time)))
ans['day'] = pd.Series(list(map(lambda time:datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S').day,ans.time)))
ans['hour'] = pd.Series(list(map(lambda time:datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S').hour,ans.time)))




ans= ans.drop('time',1)



ans.to_csv('result.csv')

