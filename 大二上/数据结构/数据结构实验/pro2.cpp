#include <iostream>
using namespace std;

typedef int ElemType;

class Node {
public:
    int i, j;      // 行和列下标
    ElemType e;    // 元素值
    Node* pRight;//行指针
    Node* pDown;//列指针
};

class Matrix {
public:
    Node** RowHead;      // 行链表头指针向量
    Node** ColHead;      // 列链表头指针向量
    int iRow, iCol, terms;  // 矩阵行数，列数，非零元个数


    // 构造函数
    Matrix(int numRows, int numCols, int numElements = 0) {
        iRow = numRows;
        iCol = numCols;
        terms = numElements;

        // 动态申请行和列指针数组
        RowHead = new Node * [iRow];
        ColHead = new Node * [iCol];

        // 初始化这两个数组
        for (int i = 0; i < iRow; i++) {
            RowHead[i] = nullptr;
        }

        for (int j = 0; j < iCol; j++) {
            ColHead[j] = nullptr;
        }
    }

    // 析构函数
    ~Matrix() {
        for (int i = 0; i < iRow; i++) {
            Node* pTemp = RowHead[i];
            while (pTemp != nullptr) {
                Node* pNext = pTemp->pRight;
                delete pTemp;
                pTemp = pNext;
            }
        }
        delete[] RowHead;
        delete[] ColHead;
    }

    // 添加节点
    void AddNode(int row, int col, ElemType value) {
        if (row >= 0 && row < iRow && col >= 0 && col < iCol) {
            // 创建一个新节点并设置其行、列和值
            Node* newNode = new Node;
            newNode->i = row;
            newNode->j = col;
            newNode->e = value;
            newNode->pDown = nullptr;
            newNode->pRight = nullptr;

            // 连接行链表
            if (RowHead[row] == nullptr || RowHead[row]->j > col) {
                // 如果行链表为空或新节点列索引小于头节点的列索引，将新节点设置为头节点
                newNode->pRight = RowHead[row];
                RowHead[row] = newNode;
            }
            else {
                Node* pTravel = RowHead[row];
                while (pTravel->pRight != nullptr && pTravel->pRight->j < col) {
                    pTravel = pTravel->pRight;
                }
                // 在适当位置插入新节点
                newNode->pRight = pTravel->pRight;
                pTravel->pRight = newNode;
            }

            // 连接列链表
            if (ColHead[col] == nullptr || ColHead[col]->i > row) {
                // 如果列链表为空或新节点行索引小于头节点的行索引，将新节点设置为头节点
                newNode->pDown = ColHead[col];
                ColHead[col] = newNode;
            }
            else {
                Node* pTravel = ColHead[col];
                while (pTravel->pDown != nullptr && pTravel->pDown->i < row) {
                    pTravel = pTravel->pDown;
                }
                // 在适当位置插入新节点
                newNode->pDown = pTravel->pDown;
                pTravel->pDown = newNode;
            }
        }
    }

    //>>运算符重载
    friend istream& operator>>(istream& is, Matrix& matrix) {

        for (int i = 0; i < matrix.terms; i++) {
            int row, col;
            cout << "请输入行、列、值" << endl;
            ElemType value;
            is >> row >> col >> value;  // 从输入流中读取每个元素的行、列和值
            matrix.AddNode(row, col, value);  // 将元素添加到十字链表中
        }
        cout << "输入运算符重载调试成功！" << endl << endl;

        return is;
    }

    //<<运算符重载
    friend ostream& operator<<(ostream& os, const Matrix& matrix) {
        int i, j;
        Node* pTemp;
        for (i = 0; i < matrix.iRow; i++) {
            pTemp = matrix.RowHead[i];
            for (j = 0; j < matrix.iCol; j++) {
                if (pTemp != nullptr && pTemp->j == j) {
                    os << pTemp->e << " ";  // 输出当前元素值
                    pTemp = pTemp->pRight;
                }
                else {
                    os << "0 ";  // 输出零，表示没有元素
                }
            }
            os << endl;  // 换行到下一行
        }
        cout << "输出运算符重载调试成功！" << endl << endl;

        return os;
    }


