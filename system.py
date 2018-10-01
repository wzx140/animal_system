# -*- coding: utf-8 -*-
import collections


# 根据路径加载规则
def loads(path):
    # 条件
    P_list = []
    # 结果
    Q_list = []
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # 去除回车
            line = line.strip('\n')
            if line:
                data_list = line.split(' ')
                # print(data_list[:-1])
                P_list.append(data_list[:-1])
                Q_list.append(data_list[-1])
    # print('规则加载完成')
    return P_list, Q_list


# 拓扑排序
def topological(P_list, Q_list):
    # 规则
    rule = collections.OrderedDict()

    # 计算入度
    ind_list = []
    for i in P_list:
        sum = 0
        for x in i:
            if Q_list.count(x) > 0:
                sum += Q_list.count(x)
        ind_list.append(sum)

    # 拓扑排序
    while (1):
        if ind_list.count(-1) == len(ind_list):
            break

        for i, ind in enumerate(ind_list):
            if ind == 0:
                rule[tuple(P_list[i])] = Q_list[i]
                ind_list[i] = -1
                # 更新入度
                for j, P in enumerate(P_list):
                    if Q_list[i] in P:
                        ind_list[j] -= 1
    return rule


# 推断
def infer(input_list, rule, display=False):
    result = []
    flag = False
    process = ''
    for key in rule.keys():
        # 如果所有规则都在输入中
        if list_in_set(key, input_list):
            # 添加推导出的条件
            input_list.append(rule[key])
            result.append(rule[key])
            process += '{key} 推导出 {value}\n'.format(key=key, value=input_list[-1])
            flag = True

    if flag:
        if display:
            return process + '\n' + '最终推出: ' + str(result[-1])
        else:
            return '最终推出: ' + str(result[-1])
    else:
        return '无法推出'


# 判断list中所有元素是否都在集合set中
def list_in_set(list, set):
    for i in list:
        if i not in set:
            return False
    return True


def run(text, display):
    if display == 'true':
        dis = True
    else:
        dis = False
    input_list = text.split(' ')
    P_list, Q_list = loads('data.txt')
    rule = topological(P_list, Q_list)
    return infer(input_list, rule, display=dis)


# 单机控制台使用
if __name__ == '__main__':
    print('每个特征之间用单个空白符相隔，请使用完整特征')
    print('如：蹄类->有蹄类，暗斑->暗斑点，x->x类(如 鸟->鸟类)，黑白->黑白色')
    print('输入1退出')
    while (1):
        print('请输入特征:')
        text = input()
        if text == '1':
            break
        print(run(text, display='true'))
