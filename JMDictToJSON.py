import sys
import json
import pdb
import os
import codecs
import pickle as pickle
import queue
import re
import time
import math

class Text:
    def getWhitespace(self, indent, initialIndent) -> str:
        return ' '*(indent + initialIndent)

    def getNewline(self, indent) -> str:
        return '' if indent == 0 else '\n'

    def getSpace(self, indent) -> str:
        return '' if indent == 0 else ' '

class JMdict:
    def __init__(self):
        self.entries = []

    def addEntry(self, entry) -> None:
        self.entries.append(entry)


# k_ele*
# r_ele+
# sense+
class Entry(Text):
    def __init__(self, ent_seq, k_ele, r_ele, sense):
        self.ent_seq = ent_seq
        self.k_ele = k_ele
        self.r_ele = r_ele
        self.sense = sense

    def getEnt_seqString(self, indent=0, initalIndent=0):
        return self.ent_seq.toString(indent, initalIndent)

    def getEleString(self, name, ele, indent=0, initialIndent=0):
        if len(ele) == 0: return ''
        whitespace1 = self.getWhitespace(indent, initialIndent)
        whitespace2 = self.getWhitespace(indent, initialIndent + indent)
        newline = self.getNewline(indent)
        space = self.getSpace(indent)
        msg = ',{newline}{whitespace1}{name}:{space}['.format(name=name, newline=newline, whitespace1=whitespace1, space=space)
        for i in range(len(ele)):
            e = ele[i]
            comma = ',' if i > 0 else ''
            value = e.toString(indent, initialIndent + indent*2)
            msg += '{comma}{newline}{whitespace2}{value}'.format(comma=comma, newline=newline, whitespace2=whitespace2, value=value)
        msg += '{newline}{whitespace1}]'.format(newline=newline, whitespace1=whitespace1)
        return msg

    def toString(self, indent=0, initialIndent=0, comma=',') -> str:
        msg = ""
        ent_seq = self.getEnt_seqString(indent, initialIndent)
        k_ele = self.getEleString('k_ele', self.k_ele, indent, initialIndent)
        r_ele = self.getEleString('r_ele', self.r_ele, indent, initialIndent)
        sense = self.getEleString('sense', self.sense, indent, initialIndent)
        newline = self.getNewline(indent)
        whitespace = self.getWhitespace(indent, initialIndent-indent)
        msg = '{{{ent_seq}{k_ele}{r_ele}{sense}{newline}{whitespace}}}{comma}'.format(ent_seq=ent_seq, k_ele=k_ele, r_ele=r_ele, sense=sense, newline=newline, whitespace=whitespace, comma=comma)
        return msg

# all *
class Sense:
    def __init__(self, stagk, stagr, pos, xref, ant, field, misc, s_inf, lsource, dial, gloss):
        self.fields = {}
        if (not len(stagk) == 0):
            self.fields['stagk'] = Stagk(stagk) 
        if (not len(stagr) == 0):
            self.fields['stagr'] = Stagr(stagr)
        if (not len(pos) == 0):
            self.fields['pos'] = Pos(pos)
        if (not len(xref) == 0):
            self.fields['xref'] = Xref(xref)
        if (not len(ant) == 0):
            self.fields['ant'] = Ant(ant)
        if (not len(field) == 0):
            self.fields['field'] = Field(field)
        if (not len(misc) == 0):
            self.fields['misc'] = Misc(misc)
        if (not len(s_inf) == 0):
            self.fields['s_inf'] = S_inf(s_inf)
        if (not len(lsource) == 0):
            self.fields['lsource'] = Lsource(lsource)
        if (not len(dial) == 0):
            self.fields['dial'] = Dial(dial)
        if (not len(gloss) == 0):
            self.fields['gloss'] = Gloss(gloss)

    def toString(self, indent=0, initialIndent=0):
        newline = self.getNewline(indent)
        whitespace1 = self.getWhitespace(indent, initialIndent-indent)
        msg = '{'
        addComma = False
        for item in self.fields.items():
            comma = ',' if addComma else ''
            addComma = True
            value = item[1].toString(indent, initialIndent)
            msg += '{comma}{value}'.format(comma=comma, value=value)
        msg += '{newline}{whitespace1}}}'.format(newline=newline, whitespace1=whitespace1)
        return msg

class K_Ele:
    def __init__(self, keb, ke_inf, ke_pri):
        self.keb = keb
        self.ke_inf = Ke_inf(ke_inf)
        self.ke_pri = Ke_pri(ke_pri)

    def toString(self, indent=0, initialIndent=0):
        keb = self.keb.toString(indent, initialIndent, '')
        ke_inf = self.ke_inf.toString(indent, initialIndent, ',')
        ke_pri = self.ke_pri.toString(indent, initialIndent, ',')
        newline = self.getNewline(indent)
        whitespace = self.getWhitespace(indent, initialIndent - indent)
        msg = '{{{keb}{ke_inf}{ke_pri}{newline}{whitespace}}}'.format(keb = keb, ke_inf = ke_inf, ke_pri = ke_pri, newline=newline, whitespace=whitespace)
        return msg

