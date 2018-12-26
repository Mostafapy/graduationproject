import os
import csv
import string
import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.models import load_model

class classifier_model:
    def prepocessing_data(self,file):
        f1=open(file)
        api_sequence=[]
        printable = set(string.printable)
        number=1
        count=0
        count_space=0
        noise=0
        for rows in f1:
         if rows.strip(''):
          if count<23146:
            api_sequence.append(rows.split(','))
            count=count+1
          else:
            api_sequence.append(rows.split(' '))

        while (count_space<len(api_sequence[1075])):
         if '' in api_sequence[1075]:
           api_sequence[1075].remove('')

           count_space=count_space+1


        for i in range (23147,len(api_sequence)):
         for j in range (0,len(api_sequence[i])):
          str1=api_sequence[i][j]
          if str1.startswith('","'):
           api_sequence[i][j]=str1.strip('","')

        binary_list=[None]*len(api_sequence)
        for i in range(0,len(api_sequence)):
         binary_list[i]=[None]*len(api_sequence[i])
         if i<23146:
          for j in range(0,len(api_sequence[i])):
           str1=''.join(filter(lambda x: x in printable, api_sequence[i][j]))
           if j>0:
            if str1.endswith('\n'):
             str2=str1.strip('\n')
             number=int(str2)
             binary_list[i][j]=number
            else:
             number=int(str1)
             binary_list[i][j]=number
           else:
             number=int(str1)
             binary_list[i][j]=number
         else:
             for j in range(0,len(api_sequence[i])):
              str1=''.join(filter(lambda x: x in printable, api_sequence[i][j]))
              if j==0:
               if str1.startswith('"'):
                str1=str1.strip('"')
                if ',' in str1:
                 str3=str1.split(',')[0]
                str4=str1.split(',')[1]
                number=int(str3)
                binary_list[i][j]=number
                number=int(str4)
                binary_list[i][j+1]=number
              else:
               if str1=='\n':
                continue
               else:
                number=int(str1)
                binary_list[i][j+1]=number

        array=np.array(binary_list)
        return array

    def Model_builder(self,array):
        # In[2]:

        len(array)

        # In[3]:

        len(array)
        count = 0
        indexes = []
        for i in range(len(array)):
            if array[i][0] == 0:
                count += 1
                indexes.append(i)

        # # Steps:
        #
        # 1. Get the csv and save it in an array variable, each row in the array represents an instance (malware/nonmalware)
        # 2. Get the non-malwares indexes and store their positions to later access them
        # 3. Create the model by using tensorflow's api, keras
        # 4. Get the training data and store them in X_train/Y_train , get half malwares and half non malwares
        # 5. Train the data
        # 6. Test the data
        # 7. create a way to test a single instance instead of whole set of data
        #

        # In[6]:

        # LSTM for sequence classification
        # fix random seed for reproducibility
        np.random.seed(7)
        # load the dataset but only keep the top n words, zero the rest
        top_words = 5000

        # truncate and pad input sequences
        # max_review_length = 500
        # X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
        # X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)

        # In[7]:

        ## getting all 0 ( non - malware ) indexes and placing them into the temp_array for testing purposes.
        nonMalwares = []
        for i in range(300, len(indexes)):
            nonMalwares.append(array[indexes[i]])

        # In[8]:

        Malwares = array[0:500]

        # In[9]:

        Malwares = sequence.pad_sequences(Malwares, maxlen=500)

        # In[10]:

        nonMalwares = sequence.pad_sequences(nonMalwares, maxlen=500)
        Malwares = sequence.pad_sequences(Malwares, maxlen=500)

        # In[11]:

        X_train = []

        # In[12]:

        X_train.extend(Malwares)

        # In[13]:

        X_train.extend(nonMalwares)

        # In[14]:

        len(X_train)

        # In[15]:

        ## will write stuff here.

        # In[16]:

        Y_train = []
        for i in range(0, 500):
            Y_train.append(array[i][0])

        # In[17]:

        for i in range(300, len(indexes)):
            Y_train.append(array[indexes[i]][0])

        print(np.array(Y_train).shape)

        # In[18]:

        ## fetching random test data x,y
        X_test = []
        Y_test = []

        for i in range(0, 300):
            rand = int(random.random() * 23000)
            X_test.append(array[rand])
            Y_test.append(array[rand][0])

        for i in range(0, 300):
            rand = int(random.randint(0, len(indexes)))
            X_test.append(array[indexes[i]])
            Y_test.append(array[indexes[i]][0])

        # In[19]:

        X_test = sequence.pad_sequences(X_test, maxlen=500)
        for i in range(len(X_test)):
            for j in range(len(X_test[i])):
                if X_test[i][j] > 1 and (X_test[0][0] == 1 or X_test[0][0] == 0):
                    X_test[i][j - 1] = 0
                    break;

        # In[20]:

        len(X_test)

        # In[21]:

        temp_x_train = np.array(X_train)
        Y_train = np.array(Y_train)

        X_train = np.array(X_train)

        for i in range(len(X_train)):
            for j in range(len(X_train[i])):
                if X_train[i][j] > 1 and (X_train[0][0] == 1 or X_train[0][0] == 0):
                    X_train[i][j - 1] = 0
                    break;

        # In[22]:

        embedding_vecor_length = 32
        model = Sequential()
        model.add(Embedding(5000, embedding_vecor_length, input_length=500))
        model.add(LSTM(100))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        print(model.summary())
        # model.fit(X_train, Y_train, epochs=3, batch_size=64)

        # In[23]:

        model.fit(X_train[0:700], Y_train[0:700], epochs=3, batch_size=64)

        # In[23]:

        # In[24]:

        scores = model.evaluate(X_test, Y_test, verbose=0)
        print("Accuracy: %.2f%%" % (scores[1] * 100))

        # In[80]:

        inst = random.randint(23800, 23850);
        j = []
        j.append(array[inst])
        answer = array[inst][0]
        j = sequence.pad_sequences(j, maxlen=500)
        ynew = model.predict_classes(np.expand_dims(j[0], axis=0))
        print('prediction:', ynew[0][0])
        print('answer is :', answer)
        return model

    # ## Wrapping up
    #
    # <p> in the above code i test any random data in the whole dataset, printing the predictions and the original y.</p>
    # You can give it any kind of data to test it, i'll create a function below to take any data for that

    # In[82]:

    def Predict(self,data,model):
        dtemp = []
        dtemp.append(data)
        dtemp = sequence.pad_sequences(dtemp, maxlen=500)
        prediction = model.predict_classes(np.expand_dims(dtemp[0], axis=0))
        return prediction[0][0]  ## the predicted output 0/1

    # saving model
    def SaveModel(file,model):
        model.save(file + '.h5')  ## saving the model in a hdf5 formate, retrieving it would be just model = load_model(file)

    def LoadModel(self,file_model):
        model=load_model(file_model)
        return model