    // 加号运算符重载
    Matrix operator+(const Matrix& other) const {
        // 检查矩阵维度是否匹配
        if (iRow != other.iRow || iCol != other.iCol) {
            cerr << "矩阵维度必须匹配才能相加。" << endl;
            return Matrix(0, 0);  // 返回一个空矩阵
        }

        Matrix result(iRow, iCol);  // 创建结果矩阵

        for (int i = 0; i < iRow; i++) {
            Node* thisRowPtr = RowHead[i];      // 当前矩阵的行指针
            Node* otherRowPtr = other.RowHead[i];  // 另一个矩阵的行指针

            while (thisRowPtr || otherRowPtr) {
                ElemType sum = 0;  // 存储两个元素的和
                int col;  // 列索引

                if (thisRowPtr && otherRowPtr) {
                    // 当两个矩阵的列索引相等
                    if (thisRowPtr->j < otherRowPtr->j) {
                        col = thisRowPtr->j;  // 使用当前矩阵的列索引
                        sum = thisRowPtr->e;  // 使用当前矩阵的元素值
                        thisRowPtr = thisRowPtr->pRight;
                    }
                    else if (thisRowPtr->j > otherRowPtr->j) {
                        col = otherRowPtr->j;  // 使用另一个矩阵的列索引
                        sum = otherRowPtr->e;  // 使用另一个矩阵的元素值
                        otherRowPtr = otherRowPtr->pRight;
                    }
                    else {
                        col = thisRowPtr->j;  // 使用当前矩阵的列索引
                        sum = thisRowPtr->e + otherRowPtr->e;  // 将两个矩阵的元素相加
                        thisRowPtr = thisRowPtr->pRight;
                        otherRowPtr = otherRowPtr->pRight;
                    }
                }
                else if (thisRowPtr) {
                    col = thisRowPtr->j;  // 使用当前矩阵的列索引
                    sum = thisRowPtr->e;  // 使用当前矩阵的元素值
                    thisRowPtr = thisRowPtr->pRight;
                }
                else {
                    col = otherRowPtr->j;  // 使用另一个矩阵的列索引
                    sum = otherRowPtr->e;  // 使用另一个矩阵的元素值
                    otherRowPtr = otherRowPtr->pRight;
                }

                if (sum != 0) {
                    result.AddNode(i, col, sum);  // 将结果添加到结果矩阵
                }
            }
        }
        cout << "加号运算符重载调试成功！" << endl << endl;
        return result;  // 返回相加后的结果矩阵
    }

    //拷贝构造函数
    Matrix(const Matrix& other) {
        // 复制矩阵的基本信息
        iRow = other.iRow;
        iCol = other.iCol;
        terms = other.terms;

        // 动态申请行和列指针数组
        RowHead = new Node * [iRow];
        ColHead = new Node * [iCol];

        // 复制数据
        for (int i = 0; i < iRow; i++) {
            RowHead[i] = nullptr;
            Node* pTemp = other.RowHead[i];
            Node* pPrev = nullptr;
            while (pTemp != nullptr) {
                // 创建一个新节点并复制元素信息
                Node* newNode = new Node;
                newNode->i = pTemp->i;
                newNode->j = pTemp->j;
                newNode->e = pTemp->e;
                newNode->pDown = nullptr;
                newNode->pRight = nullptr;

                if (pPrev == nullptr) {
                    // 如果是该行的第一个节点，设置RowHead指向新节点
                    RowHead[i] = newNode;
                }
                else {
                    // 否则将前一个节点的pRight指向新节点
                    pPrev->pRight = newNode;
                }
                pPrev = newNode;
                pTemp = pTemp->pRight;
            }
        }

        for (int j = 0; j < iCol; j++) {
            ColHead[j] = nullptr;
            Node* pTemp = other.ColHead[j];
            Node* pPrev = nullptr;
            while (pTemp != nullptr) {
                // 创建一个新节点并复制元素信息
                Node* newNode = new Node;
                newNode->i = pTemp->i;
                newNode->j = pTemp->j;
                newNode->e = pTemp->e;
                newNode->pDown = nullptr;
                newNode->pRight = nullptr;

                if (pPrev == nullptr) {
                    // 如果是该列的第一个节点，设置ColHead指向新节点
                    ColHead[j] = newNode;
                }
                else {
                    // 否则将前一个节点的pDown指向新节点
                    pPrev->pDown = newNode;
                }
                pPrev = newNode;
                pTemp = pTemp->pDown;
            }
        }
        cout << "拷贝构造函数调试成功！" << endl << endl;
    }

