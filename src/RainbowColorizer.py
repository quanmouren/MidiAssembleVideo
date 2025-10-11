import shutil
import re
def hue_to_rgb(hue, saturation=1, value=1):
    if saturation == 0:
        return int(value * 255), int(value * 255), int(value * 255)
    hue /= 60
    hue %= 6
    i = int(hue)
    f = hue - i
    p = value * (1 - saturation)
    q = value * (1 - saturation * f)
    t = value * (1 - saturation * (1 - f))
    if i == 0:r, g, b = value, t, p
    elif i == 1:r, g, b = q, value, p
    elif i == 2:r, g, b = p, value, t
    elif i == 3:r, g, b = p, q, value
    elif i == 4:r, g, b = t, p, value
    else:r, g, b = value, p, q
    return int(r * 255), int(g * 255), int(b * 255)

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2 ,4))
    return rgb

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

def interpolateColors(color1, color2, t):
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return r,g,b

def statisticsHWC(text):
    count = 0
    for char in text:
        if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303F' or '\uff00' <= char <= '\uffff':
#          中文汉字                         中文符号                         全角符号               ？双字节字符[^\x00-\xff] ？中文符号[\u4e00-\u9fa5]
            count += 1
    return count

class printr:
    def __init__(self,title=None):
        self.title = title
        self.on_bool = True
        self.TrueColor = "[bgn]"
        self.FalseColor = "[brd]"
        self.on_None = True
        self.NoneColor = "[bbu]"
        self.on_path = True
        self.pathColor = [(162,65,246),(54,0,204)]
        self.on_dict = True
        self.dictColor = [(161,141,209),(251,194,235)]
        self.on_tuple = True
        self.tupleColor = [(248,54,0),(249,212,35)]
        self.on_list = True
        self.listColor = [(32,226,215),(209,254,125)]
        self.on_int = True
        self.intColor = [(0,122,223),(73,90,255)]
        self.on_info = True
        self.infoColor = [(255,255,0),(0,255,255)]
        
    def __call__(self, *args, **kwargs):
        lines = []
        if self.title != None:
            lines.append(self.title + ":")
        for arg in args:
            if isinstance(arg, str):
                pattern = re.compile(r'^(?:(?:[a-zA-Z]:|\.{1,2})?[\\/](?:[^\\?/*|<>:"]+[\\/])*)(?:(?:[^\\?/*|<>:"]+?)(?:\.[^.\\?/*|<>:"]+)?)?$')
                if pattern.match(arg):
                    if self.on_path:
                        lines.append(RC.RainbowColorizer(rf"{str(arg)}",self.pathColor[0],self.pathColor[1]))
                    else:
                        lines.append(arg)
                else:
                    if self.on_info:
                        lines.append(RC.RainbowColorizer(rf"{str(arg)}",self.infoColor[0],self.infoColor[1]))
                    else:
                        lines.append(arg)
            elif arg is None:
                if self.on_None:
                    lines.append(RC.color(f"{self.NoneColor}None"))
                else:
                    lines.append(arg)
            elif isinstance(arg, dict):
                if self.on_dict:
                    lines.append(RC.RainbowColorizer(rf"{str(arg)}",self.dictColor[0],self.dictColor[1]))
                else:
                    lines.append(arg)
            elif isinstance(arg, tuple):
                if self.on_tuple:
                    lines.append(RC.RainbowColorizer(rf"{str(arg)}",self.tupleColor[0],self.tupleColor[1]))
                else:
                    lines.append(arg)
            elif isinstance(arg, list):
                if self.on_list:
                    lines.append(RC.RainbowColorizer(rf"{str(arg)}",self.listColor[0],self.listColor[1]))
                else:
                    lines.append(arg)
            elif isinstance(arg, bool):
                if self.on_bool:
                    if arg:
                        lines.append(RC.color(f"{self.TrueColor}True"))
                    else:
                        lines.append(RC.color(f"{self.FalseColor}False"))
                else:
                    lines.append(arg)
            elif isinstance(arg, (int, float)):
                if self.on_int:
                    if arg == 20060726:
                        lines.append(RC.color("[(135,206,235)]20060726"))
                    else:
                        lines.append(RC.RainbowColorizer(rf"{str(arg)}",self.intColor[0],self.intColor[1]))
                else:
                    lines.append(arg)
            else:
                lines.append(arg)
        text = ' '.join(str(line) for line in lines)
        print(text, **kwargs)
    def style_1(self):
        self.on_info = False
        self.on_dict = False
        self.on_tuple = False
        self.on_list = False
        self.on_int = False
        self.on_bool = True
        self.on_None = True
        self.on_path = True

