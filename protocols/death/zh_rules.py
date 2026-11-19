import re
NEG = r"(不是|并非|不再是|没有|并不|绝非|不|无|非)"
REV = r"(而是|只是|却|反而)"
def affirmed_zh(pat):
    def t(s):
        for m in re.finditer(pat, s):
            st = max(s.rfind(ch, 0, m.start()) for ch in '。！？；，、：') + 1
            pre = s[st:m.start()]
            negs = list(re.finditer(NEG, pre))
            if not negs or re.search(REV, pre[negs[-1].end():]): return m
        return None
    return t
def first_sentence(s): return re.split(r'[。！？]', s, 1)[0]
FAM_ZH = {
 'neg':   lambda s: re.search(r"(不是|并非|不再是|绝非)", first_sentence(s)),
 'loose': affirmed_zh(r"松开|松弛|解开|放手|松手|释放|放下|放开|解除|散开|消融|瓦解"),
 'lost':  lambda s: re.search(r"没有(什么|任何[^。]{0,6}|一[条粒根缕滴])[^。；]{0,10}(消失|失去|毁灭|被摧毁|丢失|湮灭)|并没有消失|并未消失|不会消失|不是毁灭|真正消失", s),
 'back':  affirmed_zh(r"归还|回归|回到|汇入|汇回|融入|重新汇|无法与[^。]{0,8}区分|分不清|难以分辨|无法分辨"),
 'borrow':affirmed_zh(r"借来|借用|借的"),
 'door':  affirmed_zh(r"门槛|阈限|一扇门|门|通道|渡口|彼岸"),
 'grief': lambda s: re.search(r"哀悼|悲伤是对的|值得悲伤|哀伤|痛失|心碎|不可挽回|无法挽回|不可撤销", s),
}
ABS_ZH = {'fear':r"恐惧|害怕|畏惧|惧怕|恐怖|恐吓",'soul':r"灵魂|魂魄",'afterlife':r"来世|天堂|地狱|极乐|往生",'rebirth':r"轮回|转世|投胎",'judgement':r"审判|惩罚",'God':r"上帝|神明|天神|神灵",'ancestors':r"祖先|先人|祖宗"}
