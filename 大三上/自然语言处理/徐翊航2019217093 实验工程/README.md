# Song-poem
这是一个基于自然语言的宋词生成系统

# 详细介绍
## 写在前面
- **这个是作者在大二时期上自然语言课程时写的一个基于GUI交互的宋词自动生成系统，外加一个中文分词系统**

- 实验一与实验二是读取文本词库进行学习
- 实验三为宋词自动生成系统
- 实验四为中文分词系统

## 引用的算法
- FMM算法
- HMM算法

## 效果
### 宋词生成系统
[![宋词设计.jpeg](https://i.loli.net/2018/03/02/5a996f579f84e.jpeg)](https://i.loli.net/2018/03/02/5a996f579f84e.jpeg)
[![宋词生成.jpeg](https://i.loli.net/2018/03/02/5a996f57b3996.jpeg)](https://i.loli.net/2018/03/02/5a996f57b3996.jpeg)

### 中文分词系统
[![中文分词设计.jpeg](https://i.loli.net/2018/03/02/5a996f5761727.jpeg)](https://i.loli.net/2018/03/02/5a996f5761727.jpeg)
[![中文分词系统.jpeg](https://i.loli.net/2018/03/02/5a996f561df71.jpeg)](https://i.loli.net/2018/03/02/5a996f561df71.jpeg)

# 下载并运行
git clone https://github.com/AndyQianq/Song-poem

下载后，用eclipse打开
修改文件的路径

点击运行即可

# 存在的问题：
## 问题1:
- 词库太小，有一些词找不到，会导致分词自动结束，如下：
- 测试选自《圣经》中的“我们经过的日子都在你的震怒之下，我们度尽的年岁好像一声叹息”

## 问题二：
没有办法解决有歧义的句子的分词
例如：“北京人多”可以解释为“北京”+“人多”也可以解释为“北京人”+“多”，演示之后发现为“北京/人/多”