    //=运算符重载
    Matrix& operator=(const Matrix& other) {
        if (this == &other) {
            return *this;  // 防止自赋值
        }

        // 清理现有数据
        for (int i = 0; i < iRow; i++) {
            Node* pTemp = RowHead[i];
            while (pTemp != nullptr) {
                Node* pNext = pTemp->pRight;
                delete pTemp;
                pTemp = pNext;
            }
        }
        delete[] RowHead;
        delete[] ColHead;

        // 复制数据
        iRow = other.iRow;
        iCol = other.iCol;
        terms = other.terms;

        RowHead = new Node * [iRow];
        ColHead = new Node * [iCol];

        for (int i = 0; i < iRow; i++) {
            RowHead[i] = nullptr;
            Node* pTemp = other.RowHead[i];
            Node* pPrev = nullptr;
            while (pTemp != nullptr) {
                Node* newNode = new Node;
                newNode->i = pTemp->i;
                newNode->j = pTemp->j;
                newNode->e = pTemp->e;
                newNode->pDown = nullptr;
                newNode->pRight = nullptr;
                if (pPrev == nullptr) {
                    RowHead[i] = newNode;
                }
                else {
                    pPrev->pRight = newNode;
                }
                pPrev = newNode;
                pTemp = pTemp->pRight;
            }
        }

        for (int j = 0; j < iCol; j++) {
            ColHead[j] = nullptr;
            Node* pTemp = other.ColHead[j];
            Node* pPrev = nullptr;
            while (pTemp != nullptr) {
                Node* newNode = new Node;
                newNode->i = pTemp->i;
                newNode->j = pTemp->j;
                newNode->e = pTemp->e;
                newNode->pDown = nullptr;
                newNode->pRight = nullptr;
                if (pPrev == nullptr) {
                    ColHead[j] = newNode;
                }
                else {
                    pPrev->pDown = newNode;
                }
                pPrev = newNode;
                pTemp = pTemp->pDown;
            }
        }
        cout << "等号运算符重载调试成功！" << endl << endl;

        return *this;
    }

    //*运算符重载
    Matrix operator*(const Matrix& other) {
        // 检查是否可以执行矩阵相乘
        if (iCol != other.iRow) {
            cerr << "无法执行矩阵相乘：第一个矩阵的列数不等于第二个矩阵的行数" << endl;
            exit(1);  // 终止程序执行
        }

        Matrix result(iRow, other.iCol, 0); // 创建结果矩阵，初始元素个数为0

        // 遍历第一个矩阵的每一行
        for (int i = 0; i < iRow; i++) {
            // 遍历第二个矩阵的每一列
            for (int j = 0; j < other.iCol; j++) {
                ElemType value = 0;
                Node* pTemp1 = RowHead[i];    // 第一个矩阵的当前行
                Node* pTemp2 = other.ColHead[j];  // 第二个矩阵的当前列

                // 遍历两个矩阵的对应元素，进行相乘并累加
                while (pTemp1 != nullptr && pTemp2 != nullptr) {
                    if (pTemp1->j == pTemp2->i) {
                        value += pTemp1->e * pTemp2->e;  // 对应元素相乘并累加到结果中
                        pTemp1 = pTemp1->pRight;         // 移动到第一个矩阵的下一个元素
                        pTemp2 = pTemp2->pDown;          // 移动到第二个矩阵的下一个元素
                    }
                    else if (pTemp1->j < pTemp2->i) {
                        pTemp1 = pTemp1->pRight;  // 第一个矩阵的元素列索引较小，移动到下一个元素
                    }
                    else {
                        pTemp2 = pTemp2->pDown;  // 第二个矩阵的元素行索引较小，移动到下一个元素
                    }
                }

                if (value != 0) {
                    result.AddNode(i, j, value);  // 将计算得到的结果添加到结果矩阵中
                }
            }
        }

        cout << "乘号运算符重载调试成功！" << endl << endl;
        return result;  // 返回相乘后的结果矩阵
    }

