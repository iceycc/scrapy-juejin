.markdown-body{word-break:break-word;line-height:1.75;font-weight:400;font-size:15px;overflow-x:hidden;color:#333}.markdown-body h1,.markdown-body h2,.markdown-body h3,.markdown-body h4,.markdown-body h5,.markdown-body h6{line-height:1.5;margin-top:35px;margin-bottom:10px;padding-bottom:5px}.markdown-body h1{font-size:30px;margin-bottom:5px}.markdown-body h2{padding-bottom:12px;font-size:24px;border-bottom:1px solid #ececec}.markdown-body h3{font-size:18px;padding-bottom:0}.markdown-body h4{font-size:16px}.markdown-body h5{font-size:15px}.markdown-body h6{margin-top:5px}.markdown-body p{line-height:inherit;margin-top:22px;margin-bottom:22px}.markdown-body img{max-width:100%}.markdown-body hr{border:none;border-top:1px solid #ddd;margin-top:32px;margin-bottom:32px}.markdown-body code{word-break:break-word;border-radius:2px;overflow-x:auto;background-color:#fff5f5;color:#ff502c;font-size:.87em;padding:.065em .4em}.markdown-body code,.markdown-body pre{font-family:Menlo,Monaco,Consolas,Courier New,monospace}.markdown-body pre{overflow:auto;position:relative;line-height:1.75}.markdown-body pre>code{font-size:12px;padding:15px 12px;margin:0;word-break:normal;display:block;overflow-x:auto;color:#333;background:#f8f8f8}.markdown-body a{text-decoration:none;color:#0269c8;border-bottom:1px solid #d1e9ff}.markdown-body a:active,.markdown-body a:hover{color:#275b8c}.markdown-body table{display:inline-block!important;font-size:12px;width:auto;max-width:100%;overflow:auto;border:1px solid #f6f6f6}.markdown-body thead{background:#f6f6f6;color:#000;text-align:left}.markdown-body tr:nth-child(2n){background-color:#fcfcfc}.markdown-body td,.markdown-body th{padding:12px 7px;line-height:24px}.markdown-body td{min-width:120px}.markdown-body blockquote{color:#666;padding:1px 23px;margin:22px 0;border-left:4px solid #cbcbcb;background-color:#f8f8f8}.markdown-body blockquote:after{display:block;content:""}.markdown-body blockquote>p{margin:10px 0}.markdown-body ol,.markdown-body ul{padding-left:28px}.markdown-body ol li,.markdown-body ul li{margin-bottom:0;list-style:inherit}.markdown-body ol li .task-list-item,.markdown-body ul li .task-list-item{list-style:none}.markdown-body ol li .task-list-item ol,.markdown-body ol li .task-list-item ul,.markdown-body ul li .task-list-item ol,.markdown-body ul li .task-list-item ul{margin-top:0}.markdown-body ol ol,.markdown-body ol ul,.markdown-body ul ol,.markdown-body ul ul{margin-top:3px}.markdown-body ol li{padding-left:6px}@media (max-width:720px){.markdown-body h1{font-size:24px}.markdown-body h2{font-size:20px}.markdown-body h3{font-size:18px}}

FFCreator是我们团队做的一个轻量、灵活的短视频加工库。您只需要添加几张图片或文字，就可以快速生成一个类似抖音的酷炫短视频。github地址：github.com/tnfe/FFCrea… 欢迎小伙伴star。

背景
好久没写文章了，沉寂了大半年
持续性萎靡不振，间歇性癫痫发作
天天来大姨爹，在迷茫、焦虑中度过每一天
不得不承认，其实自己就是个废物
作为一名低级前端工程师
最近处理了一个十几年的祖传老接口
它继承了一切至尊级复杂度逻辑
传说中调用一次就能让cpu负载飙升90%的日天服务
专治各种不服与老年痴呆
我们欣赏一下这个接口的耗时

平均调用时间在3s以上
导致页面出现严重的转菊花
经过各种深度剖析与专业人士答疑
最后得出结论是：放弃医疗
鲁迅在《狂人日记》里曾说过：“能打败我的，只有女人和酒精，而不是bug”
每当身处黑暗之时
这句话总能让我看到光
所以这次要硬起来
我决定做一个node代理层
用下面三个方法进行优化：


按需加载 -> graphQL


数据缓存 -> redis


轮询更新 -> schedule


代码地址：github
按需加载 -> graphQL
天秀老接口存在一个问题，我们每次请求1000条数据，返回的数组中，每一条数据都有上百个字段，其实我们前端只用到其中的10个字段而已。
如何从一百多个字段中，抽取任意n个字段，这就用到graphQL。
graphQL按需加载数据只需要三步：

定义数据池 root
描述数据池中数据结构 schema
自定义查询数据 query

定义数据池
我们针对屌丝追求女神的场景，定义一个数据池，如下：
// 数据池
var root = {
    girls: [{
        id: 1,
        name: '女神一',
        iphone: 12345678910,
        weixin: 'xixixixi',
        height: 175,
        school: '剑桥大学',
        wheel: [{ name: '备胎1号', money: '24万元' }, { name: '备胎2号', money: '26万元' }]
    },
    {
        id: 2,
        name: '女神二',
        iphone: 12345678910,
        weixin: 'hahahahah',
        height: 168,
        school: '哈佛大学',
        wheel: [{ name: '备胎3号', money: '80万元' }, { name: '备胎4号', money: '200万元' }]
    }]
}

复制代码
里面有两个女神的所有信息，包括女神的名字、手机、微信、身高、学校、备胎集合等信息。
接下来我们就要对这些数据结构进行描述。
描述数据池中数据结构
const { buildSchema } = require('graphql');

// 描述数据结构 schema
var schema = buildSchema(`
    type Wheel {
        name: String,
        money: String
    }
    type Info {
        id: Int
        name: String
        iphone: Int
        weixin: String
        height: Int
        school: String
        wheel: [Wheel]
    }
    type Query {
        girls: [Info]
    }
`);
复制代码
上面这段代码就是女神信息的schema。
首先我们用type Query定义了一个对女神信息的查询，里面包含了很多女孩girls的信息Info，这些信息是一堆数组，所以是[Info]
我们在type Info中描述了一个女孩的所有信息的维度，包括了名字(name)、手机(iphone)、微信(weixin)、身高(height)、学校(school)、备胎集合(wheel)
定义查询规则
得到女神的信息描述(schema)后，就可以自定义获取女神的各种信息组合了。
比如我想和女神认识，只需要拿到她的名字(name)和微信号(weixin)。查询规则代码如下：
const { graphql } = require('graphql');

// 定义查询内容
const query = `
    { 
        girls {
            name
            weixin
        }
    }
`;

// 查询数据
const result = await graphql(schema, query, root)
复制代码
筛选结果如下：

又比如我想进一步和女神发展，我需要拿到她备胎信息，查询一下她备胎们(wheel)的家产(money)分别是多少，分析一下自己能不能获取优先择偶权。查询规则代码如下：
const { graphql } = require('graphql');

// 定义查询内容
const query = `
    { 
        girls {
            name
            wheel {
            	money
            }
        }
    }
`;

// 查询数据
const result = await graphql(schema, query, root)
复制代码
筛选结果如下：

我们通过女神的例子，展现了如何通过graphQL按需加载数据。
映射到我们业务具体场景中，天秀接口返回的每条数据都包含100个字段，我们配置schema，获取其中的10个字段，这样就避免了剩下90个不必要字段的传输。
graphQL还有另一个好处就是可以灵活配置，这个接口需要10个字段，另一个接口要5个字段，第n个接口需要另外x个字段
按照传统的做法我们要做出n个接口才能满足，现在只需要一个接口配置不同schema就能满足所有情况了。
感悟
在生活中，咱们舔狗真的很缺少graphQL按需加载的思维
渣男渣女，各取所需
你的真情在名媛面前不值一提
我们要学会投其所好
上来就亮车钥匙，没有车就秀才艺
今晚我有一条祖传的染色体想与您分享一下
行就行，不行就换下一个
直奔主题，简单粗暴
缓存 -> redis
第二个优化手段，使用redis缓存
天秀老接口内部调用了另外三个老接口，而且是串行调用，极其耗时耗资源，秀到你头皮发麻
我们用redis来缓存天秀接口的聚合数据，下次再调用天秀接口，直接从缓存中获取数据即可，避免高耗时的复杂调用，简化后代码如下：
const redis = require("redis");
const { promisify } = require("util");

// 链接redis服务
const client = redis.createClient(6379, '127.0.0.1');

// promise化redis方法，以便用async/await
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

async function list() {
	// 先获取缓存中数据，没有缓存就去拉取天秀接口
	let result = await getAsync("缓存");
    if (!result) {
    	  // 拉接口
    	  const data = await 天秀接口();
          result = data;
          // 设置缓存数据
          await setAsync("缓存", data)
    }
   	return result;
}

list(); 

复制代码
先通过getAsync来读取redis缓存中的数据，如果有数据，直接返回，绕过接口调用，如果没有数据，就会调用天秀接口，然后setAsync更新到缓存中，以便下次调用。因为redis存储的是字符串，所以在设置缓存的时候，需要加上JSON.stringify(data)，为了便于大家理解，我就不加了，会把具体细节代码放在github中。
将数据放在redis缓存里有几个好处
可以实现多接口复用、多机共享缓存
这就是传说中的云备胎
追求一个女神的成功率是1%
同时追求100个女神，那你获取到一个女神的概率就是100%
鲁迅《狂人日记》里曾说过：“舔一个是舔狗，舔一百个你就是战狼”
你是想当舔狗还是当战狼？
来吧，缓存用起来，redis用起来
轮询更新 -> schedule
最后一个优化手段：轮询更新 -> schedule
女神的备胎用久了，会定时换一批备胎，让新鲜血液进来，发现新的快乐
缓存也一样，需要定时更新，保持与数据源的一致性，代码如下：
const schedule = require('node-schedule');

// 每个小时更新一次缓存
schedule.scheduleJob('* * 0 * * *', async () => {
    const data = await 天秀接口();
    // 设置redis缓存数据
    await setAsync("缓存", data)
});
复制代码
天秀接口不是一个强实时性接口，数据源一周可能才会变一次
所以我们根据实际情况用轮询来设置更新缓存频率
我们用node-schedule这个库来轮询更新缓存，* * 0 * * *这个的意思就是设置每个小时的第0分钟就开始执行缓存更新逻辑，将获取到的数据更新到缓存中，这样其他接口和机器在调用缓存的时候，就能获取到最新数据，这就是共享缓存和轮询更新的好处。
早年我在当舔狗的时候，就将轮询机制发挥到淋漓尽致
每天向白名单里的女神，定时轮询发消息
无限循环云跪舔三件套：

“啊宝贝，最近有没有想我”
“啊宝贝早安安”
“宝贝晚安，么么哒”

虽然女神依然看不上我
但仍然时刻准备着为女神服务
结尾
经过以上三个方法优化后
接口请求耗时从3s降到了860ms

这些代码都是从业务中简化后的逻辑
真实的业务场景远比这要复杂：分段式数据存储、主从同步 读写分离、高并发同步策略等等
每一个模块都晦涩难懂
就好像每一个女神都高不可攀
屌丝战胜了所有bug，唯独战胜不了她的心
受伤了只能在深夜里独自买醉
但每当梦到女神打开我做的页面
被极致流畅的体验惊艳到
在精神高潮中享受灵魂升华
那一刻
我觉得我又行了
（完）
代码地址：github

作者：第一名的小蝌蚪，公众号：前端屌丝
