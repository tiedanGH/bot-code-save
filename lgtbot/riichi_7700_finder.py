#!/usr/bin/env python3
# riichi_7700_finder.py
"""
用法:
    pip install mahjong
    python riichi_7700_finder.py "111233344456699m1222345888s"
"""
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.shanten import Shanten

import sys, time
sys.setrecursionlimit(20000)

# ---------------- 输入解析与规范化 ----------------
def normalize_and_parse_input(s):
    s = s.strip()
    man = pin = sou = honors = ""
    buf = ""
    for ch in s:
        if ch in "mpsz":
            if ch == 'm':
                man += buf
            elif ch == 'p':
                pin += buf
            elif ch == 's':
                sou += buf
            else:
                honors += buf
            buf = ""
        else:
            buf += ch
    nonred = [0]*34
    red = [0]*34
    def add_group(group_str, suit_base):
        for ch in group_str:
            if ch == '0':
                d = 5
                idx = suit_base + (d-1)
                red[idx] += 1
            else:
                d = int(ch)
                idx = suit_base + (d-1)
                nonred[idx] += 1
    add_group(man, 0); add_group(pin, 9); add_group(sou, 18); add_group(honors, 27)

    def build_group(suit_base):
        parts = []
        for d in range(1,10):
            idx = suit_base + (d-1)
            parts += ['0'] * red[idx]
            parts += [str(d)] * nonred[idx]
        return "".join(parts)
    man_s = build_group(0); pin_s = build_group(9); sou_s = build_group(18)
    honors_s = []
    for d in range(1,8):
        idx = 27 + (d-1)
        honors_s += [str(d)] * (red[idx] + nonred[idx])
    honors_s = "".join(honors_s)
    normalized = ""
    if man_s: normalized += man_s + "m"
    if pin_s: normalized += pin_s + "p"
    if sou_s: normalized += sou_s + "s"
    if honors_s: normalized += honors_s + "z"
    return nonred, red, normalized

def counts_to_notation(nonred_counts, red_counts):
    man = []; pin = []; sou = []; hon = []
    for i in range(34):
        nr = nonred_counts[i]; rr = red_counts[i]
        if nr + rr == 0: continue
        if 0 <= i <= 8:
            d = i - 0 + 1
            man += ['0'] * rr + [str(d)] * nr
        elif 9 <= i <= 17:
            d = i - 9 + 1
            pin += ['0'] * rr + [str(d)] * nr
        elif 18 <= i <= 26:
            d = i - 18 + 1
            sou += ['0'] * rr + [str(d)] * nr
        else:
            d = i - 27 + 1
            hon += [str(d)] * (nr + rr)
    s = ""
    if man: s += "".join(man) + "m"
    if pin: s += "".join(pin) + "p"
    if sou: s += "".join(sou) + "s"
    if hon: s += "".join(hon) + "z"
    return s

def counts_to_tile_string_kwargs(nonred_counts, red_counts, extra_one_tile_index=None, extra_one_tile_is_red=False):
    man = []; pin = []; sou = []; hon = []
    for i in range(34):
        nr = nonred_counts[i]; rr = red_counts[i]
        if extra_one_tile_index is not None and i == extra_one_tile_index:
            if extra_one_tile_is_red:
                rr += 1
            else:
                nr += 1
        if nr + rr == 0: continue
        if 0 <= i <= 8:
            d = i - 0 + 1
            man += ['0'] * rr + [str(d)] * nr
        elif 9 <= i <= 17:
            d = i - 9 + 1
            pin += ['0'] * rr + [str(d)] * nr
        elif 18 <= i <= 26:
            d = i - 18 + 1
            sou += ['0'] * rr + [str(d)] * nr
        else:
            d = i - 27 + 1
            hon += [str(d)] * (nr + rr)
    return {'man': "".join(man), 'pin': "".join(pin), 'sou': "".join(sou), 'honors': "".join(hon)}

def format_tile_idx(i, is_red=False):
    if 0 <= i <= 8:
        s = f"{i-0+1}m"
    elif 9 <= i <= 17:
        s = f"{i-9+1}p"
    elif 18 <= i <= 26:
        s = f"{i-18+1}s"
    else:
        s = f"{i-27+1}z"
    if is_red and '5' in s:
        s = s.replace('5', '0')
    return s