class R_Ele:
    def __init__(self, reb, re_nokanji, re_restr, re_inf, re_pri):
        self.reb = reb
        self.re_nokanji = Re_nokanji(re_nokanji)
        self.re_restr = Re_restr(re_restr)
        self.re_inf = Re_inf(re_inf)
        self.re_pri = Re_pri(re_pri)

    def toString(self, indent=0, initialIndent=0):
        reb = self.reb.toString(indent, initialIndent, '')
        re_nokanji = self.re_nokanji.toString(indent, initialIndent, ',')
        re_restr = self.re_restr.toString(indent, initialIndent, ',')
        re_inf = self.re_inf.toString(indent, initialIndent, ',')
        re_pri = self.re_pri.toString(indent, initialIndent, ',')
        newline = self.getNewline(indent)
        whitespace = self.getWhitespace(indent, initialIndent - indent)
        msg = '{{{reb}{re_nokanji}{re_restr}{re_inf}{re_pri}{newline}{whitespace}}}'.format(reb=reb, re_nokanji=re_nokanji, re_restr = re_restr, re_inf=re_inf, re_pri=re_pri, newline=newline, whitespace=whitespace)
        return msg

class Entities:
    def __init__(self):
        self.entities = {}

    def addEntityType(self, entityType, entityName):
        self.entities[entityType] = {'__name__': entityName}

    def addEntity(self, entityType, entityName, entityValue):
        self.entities[entityType][entityName] = entityValue

class PCData(Text):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def toString(self, indent=0, initialIndent=0, comma=''):
        value= self.getValue()
        if type(value) == bool:
            if value == False:
                return ''
        elif value == None or len(value) == 0:
            return ''
        newline = self.getNewline(indent)
        whitespace = self.getWhitespace(indent, initialIndent)
        name = self.getName()
        space = self.getSpace(indent)
        msg = '{comma}{newline}{indent}{name}:{space}"{value}"'.format(comma=comma, indent=whitespace, name=name, value=value, space=space, newline=newline)
        return msg

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

class PCDataArray(PCData):
    def __init__(self, name, values):
        pcdata = []
        for value in values:
            pcdata.append(value)
        super().__init__(name, pcdata)

    def toString(self, indent=0, initialIndent=0, comma=''):
        values = self.getValue()
        if len(values) == 0: return ''
        newline = self.getNewline(indent)
        whitespace1 = self.getWhitespace(indent, initialIndent)
        whitespace2 = self.getWhitespace(indent*2, initialIndent)
        space = self.getSpace(indent)
        name = self.getName()
        msg = "{comma}{newline}{indent1}{name}:{space}[".format(comma=comma, newline=newline, indent1=whitespace1, name=name, space=space)
        for i in range(len(values)):
            value = values[i].getValue()
            msg += '{newline}{whitespace2}"{value}"'.format(newline = newline, whitespace2 = whitespace2, value=value)
            msg += ',' if i < len(values) - 1 else ''
        msg += "{newline}{indent1}]".format(newline=newline, indent1=whitespace1)
        return msg

class Ent_seq(PCData):
    def __init__(self, value):
        super().__init__('ent_seq', value)

class Keb(PCData):
    def __init__(self, value):
        super().__init__('keb', value)

class Ke_inf(PCDataArray):
    def __init__(self, value):
        super().__init__('ke_inf', value)

class Ke_pri(PCDataArray):
    def __init__(self, value):
        super().__init__('ke_pri', value)

class Reb(PCData):
    def __init__(self, value):
        super().__init__('reb', value)

class Re_nokanji(PCData):
    def __init__(self, value):
        super().__init__('re_nokanji', value)

    def toString(self, indent, initialIndent, comma):
        if self.getValue():
            return super(Re_nokanji, self).toString(indent, initialIndent, comma)
        else:
            return ''
        

class Re_restr(PCDataArray):
    def __init__(self, value):
        super().__init__('re_restr', value)

class Re_inf(PCDataArray):
    def __init__(self, value):
        super().__init__('re_inf', value)

class Re_pri(PCDataArray):
    def __init__(self, value):
        super().__init__('re_pri', value)

class Stagk(PCDataArray):
    def __init__(self, value):
        super().__init__('stagk', value)

class Stagr(PCDataArray):
    def __init__(self, value):
        super().__init__('stagr', value)

