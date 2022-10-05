import numpy as np, os
from collections import Counter
from warnings import filterwarnings
filterwarnings('ignore')  # 不打印警告

from tensorflow.keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Conv1D, MaxPool1D, GlobalMaxPool1D, Dense,Flatten

corpus_path = '唐诗三百首.txt'
len_chr = 1000  # 字库大小
window = 24  # 滑窗大小
filters = 20  # 卷积录波器数量
kernel_size = 5  # 卷积核大小
times = 4 # 训练总次数
batch_size = 250
epochs = 2
window = 24  # 滑窗大小(一句诗词5个字，加一个标点共6个字符。一首诗4句。共24个字符
filepath = 'model.hdf5'

#读取古诗文件
with open(corpus_path, encoding='utf-8') as f:
    seq_chr = f.read().replace('\n', '')

len_seq = len(seq_chr)  # 语料长度372864
chr_ls = Counter(list(seq_chr)).most_common(len_chr)#按照词频统计字，从高频到低频 生成类似('，', 31072), ('。', 31072), ('不', 3779), ('人', 3377),
chr_ls = [i[0] for i in chr_ls]#将字按频数写成列表 类似['，', '。', '不', '人', '山', '日', '云', '风', '无', '一', '月', '何', '有
chr2id = {c: i for i, c in enumerate(chr_ls)}#{字：频数 }字典
id2chr = {i: c for c, i in chr2id.items()}#{频数：字 }字典
seq_id = [chr2id[c] for c in seq_chr]  # 文字序列 --> 索引序列 #找到chr2id里的每个字在原文的索引位置.
c2i = lambda c: chr2id.get(c, np.random.randint(len_chr))#字典取值，有取c,没有随便从1000（len_chr）个取一个字




#输入输出处理
reshape = lambda x: np.reshape(x, (-1, window, 1)) / len_chr#1维卷积输入格式(-1,size,1)
x = [seq_id[i: i + window] for i in range(len_seq - window)]
x = reshape(x)#(372840, 24, 1)
y = [seq_id[i + window] for i in range(len_seq - window)]
y = to_categorical(y, num_classes=len_chr)#(372840, 1000) 一个文字一个种类



def CNNmodel():
    model = Sequential()
    model.add(Conv1D(filters, kernel_size * 2, padding='same', activation='relu'))
    model.add(MaxPool1D())
    model.add(Conv1D(filters * 2, kernel_size, padding='same', activation='relu'))
    model.add(Flatten())
    model.add(Dense(len_chr, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy',metrics=['accuracy'])
    return model
"""
model=CNNmodel()
model.fit(x,y)
model.save(filepath)

"""
#模型加载
model = load_model(filepath)
#随机采样
def draw_sample(predictions, temperature):
    pred = predictions.astype('float64')  # 提高精度防报错
    pred = np.log(pred) / temperature
    pred = np.exp(pred)
    pred = pred / np.sum(pred)
    pred = np.random.multinomial(1, pred, 1)
    return np.argmax(pred)

def predict(t, pred):
    if t:
        print('随机采样，温度：%.1f' % t)
        sample = draw_sample#调用随机采样函数
    else:
        print('贪婪采样')
        sample = np.argmax
    for _ in range(window):#循环24次，进行预测,打印24个字形成一首诗
        x_pred = reshape(pred[-window:])#-window:每次取最后24个字作为输入，并变换为一维卷积神经网络输入格式reshape
        y_pred = model.predict(x_pred)[0]#y_pred为[[]]2维数组(1, 1000)，[0]表示变换格式为[](1000,)
        i = sample(y_pred, t)#随机采样
        pred.append(i)
    text = ''.join([id2chr[i] for i in pred[-window:]])#将输出添加进字符串
    print('\033[033m%s\033[0m' % text)


if __name__ == '__main__':
    while True:#无限循环
        title = input('输入标题').strip() + '。'
        len_t = len(title)
        randint = np.random.randint(len_seq - window + len_t)#数据库字的总长度-要输出的文字window长度+标题长度,从这里面取数
        randint = int(randint // 12 * 12)
        pred = seq_id[randint: randint + window - len_t] + [c2i(c) for c in title]#随机取一些字+输入标题字组成24个字作为输入

        for t in (None, 1, 2,3):
            predict(t, pred)

