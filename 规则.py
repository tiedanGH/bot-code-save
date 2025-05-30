import json

game_list = [
    "死神之门",         #0
    "讨喜抽奖",         #1
    "博饼",             #2
    "电子四驱车",       #3
    "遛鸟",             #4
    "色即是空",         #5
    "极限跳伞",         #6
    "三轮车",           #7
    "福袋",             #8
    "扩散捕捉",         #9
    "赛博斗蛐蛐",       #10
    "掷骰利息",         #11
    "绝命登山",         #12
    "完美战斗",         #13
    "龟兔赛跑",         #14
    "大海战",           #15
    "上山容易下山难",   #16
    "限界比大小",       #17
    "心跳水立方",       #18
    "猜密码",           #19
    "办公软件",         #20
    "模拟足球赛",       #21
    "Farkle",          #22
]

rule = [

#0 死神之门 作者：saiwei
'''
## 死神之门
- **作者：** saiwei
### 游戏规则
- 玩家开始前需要选择挑战活到n岁（最少80岁，最多300岁），如果挑战成功获得n*10的积分奖金，失败则支付500积分。
- 比如挑战100岁，会先随机抽一个5-20的随机数，抽到几就表示几年后会遇到死神之门，比如抽了9，那这个死神之门就有9%几率死亡，如果没死亡，则再抽一个5-20岁，直到你的年龄达到或超过100岁，则存活成功，中途死亡一次就算失败。
### 特殊成就
- 天选之人：挑战240岁以上成功。
- 鸿福齐天：挑战300岁成功。
''',

#1 讨喜抽奖 作者：saiwei
'''
## 讨喜抽奖
- **作者：** saiwei
### 玩法1
- 玩家从2-9中选一个数（比如8）作为讨厌的数字，然后saiwei随机 roll1-100。
- 如果roll的数字中没有8，奖励100。
- 如果是88，需支付4300。
- 如果是两侧的87或89，需支付1100。
- 如果是其他有8的数字，需支付100。
### 玩法2
- 玩家从2-9中选一个数（比如8）作为喜欢的数字，然后saiwei随机 roll1-100。
- 如果roll的数字中没有8，支付100。
- 如果是88，奖励4300。
- 如果是两侧的87或89，奖励1100。
- 如果是其他有8的数字，奖励100。
### 每次至少5连抽，或5的倍数。
''',

#2 博饼
'''
## 博饼
### 游戏规则
- 支付100积分，并猜测一个结果
- 裁判摇六个6面骰子，猜中按照赔率结算
    + 一秀（包含一个4）：赔率 2.5
    + 二举（包含两个4）：赔率 5
    + 三红（包含三个4）：赔率 18
    + 四进（有4个一样）：赔率 25
    + 对堂（一种一个）：赔率 65
    + 状元带N（包含四个4）：赔率 130
    + 五子带N（有5个一样）：赔率 300
    + 臭满（彩蛋：114514）：赔率 777
    + 五红带N（包含5个4）：赔率 1500
    + 状元插金花（444411）：赔率 3000
    + 六抔黑（六个全一样）：赔率 9000
    + 六抔红（包含六个4）：赔率 45000
### 概率参考
![image1](image://bobing1.png)
![image2](image://bobing2.png)
''',

#3 电子四驱车 作者：saiwei
'''
## 电子四驱车
- **作者：** saiwei
### 游戏规则
- 玩家支付1000积分，给自己和对手各选择一种车。赛道总长度20米，每回合速度为整数。
- 谁的车先冲线谁赢，同时则加赛。
### 车辆列表
- A神经刀：每回合速度在1-5之间随机。
- B先行者：每回合速度为随机数（随机范围：1至他与终点的距离的1/2向上取整）。
- C加速王：第一回合速度1，之后每次速度变成当前速度至它的两倍之间一个随机数。
- D爆发户：每回合速度2，但是有1/8几率额外前进8米。
- E老爷车：每回合速度为随机两个1-6的数字的和，但是如果速度大于等于10则抛锚淘汰，在这回合及之后回合都无法前进，如果都抛锚，先抛锚的输。
- F瞌睡虫：每回合在瞌睡和醒着中随机，瞌睡不前进，醒着速度为2-10中一个随机数。
- G阿三哥：第一回合1-6随机，如果是3的倍数，下轮1-9，否则下轮1-3。
- H闪现车：速度4-16，超出终点的部分需要回退到20才能被裁判看到，每回合1格。
''',

#4 遛鸟 作者：黑桃3
'''
## 遛鸟
- **作者：** 黑桃3
### 游戏规则
- ①每人初始选择一种鸟类，互相之间可以重复，每轮随机抽取2-5只鸟进行比赛。
- ②比赛过程每回合在自己的前进距离上下限里抽取各自的【前进距离】，前进后的位置为【进后位】，随后触发各自技能，更新后的位置为【技后位】。
- ③比赛过程中【技后位】<0的立即死亡，【技后位】大于20的时候结束比赛。
- 注：同时冲线的按照超过20的多少排出名次，未到20的继续比赛，比赛结束时若存活鸟数>1时则淘汰存活的末尾鸟。
### 鸟类列表
- 【凶残秃鹫】2-6
    + 和你同一【进后位】的其他鸟-3
- 【南飞雁】3-4
    + +n，n为场上【进后位】公差为1的数列最大数目-1
- 【方差鸟】1-8
    + 无
- 【雄鹰】3-4
    + 每一场比赛不淘汰后都会使你的初始【进后位】+2
- 【出头鸟】4-6
    + 【进后位】唯一最大时-2
- 【穿梭蜂鸟】1-3
    + 若场上【进后位】都不相同，你+4
- 【引力鸟】3-5
    + 【进后位】最大的所有鸟-2，最小的+2
- 【瞬影隼】3-5
    + 进后位唯一最小则+n，n为第一进后位和你的差值
- 【乘风鹤】3-5
    + 存在【进后位】比你大1的，你们一起+2
- 【中上鸟】3-5
    + 若【进后位】>第三，-2，【进后位】<第三，+2（5-6个对应第三，3-4个对应第二，2个也就是单挑对应第一）
- 【孤鸟】3-5
    + 【进后位】大于你的+1，小于你的-1
- 【倒反天罡鸟】3-5
    + 存在【进后位】唯一第一和唯一末尾时触发，第一-n，末尾+n，n为第一和末尾【进后位】的差值
- 【乱世鸟】0-2
    + +n，n为相邻位次【进后位】差值的最大值
- 【无足鸟】0-11
    + 抽到0立即死亡
- 【瘟疫鸟】-3-1
    + 【技后位】变为0以下不会死亡且对你来说小于-10同样视为冲线，一旦前进距离为负数，场上除【瘟疫鸟】外的所有鸟+n，n为你抽取的前进距离
- 【鸵鸟】4-7
    + 每三个回合，抽取的前进步数强制为0
- 【鹌鹑】2-4
    + 任何让你前进的技能影响都会×2，你无法被技能影响后退
- 【鸽子】0-1
    + 随机抽取其他一只鸟，取他本轮的前进距离n，你+n
- 【麻雀】2-3
    + 1/3的概率临时获得【瞬影隼】的技能，1/3的概率临时获得【倒反天罡鸟】的技能，1/3的概率临时获得【喜鹊】的技能
- 【海鸥】3-5
    + 比赛时每有一只鸟死亡，你的前进距离上下限+2，比赛结束时重置
- 【燕子】1-5
    + 每次前进距离上限为上次前进距离*2，比赛结束时重置
- 【鹦鹉】2-4
    + 每存在一对【进后位】相同，你+2
- 【鹈鹕】3-5
    + 你会吃下〖最近鸟〗并与他交换前进距离上下限，最多只能吃下一只。
    + 吃下后每个回合这只鸟-n，且你+n，n为场上其他存活未冲线鸟的数量，直到他与你不是最接近时。
    + 注：不是最接近时就会吐出来，肚子里的鸟冲线、死亡、淘汰或者主动吐出来的下一轮即可吃下别的鸟；吐出来和吃进去的回合不会-n+n。
- 【喜鹊】3-5
    + 存在【进后位】相同时，你下一回合前进距离*2，其他【进后位】相同的鸟同样下一回合获得前进距离*2
- 【乌鸦】3?-4?
    + 每当你没被抽到时，你的前进距离上下限+1，如果前进距离上下限为7-8时则变更为3-4
- 【变色鸟】3-4
    + 你这回合获得除了【变色鸟】以外〖靠近鸟〗的技能
### 词条说明
- 〖最近鸟〗:【进后位】与你最接近的鸟，优先【进后位】唯一小，次是【进后位】唯一大，都没有就不存在
- 〖靠近鸟〗:【进后位】与你最接近的鸟，有多个就随机选择
''',

#5 色即是空 作者：saiwei
'''
## 色即是空
- **作者：** saiwei
### 游戏规则
- 玩家支付300积分进入游戏，裁判rol1-20的一个整数作为目标n。
- 扔5个六面骰子，哪个数字没有就得几分。
    + 比如：11336，得分为2+4+5=11分。
- 如果得分=n，则玩家获胜，赢得1000积分。
- 玩家还可以支付100积分重投其中任意几颗骰子，也可以直接退出游戏。
- 重投次数无上限。
''',

#6 极限跳伞 作者：saiwei
'''
## 极限跳伞
- **作者：** saiwei
### 游戏规则
- 玩家支付1000积分进入游戏，并设定积分达到n时退出，n大于1000且不大于10W。
- 每回合，裁判roll-1至4之间的一个随机整数m，如果roll到正数则积分增长m*10%，roll到0则不变，如果roll到-1则游戏失败。
- 当积分达到或超过n时，游戏结束，玩家赢得n+100的积分的奖励。
''',

#7 三轮车 作者：saiwei
'''
## 三轮车
- **作者：** saiwei
### 游戏规则
- 玩家支付200积分进入游戏。
- 玩家和两个npc进行一场比赛，roll1-3，抽到1就算夺冠。
- 然后裁判roll1-100来确定冠军奖金：
    + 1-50，奖金400。
    + 51-80，奖金600。
    + 81-90，奖金800。
    + 91-95，奖金1000。
    + 96-100，奖金1900。
''',

#8 福袋 作者：爱鸽的鱼头
'''
## 福袋
- **作者：** 爱鸽的鱼头
### 游戏规则
- 游戏分为两个福袋：
    + A袋：3红球2白球5黑球
    + B袋：1红球2白球3黑球
- 玩家一共有8次开启福袋的机会，每次可以选择：
    + 支付200积分开启A福袋，从中随机摸出一个小球并放回
    + 支付300积分开启B福袋，从中随机摸出一个小球并放回
- 当玩家获得4个红球时，奖励2500积分，游戏结束
- 当玩家获得3个白球时，奖励3000积分，游戏结束
- 玩家中途可以随时结束游戏
''',

#9 扩散捕捉 作者：saiwei
'''
## 扩散捕捉
- **作者：** saiwei
### 游戏规则
- 玩家支付330进入游戏，并设置目标n，n为任意大于等于500的整数。
- 然后基准数k从20开始震荡扩散，roll1至k*10的一个整数作为下一抽的基准数，直到基准数大于50000游戏结束。
- 如果中途出现基准数与你的目标相差小于等于200，则你赢得n的奖励。
''',

#10 赛博斗蛐蛐 作者：爱鸽的鱼头
'''
## 赛博斗蛐蛐
- **作者：** 爱鸽的鱼头
### 游戏规则
- 1、【a,b】表示a到b中的一个随机整数；
- 2、（上）/（下）表示计算结果为小数时向上或者向下取整；
- 3、双方同时展开攻击，造成【1，自身攻击力-对方防御力】点伤害；
- 4、默认暴击效果：造成伤害*1.5（下）；
- 5、蛐蛐生命值没有上限，当某一方生命值降为0或以下，游戏结束，另一方获胜；
- 6、若某一回合后双方生命值同时降到0或以下则都淘汰。
- 7、每回合数值结算顺序：先结算伤害，若蛐蛐存活再结算吸血或者牧师的回血（牧师睡着时也会回血），最后结算中毒掉血。
### 蛐蛐种类
- 每名玩家可以在以下蛐蛐中选择自己的蛐蛐：
- A、普通蛐蛐：攻击力：18；防御力：1；暴击率：1/9；闪避率：1/9；初始生命值：20；
- B、坦克蛐蛐：攻击力：10；防御力：6；暴击率：1/13；闪避率：1/13；初始生命值：30；
- C、吸血蛐蛐：攻击力：25；防御力：0；暴击率：1/5；闪避率：1/5；初始生命值：10；
    + 特殊能力：每回合回复本回合造成伤害【0.4倍（下）-0.6倍（下）】点生命值。
- D、牧师蛐蛐：攻击力：12；防御力：2；暴击率：1/10；闪避率：1/10；初始生命值：15；
    + 特殊能力：每回合回复【0.2倍对方攻击力（下），0.4倍对方攻击力（下）】点生命值。
- E、催眠蛐蛐：攻击力：15；防御力：2；暴击率：1/5；闪避率：1/5；初始生命值：20；
    + 特殊能力：暴击效果改为1.3倍，同时敌方下一回合会睡觉：不可攻击和闪避。
- F、巫师蛐蛐：攻击力：15；防御力：2；暴击率：1/5；闪避率：1/5；初始生命值：20；
    + 特殊能力：暴击效果改为1.25倍，同时对敌方施加中毒效果：每回合结束后减少【1,0.4倍生命值（上）】点生命值，持续2回合
- G、模仿者：选择其中2种蛐蛐，在战斗时随机选择一种进行战斗。
''',

#11 掷骰利息 作者：桌游小黄鸭
'''
## 掷骰利息
- **作者：** 桌游小黄鸭
### 游戏规则
- 一开始有1000金币
- 持续10轮：每轮扔一D12，设结果为X，玩家的金币数会乘以(0.4+0.1*X)
- 十轮之后，如果金币为1000以上，则玩家胜利。
''',

#12 绝命登山 作者：saiwei
'''
## 绝命登山
- **作者：** saiwei
### 游戏规则
- 玩家支付1000积分进入游戏，并设定要登山n天。
- 你的登山队k人（初始k为100），每回合roll0至k中的一个随机整数，作为这回合结束后的人数。
- n回合后如果人数没有降到0，则玩家获胜。赢得：((2的n次方)-1)*10+1000的奖励。
- 也可以不设定n，则按照最高收益作为奖励，但不退还门票。
### 《登山独侠》
- 玩家支付1000积分进入游戏。
- 裁判`#run 绝命登山`，其中每出现一次1人存活，奖励1000积分
''',

#13 完美战斗 作者：黑桃3
'''
## 完美战斗 电子斗蛐蛐
- **作者：** 黑桃3
- **版本：** V1.00
### 游戏规则
- 玩家12滴血，任意选择4个行动排列好后私信裁判，游戏过程中不可以更改，可以是轻轻蓄挡，可以是蓄重挡轻
- 每回合随机抽取两个玩家对战，第一轮默认处于蓄力状态，如果任意一方没有受到伤害，则视为完美战斗，对方-4血且自己+1血
### 行动
- ①轻击：伤害1血【蓄力：伤害*3并且可以破除蓄力，对方重击时自己不受伤害】
- ②重击：伤害2血，可以破开格挡和蓄力，下一段行动不可为重击【蓄力：伤害*3】
- ③格挡：无伤害，可以挡住轻击，并且未受到伤害时下一次攻击数值翻倍【蓄力：可以挡住所有任意状态攻击】
- ④蓄力：无伤害，若未受到重击或蓄力轻击则下一次行动额外触发蓄力状态【蓄力：回复2血】
''',

#14 龟兔赛跑 作者：桌游小黄鸭
'''
## 龟兔赛跑
- **作者：** 桌游小黄鸭
### 游戏规则
- 每轮兔子扔个D6并前进相应步数，但如果扔出1且严格领先则改为睡着。睡着状态不会前进，但仍然每轮D6，扔出6则会醒过来。
- 结算完兔子后结算乌龟，扔D3并前进相应步数，如果兔子处于睡着状态则额外前进1格。
- 有至少一方到达100时结束，步数多者获胜（存在平局）。
''',

#15 大海战
'''
# 大海战BOSS详细技能和奖励明细
- **更新日期：** 2025年2月2日
### 开始BOSS挑战
- 需使用机器人LGTBot，在群聊执行指令时**需要@机器人**
- 开始BOSS挑战的指令为：
    + 「#新游戏 大海战 单机 [<配置> <配置>...]」
- 其中快捷配置可快速配置游戏所需要的所有配置
    + 详细使用方法可通过「#规则 大海战」查看
- 注：在对战BOSS时，每回合都会将赛况存档，如需中途的复盘（如空军指挥前的局面），可联系铁蛋。*图片缓存会定期清理，保存时间为一周至一个月*
### 积分奖励规则
- **挑战BOSS胜利可以获得积分奖励**，失败不会有任何惩罚。每个BOSS的积分奖励规则详见下方对应的BOSS说明
- 挑战的积分奖励会随着游戏特殊规则和配置发生变化，不同BOSS的积分奖励不同，当局获胜奖励积分数会在开始时告知
- 下方为连发和侦察对积分倍率的影响：
    + **连发：** 连发1为400%，连发2为200%，连发3为100%；大于3每多一个连发，倍率下降10%
    + **侦察：** 侦察10为100%，每少一个倍率上升10%，每多一个倍率下降4%
## 【BOSS1】无限火力
- BOSS每回合最多发动一个技能，且都会进行普通打击：随机向地图上发射 1-4 枚导弹。当达到 20 回合时，BOSS将增强普攻至 3-6 枚导弹
- 【主动技能1】15% 概率发动 [空军指挥]——随机移动所有未被击落的飞机至其他位置，并尽可能避开已侦察区域
- 【主动技能3】15% 概率发动 [连环轰炸]——随机打击地图上某个坐标的整个十字区域
- 【主动技能2】15% 概率发动 [雷达扫描]——随机扫描地图上 5*5 的区域，其中的所有飞机（飞机头+机身）会被直接击落
- 【主动技能4】25% 概率发动 [火力打击]——BOSS会发射一枚高爆导弹，炸毁地图上 3*3 的区域
- 【被动技能】当BOSS有 3 架飞机被击落时，所有技能的触发概率提升 5%！
- **BOSS1挑战奖励：**
    + 基础奖励　　400 积分
    + 可重叠　　　+400 积分
    + 首要害　　　+900 积分
    + 无要害　　　+1200 积分
    + 双特规叠加　+1000 积分
## 【BOSS2】核平铀好
- 【特殊飞机】核弹研发中心：呈十字形，要害在其中心，形状见下图。被打击要害时使核弹发射基础概率减少 10%（此要害不计算在总要害数中）
> ![boss2](image://boss2.png)
- BOSS每回合最多发动一个主动技能，且都会进行普通打击：随机向地图上发射 3-6 枚导弹。当达到 18 回合时，BOSS将增强普攻至 6-8 枚导弹
- 【主动技能1】[核弹]——摧毁整个地图，但如果概率低于 6% 时引爆威力会下降。基础概率为0，每回合概率提升 0.5%；BOSS每有一个机身被打击，概率提升 0.1%；每有一个要害被打击，概率提升 0.5%；可通过打击研发中心来延缓进展
- 【主动技能2】5% 概率发动 [空军支援]——将一架已被击落的飞机更换为新飞机，并转移位置。如果BOSS没有被击落的飞机，会额外起飞一架（最多不超过 6 架）
- 【主动技能3】15% 概率发动 [石墨炸弹]——发动技能的回合，玩家仅有 1 枚导弹
- 【被动技能】玩家每次攻击时都有 8% 概率触发 [导弹拦截]，拦截玩家的导弹并打击到玩家自己地图的相同位置，小心了！
- **BOSS2挑战奖励：**
    + 基础奖励　　500 积分
    + 可重叠　　　+500 积分
    + 首要害　　　+1000 积分
    + 无要害　　　+1200 积分
    + 双特规叠加　+800 积分
## 【BOSS3】科技时代
- BOSS每回合最多发动一个技能，且都会进行普通打击：随机向地图上发射 3-5 枚导弹。
- 【主动技能1】10% 概率发动 [高能激光]——从地图边缘随机一格射入激光进行斜线打击，在到达地图边缘后会反射两次
- 【主动技能2】10% 概率发动 [热跟踪弹]——随机跟踪一个已知的机身位置，并打击附近的 3*3 区域
- 【主动技能3】15% 概率发动 [自爆无人机]——随机对 3 个横竖各5格共9格的十字形区域进行打击
- 【主动技能4】15% 概率发动 [分导弹头]——每发导弹落点 5*5 范围内再随机打击 3 个格子
- 【主动技能5】15% 概率发动 [电磁干扰]——本回合玩家的所有导弹实际落点会在选择的坐标周围 5*5 区域内发生偏移
- 【被动技能】当BOSS有 3 架飞机被击落时，技能5[电磁干扰]将不能发动，但使其他所有技能的触发概率提升 5%，同时技能3[自爆无人机]数量变为 2 个
- **BOSS3挑战奖励：**
    + 基础奖励　　500 积分
    + 可重叠　　　+500 积分
    + 首要害　　　+900 积分
    + 无要害　　　+1200 积分
    + 双特规叠加　+800 积分
## 【BOSS0】？？？
- 【特殊飞机】万能核心：形状不固定，要害在其中心，随机在某个编号对应的位置上安置4个机身。被打击要害时视为所有BOSS形态的特殊要害被击中（此要害不计算在总要害数中）
> ![boss0](image://boss0.png)
- 【变换技能】每回合会从所有BOSS中随机一个并改变形态，根据变换对应的BOSS发动普通打击和主动技能。被动技能仅在切换至对应的BOSS时才有可能触发。
- **BOSS0挑战奖励：**
    + 基础奖励　　600 积分
    + 可重叠　　　+600 积分
    + 首要害　　　+1200 积分
    + 无要害　　　+1500 积分
    + 双特规叠加　+800 积分
''',

#16 上山容易下山难 作者：saiwei
'''
## 上山容易下山难
- **作者：** saiwei
### 游戏规则
- 玩家支付1000进入游戏。并设定下山n回合。（最高奖励100w）
- 分为上山和下山两部分。
- 上山：k一开始为0，每回合roll k至1000中的一个数作为新的k，三回合后k就是你的登山高度。
- 下山：每回合roll k/10（向下取整）至k中的一个数，如果n回合内k变为0，则玩家赢得1000000/(2的n次方-1)
''',

#17 限界比大小 作者：桌游小黄鸭
'''
## 限界比大小
- **作者：** 桌游小黄鸭
### 游戏规则
- 双方同时各选择一个0到1之间的数。
- 然后系统生成一个0-1均匀分布的随机数 称为“限界”。
- 选的数超过限界就爆了，双方爆则平局，单方爆则对方胜，都没爆则大者胜。
- `#run 限界比大小 (输入的数值)`
- 可与机器人单挑
''',

#18 心跳水立方 作者：Chance
'''
## 心跳水立方
- **作者：** Chance
### 游戏规则
- 每关有1-(关数+1)的格子，只有随机到空的格子才能存活
- 开局随机生命数3-10
- 最后分数为 2^最高关数×0.2×随机生命数+随机-10-10的数) (2^最高层数/最高生命数大于等于10时) 或者 2^最高关数/(随机生命数×0.2)+随机-10-10的数
''',

#19 猜密码 作者：Chance
'''
## 猜密码
- **作者：** Chance
### 游戏规则
- 初始随机一个0-999数字作为密码，每轮选择一个数字验证，在存档情况下，还会随机一个n(0-9)，每轮该密码的百，十，个位会往后移n位(例如6后移9为5)。未存档则不会有这一规则，有下列四个效果：(验证数字为你每轮输入数字)
    + 1.【索求】验证数字的各位上是否有n
    + 2.【平均】验证数字的三位的平均数的整数位是否有密码任意位
    + 3.【验证】验证数字是否存在某一位和密码对应位上相同
    + 4.【范围】验证数字与密码是否相差(密码三位数字中最小一位*100)以内
- 种子：每个数字与n对应最多5个种子，种子有极小概率(估计就是0)对应两个密码，种子生成方式保密(与时间无关)可以尝试破解一下(与密码，n和密码的百位有关) 
- 注：游戏玩法非本人原创，代码由本人编写
''',

#20 办公软件 作者：saiwei
'''
## 办公软件
- **作者：** saiwei
### 游戏规则
- 玩家支付1000进入游戏。
- word里只有一个1，一开始剪切板里有一个1，裁判roll10次操作：
    + /rd r 10 全选 选择一个 复制 剪切 粘贴 粘贴看最后有几个1。
- 每个1奖励400积分。
''',

#21 模拟足球赛 作者：saiwei
'''
## 模拟足球赛
- **作者：** saiwei
### 游戏规则
- 玩家每支付200积分可选一个选项。
- 比赛流程：
    + roll5-20作为第一球进球时间n，然后roll1-30作为进球值m，如果m小于等于n则进球，如果进球再rollA或B作为进球的球队。
    + 之后再roll5-20作为下一球进球时间，以此进行下去，直到时间大于等于90分钟，游戏结束。
### 选项列表
- A队获胜，赔率2.5
- B队获胜，赔率2.5
- 平局，赔率4.5
- A或B净胜球1，赔率2.5
- A或B净胜球2，赔率4
- A或B净胜球3，赔率8
- A或B净胜球4及以上，赔率20
- 总进球0-1，赔率10
- 总进球2-3，赔率2
- 总进球4-6，赔率2.5
- 总进球7及以上，赔率100
''',

#21 Farkle 作者：桌游小黄鸭
'''
## Farkle
- **作者：** 桌游小黄鸭
### 游戏规则
- Farkle是一个骰子游戏。
    + `#run Farkle start` 可以开始一轮新游戏
    + `#run Farkle rank` 查看排行榜
    + `#run Farkle state` 查看个人当前游戏状态
- 游戏目标：游戏进行若干回合，玩家积累分数，直到达到5000分时，游戏结束。
### 游戏流程
- 玩家每轮掷6颗骰子，根据结果得分。每轮可选择继续掷剩余骰子或结束回合。
- 得分规则：
    + 1：100分
    + 5：50分
    + 三条X：100X分（2<=X<=6）
    + 三条1：1000分
    + 四条为对应三条的分数的2倍，五条为4倍，六条为8倍
    + 此外：123456记1000分，六个无法计分的骰子记500分。
- 每轮玩家都可以选择使用哪些骰子计分（至少计一个骰子），若无法计分，则失去本轮的得分且回合强制结束。
- 热骰：如果所有骰子都进行了计分，则恢复至6个骰子。
- 游戏过程中操作：
    + 输入bank或者stop以计分当前所有分数骰并结束回合。
    + 输入数字以选择计分的骰子并继续回合。
''',

]

# ----------main----------
data_output = {}
data_output["format"] = "markdown"
data_output["width"] = 750
data_output["content"] = ""
lst = []
try:
    lst = input().split()
    data_output["content"] += rule[game_list.index(lst[0])]
    if len(lst) > 1 and lst[1] == "文字":
        data_output["format"] = "text"
    print(json.dumps(data_output))
except:
    if len(lst) > 0:
        data_output["content"] += "### 尚未录入这款游戏的规则，可联系铁蛋投稿\n"
    data_output["content"] += "## 支持查看规则的游戏列表：\n"
    index = 5
    for name in game_list:
        if index > 4:
            data_output["content"] += '''<br>\n　'''
            index = 1
        data_output["content"] += name
        block = 11 - len(name)
        for _ in range(block):
            data_output["content"] += "　"
        index += 1
    print(json.dumps(data_output))
