from fractions import Fraction
from copy import deepcopy

#是否显示过程
displayProcess = False

class vector(object):
    def __init__(self, T):
        if isinstance(T, list):
            self.data = [Fraction(num).limit_denominator() for num in T]
        elif isinstance(T, vector):
            self.data = deepcopy(T.data)
        elif isinstance(T, int):
            self.data = [Fraction(0) for i in range(T)]
    
    def __str__(self):
        return str(list(map(str, self.data)))
    
    def getlist(self):
        return self.data

    def __iter__(self):
        return self.data
    
    def __getitem__(self, n):
        return self.data[n]

    def __add__(self, rhs):
        if isinstance(rhs, vector) and len(self.data) == len(rhs.data):
            ans = vector(self)
            for i in range(len(self.data)):
                ans.data[i] += rhs[i]
            return ans

    def __mul__(self, rhs): #右乘
        if not isinstance(rhs, vector):
            raise Exception("Vector can't be multiply by a nonvector.")
        if len(self.data) != len(rhs.data):
            raise Exception("The length of two vector is not same.")
        
        ans = Fraction(0)
        for i in range(len(self.data)):
            ans += self.data[i] * rhs.data[i]
        
        return ans
    
    def __rmul__(self, lhs):    #左乘
        if isinstance(lhs, vector):
            return self * lhs

        ans = vector(self)
        ans.data = [lhs * num for num in ans.data]
        return ans