# ---------------- 和牌 / 四暗刻 检测 ----------------
def is_kokushi(counts):
    terminals_honors = [0,8,9,17,18,26] + list(range(27,34))
    for i in terminals_honors:
        if counts[i] <= 0:
            return False
    for i in terminals_honors:
        if counts[i] >= 2:
            return True
    return False

def is_chiitoitsu(counts):
    if sum(counts) != 14:
        return False
    pairs = sum(c // 2 for c in counts)
    return pairs == 7

def can_form_melds(counts):
    for i in range(34):
        if counts[i] > 0:
            break
    else:
        return True
    if counts[i] >= 3:
        counts[i] -= 3
        if can_form_melds(counts):
            counts[i] += 3
            return True
        counts[i] += 3
    if (0 <= i <= 6) or (9 <= i <= 15) or (18 <= i <= 24):
        if counts[i+1] > 0 and counts[i+2] > 0:
            counts[i] -= 1; counts[i+1] -= 1; counts[i+2] -= 1
            if can_form_melds(counts):
                counts[i] += 1; counts[i+1] += 1; counts[i+2] += 1
                return True
            counts[i] += 1; counts[i+1] += 1; counts[i+2] += 1
    return False

def is_standard_agari(counts):
    if sum(counts) != 14:
        return False
    for i in range(34):
        if counts[i] >= 2:
            counts[i] -= 2
            ccopy = counts[:]
            if can_form_melds(ccopy):
                counts[i] += 2
                return True
            counts[i] += 2
    return False

def is_agari_shape(total_counts):
    if sum(total_counts) != 14:
        return False
    if is_kokushi(total_counts): return True
    if is_chiitoitsu(total_counts): return True
    if is_standard_agari(total_counts): return True
    return False

def is_su_anko(total_counts):
    """
    手动检测四暗刻（四暗刻要求：14张，存在一个雀头，剩余全部由四个刻子组成）
    注意：这里不判断副露/暗明（本脚本生成的手默认闭门），仅按13张+补一张的结构判定是否符合纯刻子结构。
    返回 True/False。
    """
    if sum(total_counts) != 14:
        return False
    # 尝试每个可能作雀头的位置
    for i in range(34):
        if total_counts[i] >= 2:
            tmp = total_counts.copy()
            tmp[i] -= 2
            # 检查剩余 12 张是否都可按刻子分解（即每个牌数都能被 3 整除）
            ok = True
            for j in range(34):
                if tmp[j] % 3 != 0:
                    ok = False
                    break
            if ok:
                # 还可以确认总张数为12且每组为刻子
                return True
    return False

# ---------------- 主枚举与计算 ----------------
def find_tenpai_hands(input_str, target_point=7700, assume_ippatsu=False, dealer=False, verbose=False):
    nonred_avail, red_avail, normalized_input = normalize_and_parse_input(input_str)
    total_available = [nonred_avail[i] + red_avail[i] for i in range(34)]
    total_tiles = sum(total_available)
    if verbose:
        print("输入总牌数 =", total_tiles)
        print("候选牌池（规范化）:", normalized_input)

    calc = HandCalculator()
    shanten_calc = Shanten()
    HAND_SIZE = 13
    results = []
    start_time = time.time()

    partial_nonred = [0]*34
    partial_red = [0]*34
    shanten_cache = {}
    calls = 0
    pruned = 0

    def safe_tiles34_from_counts(pn, pr):
        notation = counts_to_notation(pn, pr)
        man = pin = sou = honors = ""
        if 'm' in notation:
            man = notation.split('m')[0]
        if 'p' in notation:
            pin = notation.split('p')[0].split('m')[-1]
        if 's' in notation:
            sou = notation.split('s')[0].split('p')[-1]
        if 'z' in notation:
            honors = notation.split('z')[0].split('s')[-1]
        return TilesConverter.string_to_34_array(man=man, pin=pin, sou=sou, honors=honors)

    def dfs(idx, remaining):
        nonlocal calls, pruned
        if idx == 34:
            calls += 1
            if remaining != 0:
                return
            total_counts = [partial_nonred[i] + partial_red[i] for i in range(34)]
            key = tuple(total_counts)
            sh = shanten_cache.get(key)
            if sh is None:
                try:
                    tiles34 = safe_tiles34_from_counts(partial_nonred, partial_red)
                    sh = shanten_calc.calculate_shanten(tiles34)
                except Exception:
                    sh = 100
                shanten_cache[key] = sh
            if sh != 0:
                return

            waits = []
            best_point = 0
            for t in range(34):
                # 尝试合理的赤与非赤变体（赤必须存在于输入）
                is_five = (t in (4, 13, 22))
                variants = [False]
                if is_five and red_avail[t] > 0:
                    variants = [False, True]
                for is_red_win in variants:
                    total_after = total_counts.copy()
                    total_after[t] += 1
                    # 物理上不可超过四张
                    if total_after[t] > 4:
                        continue
                    if not is_agari_shape(total_after):
                        continue

                    # 先用 mahjong 库尝试计分
                    result = None
                    ron_point = None
                    try:
                        kwargs = counts_to_tile_string_kwargs(partial_nonred, partial_red, extra_one_tile_index=t, extra_one_tile_is_red=is_red_win)
                        tiles136 = TilesConverter.string_to_136_array(man=kwargs['man'], pin=kwargs['pin'], sou=kwargs['sou'], honors=kwargs['honors'])
                        win_kwargs = counts_to_tile_string_kwargs([0]*34, [0]*34, extra_one_tile_index=t, extra_one_tile_is_red=is_red_win)
                        win_tile_list = TilesConverter.string_to_136_array(man=win_kwargs['man'], pin=win_kwargs['pin'], sou=win_kwargs['sou'], honors=win_kwargs['honors'])
                        if win_tile_list:
                            win_tile = win_tile_list[0]
                            config = HandConfig(is_riichi=True, is_tsumo=False, is_ippatsu=assume_ippatsu, player_wind=None, round_wind=None, options=None)
                            result = calc.estimate_hand_value(tiles136, win_tile, config=config, dora_indicators=None)
                            try:
                                ron_point = result.cost.get('main', None)
                            except Exception:
                                ron_point = None
                    except Exception:
                        result = None
                        ron_point = None

                    # 手动检测四暗刻（若计分库没有返回）
                    suanko_flag = False
                    if is_su_anko(total_after):
                        # 如果 mahjong 库已经把四暗刻作为 yakuman 返回，就不需要重复
                        yaku_names = []
                        if result is not None:
                            yaku_list = getattr(result, 'yaku', None)
                            if yaku_list:
                                try:
                                    yaku_names = [str(y) for y in yaku_list]
                                except Exception:
                                    yaku_names = []
                        # 名称可能不同，判断已有列表中是否包含四暗刻相关词
                        found = any(('Su' in n or '四暗' in n or '安' in n or 'Anko' in n or '暗刻' in n) for n in yaku_names)
                        if not found:
                            suanko_flag = True
                            # 若计分库没有给点数，我们在这里用标准 yakuman 点数（非庄家 Ron = 32000，庄家 Ron = 48000）
                            if ron_point is None:
                                ron_point = 48000 if dealer else 32000

                    waits.append({
                        'tile_index': t,
                        'is_red': is_red_win,
                        'result': result,
                        'ron_point': ron_point,
                        'suanko_detected': suanko_flag
                    })
                    if ron_point is not None and ron_point > best_point:
                        best_point = ron_point

            if not waits:
                return

            best_point = max([w['ron_point'] for w in waits if w['ron_point'] is not None] + [0])
            results.append({
                'hand_nonred': partial_nonred.copy(),
                'hand_red': partial_red.copy(),
                'waits': waits,
                'best_point': best_point
            })
            return

        max_take = min(total_available[idx], remaining)
        for k in range(0, max_take+1):
            if k == 0:
                partial_total = [partial_nonred[i] + partial_red[i] for i in range(34)]
                key = tuple(partial_total)
                sh = shanten_cache.get(key)
                if sh is None:
                    try:
                        tiles34 = safe_tiles34_from_counts(partial_nonred, partial_red)
                        sh = shanten_calc.calculate_shanten(tiles34)
                    except Exception:
                        sh = 100
                    shanten_cache[key] = sh
                if sh > remaining:
                    pruned += 1
                    return
                dfs(idx+1, remaining)
                continue
            avail_red = red_avail[idx]
            avail_nonred = nonred_avail[idx]
            rmin = max(0, k - avail_nonred)
            rmax = min(k, avail_red)
            for r in range(rmin, rmax+1):
                nr_take = k - r
                partial_red[idx] += r
                partial_nonred[idx] += nr_take
                partial_total = [partial_nonred[i] + partial_red[i] for i in range(34)]
                key = tuple(partial_total)
                sh = shanten_cache.get(key)
                if sh is None:
                    try:
                        tiles34 = safe_tiles34_from_counts(partial_nonred, partial_red)
                        sh = shanten_calc.calculate_shanten(tiles34)
                    except Exception:
                        sh = 100
                    shanten_cache[key] = sh
                if sh <= (remaining - k):
                    dfs(idx+1, remaining - k)
                else:
                    pruned += 1
                partial_red[idx] -= r
                partial_nonred[idx] -= nr_take

    dfs(0, HAND_SIZE)

    # 排序：按 best_point 降序，best 相同按等待数降序
    results.sort(key=lambda x: (-(x['best_point'] or 0), -len(x['waits'])))

    elapsed = time.time() - start_time
    if verbose:
        print(f"枚举完成：calls={calls}, pruned={pruned}, found_hand_count={len(results)}, time={elapsed:.2f}s")
    good = [r for r in results if r['best_point'] is not None and r['best_point'] >= target_point]
    return results, good

# ---------------- 输出 ----------------
def hand_counts_to_notation(nonred, red):
    return counts_to_notation(nonred, red)

def pretty_print_results(results):
    if not results:
        print("（无符合的听牌组合）")
        return
    for idx, r in enumerate(results, 1):
        hand_str = hand_counts_to_notation(r['hand_nonred'], r['hand_red'])
        print(f"--- 听牌组合 #{idx}: {hand_str}  (best 点数 {r['best_point']})")
        for w in r['waits']:
            tile_str = format_tile_idx(w['tile_index'], w['is_red'])
            res = w['result']
            suanko_flag = w.get('suanko_detected', False)
            # yaku 输出
            yaku_names = []
            if res is not None:
                try:
                    yaku_list = getattr(res, 'yaku', None)
                    if yaku_list:
                        yaku_names = [str(y) for y in yaku_list]
                except Exception:
                    yaku_names = []
            if suanko_flag:
                # 将中文四暗刻插到显示里（若库里已经有相应 yakuman 则避免重复）
                if not any('四暗' in n or 'Su' in n or 'Anko' in n for n in yaku_names):
                    yaku_names.append('四暗刻 (手动检测)')
            fu = getattr(res, 'fu', '?') if res is not None else '?'
            han = getattr(res, 'han', '?') if res is not None else '?'
            point = w.get('ron_point', '?')
            print(f"    听牌: {tile_str:>4}  |  役: {yaku_names}  |  符: {fu}  番: {han}  点数(Ron): {point}")
        print()

# ---------------- main ----------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python riichi_7700_finder.py \"123m456p357z...\"")
        sys.exit(1)
    input_pool = sys.argv[1]
    nonred_avail, red_avail, normalized_input = normalize_and_parse_input(input_pool)
    all_res, good_res = find_tenpai_hands(normalized_input, target_point=7700, assume_ippatsu=False, verbose=True)
    if good_res:
        print("找到满足 >=7700 点的听牌组合（不含一发）:")
        pretty_print_results(good_res)
        sys.exit(0)
    all_res_ip, good_res_ip = find_tenpai_hands(normalized_input, target_point=7700, assume_ippatsu=True, verbose=True)
    if good_res_ip:
        print("没有直接满足的，但开启一发后能满足的听牌组合（假设一发成立）:")
        pretty_print_results(good_res_ip)
        sys.exit(0)
    print("没救了，弃胡吧")