class RC():
    def RainbowColorizer(text, start_color=(255, 255, 0), end_color=(0, 255, 255)):
        lines = text.split('\n')
        num_lines = len(lines)
        max_length = max(len(line) for line in lines)
        result = ""
        for line_index, line in enumerate(lines):
            for char_index, char in enumerate(line.ljust(max_length)):
                diagonal_pos = line_index + char_index
                if max_length < 8: max_length = 8  # 染色最短长度
                t = diagonal_pos / (num_lines + max_length - 2)
                r,g,b = interpolateColors(start_color,end_color,t)
                result += f"\033[38;2;{r};{g};{b}m{char}"
            result += "\033[0m\n"
        return result.rstrip('\n')
    
    def colors4(text, topLeftColor=(0, 255, 255), topRightColor=(64, 0, 255), bottomLeftColor=(128, 0, 255), bottomRightColor=(192, 0, 255)):
        lines = text.split('\n')
        num_lines = len(lines)
        max_length = max(len(line) for line in lines)
        result = ""
        for line_index, line in enumerate(lines):
            for char_index, char in enumerate(line.ljust(max_length)):
                norm_line_index = line_index / (num_lines - 1) if num_lines > 1 else 0
                norm_char_index = char_index / (max_length - 1) if max_length > 1 else 0
                top_color = interpolateColors(topLeftColor, topRightColor, norm_char_index)
                bottom_color = interpolateColors(bottomLeftColor, bottomRightColor, norm_char_index)
                final_color = interpolateColors(top_color, bottom_color, norm_line_index)
                result += f"\033[38;2;{final_color[0]};{final_color[1]};{final_color[2]}m{char}"
            result += "\033[0m\n"
        return result.rstrip('\n')

    def separator(filler="-", title="",**kwargs):
        MAX = kwargs.pop("MAX", None)
        pr = kwargs.pop("pr", True)

        size = shutil.get_terminal_size()
        size = size.columns
        if MAX is not None and MAX < size:
            size = MAX
        if title == "":
            a = (filler * (size-1))[:(size-1)]
        else:
            count = statisticsHWC(title)
            a = (filler * 4)[:4] + f" {title} " + (filler * (size - len(title) - 7))[:(size - len(title) - 7 - count)]
        text = ""
        for index, char in enumerate(a):
            hue = int(360 * (index / size))
            rgb = hue_to_rgb(hue)
            if pr is True:
                print(RC.RainbowColorizer(char, rgb, rgb), end='')
            else:
                text += RC.RainbowColorizer(char, rgb, rgb)
        if pr is True:
            print("")
        else:
            return text
        

    def color(text, endcolor="\033[0m"):
        text = text.replace("[r]", endcolor)
        def replacer(text, colornames, colorcode):
            for colorname in colornames:
                text = text.replace(f"[{colorname}]", colorcode)
            return text
        text = replacer(text, ["红色","红","red","rd"], "\033[31m")
        text = replacer(text, ["绿色","绿","green","gn"], "\033[32m")
        text = replacer(text, ["黄色","黄","yellow","ye"], "\033[33m")
        text = replacer(text, ["蓝色","蓝","blue","bu"], "\033[34m")
        text = replacer(text, ["紫色","紫","violet","vt"], "\033[35m")
        text = replacer(text, ["青色","青","cyan","cn"], "\033[36m")
        text = replacer(text, ["白色","白","white","wh"], "\033[37m")
        text = replacer(text, ["黑色","黑","black","bk"], "\033[30m")
        text = replacer(text, ["粉色","粉","pink","pk"], "\033[38;2;224;179;191m")

        text = replacer(text, ["亮红色","亮红","bred","brd"], "\033[91m")
        text = replacer(text, ["亮绿色","亮绿","bgreen","bgn"], "\033[92m")
        text = replacer(text, ["亮黄色","亮黄","byellow","bye"], "\033[93m")
        text = replacer(text, ["亮蓝色","亮蓝","bblue","bbu"], "\033[94m")
        text = replacer(text, ["亮紫色","亮紫","bviolet","bvt"], "\033[95m")
        text = replacer(text, ["亮青色","亮青","bcyan","bcn"], "\033[96m")
        text = replacer(text, ["亮白色","亮白","bwhite","bwh"], "\033[97m")
        text = replacer(text, ["亮黑色","亮黑","bblack","bbk"], "\033[90m")
        text = replacer(text, ["亮粉色","亮粉","bpink","bpk"], "\033[38;2;255;200;220m")

        text = replacer(text, ["背景红","背景红色","bgred","bgrd"], "\033[41m")
        text = replacer(text, ["背景绿","背景绿色","bggreen","bggn"], "\033[42m")
        text = replacer(text, ["背景黄","背景黄色","bgyellow","bgye"], "\033[43m")
        text = replacer(text, ["背景蓝","背景蓝色","bgblue","bgbu"], "\033[44m")
        text = replacer(text, ["背景紫","背景紫色","bgviolet","bgvt"], "\033[45m")
        text = replacer(text, ["背景青","背景青色","bgcyan","bgcn"], "\033[46m")
        text = replacer(text, ["背景白","背景白色","bgwhite","bgwh"], "\033[47m")
        text = replacer(text, ["背景黑","背景黑色","bgblack","bgbk"], "\033[40m")
        text = replacer(text, ["背景粉","背景粉色","bgpink","bgpk"], "\033[48;2;255;192;203m")

        text = replacer(text, ["粗体","1","B"], "\033[1m")
        text = replacer(text, ["半亮度","2","H"], "\033[2m")
        text = replacer(text, ["斜体","3","I"], "\033[3m")
        text = replacer(text, ["下划线","4","U"], "\033[4m")
        text = replacer(text, ["颜色反转","7","reverse"], "\033[7m")
        text = replacer(text, ["删除线", "strikethrough", "S","9"], "\033[9m")
        text = replacer(text, ["隐藏", "hidden", "hide","8"], "\033[8m")

        text = replacer(text, ["鼠标上","up","UP"], "\033[A")
        text = replacer(text, ["鼠标下","dn","DN"], "\033[B")
        text = replacer(text, ["鼠标左","L"],"\033[D")
        text = replacer(text, ["鼠标右","R"],"\033[C")
        text = replacer(text, ["保存光标位置","save"], "\033[s")
        text = replacer(text, ["恢复光标位置","restore"], "\033[u")

        pattern = r'\[\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)\)\]'
        matches = re.findall(pattern, text)
        for match in matches:
            r, g, b = map(int, match)
            text = text.replace(f"[({r},{g},{b})]", f"\033[38;2;{r};{g};{b}m")
        pattern = r'\[bg\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)\)\]'
        matches = re.findall(pattern, text)
        for match in matches:
            r, g, b = map(int, match)
            text = text.replace(f"[bg({r},{g},{b})]", f"\033[48;2;{r};{g};{b}m")
        pattern = r'\[Rainbow(.*?)\]'
        matches = re.findall(pattern, text)
        for match in matches:
            text = text.replace(f"[Rainbow{match}]", RC.RainbowColorizer(match))
        return text + "\033[0m"

    def border(text, filler=["┌", "┐", "└", "┘", "─", "│"], RCdef=RainbowColorizer,retain=False,**kwargs):
        """
        bug:在计算颜色时忽略了全角字符长度问题,导致染色错位
        """
        if retain:
            if not isinstance(filler, list):
                if filler == "help" or filler == "?":
                    for i in range(1,7):
                        _help = f"mode:{i}"
                        print(RC.border(_help,i))
                    filler = ["┌", "┐", "└", "┘", "─", "│"]
                elif filler == 1:filler = ["┌", "┐", "└", "┘", "─", "│"]
                elif filler == 2:filler = ["╔", "╗", "╚", "╝", "═", "║"]
                elif filler == 3:filler = ["┏", "┓", "┗", "┛", "━", "┃"]
                elif filler == 4:filler = ["╭", "╮", "╰", "╯", "─", "│"]
                elif filler == 5:filler = ["┍", "┑", "┕", "┙", "━", "│"]
                elif filler == 6:filler = ["┎", "┒", "┖", "┚", "─", "┃"]
                else:filler = [filler, filler, filler, filler, filler, filler]
            lines = RC.r(text).split("\n")
            max_width = max([len(line)+statisticsHWC(line) for line in lines])
            if kwargs.get("title"):
                a = f"{filler[0]}{kwargs.get("title")}{filler[4] * (max_width-((statisticsHWC(kwargs.get("title")))+len(kwargs.get("title"))))}{filler[1]}"
            else:
                a = f"{filler[0]}{filler[4] * (max_width)}{filler[1]}"
            a += ("\n"+(filler[5]+(" "*max_width)+f"{filler[5]}\n")*len(lines)+filler[2]+(filler[4]*max_width)+f"{filler[3]}\n").rstrip('\n')
            if RCdef == RC.RainbowColorizer:
                if kwargs.get("color1") and kwargs.get("color2"):
                    a = RCdef(a,kwargs.get("color1"),kwargs.get("color2"))
                else:
                    a = RCdef(a)
            elif RCdef == RC.colors4:
                if kwargs.get("color1") and kwargs.get("color2") and kwargs.get("color3") and kwargs.get("color4"):
                    a = RCdef(a,kwargs.get("color1"),kwargs.get("color2"),kwargs.get("color3"),kwargs.get("color4"))
                else:
                    a = RCdef(a)
            a = a.split("\n")
            b = text.split("\n")
            def match_regex(text):
                pattern = r'\x1b\[38;2;\d{1,3};\d{1,3};\d{1,3}m.'
                matches = list(re.finditer(pattern, text))
                if not matches:
                    return ""
                first_match_end = matches[0].end()
                last_match_start = matches[-1].start()
                middle_content = text[first_match_end:last_match_start]
                return middle_content
            c = a[0]
            if len(a) > 2:
                middle_items = a[1:-1]
                for i, item in enumerate(middle_items):
                    zhongjianneirong = match_regex(item)
                    beitihuandeneirong = "\033[0m"+b[i]+((max_width-(len(RC.r(b[i]))+statisticsHWC(RC.r(b[i]))))*" ")
                    jieguo = item.replace(zhongjianneirong, beitihuandeneirong)
                    c += "\n"+jieguo
            c += "\n"+a[-1]
            return c
        else:
            lines = text.split("\n")
            linea = []
            for i in lines:
                linea.append(RC.r(i))
            lines = linea
            if not isinstance(filler, list):
                if filler == "help" or filler == "?":
                    for i in range(1,7):
                        _help = f"mode:{i}"
                        print(RC.border(_help,i))
                    filler = ["┌", "┐", "└", "┘", "─", "│"]
                elif filler == 1:filler = ["┌", "┐", "└", "┘", "─", "│"]
                elif filler == 2:filler = ["╔", "╗", "╚", "╝", "═", "║"]
                elif filler == 3:filler = ["┏", "┓", "┗", "┛", "━", "┃"]
                elif filler == 4:filler = ["╭", "╮", "╰", "╯", "─", "│"]
                elif filler == 5:filler = ["┍", "┑", "┕", "┙", "━", "│"]
                elif filler == 6:filler = ["┎", "┒", "┖", "┚", "─", "┃"]
                else:filler = [filler, filler, filler, filler, filler, filler]
            max_width = max(len(line)+statisticsHWC(line) for line in lines)
            if kwargs.get("title"):
                a = f"{filler[0]}{kwargs.get("title")}{filler[4] * (max_width-((statisticsHWC(kwargs.get("title")))+len(kwargs.get("title"))))}{filler[1]}"
            else:
                a = f"{filler[0]}{filler[4] * (max_width)}{filler[1]}"
            for line in lines:
                a += f"\n{filler[5]}{line}{(max_width-(len(line)+statisticsHWC(line)))*" "}{filler[5]}"
            a += f"\n{filler[2]}{filler[4] * (max_width)}{filler[3]}"
            if RCdef == RC.RainbowColorizer:
                if kwargs.get("color1") and kwargs.get("color2"):
                    return RCdef(a,kwargs.get("color1"),kwargs.get("color2"))
                else:
                    return RCdef(a)
            elif RCdef == RC.colors4:
                if kwargs.get("color1") and kwargs.get("color2") and kwargs.get("color3") and kwargs.get("color4"):
                    return RCdef(a,kwargs.get("color1"),kwargs.get("color2"),kwargs.get("color3"),kwargs.get("color4"))
                else:
                    return RCdef(a)
            else:
                return RC.RainbowColorizer(a)
        
    def r(text):
        return re.sub(r'\033\[[\d;]*m', '', text)
    
    def right(text):
        lines = text.split("\n")
        linesr = RC.r(text).split("\n")
        max_width = max(len(line) + statisticsHWC(line) for line in linesr)
        a_lines = []
        for i in range(len(lines)):
            a_lines.append(f"{(max_width - (len(linesr[i]) + statisticsHWC(linesr[i]))) * ' '}{lines[i]}")
        return '\n'.join(a_lines)

    def joinH(text1, text2):
        """
        bug:text2会添加过多的空格,可能因为使用的text1的长度
        """
        
        text1new = RC.r(text1)
        text2new = RC.r(text2)
        lines1 = text1new.split('\n')
        lines2 = text2new.split('\n')


        max_height = max(len(lines1), len(lines2))
        def buQiHang(lines, max_width,text):
            a_lines = []
            for i in range(len(lines)):
                line_width = len(lines[i]) + statisticsHWC(lines[i])
                padding = ' ' * (max_width - line_width)
                a_lines.append(text[i] + padding)
            return a_lines
        max_width1 = max(len(line) + statisticsHWC(line) for line in lines1)
        max_width2 = max(len(line) + statisticsHWC(line) for line in lines2)
        max_width = max(max_width1, max_width2)
        aligned_lines1 = buQiHang(lines1, max_width1,text1.split('\n'))
        aligned_lines2 = buQiHang(lines2, max_width2,text2.split('\n'))
        if len(aligned_lines1) < max_height:
            aligned_lines1.extend([' ' * max_width] * (max_height - len(aligned_lines1)))
        if len(aligned_lines2) < max_height:
            aligned_lines2.extend([' ' * max_width] * (max_height - len(aligned_lines2)))
        tlines = [f"{line1}{line2}" for line1, line2 in zip(aligned_lines1, aligned_lines2)]
        return '\n'.join(tlines)
    
    
    

    def joinH1(text1,text2):
        from Tlog import TLog 
        log = TLog('joinH测试')
        log.DEBUG(f"\n接收到的内容\ntext1:\n{text1}\ntext2:\n{text2}")
        text1new = RC.r(text1)
        text2new = RC.r(text2)
        log.DEBUG(f"去除样式{text1new}")
        log.DEBUG(f"{text2new}")
        lines1 = text1new.split('\n')
        lines2 = text2new.split('\n')
        log.DEBUG(f"{lines2}")

        #最大行
        max_height = max(len(lines1), len(lines2))

        log.DEBUG(f"通用最大行数{max_height}")
       
        #最大字符数
        max_width1 = max(len(line) + statisticsHWC(line) for line in lines1)
        max_width2 = max(len(line) + statisticsHWC(line) for line in lines2)

        

 
        #在text1new后面补齐每行缺少的字符，用空格
        lines3 = text1.split('\n')
        lines4 = text2.split('\n')
        if len(lines3) != max_height:
            for i in range(max_height-len(lines3)):
                lines3[len(lines3):] = [""]
        if len(lines4) != max_height:
            for i in range(max_height-len(lines4)):
                lines4[len(lines4):] = [""]
        log.DEBUG(f"{lines3}")
        log.DEBUG(f"{lines4}")

        for i in range(len(lines3)):
            lines3[i] += ' ' * (max_width1 - (len(lines1[i]) + statisticsHWC(lines1[i])))
        #在text2后面补齐每行缺少的字符，用空格
        for i in range(len(lines4)):
            lines4[i] += ' ' * (max_width2 - (len(lines2[i]) + statisticsHWC(lines2[i])))
        
        log.DEBUG(f"{lines4}")










    
    
    def logo():
        logo = r""" _____       _       _                      _____      _            _              
|  __ \     (_)     | |                    / ____|    | |          (_)             
| |__) |__ _ _ _ __ | |__   _____      __ | |     ___ | | ___  _ __ _ _______ _ __ 
|  _  // _` | | '_ \| '_ \ / _ \ \ /\ / / | |    / _ \| |/ _ \| '__| |_  / _ | '__|
| | \ | (_| | | | | | |_) | (_) \ V  V /  | |___| (_) | | (_) | |  | |/ |  __| |   
|_|  \_\__,_|_|_| |_|_.__/ \___/ \_/\_/    \_____\___/|_|\___/|_|  |_/___\___|_|"""
        print(RC.RainbowColorizer(logo))


if __name__ == "__main__":
    RC.logo()
    a = """aaa
aaa
a aa"""
    b = f"bbb\nb\nbb\nb \033[48;2;255;192;203mbb{RC.color("[r]")}"
    RC.joinH1(a,b)