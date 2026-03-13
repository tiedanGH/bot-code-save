# 本程序大部分内容均使用 AI 生成
# 准确性可能存在误差，请谨慎参考
# 图片素材来源：https://www.flickr.com/photos/laird_of_kiloran/albums/72157627745527329/

import random
import json

# ----------- 大阿卡那（22张）-----------
major_arcana = [
    {
        "id": 0,
        "name": "愚人",
        "upright": "象征新的开始与未知旅程的开启。代表纯真、信任与勇气，鼓励你放下顾虑迈出第一步。在探索中学习，在体验中成长。",
        "reversed": "暗示冲动、准备不足或对风险缺乏判断。可能过度理想化现实，忽视潜在问题。需要在自由与责任之间找到平衡。",
        "image": "https://live.staticflickr.com/6102/6234580670_0d2de3f65d_z.jpg",
    },
    {
        "id": 1,
        "name": "魔术师",
        "upright": "象征创造力与行动力的结合。代表资源齐备、思维清晰，能够把想法转化为现实成果。提醒你主动掌握局势。",
        "reversed": "可能出现能力被滥用或沟通失误。暗示自信不足或方向混乱。需要重新聚焦目标并保持诚实。",
        "image": "https://live.staticflickr.com/6159/6234582750_2f945de319_z.jpg",
    },
    {
        "id": 2,
        "name": "女祭司",
        "upright": "象征直觉与潜意识的智慧。提醒你倾听内在声音，关注隐藏的信息。真相往往存在于表象之下。",
        "reversed": "暗示忽略直觉或情绪压抑。可能存在秘密或信息阻隔。需要静下心来重新连接内心。",
        "image": "https://live.staticflickr.com/6113/6234585244_0dbd61dffb_z.jpg",
    },
    {
        "id": 3,
        "name": "女皇",
        "upright": "象征丰盛、滋养与创造力。代表自然成长与情感支持，一切正处于繁荣状态。适合发展关系或创造新成果。",
        "reversed": "可能出现情感依赖或创造受阻。暗示过度付出或自我忽视。需要重新照顾自己的需求。",
        "image": "https://live.staticflickr.com/6213/6234588362_6f906e96d7_z.jpg",
    },
    {
        "id": 4,
        "name": "皇帝",
        "upright": "象征秩序、结构与领导力。代表理性决策与稳定基础。强调责任与掌控能力。",
        "reversed": "暗示控制欲过强或权威失衡。可能过于僵化或缺乏自律。需要学会灵活应对变化。",
        "image": "https://live.staticflickr.com/6224/6234066109_f4bcab4497_z.jpg",
    },
    {
        "id": 5,
        "name": "教皇",
        "upright": "象征传统、信仰与精神指导。代表学习、制度或长辈的支持。鼓励在规则中寻找智慧。",
        "reversed": "暗示质疑权威或拒绝传统。可能陷入教条或过度叛逆。需要找到真正适合自己的价值体系。",
        "image": "https://live.staticflickr.com/6042/6234068727_0ee6c0302f_z.jpg",
    },
    {
        "id": 6,
        "name": "恋人",
        "upright": "象征爱与价值观的契合。代表重要选择与关系的结合。提醒你遵从内心做出真诚决定。",
        "reversed": "暗示关系冲突或价值观不一致。可能优柔寡断或缺乏承诺。需要正视真实需求。",
        "image": "https://live.staticflickr.com/6155/6234595528_067288e813_z.jpg",
    },
    {
        "id": 7,
        "name": "战车",
        "upright": "象征意志力与胜利。代表通过自律与决心克服阻碍。只要方向明确便能稳步前进。",
        "reversed": "暗示失去控制或过度冲动。可能方向混乱或动力不足。需要重新找回内在平衡。",
        "image": "https://live.staticflickr.com/6038/6234072405_fcfbcf46d9_z.jpg",
    },
    {
        "id": 8,
        "name": "力量",
        "upright": "象征内在勇气与温和的力量。代表以耐心和同理心解决问题。真正的强大来自自我掌控。",
        "reversed": "暗示自信不足或情绪失控。可能压抑愤怒或失去耐心。需要重建内在稳定。",
        "image": "https://live.staticflickr.com/6232/6234598040_ab57f2df1e_z.jpg",
    },
    {
        "id": 9,
        "name": "隐者",
        "upright": "象征内省与智慧的寻找。提醒你暂时退隐，倾听内心答案。独处有助于获得清晰判断。",
        "reversed": "暗示孤立过度或拒绝帮助。可能陷入封闭状态。需要重新与外界建立健康连接。",
        "image": "https://live.staticflickr.com/6167/6234075619_362ee6b629_z.jpg",
    },
    {
        "id": 10,
        "name": "命运之轮",
        "upright": "象征周期变化与命运转折。代表机遇正在出现。顺势而为将带来积极发展。",
        "reversed": "暗示抗拒改变或遭遇阻碍。可能陷入停滞循环。需要主动调整方向。",
        "image": "https://live.staticflickr.com/6116/6234602206_afaa17f901_z.jpg",
    },
    {
        "id": 11,
        "name": "正义",
        "upright": "象征公平与因果。代表诚实面对现实与责任。所有决定都会产生相应结果。",
        "reversed": "暗示不公或判断失衡。可能逃避责任或偏见影响决策。需要重新审视立场。",
        "image": "https://live.staticflickr.com/6098/6234605714_b666acb3ba_z.jpg",
    },
    {
        "id": 12,
        "name": "倒吊人",
        "upright": "象征暂停与换位思考。通过放下执念获得新的视角。等待本身也是一种成长。",
        "reversed": "暗示固执或无意义拖延。可能拒绝改变现状。需要主动调整态度。",
        "image": "https://live.staticflickr.com/6155/6234084897_5f07a81f70_z.jpg",
    },
    {
        "id": 13,
        "name": "死亡",
        "upright": "象征终结与重生。旧阶段结束，新循环即将开启。转化虽痛却必要。",
        "reversed": "暗示抗拒改变或停滞不前。可能执着于过去。需要勇敢放手。",
        "image": "https://live.staticflickr.com/6037/6234086467_17fb2a5a3b_z.jpg",
    },
    {
        "id": 14,
        "name": "节制",
        "upright": "象征平衡与协调。代表不同元素的融合与调和。耐心将带来稳定发展。",
        "reversed": "暗示失衡或过度放纵。可能缺乏节制。需要恢复规律与秩序。",
        "image": "https://live.staticflickr.com/6050/6234088279_0c47d30728_z.jpg",
    },
    {
        "id": 15,
        "name": "恶魔",
        "upright": "象征束缚与欲望。提醒你留意依赖关系或恐惧控制。认清问题是解脱的开始。",
        "reversed": "暗示摆脱枷锁或觉醒。正在脱离不健康模式。自由正在恢复。",
        "image": "https://live.staticflickr.com/6038/6234090311_9637d1d188_z.jpg",
    },
    {
        "id": 16,
        "name": "塔",
        "upright": "象征突发变化与震撼真相。旧结构被打破，为重建创造空间。冲击带来觉醒。",
        "reversed": "暗示危机延迟或内在动荡。可能抗拒面对现实。需要主动重整基础。",
        "image": "https://live.staticflickr.com/6162/6234092237_60186c6a5c_z.jpg",
    },
    {
        "id": 17,
        "name": "星星",
        "upright": "象征希望与疗愈。代表重新找回信念与方向。内在光芒正在恢复。",
        "reversed": "暗示信心不足或迷失目标。可能暂时失去动力。需要重新点燃希望。",
        "image": "https://live.staticflickr.com/6115/6234094083_a5764ccdd2_z.jpg",
    },
    {
        "id": 18,
        "name": "月亮",
        "upright": "象征潜意识与迷雾。提醒警惕幻象与情绪波动。直觉是穿越迷雾的钥匙。",
        "reversed": "暗示恐惧逐渐消散。真相开始显现。需要理性分析情绪来源。",
        "image": "https://live.staticflickr.com/6046/6234620480_231169eba4_z.jpg",
    },
    {
        "id": 19,
        "name": "太阳",
        "upright": "象征成功与喜悦。代表清晰、自信与生命力。前景光明且充满活力。",
        "reversed": "暗示短暂低落或自信受挫。可能忽略简单快乐。需要重新调整心态。",
        "image": "https://live.staticflickr.com/6216/6234097611_714dc3503c_z.jpg",
    },
    {
        "id": 20,
        "name": "审判",
        "upright": "象征觉醒与复苏。代表对过去的总结与新阶段的开启。回应内心召唤至关重要。",
        "reversed": "暗示逃避自我反省。可能拒绝改变或害怕承担责任。需要正视内在声音。",
        "image": "https://live.staticflickr.com/6053/6234099599_e9dd89f0de_z.jpg",
    },
    {
        "id": 21,
        "name": "世界",
        "upright": "象征完成与圆满。代表阶段性成功与整合成果。新的旅程即将展开。",
        "reversed": "暗示收尾未完成或延迟满足。可能缺乏最后一步行动。需要完善细节。",
        "image": "https://live.staticflickr.com/6096/6234101445_fdbf4b86fc_z.jpg",
    },
]

