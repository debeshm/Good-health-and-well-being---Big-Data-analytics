#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tensorflow as tf
import pandas as pd
import numpy as np
from scipy.stats import t


# In[2]:


df = pd.read_csv("hepatitisA_count_matrix.csv")
dfy = pd.read_csv("influenza_y.csv")


# In[3]:


df.columns


# In[4]:


df.values


# In[5]:


df = df.replace(0, 0.1)

df = df.drop('state', axis=1)
df = df.drop('week', axis=1)


# In[6]:


df


# In[7]:


y_val = dfy['y'] / 100
y_val


# In[8]:


X_val = df.values
X_val = (X_val - np.mean(X_val, axis=0)) / np.std(X_val, axis=0)

y_val = np.expand_dims(y_val, axis=1) 


# In[9]:


n_features = X_val.shape[1]


# In[10]:


y_val


# In[11]:


X_in = tf.placeholder(tf.float32, [None, n_features], "X_in")
w = tf.Variable(tf.random_normal([n_features, 1]), name="w")
b = tf.Variable(tf.constant(0.1, shape=[]), name="b")
h = tf.add(tf.matmul(X_in, w), b)


# In[12]:


y_in = tf.placeholder(tf.float32, [None, 1], "y_in")
loss_op = tf.reduce_mean(tf.square(tf.subtract(y_in, h)),
                         name="loss")
train_op = tf.train.GradientDescentOptimizer(0.3).minimize(loss_op)


# In[13]:


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
#     hh = sess.run(h , feed_dict={
#             X_in: X_val})
    for batch in range(100):
        sess.run(train_op, feed_dict={
            X_in: X_val,
            y_in: y_val
        })
    w_computed = sess.run(w)
    b_computed = sess.run(b)


# In[14]:


w_computed


# In[15]:


b_computed


# In[16]:


X_in = tf.placeholder(tf.float32, [None, n_features], "X_in")
w_f = tf.constant(w_computed, shape = w_computed.shape)
b_f = tf.constant(b_computed,  shape = b_computed.shape)
op_preds = tf.add(tf.matmul(X_in, w_f), b_f)
errors = tf.subtract(op_preds, y_in)
RSS = tf.tensordot(tf.transpose(errors), errors, 1)


# In[17]:


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    rss = sess.run(RSS , feed_dict={
        X_in: X_val,
        y_in : y_val})
#     sess.run(rss)
    


# In[18]:


w_computed


# In[19]:


rss


# In[20]:


df = len(X_val) - n_features


# In[21]:


s_sq = rss / df


# In[22]:


for i in range(n_features) :
    cc = X_val[:, i]
    temp = (cc - np.mean(cc, axis=0))
    den = np.dot(temp.T, temp)
    t_for_i = w_computed[i] / (np.sqrt(s_sq / den))
#     print(t_for_word_freqc)
    p = t.sf(t_for_i, df)
    print(p)


# In[ ]:




