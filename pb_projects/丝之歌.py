import json
import random
import sys
import time
from typing import Dict, Any, List

# Boss数据
BOSSES = [
    {"name": "苔藓之母", "hp": 5, "attack": 1},
    {"name": "钟道兽", "hp": 8, "attack": 2},
    {"name": "骷髅暴君", "hp": 10, "attack": 2},
    {"name": "蕾丝", "hp": 14, "attack": 2},
    {"name": "残暴的兽蝇", "hp": 18, "attack": 2},
    {"name": "第四圣咏团", "hp": 14, "attack": 2},
    {"name": "荒沼翼主", "hp": 16, "attack": 2},
    {"name": "碎裂者修女", "hp": 16, "attack": 2},
    {"name": "黑寡妇", "hp": 18, "attack": 2},
    {"name": "巨型螺蝇", "hp": 14, "attack": 2},
    {"name": "狂暴螺蝇", "hp": 16, "attack": 4},
    {"name": "末代裁决者", "hp": 18, "attack": 2},
    {"name": "机枢舞者", "hp": 20, "attack": 2},
    {"name": "散茧魂渊", "hp": 26, "attack": 2},
    {"name": "特罗比奥", "hp": 20, "attack": 2},
    {"name": "幽影", "hp": 18, "attack": 2},
    {"name": "原罪者", "hp": 30, "attack": 2},
    {"name": "伟大的格洛", "hp": 28, "attack": 2},
    {"name": "大跳蚤", "hp": 12, "attack": 2},
    {"name": "失格大厨", "hp": 24, "attack": 2},
    {"name": "监工兄弟", "hp": 18, "attack": 3},
    {"name": "次席戍卫", "hp": 24, "attack": 2},
    {"name": "圣所蕾丝", "hp": 24, "attack": 2},
    {"name": "苍白之母", "hp": 30, "attack": 2},

    {"name": "三叶草舞者", "hp": 32, "attack": 2},
    {"name": "失心加蒙德", "hp": 28, "attack": 2},
    {"name": "针姬", "hp": 32, "attack": 2},
    {"name": "腐囊之父", "hp": 32, "attack": 2},
    {"name": "边陲守望者", "hp": 32, "attack": 2},
    {"name": "伏特维姆", "hp": 20, "attack": 2},
    {"name": "被放逐的格尔", "hp": 22, "attack": 2},
    {"name": "育母", "hp": 32, "attack": 2},
    {"name": "壳王卡汗", "hp": 40, "attack": 2},
    {"name": "尼莱斯", "hp": 40, "attack": 2},
    {"name": "圣所守卫者·赛斯", "hp": 40, "attack": 2},
    {"name": "斯卡尔歌后·卡梅莉塔", "hp": 40, "attack": 2},
    {"name": "失心蕾丝", "hp": 50, "attack": 2}
]

class SilkSongGame:
    def __init__(self, storage_data: Dict, global_data: Dict, user_info: Dict):
        self.storage = storage_data if storage_data else {}
        self.global_data = global_data if global_data else {}
        self.user_info = user_info
        self.output = {"content": "", "storage": "", "global": ""}
        
        # 初始化玩家数据
        self.init_player_data()
        
    def init_player_data(self):
        """初始化玩家数据"""
        # 使用setdefault确保所有必要的键都存在
        self.storage.setdefault("current_position", 0)
        self.storage.setdefault("checkpoint_position", 0)
        self.storage.setdefault("hp", 5)
        self.storage.setdefault("max_hp", 5)
        self.storage.setdefault("silk", 9)
        self.storage.setdefault("max_silk", 9)
        self.storage.setdefault("beads", 0)
        self.storage.setdefault("attack", 1)
        self.storage.setdefault("death_info", None)
        self.storage.setdefault("mask_fragments", 0)
        self.storage.setdefault("silk_fragments", 0)
        self.storage.setdefault("pale_oil", 0)
        self.storage.setdefault("max_distance", 0)
        self.storage.setdefault("in_battle", False)
        self.storage.setdefault("battle_type", None)
        self.storage.setdefault("enemy_hp", 0)
        self.storage.setdefault("boss_name", None)
        self.storage.setdefault("battle_phase", "normal")
        self.storage.setdefault("encounter_stages", [])
        self.storage.setdefault("current_stage", 0)
        self.storage.setdefault("encounter_chair_price", 0)
        self.storage.setdefault("encounter_chair_available", False)
        self.storage.setdefault("jump_count", 0)
        self.storage.setdefault("jump_total", 0)
        self.storage.setdefault("void_invasion", False)
    
    def save_data(self):
        """保存数据到输出"""
        self.output["storage"] = json.dumps(self.storage)
        self.output["global"] = json.dumps(self.global_data)
    
    def handle_command(self, command: str):
        """处理用户指令"""
        command = command.strip().lower()
        
        # 排行指令可以在任何状态下使用
        if command in ["排行", "r", "rank"]:
            self.show_rank()
            self.save_data()
            return self.output
        elif command.startswith("排行 通关") or command.startswith("rank 通关") or command.startswith("r 通关"):
            self.show_clear_rank()
            self.save_data()
            return self.output
        
        if self.storage["in_battle"]:
            return self.handle_battle_command(command)
        else:
            return self.handle_base_command(command)
    
    def handle_base_command(self, command: str):
        """处理基础指令"""
        if command in ["帮助", "h", "help"]:
            self.show_help()
        elif command in ["状态", "s", "status"]:
            self.show_status()
        elif command in ["前进", "g", "go"]:
            self.move_forward()
        elif command in ["回血", "heal"]:
            self.heal()
        elif command in ["回椅子", "c", "chair"]:
            self.return_to_chair()
        elif command in ["购买", "b", "buy"]:
            self.buy_chair()
        else:
            self.output["content"] = "未知指令，请输入「帮助」查看可用指令"
        
        self.save_data()
        return self.output
    
    def handle_battle_command(self, command: str):
        """处理战斗指令"""
        if command in ["攻击", "a", "attack"]:
            self.attack()
        elif command in ["闪避", "d", "dodge"]:
            self.dodge()
        elif command in ["技能", "skill"]:
            self.use_skill()
        elif command in ["回血", "heal"]:
            self.battle_heal()
        elif command in ["状态", "s", "status"]:
            self.show_status()
        else:
            self.output["content"] = "战斗中未知指令，可用指令：攻击/a/attack、闪避/d/dodge、技能/skill、回血/heal"
        
        self.save_data()
        return self.output
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
===== 丝之歌游戏帮助 =====

【基础指令】
帮助/h/help - 查看游戏规则和指令说明
状态/s/status - 查看当前游戏状态
前进/g/go - 向前移动，可能触发各种事件
回血/hp - 消耗9灵丝恢复3点生命
回椅子/c/chair - 返回存档点并恢复生命
购买/b/buy - 在遇到椅子时购买存档点
排行/r/rank - 查看距离排行榜
排行 通关 - 查看通关排行榜

【战斗指令】（仅在战斗中使用）
攻击/a/attack - 攻击敌人
闪避/d/dodge - 躲避敌人攻击
技能/skill - 消耗4灵丝使用强力技能
回血/heal - 战斗中恢复生命（有失败概率）

【游戏规则】
- 初始位置为0，每次前进+1距离
- 死亡后返回存档点，念珠归零
- 到达死亡位置可回收掉落的念珠
- 收集道具提升能力
- 击败最终boss通关游戏
"""
        self.output["content"] = help_text
    
    def show_status(self):
        """显示状态信息"""
        status = f"""
===== 玩家状态 =====
当前位置：{self.storage['current_position']}
存档点位置：{self.storage['checkpoint_position']}
生命值：{self.storage['hp']}/{self.storage['max_hp']}
灵丝：{self.storage['silk']}/{self.storage['max_silk']}
念珠：{self.storage['beads']}
攻击力：{self.storage['attack']}
"""
        
        if self.storage['death_info']:
            status += f"死亡记录：在位置 {self.storage['death_info']['position']} 死亡，掉落 {self.storage['death_info']['beads_lost']} 念珠\n"
        
        status += f"道具：面具碎片×{self.storage['mask_fragments']}，灵丝轴碎片×{self.storage['silk_fragments']}，苍白油×{self.storage['pale_oil']}"
        
        if self.storage['void_invasion']:
            status += "\n虚空入侵状态：已激活"
        
        if self.storage['in_battle']:
            status += f"\n\n【战斗状态】"
            if self.storage['battle_type'] == 'boss':
                status += f"\n正在与 {self.storage['boss_name']} 战斗"
                status += f"\nBoss生命值：{self.storage['enemy_hp']}"
                if self.storage['battle_phase'] == 'skill':
                    status += "\nBoss正在使用技能！"
            else:
                current_stage = self.storage['current_stage']
                total_stages = len(self.storage['encounter_stages'])
                status += f"\n遭遇战 - 阶段 {current_stage+1}/{total_stages}"
                status += f"\n当前阶段怪物：{self.storage['encounter_stages'][current_stage]}"
        
        self.output["content"] = status
    
    def move_forward(self):
        """前进指令"""
        if self.storage['in_battle']:
            self.output["content"] = "战斗中无法前进！"
            return
        
        # 重置椅子可用状态（除非遇到新椅子）
        self.storage['encounter_chair_available'] = False
        
        self.storage['current_position'] += 1
        event_text = f"前进到位置 {self.storage['current_position']}\n"
        
        # 检查是否到达死亡位置
        if (self.storage['death_info'] and 
            self.storage['current_position'] == self.storage['death_info']['position']):
            event_text += f"到达上次死亡位置！灵丝恢复至上限，回收 {self.storage['death_info']['beads_lost']} 念珠\n"
            self.storage['silk'] = self.storage['max_silk']
            self.storage['beads'] += self.storage['death_info']['beads_lost']
            self.storage['death_info'] = None
        
        # 更新最远距离
        if self.storage['current_position'] > self.storage['max_distance']:
            self.storage['max_distance'] = self.storage['current_position']
            self.update_distance_rank()
        
        # 随机事件
        event_chance = random.random()
        original_hp = self.storage['hp']
        original_silk = self.storage['silk']
        
        if event_chance < 0.30:  # 30% 遇到小怪
            event_text += self.encounter_small_monster()
        elif event_chance < 0.55:  # 25% 跳跳乐
            event_text += self.jumping_event()
        elif event_chance < 0.75:  # 20% 正常赶路
            event_text += self.normal_travel()
        elif event_chance < 0.85:  # 10% 精英怪
            event_text += self.encounter_elite()
        elif event_chance < 0.92:  # 7% 遭遇战
            event_text += self.encounter_battle()
        elif event_chance < 0.97:  # 5% Boss战
            event_text += self.encounter_boss()
        else:  # 3% 获得道具
            event_text += self.get_item()
        
        # 检查血量变化并添加提示
        if self.storage['hp'] < original_hp:
            event_text += f"\n当前剩余生命：{self.storage['hp']}/{self.storage['max_hp']}"
        
        # 检查灵丝是否达到回血限制
        if self.storage['silk'] >= 9 and self.storage['silk'] > original_silk:
            event_text += f"\n灵丝已恢复至{self.storage['silk']}点！"
        
        self.output["content"] = event_text
    
    def encounter_small_monster(self):
        """遇到小怪"""
        text = "遇到小怪！\n"
        damage = random.randint(0, 2)
        if damage > 0:
            self.storage['hp'] -= damage
            text += f"受到 {damage} 点伤害\n"
        
        if self.storage['hp'] <= 0:
            text += self.player_die()
            return text
        
        beads_gain = random.randint(4, 20)
        silk_gain = random.randint(3, 5)
        self.storage['beads'] += beads_gain
        self.storage['silk'] = min(self.storage['silk'] + silk_gain, self.storage['max_silk'])
        text += f"击败小怪！获得 {beads_gain} 念珠，{silk_gain} 灵丝\n"
        return text
    
    def jumping_event(self):
        """跳跳乐事件"""
        self.storage['jump_count'] = 0
        self.storage['jump_total'] = random.randint(3, 5)
        text = f"开始跳跳乐！需要完成 {self.storage['jump_total']} 次跳跃\n"
        
        for i in range(self.storage['jump_total']):
            chance = random.random()
            if chance < 0.20:  # 20% 受伤
                self.storage['hp'] -= 1
                text += f"第{i+1}跳：受伤-1生命\n"
                if self.storage['hp'] <= 0:
                    text += self.player_die()
                    return text
            elif chance < 0.30:  # 10% 位置-1
                self.storage['current_position'] = max(0, self.storage['current_position'] - 1)
                text += f"第{i+1}跳：不小心脚滑，掉了下去，距离-1\n"
            elif chance < 0.35:  # 5% 位置-2
                self.storage['current_position'] = max(0, self.storage['current_position'] - 2)
                text += f"第{i+1}跳：不小心脚滑，掉了下去，距离-2\n"
            else:
                text += f"第{i+1}跳：成功！\n"
        
        text += "跳跳乐完成！\n"
        return text
    
    def normal_travel(self):
        """正常赶路"""
        text = "平静的赶路...\n"
        if random.random() < 0.30:  # 30% 遇到椅子
            price = random.choice([50, 60, 70, 80])
            self.storage['encounter_chair_price'] = price
            self.storage['encounter_chair_available'] = True
            text += f"发现一把椅子！需要 {price} 念珠购买（使用「购买」指令）\n"
        return text
    
    def encounter_battle(self):
        """遭遇战"""
        self.storage['in_battle'] = True
        self.storage['battle_type'] = 'encounter'
        
        # 生成遭遇战阶段（1-3个阶段，每个阶段2-4个小怪）
        num_stages = random.randint(1, 3)
        self.storage['encounter_stages'] = [random.randint(2, 4) for _ in range(num_stages)]
        self.storage['current_stage'] = 0
        
        return "进入了一个奇怪的房间，身后的门关上了！进入遭遇战！\n"
    
    def encounter_elite(self):
        """精英怪"""
        text = "遇到精英怪！\n"
        if random.random() < 0.3:  # 30% 受伤
            self.storage['hp'] -= 2
            text += "受到 2 点伤害\n"
            if self.storage['hp'] <= 0:
                text += self.player_die()
                return text
        
        beads_gain = random.randint(15, 30)
        silk_gain = random.randint(5, 8)
        self.storage['beads'] += beads_gain
        self.storage['silk'] = min(self.storage['silk'] + silk_gain, self.storage['max_silk'])
        text += f"击败精英怪！获得 {beads_gain} 念珠，{silk_gain} 灵丝\n"
        return text
    
    def encounter_boss(self):
        """Boss战"""
        # 检查是否触发最终boss
        if self.storage['void_invasion'] and self.storage['current_position'] >= 100 and random.random() < 0.4:
            boss = next(b for b in BOSSES if b['name'] == "失心蕾丝")
        elif (not self.storage['void_invasion']) and self.storage['current_position'] >= 50 and random.random() < 0.8:
            boss = next(b for b in BOSSES if b['name'] == "苍白之母")
        else:
            # 根据虚空入侵状态选择boss池
            hard_bosses = ["三叶草舞者", "失心加蒙德", "针姬", "腐囊之父", "边陲守望者", "伏特维姆", "被放逐的格尔", "育母", "壳王卡汗", "尼莱斯", "圣所守卫者·赛斯", "斯卡尔歌后·卡梅莉塔"]
            if self.storage['void_invasion']:
                available_bosses = [b for b in BOSSES if b['name'] in hard_bosses]
            else:
                available_bosses = [b for b in BOSSES if b['name'] not in hard_bosses and b['name'] not in ["苍白之母", "失心蕾丝"]]
            
            boss = random.choice(available_bosses)
        
        self.storage['in_battle'] = True
        self.storage['battle_type'] = 'boss'
        self.storage['boss_name'] = boss['name']
        self.storage['enemy_hp'] = boss['hp']
        self.storage['battle_phase'] = 'normal'
        
        return f"遭遇Boss：{boss['name']}！进入Boss战！\n"
    
    def get_item(self):
        """获得道具"""
        item_chance = random.random()
        text = "发现神秘道具！\n"
        
        if item_chance < 0.35:  # 面具碎片
            self.storage['mask_fragments'] += 1
            text += "获得面具碎片×1\n"
            if self.storage['mask_fragments'] >= 4:
                self.storage['max_hp'] += 1
                self.storage['hp'] = self.storage['max_hp']
                self.storage['mask_fragments'] = 0
                text += "集齐4个面具碎片！生命上限+1，生命回满！\n"
        
        elif item_chance < 0.65:  # 灵丝轴碎片
            self.storage['silk_fragments'] += 1
            text += "获得灵丝轴碎片×1\n"
            if self.storage['silk_fragments'] >= 2:
                self.storage['max_silk'] += 1
                self.storage['silk'] = self.storage['max_silk']
                self.storage['silk_fragments'] = 0
                text += "集齐2个灵丝轴碎片！灵丝上限+1，灵丝回满！\n"
        
        elif item_chance < 0.85:  # 苍白油
            self.storage['pale_oil'] += 1
            self.storage['attack'] += 1
            text += "获得苍白油！攻击力+1\n"
        
        else:  # 念珠串📿
            bead_types = [
                ("破损念珠串📿", 30, 0.4),
                ("念珠串📿", 60, 0.7),
                ("珍贵念珠串📿", 120, 0.9),
                ("沉甸甸的念珠串📿", 220, 1.0)
            ]
            
            for name, amount, prob in bead_types:
                if random.random() < prob:
                    self.storage['beads'] += amount
                    text += f"获得{name}！念珠+{amount}\n"
                    break
        
        return text
    
    def player_die(self):
        """玩家死亡处理"""
        death_beads = self.storage['beads']
        death_position = self.storage['current_position']
        
        # 保存死亡信息
        self.storage['death_info'] = {
            'position': death_position,
            'beads_lost': death_beads
        }
        
        # 重置玩家状态
        self.storage['current_position'] = self.storage['checkpoint_position']
        self.storage['hp'] = self.storage['max_hp']
        self.storage['beads'] = 0
        self.storage['silk'] = 1  # 灵丝回到1
        
        # 退出战斗状态
        self.storage['in_battle'] = False
        self.storage['battle_type'] = None
        self.storage['encounter_stages'] = []
        self.storage['current_stage'] = 0
        self.storage['battle_phase'] = 'normal'
        
        return f"💀 玩家死亡！在位置 {death_position} 掉落 {death_beads} 念珠\n已返回存档点位置 {self.storage['checkpoint_position']}"
    
    def heal(self):
        """回血指令"""
        if self.storage['silk'] < 9:
            self.output["content"] = "灵丝不足9点，无法回血"
            return
        
        self.storage['silk'] -= 9
        heal_amount = min(3, self.storage['max_hp'] - self.storage['hp'])
        self.storage['hp'] += heal_amount
        
        if self.storage['silk'] == 0:
            self.storage['silk'] = 1
        
        self.output["content"] = f"消耗9灵丝，恢复{heal_amount}点生命"
    
    def return_to_chair(self):
        """回椅子指令"""
        self.storage['current_position'] = self.storage['checkpoint_position']
        self.storage['hp'] = self.storage['max_hp']
        self.output["content"] = f"已返回存档点位置 {self.storage['checkpoint_position']}，生命恢复至上限"
    
    def buy_chair(self):
        """购买椅子"""
        if not self.storage['encounter_chair_available']:
            self.output["content"] = "当前没有遇到可购买的椅子"
            return
        
        price = self.storage['encounter_chair_price']
        if self.storage['beads'] >= price:
            self.storage['beads'] -= price
            self.storage['checkpoint_position'] = self.storage['current_position']
            self.storage['hp'] = self.storage['max_hp']
            self.storage['encounter_chair_available'] = False
            self.output["content"] = f"花费{price}念珠购买椅子成功！当前位置设为存档点，生命回满"
        else:
            self.output["content"] = f"念珠不足！需要{price}念珠，当前只有{self.storage['beads']}念珠"
    
    # 战斗相关方法
    def attack(self):
        """攻击指令"""
        if not self.storage['in_battle']:
            self.output["content"] = "非战斗状态无法攻击"
            return
        
        # 随机决定Boss是否使用技能
        if self.storage['battle_type'] == 'boss' and random.random() < 0.1:
            self.storage['battle_phase'] = 'skill'
            self.output["content"] = f"{self.storage['boss_name']}使用了强力技能！小心！"
            return
        
        attack_result = random.random()
        hits = 0
        
        if attack_result < 0.05:  # 5% 打3次
            hits = 3
        elif attack_result < 0.40:  # 35% 打2次
            hits = 2
        elif attack_result < 0.90:  # 50% 打1次
            hits = 1
        else:  # 10% 没打中
            hits = 0
        
        damage = hits * self.storage['attack']
        self.storage['silk'] = min(self.storage['silk'] + hits, self.storage['max_silk'])
        text = ""
        
        if self.storage['battle_type'] == 'boss':
            self.storage['enemy_hp'] -= damage
            text = f"对{self.storage['boss_name']}造成{damage}点伤害！"
            
            # 检查Boss是否死亡
            if self.storage['enemy_hp'] <= 0:
                text += self.defeat_boss()
            else:
                # Boss反击
                attack_chance = 0.15 if self.storage['battle_phase'] == 'normal' else 0.65
                if random.random() < attack_chance:
                    boss_attack = next(b['attack'] for b in BOSSES if b['name'] == self.storage['boss_name'])
                    self.storage['hp'] -= boss_attack
                    text += f"\n{self.storage['boss_name']}反击！受到{boss_attack}点伤害"
                    if self.storage['hp'] <= 0:
                        text += self.player_die()
                
                # 重置Boss技能阶段
                if self.storage['battle_phase'] == 'skill':
                    self.storage['battle_phase'] = 'normal'
        
        else:  # 遭遇战
            current_stage = self.storage['current_stage']
            self.storage['encounter_stages'][current_stage] = max(0, self.storage['encounter_stages'][current_stage] - hits)
            text = f"攻击消灭{hits}只怪物！"
            
            # 检查当前阶段是否完成
            if self.storage['encounter_stages'][current_stage] <= 0:
                self.storage['current_stage'] += 1
                
                # 检查是否完成所有阶段
                if self.storage['current_stage'] >= len(self.storage['encounter_stages']):
                    text += self.escape_encounter()
                else:
                    text += f"\n进入下一阶段！当前阶段怪物：{self.storage['encounter_stages'][self.storage['current_stage']]}"
            else:
                # 怪物反击
                monsters_left = self.storage['encounter_stages'][current_stage]
                attack_chance = 0.15 if monsters_left < 3 else 0.40
                if random.random() < attack_chance:
                    self.storage['hp'] -= 1
                    text += f"\n受到怪物攻击！损失1点生命"
                    if self.storage['hp'] <= 0:
                        text += self.player_die()
        
        # 检查灵丝是否达到回血限制
        if self.storage['silk'] >= 9 and hits > 0:
            text += f"\n灵丝已恢复至{self.storage['silk']}点！"

        self.output["content"] = text
    
    def dodge(self):
        """闪避指令"""
        if not self.storage['in_battle']:
            self.output["content"] = "非战斗状态无法闪避"
            return
        
        if random.random() < 0.95:  # 95% 成功闪避
            self.output["content"] = "成功闪避攻击！"
        else:
            if self.storage['battle_type'] == 'boss':
                boss_attack = next(b['attack'] for b in BOSSES if b['name'] == self.storage['boss_name'])
                self.storage['hp'] -= boss_attack
                self.output["content"] = f"闪避失败！受到{boss_attack}点伤害"
            else:
                self.storage['hp'] -= 1
                self.output["content"] = "闪避失败！受到1点伤害"
            
            if self.storage['hp'] <= 0:
                self.output["content"] += self.player_die()
    
    def use_skill(self):
        """使用技能"""
        if not self.storage['in_battle']:
            self.output["content"] = "非战斗状态无法使用技能"
            return
        
        if self.storage['silk'] < 4:
            self.output["content"] = "灵丝不足4点，无法使用技能"
            return
        
        self.storage['silk'] -= 4
        text = ""
        
        if self.storage['battle_type'] == 'boss':
            damage = 8
            self.storage['enemy_hp'] -= damage
            text = f"使用技能！对{self.storage['boss_name']}造成{damage}点伤害！"
            
            if self.storage['enemy_hp'] <= 0:
                text += self.defeat_boss()
            else:
                # 技能使用后Boss可能反击
                if random.random() < 0.5:  # 50%概率反击
                    boss_attack = next(b['attack'] for b in BOSSES if b['name'] == self.storage['boss_name'])
                    self.storage['hp'] -= boss_attack
                    text += f"\n{self.storage['boss_name']}反击！受到{boss_attack}点伤害"
                    if self.storage['hp'] <= 0:
                        text += self.player_die()
        else:
            current_stage = self.storage['current_stage']
            self.storage['encounter_stages'][current_stage] = 0
            text = "使用技能！秒杀当前阶段所有怪物！"
            
            # 进入下一阶段
            self.storage['current_stage'] += 1
            if self.storage['current_stage'] >= len(self.storage['encounter_stages']):
                text += self.escape_encounter()
            else:
                text += f"\n进入下一阶段！当前阶段怪物：{self.storage['encounter_stages'][self.storage['current_stage']]}"
        
        self.output["content"] = text
    
    def battle_heal(self):
        """战斗回血"""
        if self.storage['silk'] < 9:
            self.output["content"] = "灵丝不足9点，无法回血"
            return
        
        # 检查回血失败概率
        fail_chance = 0
        if self.storage['battle_type'] == 'boss':
            if self.storage['battle_phase'] == 'normal':
                fail_chance = 0.20
            else:
                fail_chance = 0.60
        else:
            current_stage = self.storage['current_stage']
            monsters_left = self.storage['encounter_stages'][current_stage]
            if monsters_left < 3:
                fail_chance = 0.15
            else:
                fail_chance = 0.50
        
        if random.random() < fail_chance:
            self.storage['silk'] = 1
            self.storage['hp'] -= 1  # 受到攻击
            self.output["content"] = "回血失败！受到攻击且灵丝被清空"

            if self.storage['hp'] <= 0:
                self.output["content"] += self.player_die()
        else:
            self.storage['silk'] -= 9
            heal_amount = min(3, self.storage['max_hp'] - self.storage['hp'])
            self.storage['hp'] += heal_amount
            
            if self.storage['silk'] == 0:
                self.storage['silk'] = 1
            
            self.output["content"] = f"消耗9灵丝，恢复{heal_amount}点生命"
    
    def defeat_boss(self):
        """击败Boss"""
        self.storage['in_battle'] = False
        self.storage['battle_type'] = None
        self.storage['battle_phase'] = 'normal'
        
        text = f"\n🎉 击败{self.storage['boss_name']}！"
        
        # 检查是否是特殊Boss
        if self.storage['boss_name'] == "苍白之母":
            if random.random() < 0.6:  # 60%概率触发虚空入侵
                self.storage['void_invasion'] = True
                text += "\n💀 虚空入侵！游戏继续，但世界已改变..."
                # 不记录通关，继续游戏
            else:
                self.record_clear("普通")
                text += "\n🏆 恭喜通关丝之歌！游戏记录已保存到通关榜"
                self.reset_after_clear()
        
        elif self.storage['boss_name'] == "失心蕾丝":
            self.record_clear("特殊")
            text += "\n🏆 恭喜达成特殊结局！游戏记录已保存到通关榜"
            self.reset_after_clear()
        
        else:
            # 普通Boss奖励灵丝
            silk_reward = random.randint(8, 15)
            self.storage['silk'] = min(self.storage['silk'] + silk_reward, self.storage['max_silk'])
            text += f"获得{silk_reward}灵丝"
        
        return text
    
    def escape_encounter(self):
        """完成遭遇战"""
        self.storage['in_battle'] = False
        self.storage['battle_type'] = None
        self.storage['encounter_stages'] = []
        self.storage['current_stage'] = 0
        
        beads_reward = random.randint(20, 40)
        silk_reward = random.randint(3, 6)
        self.storage['beads'] += beads_reward
        self.storage['silk'] = min(self.storage['silk'] + silk_reward, self.storage['max_silk'])
        return f"\n成功完成遭遇战！获得{beads_reward}念珠，{silk_reward}灵丝"
    
    def reset_after_clear(self):
        """通关后重置玩家数据（保留排行榜记录）"""
        self.storage = {
            "current_position": 0,
            "checkpoint_position": 0,
            "hp": 5,
            "max_hp": 5,
            "silk": 9,
            "max_silk": 9,
            "beads": 0,
            "attack": 1,
            "death_info": None,
            "mask_fragments": 0,
            "silk_fragments": 0,
            "pale_oil": 0,
            "max_distance": self.storage['max_distance'],
            "in_battle": False,
            "battle_type": None,
            "enemy_hp": 0,
            "boss_name": None,
            "battle_phase": "normal",
            "encounter_stages": [],
            "current_stage": 0,
            "encounter_chair_price": 0,
            "encounter_chair_available": False,
            "jump_count": 0,
            "jump_total": 0,
            "void_invasion": False
        }
    
    # 排行榜相关方法
    def update_distance_rank(self):
        """更新距离排行榜"""
        user_id = self.user_info.get('userID', 'unknown')
        nickname = self.user_info.get('nickname', '未知玩家')
        max_distance = self.storage['max_distance']
        
        if 'distance_rank' not in self.global_data:
            self.global_data['distance_rank'] = []
        
        # 查找是否已有记录
        existing_index = -1
        for i, record in enumerate(self.global_data['distance_rank']):
            if record.get('userID') == user_id:
                existing_index = i
                break
        
        if existing_index >= 0:
            # 更新现有记录
            if max_distance > self.global_data['distance_rank'][existing_index]['max_distance']:
                self.global_data['distance_rank'][existing_index]['max_distance'] = max_distance
                self.global_data['distance_rank'][existing_index]['nickname'] = nickname
        else:
            # 添加新记录
            self.global_data['distance_rank'].append({
                'userID': user_id,
                'nickname': nickname,
                'max_distance': max_distance
            })
        
        # 按距离排序
        self.global_data['distance_rank'].sort(key=lambda x: x['max_distance'], reverse=True)
        # 只保留前50名
        self.global_data['distance_rank'] = self.global_data['distance_rank'][:50]
    
    def record_clear(self, clear_type):
        """记录通关"""
        user_id = self.user_info.get('userID', 'unknown')
        nickname = self.user_info.get('nickname', '未知玩家')
        distance = self.storage['current_position']
        timestamp = int(time.time())
        
        if 'clear_rank' not in self.global_data:
            self.global_data['clear_rank'] = []
        
        self.global_data['clear_rank'].append({
            'userID': user_id,
            'nickname': nickname,
            'distance': distance,
            'timestamp': timestamp,
            'type': clear_type
        })
        
        # 特殊结局排在前面，然后按距离和时间排序
        self.global_data['clear_rank'].sort(key=lambda x: (
            0 if x.get('type', '普通') == '特殊' else 1,  # 特殊结局优先
            x['distance'],  # 距离短的优先
            x['timestamp']  # 时间早的优先
        ))
        # 只保留前50名
        self.global_data['clear_rank'] = self.global_data['clear_rank'][:50]
    
    def show_rank(self):
        """显示距离排行榜"""
        if 'distance_rank' not in self.global_data or not self.global_data['distance_rank']:
            self.output["content"] = "暂无排行榜数据"
            return
        
        text = "===== 最远距离排行榜 =====\n"
        for i, record in enumerate(self.global_data['distance_rank'][:10], 1):
            text += f"{i}. {record['nickname']} - 最远距离: {record['max_distance']}\n"
        
        # 显示玩家自己的排名
        user_id = self.user_info.get('userID', 'unknown')
        for i, record in enumerate(self.global_data['distance_rank']):
            if record.get('userID') == user_id:
                text += f"\n您的排名: 第{i+1}名 - 最远距离: {record['max_distance']}"
                break
        
        self.output["content"] = text
    
    def show_clear_rank(self):
        """显示通关排行榜"""
        if 'clear_rank' not in self.global_data or not self.global_data['clear_rank']:
            self.output["content"] = "暂无通关记录"
            return
        
        text = "===== 通关排行榜 =====\n"
        text += "（特殊结局优先，然后按通关距离排序）\n\n"
        
        for i, record in enumerate(self.global_data['clear_rank'][:10], 1):
            # 转换时间戳为可读格式
            time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(record['timestamp']))
            type_marker = "🌟" if record.get('type', '普通') == '特殊' else "⭐"
            text += f"{i}. {type_marker} {record['nickname']} - 通关距离: {record['distance']} - {time_str}\n"
        
        self.output["content"] = text

def main():
    # 读取输入
    lines = sys.stdin.read().splitlines()
    
    if not lines:
        print(json.dumps({"content": "输入错误"}))
        return
    
    # 解析第一行JSON（存储数据）
    try:
        first_line = json.loads(lines[0])
        storage_data = json.loads(first_line.get('storage', '{}')) if first_line.get('storage') else {}
        global_data = json.loads(first_line.get('global', '{}')) if first_line.get('global') else {}
        user_info = {
            'userID': first_line.get('userID', 'unknown'),
            'nickname': first_line.get('nickname', '未知玩家'),
            'from': first_line.get('from', 'private')
        }
    except:
        storage_data = {}
        global_data = {}
        user_info = {'userID': 'unknown', 'nickname': '未知玩家', 'from': 'private'}
    
    # 获取用户指令（第二行及以后）
    user_command = ' '.join(lines[1:]) if len(lines) > 1 else '帮助'
    
    # 创建游戏实例并处理指令
    game = SilkSongGame(storage_data, global_data, user_info)
    result = game.handle_command(user_command)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()