# ----------- 小阿卡那（56张） -----------
minor_arcana = [
    # 权杖组
    {
        "id": 22,
        "name": "权杖A",
        "upright": "象征新的行动契机与创意萌发，代表热情和开始的动力。适合启动计划或勇敢迈出第一步。带来发展与可能性的开端。",
        "reversed": "暗示动力不足或计划尚未成熟，可能因冲动或准备不足而受阻。需要重新检视基础与节奏，等待更合适的时机。",
        "image": "https://live.staticflickr.com/6178/6234634378_1f43a84a9d_z.jpg",
    },
    {
        "id": 23,
        "name": "权杖2",
        "upright": "象征远见与规划，处于评估与选择的发展期。代表为长远目标做出布局并衡量资源。适合制定下一步的策略。",
        "reversed": "暗示犹豫不决或恐惧扩张，可能因害怕风险而错失机会。需要明确优先级并鼓起决断力。",
        "image": "https://live.staticflickr.com/6161/6234636276_b1f6d5aa74_z.jpg",
    },
    {
        "id": 24,
        "name": "权杖3",
        "upright": "象征计划的初步展开与远景实现的迹象，合作与扩展逐渐显效。代表耐心等待成果并继续推进。鼓励保持信念与持续努力。",
        "reversed": "暗示进展迟缓或合作不顺，预期落差导致焦虑。需要调整策略或重新沟通以恢复推进力。",
        "image": "https://live.staticflickr.com/6234/6234113573_01cb57abe9_z.jpg",
    },
    {
        "id": 25,
        "name": "权杖4",
        "upright": "象征稳定与庆祝，代表阶段性成果与安全感的建立。适合团体庆贺或确立长期基础。气氛和谐，有利巩固成就。",
        "reversed": "暗示表面安稳下潜藏紧张或停滞，可能过于保守导致机会流失。建议检视内在结构并适度开放。",
        "image": "https://live.staticflickr.com/6222/6234115553_5bc7062f77_z.jpg",
    },
    {
        "id": 26,
        "name": "权杖5",
        "upright": "象征冲突与竞争，代表观点或利益的碰撞。通过较量可以明确立场并促成成长。适合在摩擦中学习与调整策略。",
        "reversed": "暗示无谓争执或内耗，冲突消耗资源且未必有益。需冷静沟通并寻找共识以化解矛盾。",
        "image": "https://live.staticflickr.com/6159/6234117635_040cb3f882_z.jpg",
    },
    {
        "id": 27,
        "name": "权杖6",
        "upright": "象征胜利與公認，代表努力被看见与得到肯定。适合展示成果并扩大影响力。保持谦逊有助长期发展。",
        "reversed": "暗示虚荣或成功被夸大，可能忽略實質的不足。需检视内功并避免自满或倚赖表面光环。",
        "image": "https://live.staticflickr.com/6107/6234119573_88c25c8dab_z.jpg",
    },
    {
        "id": 28,
        "name": "权杖7",
        "upright": "象征守护与捍卫立场，面对挑战仍能坚守。代表勇气与抵抗外来压力。需要坚定信念并维护已有成果。",
        "reversed": "暗示感觉孤立或资源薄弱，难以持续抵抗外界压力。建议寻求支持并审视防御策略是否合适。",
        "image": "https://live.staticflickr.com/6055/6234645990_a72ed7cd68_z.jpg",
    },
    {
        "id": 29,
        "name": "权杖8",
        "upright": "象征速度与信息的快速流动，事情加速推进。适合把握时机并迅速执行计划。沟通畅通将有利于成果到达。",
        "reversed": "暗示节奏失衡或信息混乱，仓促可能导致误判。需放慢脚步并核对细节以避免差错。",
        "image": "https://live.staticflickr.com/6096/6234123431_1656ba0bd1_z.jpg",
    },
    {
        "id": 30,
        "name": "权杖9",
        "upright": "象征韧性与防备，代表坚持到底的决心与警觉心。经历考验但仍有能力守护目标。注意保留能量以应对最后一搏。",
        "reversed": "暗示疲惫或过度戒备，长期压力可能导致精疲力竭。需要学会放松并寻求援助以恢复元气。",
        "image": "https://live.staticflickr.com/6042/6234125333_eb231d1dae_z.jpg",
    },
    {
        "id": 31,
        "name": "权杖10",
        "upright": "象征负担沉重與責任壓力，代表承担过多任务已接近极限。需要合理分配或寻求协助以避免崩溃。完成任务后能获得成长经验。",
        "reversed": "暗示压垮或迷失方向，责任堆积导致产出下降。建议简化并优先处理最关键的事项。",
        "image": "https://live.staticflickr.com/6059/6234651626_fec9ffe589_z.jpg",
    },
    {
        "id": 32,
        "name": "权杖侍从",
        "upright": "象征好奇与探索的新讯息，代表学习新事物或接收机会。态度热情且愿意实践。适合尝试并积累经验。",
        "reversed": "暗示浮躁或浅尝辄止，容易三分钟热度。需要集中注意力并建立持续力以见成效。",
        "image": "https://live.staticflickr.com/6101/6234129705_d69050530a_z.jpg",
    },
    {
        "id": 33,
        "name": "权杖骑士",
        "upright": "象征勇猛與行动力，代表主动追求目标并快速投入实践。适合短期冲刺或承担外向任务。把握方向能带来明显进展。",
        "reversed": "暗示鲁莽或缺乏计划，可能因急躁而犯错。需要在冲劲之外加入策略与耐心。",
        "image": "https://live.staticflickr.com/6161/6234131585_2b426178fe_z.jpg",
    },
    {
        "id": 34,
        "name": "权杖皇后",
        "upright": "象征热情与影响力結合的成熟领袖，代表以行动激励他人并培育团队。具备感染力和创造力。适合推动群体计划。",
        "reversed": "暗示控制欲或情绪化的领导方式，可能影响团队士气。需平衡权威与包容以维持合作。",
        "image": "https://live.staticflickr.com/6102/6234133349_70bdfe5a46_z.jpg",
    },
    {
        "id": 35,
        "name": "权杖国王",
        "upright": "象征稳健的掌控力與战略眼光，代表有效管理与长期规划的能力。以经验领导并达成目标。适合承担高阶责任。",
        "reversed": "暗示独裁或固执己见，可能忽视团队建议。需开放视野并调整管理风格。",
        "image": "https://live.staticflickr.com/6058/6234659884_0d779fcc3e_z.jpg",
    },
    # 圣杯组
    {
        "id": 36,
        "name": "圣杯A",
        "upright": "象征情感的新开始或疗愈能量，代表内心的喜悦与感性契机。适合培养新关系或艺术灵感。带来情感的温暖与流动。",
        "reversed": "暗示情感封闭或机会错过，可能因害怕受伤而退缩。建议先疗愈自我再迈向他者。",
        "image": "https://live.staticflickr.com/6100/6234141143_e951747735_z.jpg",
    },
    {
        "id": 37,
        "name": "圣杯2",
        "upright": "象征互相吸引与深度联结，代表合作或恋情中的真诚连接。双方价值观或情感契合。适合建立亲密关系或伙伴关系。",
        "reversed": "暗示沟通不畅或不对等的付出，关系中可能存在误解。需修复信任并重建平衡。",
        "image": "https://live.staticflickr.com/6231/6234669216_ecc2d13584_z.jpg",
    },
    {
        "id": 38,
        "name": "圣杯3",
        "upright": "象征庆祝与友情，代表社群支持和团队的欢乐时刻。适合共享成功与扩大社交圈。友谊与合作带来丰硕回报。",
        "reversed": "暗示表面的热闹掩盖深层问题，可能有圈内排斥或八卦。需专注真实连接而非表面应酬。",
        "image": "https://live.staticflickr.com/6037/6234672074_51464857d9_z.jpg",
    },
    {
        "id": 39,
        "name": "圣杯4",
        "upright": "象征情感上的不满或倦怠，代表对现状的冷漠或寻求更深层意义。提醒审视内心需求并寻找新刺激。可以视为重新定位情感方向的信号。",
        "reversed": "暗示停止消极等待并主动改变，机会可能在于行动而非沉思。重新投入生活将带来新希望。",
        "image": "https://live.staticflickr.com/6222/6234675624_da9a20a393_z.jpg",
    },
    {
        "id": 40,
        "name": "圣杯5",
        "upright": "象征失落與悔恨，代表对过去的伤感与遗憾。提醒面对失去并寻找可以依靠的资源。悲伤过后往往能发现新的方向。",
        "reversed": "暗示从失落中觉醒并看到希望，疗愈开始显现。逐步接纳现实将带来内心的恢复。",
        "image": "https://live.staticflickr.com/6031/6234679202_11e2c26576_z.jpg",
    },
    {
        "id": 41,
        "name": "圣杯6",
        "upright": "象征怀旧与温柔的回忆，代表过去的纯真或童年影响。适合以温暖的方式连接旧识或疗愈旧伤。也提醒保持成长的步伐。",
        "reversed": "暗示沉溺于过去或拒绝前行，影响当前发展。需要学会放下并以成熟的方式面对当下。",
        "image": "https://live.staticflickr.com/6214/6234681960_66d9ab4b09_z.jpg",
    },
    {
        "id": 42,
        "name": "圣杯7",
        "upright": "象征幻想與多重选择，代表丰富的情感想像或诱惑。提醒辨别真实需求而非被幻象牵引。需慎重选择并脚踏实地。",
        "reversed": "暗示逃避选择或被虚幻迷惑，可能难以落地。建议回归现实并逐项评估可行性。",
        "image": "https://live.staticflickr.com/6222/6234162753_4efca3bef5_z.jpg",
    },
    {
        "id": 43,
        "name": "圣杯8",
        "upright": "象征离开与追寻更深意义的旅程，代表放下熟悉以探索内在。适合主动结束不再满足的关系或路径。勇气将带来新的成长。",
        "reversed": "暗示逃避或半途而废，离开未必带来解脱。建议明晰动机并确保行动是为追寻真实需求。",
        "image": "https://live.staticflickr.com/6222/6234165989_158e20e3e1_z.jpg",
    },
    {
        "id": 44,
        "name": "圣杯9",
        "upright": "象征愿望实现與情感满足，代表对生活的小确幸与内心的满足感。适合庆祝个人成就并享受成果。保持感恩心态更能延续幸福。",
        "reversed": "暗示过度自我满足或倚赖外界认可，可能忽视深层需求。需检视快乐的来源并寻找更持久的满足方式。",
        "image": "https://live.staticflickr.com/6152/6234168247_37b9ca06a5_z.jpg",
    },
    {
        "id": 45,
        "name": "圣杯10",
        "upright": "象征家庭与情感的圆满，代表和谐关系与稳定的支持网。适合巩固亲密关系与共享幸福时刻。体现代际间的温暖与传承。",
        "reversed": "暗示表面和谐可能掩盖矛盾或牺牲自我以维持表象。需要面对真实问题并修复关系裂痕。",
        "image": "https://live.staticflickr.com/6239/6234171803_e213374357_z.jpg",
    },
    {
        "id": 46,
        "name": "圣杯侍从",
        "upright": "象征情感讯息與敏感观察，代表愿意表达内心并传递关怀。适合初步的情感沟通或创意萌发。保持真诚将带来连结。",
        "reversed": "暗示情感幼稚或过于幻想，可能误读讯息。需要厘清边界并以成熟方式表达情绪。",
        "image": "https://live.staticflickr.com/6100/6234174547_11b78aafa1_z.jpg",
    },
    {
        "id": 47,
        "name": "圣杯骑士",
        "upright": "象征浪漫與追求，代表以情感驱动的行动与温柔的表达。适合追求心仪对象或以同理心推动关系。保持真诚能打动对方。",
        "reversed": "暗示滥情或不切实际的浪漫，可能忽视现实需求。需要设立界限并检视情感的可持续性。",
        "image": "https://live.staticflickr.com/6114/6234177439_98d61c42ea_z.jpg",
    },
    {
        "id": 48,
        "name": "圣杯皇后",
        "upright": "象征同理心與滋养，代表以温柔与理解支持他人的情感力量。适合承担疗愈或照护的角色。情感智慧是其主要资源。",
        "reversed": "暗示情绪操控或过度依赖他人，可能忽略自我需求。需保持界限并照顾自身感受。",
        "image": "https://live.staticflickr.com/6106/6234181309_93bd98f410_z.jpg",
    },
    {
        "id": 49,
        "name": "圣杯国王",
        "upright": "象征情感成熟與稳定，代表平衡理性與感性的领导力。以温和而坚定的态度处理人际事务。适合担任支持与顾问角色。",
        "reversed": "暗示情感冷漠或压抑，可能难以表达真实感受。需勇于开放并与他人建立深层连接。",
        "image": "https://live.staticflickr.com/6041/6234708876_773a62382c_z.jpg",
    },
    # 宝剑组
    {
        "id": 50,
        "name": "宝剑A",
        "upright": "象征真相與清晰的思考，代表突破迷雾的洞察力與理性判断。适合下决断或解决复杂问题。思想清晰将带来解脱。",
        "reversed": "暗示沟通受阻或观念混乱，可能被误导或自我欺骗。需要核实信息并冷静分析再行动。",
        "image": "https://live.staticflickr.com/6162/6234712912_0f3c962f95_z.jpg",
    },
    {
        "id": 51,
        "name": "宝剑2",
        "upright": "象征两难与内心平衡的需求，代表需要暂停并权衡利弊。鼓励面对事实而非逃避。寻求中庸将有助于决断。",
        "reversed": "暗示僵局被打破或不得不做出牺牲，可能需要承担短期痛苦以换取前行。接纳变化将解开困局。",
        "image": "https://live.staticflickr.com/6158/6234716234_1a2a9e519a_z.jpg",
    },
    {
        "id": 52,
        "name": "宝剑3",
        "upright": "象征心碎與痛苦的觉醒，代表关系或信任遭受伤害。通过直视痛苦可以开启疗愈的过程。接纳悲伤是复原的第一步。",
        "reversed": "暗示逐步释怀或拒绝面对创伤，可能选择放下或压抑伤痛。健康的处理方式才能带来真正修复。",
        "image": "https://live.staticflickr.com/6119/6234719796_e8d4441d2e_z.jpg",
    },
    {
        "id": 53,
        "name": "宝剑4",
        "upright": "象征休养與恢复，代表暂时退让以疗愈身心。适合反思并补充能量以重新出发。静止也有其必要价值。",
        "reversed": "暗示逃避现实或过度被动，可能延缓复原进程。建议主动采取小步伐的行动促进恢复。",
        "image": "https://live.staticflickr.com/6094/6234722694_ee232d121c_z.jpg",
    },
    {
        "id": 54,
        "name": "宝剑5",
        "upright": "象征冲突的代价與不光彩的胜利，代表在争斗中失去尊重或良知。提醒权衡得失并寻求成熟的解决方式。避免短视的胜利。",
        "reversed": "暗示结束争斗或选择和解，可能通过让步获得更长远的利益。寻求共赢能减少伤害。",
        "image": "https://live.staticflickr.com/6180/6234201033_73496b57d0_z.jpg",
    },
    {
        "id": 55,
        "name": "宝剑6",
        "upright": "象征过渡與离开困境，代表向更平静或更理性的环境移动。适合规划改变并接受疗愈的过程。向前看将带来新的机会。",
        "reversed": "暗示逃避或回头，未能真正离开问题根源。需要正视内在的阻力并采取实际步骤前行。",
        "image": "https://live.staticflickr.com/6219/6234729032_427d796c6c_z.jpg",
    },
    {
        "id": 56,
        "name": "宝剑7",
        "upright": "象征策略與机智，代表以巧思解决难题或采取非传统方法。适合短期的隐蔽行动或规划。提醒注意道德界限。",
        "reversed": "暗示欺瞒被揭露或策略失败，可能需为不诚实行为承担后果。建议以正直重建信任。",
        "image": "https://live.staticflickr.com/6091/6234207565_41965b098a_z.jpg",
    },
    {
        "id": 57,
        "name": "宝剑8",
        "upright": "象征受限與自我设限，代表被恐惧或思维模式束缚。需要意識到限制并逐步打破桎梏。认知的转变会带来自由。",
        "reversed": "暗示开始突破束缚或逃离困境，逐渐恢复行动能力。通过练习与支持可以重获自主权。",
        "image": "https://live.staticflickr.com/6046/6234210379_9c14267317_z.jpg",
    },
    {
        "id": 58,
        "name": "宝剑9",
        "upright": "象征焦虑與夜间忧虑，代表内心恐惧与过度担忧侵蚀生活质量。面对恐惧并寻求支持有助缓解困扰。逐步采取行动能减少负面循环。",
        "reversed": "暗示开始释怀或恐惧程度下降，内心渐趋平静。需继续实践自我照顾以巩固疗愈成果。",
        "image": "https://live.staticflickr.com/6214/6234213789_88ba4db36f_z.jpg",
    },
    {
        "id": 59,
        "name": "宝剑10",
        "upright": "象征极端结束與败局的清算，代表痛苦或失败达到顶点后不得不收场。尽管过程痛楚，但也带来新生的可能。接受结局是转化的开始。",
        "reversed": "暗示难以放手或延长痛苦的周期，抗拒结束反而阻碍恢复。需要勇于放下以开启重建之路。",
        "image": "https://live.staticflickr.com/6230/6234741256_b0a675c122_z.jpg",
    },
    {
        "id": 60,
        "name": "宝剑侍从",
        "upright": "象征求知與信息收集，代表敏锐的观察力与逻辑思维。适合探索真相或学习新知。谨慎核实将带来优势。",
        "reversed": "暗示信息误判或言语伤人，可能因冲动表达而造成误会。需冷静核实并谨慎沟通。",
        "image": "https://live.staticflickr.com/6217/6234743864_2b0c270bcc_z.jpg",
    },
    {
        "id": 61,
        "name": "宝剑骑士",
        "upright": "象征果断與迅速行动，代表以理性和速度解决问题。适合需要立即处理的事务。保持冷静可避免冲突升级。",
        "reversed": "暗示鲁莽或好战，过度急切可能引发冲突。建议在行动前权衡影响并避免情绪化决策。",
        "image": "https://live.staticflickr.com/6160/6234222761_282618aeb0_z.jpg",
    },
    {
        "id": 62,
        "name": "宝剑皇后",
        "upright": "象征理性與公正的判断力，代表以清晰与同理处理复杂局面。适合担任裁决或顾问角色。逻辑与同理心并重是其优势。",
        "reversed": "暗示冷酷或过度挑剔，可能伤害他人感受。需融入温度以平衡严谨的判断。",
        "image": "https://live.staticflickr.com/6172/6234749846_71479a107d_z.jpg",
    },
    {
        "id": 63,
        "name": "宝剑国王",
        "upright": "象征权威與战略思维，代表强大的逻辑与决策能力。适合领导复杂议题并制定清晰方针。以理性为基础带来稳定力量。",
        "reversed": "暗示专断或滥用权力，可能忽略人情与柔软。需要倾听团队并以智慧整合不同观点。",
        "image": "https://live.staticflickr.com/6119/6234228441_35e5e0d483_z.jpg",
    },
    # 星币组
    {
        "id": 64,
        "name": "星币A",
        "upright": "象征实务机会與物质新开端，代表务实的计划或财务上的好机会。适合踏实投入并制定可执行的步骤。长期规划将带来稳固回报。",
        "reversed": "暗示投入回报低或资源浪费，可能缺乏周详评估。建议审慎理财并优化执行方式。",
        "image": "https://live.staticflickr.com/6167/6234755746_81ba607e87_z.jpg",
    },
    {
        "id": 65,
        "name": "星币2",
        "upright": "象征平衡多重责任的能力，代表灵活应对与资源调配。适合在变动中找到节奏并保持稳定。注意时间管理以维持效能。",
        "reversed": "暗示精力分散或无法兼顾多方，导致效率下降。需优先处理最关键的事务并减轻负担。",
        "image": "https://live.staticflickr.com/6153/6234759442_5904ec848e_z.jpg",
    },
    {
        "id": 66,
        "name": "星币3",
        "upright": "象征合作與工匠精神，代表团队协作与技能的精进。透过分工与专业能建立稳固成果。适合在项目中累积口碑与资历。",
        "reversed": "暗示合作破裂或急功近利，可能因沟通不良影响质量。需重建信任并回归专业态度。",
        "image": "https://live.staticflickr.com/6153/6234238151_2f03a83239_z.jpg",
    },
    {
        "id": 67,
        "name": "星币4",
        "upright": "象征守护资源與谨慎管理，代表保守与稳固的财务观念。适合建立储备与保护已得之物。注意避免过度吝啬影响流动性。",
        "reversed": "暗示吝啬或对变动恐惧，可能阻碍机会流入。建议适度放手并评估合理风险以促进成长。",
        "image": "https://live.staticflickr.com/6116/6234766364_9bdcf943f6_z.jpg",
    },
    {
        "id": 68,
        "name": "星币5",
        "upright": "象征匮乏與挑战，代表物质或精神上的窘境与孤立。提醒寻求支持并采取实际步骤改善处境。共情与互助将带来转机。",
        "reversed": "暗示困境开始改善或接受帮助，逐步恢复安全感。需抓住援助并调整资源分配以稳固基础。",
        "image": "https://live.staticflickr.com/6159/6234768838_3d8cca879f_z.jpg",
    },
    {
        "id": 69,
        "name": "星币6",
        "upright": "象征慷慨與给予的平衡，代表付出与回报之间的调和。适合执行互助或慈善行动并建立信任。维持公平能促进长期合作。",
        "reversed": "暗示依赖或施舍带来的权力不平衡，可能造成依赖关系。需鼓励独立并审核给予的方式是否恰当。",
        "image": "https://live.staticflickr.com/6156/6234772038_88511940b8_z.jpg",
    },
    {
        "id": 70,
        "name": "星币7",
        "upright": "象征耕耘與等待收获，代表耐心观察与长期投资的回报期。适合评估进展并决定是否继续耕耘。务实的坚持将带来回报。",
        "reversed": "暗示急于求成或对结果失望，可能因短期焦虑影响判断。建议审视方法并适时调整策略。",
        "image": "https://live.staticflickr.com/6223/6234250873_ec12564bb8_z.jpg",
    },
    {
        "id": 71,
        "name": "星币8",
        "upright": "象征勤勉與精进，代表通过持续练习提升技能与专业度。专注与细致会带来显著成长。适合投入时间打磨工艺。",
        "reversed": "暗示机械重复或失去热情，可能导致倦怠。建议寻找意义或调整节奏以恢复动力。",
        "image": "https://live.staticflickr.com/6106/6234777816_1f6b8a31fc_z.jpg",
    },
    {
        "id": 72,
        "name": "星币9",
        "upright": "象征独立與物质丰裕，代表自给自足与享受劳动成果。适合享受个人努力带来的舒适与自由。保持慷慨心态能延续福祉。",
        "reversed": "暗示虚荣或孤立，可能以物质掩饰内心空虚。需平衡享乐与人际关系以免疏离他人。",
        "image": "https://live.staticflickr.com/6162/6234255825_f46074541e_z.jpg",
    },
    {
        "id": 73,
        "name": "星币10",
        "upright": "象征家族與財務的稳定与传承，代表长久的安全与丰饶。适合规划遗产或建立长远保障。价值观与传统在此得以延续。",
        "reversed": "暗示物质优先导致情感失衡或家庭冲突，可能忽略内在需求。需重建家庭价值与情感连结。",
        "image": "https://live.staticflickr.com/6220/6234259139_ba0a2d571a_z.jpg",
    },
    {
        "id": 74,
        "name": "星币侍从",
        "upright": "象征务实的学习與踏实练习，代表愿意积累技能与打好基础。适合投入学业或职业训练。谦逊与勤奋将带来回报。",
        "reversed": "暗示懒散或缺乏远见，可能因短视而错失成长机会。需制定计划并持之以恒。",
        "image": "https://live.staticflickr.com/6100/6234261387_46b40c4b50_z.jpg",
    },
    {
        "id": 75,
        "name": "星币骑士",
        "upright": "象征稳健與可靠，代表以耐心与责任完成长期目标。适合稳步推进计划并建立信誉。坚持与踏实是其核心优势。",
        "reversed": "暗示保守或固执，可能错过转机与创新机会。需要在稳定与灵活间取得平衡以应对变化。",
        "image": "https://live.staticflickr.com/6093/6234264177_753846d87c_z.jpg",
    },
    {
        "id": 76,
        "name": "星币皇后",
        "upright": "象征丰饶與照護，代表理财智慧与以物质滋养他人的能力。适合管理家务或培育资源。温暖与实用并存的能量。",
        "reversed": "暗示物质依赖或控制欲，可能以占有或保护名义过度干预。需学会分享并尊重他人独立性。",
        "image": "https://live.staticflickr.com/6052/6234266673_cfee88065c_z.jpg",
    },
    {
        "id": 77,
        "name": "星币国王",
        "upright": "象征财富與权威的稳健管理，代表在商业或实体事务上具备实力与信誉。适合承担重大财务或经营决策。长远视角带来持续成功。",
        "reversed": "暗示贪婪或过度功利，可能以牺牲他人为代价追求利益。需承担社会责任并以诚信为本。",
        "image": "https://live.staticflickr.com/6111/6234270179_2c808b9e32_z.jpg",
    },
]