    //求转置函数
    Matrix GetTranspose() {
        Matrix transposedMatrix(iCol, iRow, terms); // 创建一个新的CrossList对象，交换行和列，但节点数不变

        // 遍历原矩阵的每一行
        for (int i = 0; i < iRow; i++) {
            Node* pTemp = RowHead[i];  // 获取当前行的头结点指针

            // 遍历当前行的所有元素
            while (pTemp != nullptr) {
                // 在新的矩阵中交换行列索引，并添加节点
                transposedMatrix.AddNode(pTemp->j, pTemp->i, pTemp->e);
                pTemp = pTemp->pRight;  // 移动到当前行的下一个元素
            }
        }

        cout << "转置函数调试成功！" << endl << endl;
        return transposedMatrix;  // 返回转置后的矩阵
    }



    //-运算符重载
    Matrix operator-(const Matrix& other) const {
        // 检查矩阵是否匹配
        if (iRow != other.iRow || iCol != other.iCol) {
            cerr << "矩阵必须匹配才能相减。" << endl;
            return Matrix(0, 0);  // 返回一个空矩阵
        }

        Matrix result(iRow, iCol);  // 创建结果矩阵

        for (int i = 0; i < iRow; i++) {
            Node* thisRowPtr = RowHead[i];      // 当前矩阵的行指针
            Node* otherRowPtr = other.RowHead[i];  // 另一个矩阵的行指针

            while (thisRowPtr || otherRowPtr) {
                ElemType diff = 0;  // 存储两个元素的差值
                int col;  // 列索引

                if (thisRowPtr && otherRowPtr) {
                    // 当两个矩阵的列索引相等
                    if (thisRowPtr->j < otherRowPtr->j) {
                        col = thisRowPtr->j;  // 使用当前矩阵的列索引
                        diff = thisRowPtr->e;  // 使用当前矩阵的元素值
                        thisRowPtr = thisRowPtr->pRight;
                    }
                    else if (thisRowPtr->j > otherRowPtr->j) {
                        col = otherRowPtr->j;  // 使用另一个矩阵的列索引
                        diff = -otherRowPtr->e;  // 从另一个矩阵中减去元素值
                        otherRowPtr = otherRowPtr->pRight;
                    }
                    else {
                        col = thisRowPtr->j;  // 使用当前矩阵的列索引
                        diff = thisRowPtr->e - otherRowPtr->e;  // 从两个矩阵中减去元素值
                        thisRowPtr = thisRowPtr->pRight;
                        otherRowPtr = otherRowPtr->pRight;
                    }
                }
                else if (thisRowPtr) {
                    col = thisRowPtr->j;  // 使用当前矩阵的列索引
                    diff = thisRowPtr->e;  // 使用当前矩阵的元素值
                    thisRowPtr = thisRowPtr->pRight;
                }
                else {
                    col = otherRowPtr->j;  // 使用另一个矩阵的列索引
                    diff = -otherRowPtr->e;  // 从另一个矩阵中减去元素值
                    otherRowPtr = otherRowPtr->pRight;
                }

                if (diff != 0) {
                    result.AddNode(i, col, diff);  // 将结果添加到结果矩阵
                }
            }
        }
        cout << "减号运算符重载调试成功！" << endl << endl;
        return result;  // 返回相减后的结果矩阵
    }
};
int main()
{
    int r1, c1, e1, r2, c2, e2;
    cout << "请输入矩阵1行数、列数和非零元素个数：" << endl;
    cin >> r1 >> c1 >> e1;        
    Matrix matrix1(r1, c1, e1);
    cin >> matrix1;
    cout << "请输入矩阵2行数、列数和非零元素个数：" << endl;
    cin >> r2 >> c2 >> e2;
        Matrix matrix2(r2,c2,e2);
    cin >> matrix2;
    cout << "Matrix1:" << endl<< matrix1;
    cout << "Matrix2:" << endl<< matrix2;
    cout << "matrix1 + matrix2=" << endl;
    Matrix matrix3 = matrix1 + matrix2;
    cout << matrix3<< endl;
    cout << "matrix1 - matrix2=" << endl;
    Matrix matrix6 = matrix1 - matrix2;
    cout << matrix6<<endl;
    cout << "matrix1 * matrix2=" << endl;
    Matrix matrix4 = matrix1 * matrix2;
    cout << matrix4<< endl;
    cout << "matrix1的转置：" << endl;
    Matrix matrix5(matrix1.GetTranspose());
    cout << matrix5<< endl;
    matrix2 = matrix1;cout << matrix2;




    return 0;
}