class Pos(PCDataArray):
    def __init__(self, value):
        super().__init__('pos', value)

class Xref(PCDataArray):
    def __init__(self, value):
        super().__init__('xref', value)

class Ant(PCDataArray):
    def __init__(self, value):
        super().__init__('ant', value)

class Field(PCDataArray):
    def __init__(self, value):
        super().__init__('field', value)

class Misc(PCDataArray):
    def __init__(self, value):
        super().__init__('misc', value)

class S_inf(PCDataArray):
    def __init__(self, value):
        super().__init__('s_inf', value)

class Lsource(PCDataArray):
    def __init__(self, value):
        super().__init__('lsource', value)

class Dial(PCDataArray):
    def __init__(self, value):
        super().__init__('dial', value)

class Gloss(PCDataArray):
    def __init__(self, value):
        super().__init__('gloss', value)

cDir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(cDir, 'JMdict_e')

class Controller(Text):
    def __init__(self):
        self.entities = Entities()
        self.jmdict = JMdict()
        self.entries = {}

    def addEntityType(self, line) -> str:
        line = re.sub(r'[<>]', '', line)
        words = line.split(' ')
        entityType = words[0]
        entityName = words[1] if len(words) > 2 else words[0]
        self.entities.addEntityType(entityType, entityName)
        return entityType
        
    def processEntities(self, line):
        line = re.sub(r'<!-- | -->\n', '', line)
        if '<' in line:
            entityType = self.addEntityType(line)
            line = self.read_file.readline()
            while ('<!--' not in line):
                line = re.sub(r'<!ENTITY |>', '', line)
                words = line.split(' ', maxsplit=1)
                entityName = words[0]
                entityValue = words[1]
                self.entities.addEntity(entityType, entityName, entityValue)
                line = self.read_file.readline()
                
    def parseEnt_seq(self, line) -> str:
        return Ent_seq(re.sub(r'<[/]*ent_seq>(\n)*', '', line))

    def parseKeb(self, line) -> str:
        return PCData('keb', re.sub(r'<[/]*keb>(\n)*', '', line))

    def parseKe_inf(self, line) -> str:
        return PCData('ke_inf', re.sub(r'<[/]*ke_inf>(\n)*|&|;', '', line))

    def parseKe_pri(self, line) -> str:
        return PCData('ke_pri', re.sub(r'<[/]*ke_pri>(\n)*', '', line))

    def processK_Ele(self):
        line = self.read_file.readline()
        keb = self.parseKeb(line)
        ke_inf = []
        ke_pri = []
        line = self.read_file.readline()
        while '</k_ele>' not in line:
            if 'ke_inf' in line:
                ke_inf.append(self.parseKe_inf(line))
            elif 'ke_pri' in line:
                ke_pri.append(self.parseKe_pri(line))
            line = self.read_file.readline()
        return K_Ele(keb, ke_inf, ke_pri)



    def parseReb(self, line) -> str:
        return Reb(re.sub(r'<[/]*reb>(\n)*', '', line))
    
    def parseRe_restr(self, line) -> str:
        return PCData('re_restr', re.sub(r'<[/]*re_restr>(\n)*', '', line))
    
    def parseRe_pri(self, line) -> str:
        return PCData('re_pri', re.sub(r'<[/]*re_pri>(\n)*', '', line))
    
    def parseRe_inf(self, line) -> str:
        return PCData('re_inf', re.sub(r'(;)*<[/]*re_inf>(\n)*(&)*', '', line))
    
    def processR_Ele(self):
        line = self.read_file.readline()
        reb = self.parseReb(line)
        line = self.read_file.readline()
        if 're_nokanji' in line:
            re_nokanji = True
            line = self.read_file.readline()
        else:
            re_nokanji = False
        re_restr = []
        re_inf = []
        re_pri = []
        while '</r_ele>' not in line:
            if 're_restr' in line:
                re_restr.append(self.parseRe_restr(line))
            elif 're_inf' in line:
                re_inf.append(self.parseRe_inf(line))
            elif 're_pri' in line:
                re_pri.append(self.parseRe_pri(line))
            line = self.read_file.readline()
        return R_Ele(reb, re_nokanji, re_restr, re_inf, re_pri)
            
    
    def getStagk(self, line) -> str:
        return PCData('stagk', re.sub(r'<[/]*stagk>(\n)*', '', line))
    
    def getStagr(self, line) -> str:
        return PCData('stagr', re.sub(r'<[/]*stagr>(\n)*', '', line))
    
    def getPos(self, line) -> str:
        return PCData('pos', re.sub(r'(;)*<[/]*pos>(\n)*(&)*', '', line))
    
    def getAnt(self, line) -> str:
        return PCData('ant', re.sub(r'<[/]*ant>(\n)*', '', line))
    
    def getField(self, line) -> str:
        return PCData('field', re.sub(r'(;)*<[/]*field>(\n)*(&)*', '', line))
    
    def getMisc(self, line) -> str:
        return PCData('misc', re.sub(r'(;)*<[/]*misc>(\n)*(&)*', '', line))
    
    def getS_inf(self, line) -> str:
        return PCData('s_inf', re.sub(r'<[/]*s_inf>(\n)*', '', line))
    
    def getLSource(self, line) -> str:
        if 'xml:lang' in line:
            return PCData('lsource', re.search(r'xml:lang="([a-z]*)"', line).group(1))

    def getDial(self, line) -> str:
        return PCData('dial', re.sub(r'(;)*<[/]*dial>(\n)*(&)*', '', line))
    
    def getGloss(self, line) -> str:
        return PCData('gloss', re.sub(r'<[/]*gloss>(\n)*', '', line))
    
    def getXref(self, line) -> str:
        return PCData('xref', re.sub(r'<[/]*xref>(\n)*', '', line))
    
    def processSense(self):
        stagk = []
        stagr = []
        pos = []
        xref = []
        ant = []
        field = []
        misc = []
        s_inf = []
        lsource = []
        dial = []
        gloss = []
        line = self.read_file.readline()
        while '</sense>' not in line:
            if '<stagk>' in line:
                stagk.append(self.getStagk(line))
            elif '<stagr>' in line:
                stagr.append(self.getStagr(line))
            elif '<pos>' in line:
                pos.append(self.getPos(line))
            elif '<xref>' in line:
                xref.append(self.getXref(line))
            elif '<ant>' in line:
                ant.append(self.getAnt(line))
            elif '<field>' in line:
                field.append(self.getField(line))
            elif '<misc>' in line:
                misc.append(self.getMisc(line))
            elif '<s_inf>' in line:
                s_inf.append(self.getS_inf(line))
            elif '<lsource' in line and 'xml:lang' in line:
                lsource.append(self.getLSource(line))
            elif '<dial>' in line:
                dial.append(self.getDial(line))
            elif '<gloss>' in line:
                gloss.append(self.getGloss(line))
            line = self.read_file.readline()
        return Sense(stagk, stagr, pos, xref, ant, field, misc, s_inf, lsource, dial, gloss)
    
    def processEntry(self):
        line = self.read_file.readline()
        ent_seq = self.parseEnt_seq(line)
        line = self.read_file.readline()
        k_ele = []
        r_ele = []
        sense = []
        self.count += 1
        while '</entry>' not in line:
            if 'k_ele' in line:
                k_ele.append(self.processK_Ele())
            elif 'r_ele' in line:
                r_ele.append(self.processR_Ele())
            elif 'sense' in line:
                sense.append(self.processSense())
            line = self.read_file.readline()
        self.entries[ent_seq.getValue()] = Entry(ent_seq, k_ele, r_ele, sense)

    def loadDict(self, filename):
        self.count = 0
        self.read_file = open(filename, "r", encoding="utf8")
