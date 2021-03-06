# chinese-nlp
提取关键词、提取摘要、词云、句子相似度计算、文本相似度计算；图片相似度计算。

## 句子相似度计算
测试环境：Mac 10.13.6，6核，16G内存，i7处理器

|算法|数据量|运行时间|准确度|
|----|----|----|----|
|cilin|102372|13000s|18.41%|
|hownet|10000|2165s|24.57%|
|Simhash|102372|167s|18.89%|
|Minhash|102372|262s|76.05%|
|VSM|102372|161s|49.14%|
|word2vector|102372|176s|89.16%|

针对项目特点选择适用的算法。如果项目对正样本检测的容忍度低，需要尽可能多的将正样本识别出来，则选择word2vector算法，反之，则选择minhash算法。

从运算时间的角度，minhash不需要训练模型，总体运行时间较短，word2vector需要训练模型，训练时间较长。

从识别准确度的角度，由于样本不均衡，上面得到的准确率并不准确。无监督算法对句子相似度计算始终受限，未来考虑使用有监督算法提高准确度。

## 文本相似度计算
### MinHash
MinHash原理

https://www.jianshu.com/p/535c537a5766
https://zhuanlan.zhihu.com/p/82162303
#### 算法步骤
集合A、B是docA、docB的one-hot词向量。
1. 使用一组随机的hash函数h(x)对集合A和B中的每个元素进行hash
2. hmin(A)、hmin(B)分别表示分别hash后集合A和集合B的最小值的向量。
3. jarcarrd距离来衡量相似度。

### Doc2Vec
Doc2vec段落向量方法是一种非监督算法，能从变长的文本（例如：句子，段落和文档）中学习得到固定长度的特征表示。该算法训练在文档内预测词，使其能够使用单个密集向量表示每个文档。它是受到词向量学习的启发，段落向量能根据从段落中给定的上下文样本去预测下一个词，两种方法：分布记忆的段落向量（Distributed Memory Model of Paragraph Vectors,，PV-DM）和分布词袋版本的段落向量（Distributed Bag of Words version of Paragraph Vector，PV-DBOW）。

模型中，上下文长度是固定的，并且是在段落上的滑动窗口上取到的样本。段落向量是被分享于所有由同一段落生成的上下文，而不是所有段落都实现共享。而词向量矩阵W，是跨段落分享的，例如：关于’强大的’的词向量在所有段落中都是一样的。段落向量和词向量都用随机梯度下降进行训练，梯度由反向传播获取。在预测期间，模型需要实现一个推理步骤，给新段落计算段落向量。这个也是由梯度下降得到的，在这个过程中，模型的其它部分，词向量W和softmax权重都是固定住的。

假设词库中有N个段落，M个词。我们想要学习段落向量使得每个段落向量被映射到p维，每个词被映射到q维，然后模型总共就有N x p +M x q个参数（除了softmax的参数）。即使当N很大时，模型的参数也会很大，但是在训练时的更新是稀疏的，因此模型有效率。训练完之后，段落向量可用于表示段落的特征，我们可以将这些特征直接用在传统的机器学习方法里，例如逻辑回归，支持向量机或K-means。

段落向量的好处在于它克服了词袋模型的劣势，首先，特征向量能够继承到词的语义信息，例如”powerful”比“Paris”更接近“strong”。第二个好处是：至少在小的上下文基础上，它们跟n-gram模型一样考虑了词顺序。这点很重要，因为n-gram模型保留了段落很多信息，包括词顺序。但因为高维表示会倾向于低的通用性，因此这段落向量可能会比n-grams模型好。

另外一种段落向量是PV-DBOW，它与PV-DM相反。它忽略输入的上下文词，但强迫模型去预测从段落上随机样本出的词。实际上，这意味着在每次随机梯度下降循环里，我们样本出一个文本窗，然后从文本窗中样本出一个随机的词，之后在给定段落向量下去完成一个分类任务。

除了概念简单外，此模型不需要储存过多的数据，只需要储存softmax权重，而不需要像PV-DM模型一样存softmax权重和词向量。这个模型类似于word2vec中的skip-gram模型。

### 文本相似度计算小结
对于海量文本的相似度计算，根据项目特点，选择MinHash算法；
对于某一特定文本，计算其与黑明单文本库中文本的相似度，选择doc2vec算法。该算法需要首先训练模型，时间较长，在实际计算文本相似度时，每一个文本计算时间在毫秒级，速度较快。可以定期（每月或每季度）更新迭代算法模型，提升其计算准确度。

#### 同文本识别
对于相同文本，通过MD5或SHA1获取其hash值，hash值若相等，则是同文本。

## 图片相似度计算
### 感知哈希算法（Perceptual hash algorithm）

那这种技术的原理是什么呢？根据Neal Krawetz博士的解释，原理非常简单易懂。我们可以用一个快速算法，就达到基本的效果。这里的关键技术叫做感知哈希算法（Perceptual hash algorithm），它的作用是对每张图片生成一个"指纹"（fingerprint）字符串，然后比较不同图片的指纹。结果越接近，就说明图片越相似。下面是一个最简单的实现：
* 第一步，缩小尺寸。将图片缩小到8x8的尺寸，总共64个像素。这一步的作用是去除图片的细节，只保留结构、明暗等基本信息，摒弃不同尺寸、比例带来的图片差异。
* 第二步，简化色彩。将缩小后的图片，转为64级灰度。也就是说，所有像素点总共只有64种颜色。
* 第三步，计算平均值。计算所有64个像素的灰度平均值。
* 第四步，比较像素的灰度。将每个像素的灰度，与平均值进行比较。大于或等于平均值，记为1；小于平均值，记为0。
* 第五步，计算哈希值。将上一步的比较结果，组合在一起，就构成了一个64位的整数，这就是这张图片的指纹。组合的次序并不重要，只要保证所有图片都采用同样次序就行了。

1. aHash：平均值哈希。速度比较快，但是常常不太精确。
1. pHash：感知哈希。精确度比较高，但是速度方面较差一些。
1. dHash：差异值哈希。Amazing！精确度较高，且速度也非常快。

### 直方图算法

直方图算法是对源图像与要筛选的图像进行直方图数据采集，对采集的各自图像直方图进行归一化再使用巴氏系数算法对直方图数据进行计算，最终得出图像相似度值，其值范围在[0, 1]之间0表示极其不同，1表示极其相似（相同）。

1. 缩小尺寸：
一般将图片缩放为 8 * 8 的尺寸大小，共64个像素的图片。但是由于64个像素对于我来说，损失的细节太多所以我选择了缩放到 32 * 32 的尺寸大小
2. 降低位深：
原来 RGB 每个颜色都有 256 种变化，现在做一个映射，将原来的 256 分为 8(3个比特表示) 个颜色区间。类似旧的 0 - 31 对应新的颜色 0，以达到降低计算的效果
3. 计算像素值：
由于降低了位深，图片颜色值变小。每个颜色值不大于8（0 - 7），然后我们给三元素不同的权重，分别为 8 * 8，8，1 作为数组的 key，用以统计每个颜色的像素出现次数，并且不会出现不同颜色统计到了同一个 key 值下的目的。
4. 计算相似度：
计算出像素值后得到，我们得到了以不同颜色的数值为 key，出现次数为 value 的数组。这时候我们可以使用用余弦相似度去计算相同颜色出现次数的相似度，越是相似的像素最后值越接近于1。