class matrix(object):
    def __init__(self, T):    #初始化
        if isinstance(T, list) and isinstance(T[0], list):
            self.matrixData = [[Fraction(num).limit_denominator() for num in row] for row in T]   #将每一个数都转换成分数
            self.row, self.cloumn = len(T), len(T[0])
        elif isinstance(T, matrix):   #若传入值是一个矩阵，则将其赋值为该矩阵
            self.matrixData, self.row, self.cloumn = deepcopy(T.matrixData), T.row, T.cloumn
        elif isinstance(T, list): #若传入值为一个list,即两个参数
            self.row, self.cloumn = T[0], T[1]
            self.matrixData = [[Fraction(0) for c in range(self.cloumn)] for r in range(self.row)]    #生成一个0矩阵       
    
    def __getitem__(self, n):   #实现下标操作
        return self.matrixData[n]
    
    def __str__(self):  #实现str使其能正常输出
        s = ""
        for row in self.matrixData:
            s += str(list(map(str, row))) + "\n"
        return s

    def __iter__(self): #使for函数可以迭代一个矩阵
        return self.matrixData
    
    __repr__ = __str__

    def __add__(self, rhs): #矩阵加，由于两个数都是矩阵，所以不用定义反向加
        if not isinstance(rhs, matrix): #错误处理
            raise Exception("Matrix can't be added by a nonmatrix.")
        if self.row != rhs.row or self.cloumn != rhs.cloumn:
            raise Exception("Size of two matrix is different.")
        
        ans = matrix(self)
        for i in range(self.row):
            for j in range(self.cloumn):
                ans[i][j] += rhs[i][j]
        
        return ans
    
    def __neg__(self):  #负号
        temp = matrix(self) #一定要这样写，开一个新矩阵
        temp.matrixData = [[-num for num in row] for row in temp.matrixData]    #每个值都取负
        return temp

    def __sub__(self, rhs):
        if not isinstance(rhs, matrix): #错误处理
            raise Exception("Matrix can't be minused by a nonmatrix.")
        if self.row != rhs.row or self.cloumn != rhs.cloumn:
            raise Exception("Size of two matrix is different.")

        return self + (-rhs)

    def getRow(self, n):
        return vector(self[n])

    def getCloumn(self, n):
        return vector([row[n] for row in self.matrixData])

    def setRow(self, row, n):
        if isinstance(row, vector):
            self.matrixData[n] = row.getlist()
        elif isinstance(row, list):
            self.matrixData[n] = row

    def setCloumn(self, cloumn, n):
        for r in range(self.row):
            self[r][n] = cloumn[r]

    def __mul__(self, rhs):
        if not isinstance(rhs, matrix):
            raise Exception("Matrix can't be multiply by a nonmatrix.")
        if self.cloumn != rhs.row:
            raise Exception("The column of matrix 1 is different to the row of matrix 2.")
        
        ans = matrix([self.row, rhs.cloumn])
        for r in range(self.row):
            for c in range(rhs.cloumn):
                ans[r][c] = self.getRow(r) * rhs.getCloumn(c)
        
        return ans

    def __rmul__(self, lhs):
        if isinstance(lhs, matrix):
            return lhs * self
        ans = matrix(self)
        ans.matrixData = [[lhs * num for num in row] for row in ans.matrixData]
        return ans

    def swapRow(self, r1, r2):  #r1<->r2
        if displayProcess:
            print("r%d<->r%d" %(r1 + 1, r2 + 1))
        temprow = self.getRow(r1)
        self.setRow(self.getRow(r2), r1)
        self.setRow(temprow, r2)
        return self
    
    def swapCloumn(self, c1, c2):   #c1<->c2
        if displayProcess:
            print("c%d<->c%d" %(c1 + 1, c2 + 1))
        tempcloumn = self.getCloumn(c1)
        self.setCloumn(self.getCloumn(c2), c1)
        self.setCloumn(tempcloumn, c2)
        return self

    def mulRow(self, r, n): #n*r
        if displayProcess:
            print("%s*r%d" %(str(n), r + 1))
        self.setRow(n * self.getRow(r), r)
        return self
    
    def mulCloumn(self, c, n):  #n*c
        if displayProcess:
            print("%s*c%d" %(str(n), c + 1))
        self.setCloumn(n * self.getCloumn(c), c)
        return self

    def nAddRow(self, r1, r2, n):   #r1 + n*r2
        if displayProcess:
            print("r%d+%s*r%d" %(r1 + 1, str(n), r2 + 1))
        self.setRow(self.getRow(r1) + n * self.getRow(r2), r1)
        return self
    
    def nAddCloumn(self, c1, c2, n):    #c1 + n*c2
        if displayProcess:
            print("c%d+%s*c%d" %(c1 + 1, str(n), c2 + 1))
        self.setCloumn(self.getCloumn(c1) + n * self.getCloumn(c2), c1)
        return self
    
    def transposeItself(self):    #转置自己
        self.matrixData, self.row, self.cloumn = [self.getCloumn(i).getlist() for i in range(self.cloumn)], self.cloumn, self.row
        return self
    
    def transpose(self):    #返回转置矩阵
        return matrix(self).transposeItself()
    
    def searchFirstUnzeroRow(self, c, r = 0):  #在c中从第r行寻找第一个非0的行
        for i in range(r, self.row):
            if self[i][c] != 0:
                return i
        
        return -1

    def transformToRowEchelonForm(self):    #将其自己转换成行阶梯矩阵
        curR, curC = 0, 0
        while curR != self.row - 1 or curC != self.cloumn - 1:
            UnzeroRow = self.searchFirstUnzeroRow(curC, curR)
            if UnzeroRow == -1:
                curC += 1
                continue
            else:
                if curR != UnzeroRow:
                    self.swapRow(curR, UnzeroRow)
                for r in range(curR + 1, self.row):
                    self.nAddRow(r, curR, -self[r][curC] / self[curR][curC])
                curR = curR + 1 if curR != self.row - 1 else curR
                curC = curC + 1 if curC != self.cloumn - 1 else curC
        return self

    def det(self):
        if self.row != self.cloumn:
            raise Exception("Only a matrix has same row and column can have det.")

        ans = Fraction(1)
        temp = matrix(self).transformToRowEchelonForm()
        for i in range(self.row):
            ans *= temp[i][i]
            
        return ans

        

    

l = [[1, 4, 2], 
    [0, -3, 4], 
    [0, 4, 3]]
m = matrix(l)
for i in range(8):
    m *= m

print(m)

'''
print(m)
m.nAddRow(1, 0, -4)
m.nAddRow(2, 0, -7)
print(m)
m.mulRow(1, 1 / m[1][1])
m.nAddRow(2, 1, 6)
print(m)
'''