##          DON'T USE READLINES - No need to load into memory
        line = self.read_file.readline()
        while (line != ''):
            if ('<!-- ' in line):
                if ('-->' in line):
                    self.processEntities(line)
                while ('-->' not in line):
                    line = self.read_file.readline()
            elif '<entry>' in line:
                self.processEntry()
                self.count += 1
                if self.count % 1000 == 0:
                    self.printStatus()
            try:
                line = self.read_file.readline()
            except Exception:
                line = None
        print(self.count)

    def printStatus(self):
        os.system('cls' if os.name=='nt' else 'clear')
        print(str(math.floor((self.count / 382000)*100)) + '% done')
        print(self.count)

    def toString(self, indent=0, initialIndent=0):
        newline = self.getNewline(indent)
        whitespace2 = self.getWhitespace(indent, initialIndent-indent)
        msg = "["
        comma=','
        for entry in self.entries.values():
            msg += entry.toString(indent, initialIndent+indent, comma)
        msg = msg[0:-1]
        msg += "{newline}{whitespace2}]".format(newline=newline, whitespace2=whitespace2)
        return msg

    def saveData(self):
        indent = 0 if len(sys.argv) == 1 else int(sys.argv[1])
        with open('output.json', "w", encoding="utf8") as write_file:
            write_file.write(self.toString(indent,0))

     
    class smart_dict(dict):
         def __missing__(self, key):
             return 'exp'

if __name__ == '__main__':
    controller = Controller()
    print('loading dict')
    epoch = time.time()
    controller.loadDict(filename)
    print(time.time() - epoch)

    #data = loadDict(filename)
    #JMDict = new JMDict();
    #controller.saveData()