# ----------- 完整牌组 -----------
full_deck = major_arcana + minor_arcana

# ----------- 输出JSON -----------
output_data = {
    "format": "MultipleMessage",
    "messageList": []
}

# ----------- 抽卡 -----------
def draw_cards(n, use_full_deck=False):
    """从指定牌组抽取n张牌"""
    deck = full_deck if use_full_deck else major_arcana
    total = len(deck)
    
    if n < 1 or n > 10:
        output_data["format"] = "text"
        output_data["content"] = "每次只能抽取 1-10 张"
        return

    sampled = random.sample(deck, n)
    for i, card in enumerate(sampled):
        is_upright = random.choice([True, False])
        position = "正位" if is_upright else "逆位"
        text = card["upright"] if is_upright else card["reversed"]
        
        transform = "" if is_upright else "transform: scale(-1, -1);"
        markdown = (
            f"<img src='{card['image']}' alt='image' style='{transform}'/>"
            "<style>body { border: 0; padding: 0; margin: 0; }</style>"
        )
        output_data["messageList"].append({
            "format": "MessageChain",
            "messageList": [
                {
                    "content": f"【{card['id']}】{card['name']}·{position}"
                },
                {
                    "format": "markdown",
                    "width": 300,
                    "content": markdown
                },
                {
                    "content": text
                }
            ]
        })

if __name__ == "__main__":
    try:
        user_input = input().strip()
        
        # ===== 帮助指令 =====
        if user_input.lower() in ["help", "帮助"]:
            output_data["format"] = "text"
            output_data["content"] = (
                "《塔罗牌》使用说明：\n"
                "\n"
                "1. 随机抽取一张：##塔罗牌\n"
                "2. 输入数字（1-10）连续抽取对应数量的牌\n"
                "   例如：##塔罗牌 3\n"
                "3. 若想使用完整牌组（78张），在数字后加[完整]或[all]\n"
                "   例如：##塔罗牌 3 完整\n"
                "\n"
                "※ 本程序大部分内容和解析均使用 AI 生成，解析准确性可能存在误差，请谨慎参考"
            )
        else:
            inputs = user_input.split()
            n = int(inputs[0])
            use_full = len(inputs) > 1 and (inputs[1] == "完整" or inputs[1] == "all")
            draw_cards(n, use_full)
    except:
        draw_cards(1)
    print(json.dumps(output_data))
