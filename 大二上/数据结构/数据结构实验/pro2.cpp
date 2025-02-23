#include <iostream>
using namespace std;

typedef int ElemType;

class Node {
public:
    int i, j;      // �к����±�
    ElemType e;    // Ԫ��ֵ
    Node* pRight;//��ָ��
    Node* pDown;//��ָ��
};

class Matrix {
public:
    Node** RowHead;      // ������ͷָ������
    Node** ColHead;      // ������ͷָ������
    int iRow, iCol, terms;  // ��������������������Ԫ����


    // ���캯��
    Matrix(int numRows, int numCols, int numElements = 0) {
        iRow = numRows;
        iCol = numCols;
        terms = numElements;

        // ��̬�����к���ָ������
        RowHead = new Node * [iRow];
        ColHead = new Node * [iCol];

        // ��ʼ������������
        for (int i = 0; i < iRow; i++) {
            RowHead[i] = nullptr;
        }

        for (int j = 0; j < iCol; j++) {
            ColHead[j] = nullptr;
        }
    }

    // ��������
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

    // ��ӽڵ�
    void AddNode(int row, int col, ElemType value) {
        if (row >= 0 && row < iRow && col >= 0 && col < iCol) {
            // ����һ���½ڵ㲢�������С��к�ֵ
            Node* newNode = new Node;
            newNode->i = row;
            newNode->j = col;
            newNode->e = value;
            newNode->pDown = nullptr;
            newNode->pRight = nullptr;

            // ����������
            if (RowHead[row] == nullptr || RowHead[row]->j > col) {
                // ���������Ϊ�ջ��½ڵ�������С��ͷ�ڵ�������������½ڵ�����Ϊͷ�ڵ�
                newNode->pRight = RowHead[row];
                RowHead[row] = newNode;
            }
            else {
                Node* pTravel = RowHead[row];
                while (pTravel->pRight != nullptr && pTravel->pRight->j < col) {
                    pTravel = pTravel->pRight;
                }
                // ���ʵ�λ�ò����½ڵ�
                newNode->pRight = pTravel->pRight;
                pTravel->pRight = newNode;
            }

            // ����������
            if (ColHead[col] == nullptr || ColHead[col]->i > row) {
                // ���������Ϊ�ջ��½ڵ�������С��ͷ�ڵ�������������½ڵ�����Ϊͷ�ڵ�
                newNode->pDown = ColHead[col];
                ColHead[col] = newNode;
            }
            else {
                Node* pTravel = ColHead[col];
                while (pTravel->pDown != nullptr && pTravel->pDown->i < row) {
                    pTravel = pTravel->pDown;
                }
                // ���ʵ�λ�ò����½ڵ�
                newNode->pDown = pTravel->pDown;
                pTravel->pDown = newNode;
            }
        }
    }

    //>>���������
    friend istream& operator>>(istream& is, Matrix& matrix) {

        for (int i = 0; i < matrix.terms; i++) {
            int row, col;
            cout << "�������С��С�ֵ" << endl;
            ElemType value;
            is >> row >> col >> value;  // ���������ж�ȡÿ��Ԫ�ص��С��к�ֵ
            matrix.AddNode(row, col, value);  // ��Ԫ����ӵ�ʮ��������
        }
        cout << "������������ص��Գɹ���" << endl << endl;

        return is;
    }

    //<<���������
    friend ostream& operator<<(ostream& os, const Matrix& matrix) {
        int i, j;
        Node* pTemp;
        for (i = 0; i < matrix.iRow; i++) {
            pTemp = matrix.RowHead[i];
            for (j = 0; j < matrix.iCol; j++) {
                if (pTemp != nullptr && pTemp->j == j) {
                    os << pTemp->e << " ";  // �����ǰԪ��ֵ
                    pTemp = pTemp->pRight;
                }
                else {
                    os << "0 ";  // ����㣬��ʾû��Ԫ��
                }
            }
            os << endl;  // ���е���һ��
        }
        cout << "�����������ص��Գɹ���" << endl << endl;

        return os;
    }


    // �Ӻ����������
    Matrix operator+(const Matrix& other) const {
        // ������ά���Ƿ�ƥ��
        if (iRow != other.iRow || iCol != other.iCol) {
            cerr << "����ά�ȱ���ƥ�������ӡ�" << endl;
            return Matrix(0, 0);  // ����һ���վ���
        }

        Matrix result(iRow, iCol);  // �����������

        for (int i = 0; i < iRow; i++) {
            Node* thisRowPtr = RowHead[i];      // ��ǰ�������ָ��
            Node* otherRowPtr = other.RowHead[i];  // ��һ���������ָ��

            while (thisRowPtr || otherRowPtr) {
                ElemType sum = 0;  // �洢����Ԫ�صĺ�
                int col;  // ������

                if (thisRowPtr && otherRowPtr) {
                    // ��������������������
                    if (thisRowPtr->j < otherRowPtr->j) {
                        col = thisRowPtr->j;  // ʹ�õ�ǰ�����������
                        sum = thisRowPtr->e;  // ʹ�õ�ǰ�����Ԫ��ֵ
                        thisRowPtr = thisRowPtr->pRight;
                    }
                    else if (thisRowPtr->j > otherRowPtr->j) {
                        col = otherRowPtr->j;  // ʹ����һ�������������
                        sum = otherRowPtr->e;  // ʹ����һ�������Ԫ��ֵ
                        otherRowPtr = otherRowPtr->pRight;
                    }
                    else {
                        col = thisRowPtr->j;  // ʹ�õ�ǰ�����������
                        sum = thisRowPtr->e + otherRowPtr->e;  // �����������Ԫ�����
                        thisRowPtr = thisRowPtr->pRight;
                        otherRowPtr = otherRowPtr->pRight;
                    }
                }
                else if (thisRowPtr) {
                    col = thisRowPtr->j;  // ʹ�õ�ǰ�����������
                    sum = thisRowPtr->e;  // ʹ�õ�ǰ�����Ԫ��ֵ
                    thisRowPtr = thisRowPtr->pRight;
                }
                else {
                    col = otherRowPtr->j;  // ʹ����һ�������������
                    sum = otherRowPtr->e;  // ʹ����һ�������Ԫ��ֵ
                    otherRowPtr = otherRowPtr->pRight;
                }

                if (sum != 0) {
                    result.AddNode(i, col, sum);  // �������ӵ��������
                }
            }
        }
        cout << "�Ӻ���������ص��Գɹ���" << endl << endl;
        return result;  // ������Ӻ�Ľ������
    }

    //�������캯��
    Matrix(const Matrix& other) {
        // ���ƾ���Ļ�����Ϣ
        iRow = other.iRow;
        iCol = other.iCol;
        terms = other.terms;

        // ��̬�����к���ָ������
        RowHead = new Node * [iRow];
        ColHead = new Node * [iCol];

        // ��������
        for (int i = 0; i < iRow; i++) {
            RowHead[i] = nullptr;
            Node* pTemp = other.RowHead[i];
            Node* pPrev = nullptr;
            while (pTemp != nullptr) {
                // ����һ���½ڵ㲢����Ԫ����Ϣ
                Node* newNode = new Node;
                newNode->i = pTemp->i;
                newNode->j = pTemp->j;
                newNode->e = pTemp->e;
                newNode->pDown = nullptr;
                newNode->pRight = nullptr;

                if (pPrev == nullptr) {
                    // ����Ǹ��еĵ�һ���ڵ㣬����RowHeadָ���½ڵ�
                    RowHead[i] = newNode;
                }
                else {
                    // ����ǰһ���ڵ��pRightָ���½ڵ�
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
                // ����һ���½ڵ㲢����Ԫ����Ϣ
                Node* newNode = new Node;
                newNode->i = pTemp->i;
                newNode->j = pTemp->j;
                newNode->e = pTemp->e;
                newNode->pDown = nullptr;
                newNode->pRight = nullptr;

                if (pPrev == nullptr) {
                    // ����Ǹ��еĵ�һ���ڵ㣬����ColHeadָ���½ڵ�
                    ColHead[j] = newNode;
                }
                else {
                    // ����ǰһ���ڵ��pDownָ���½ڵ�
                    pPrev->pDown = newNode;
                }
                pPrev = newNode;
                pTemp = pTemp->pDown;
            }
        }
        cout << "�������캯�����Գɹ���" << endl << endl;
    }

    //=���������
    Matrix& operator=(const Matrix& other) {
        if (this == &other) {
            return *this;  // ��ֹ�Ը�ֵ
        }

        // ������������
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

        // ��������
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
        cout << "�Ⱥ���������ص��Գɹ���" << endl << endl;

        return *this;
    }

    //*���������
    Matrix operator*(const Matrix& other) {
        // ����Ƿ����ִ�о������
        if (iCol != other.iRow) {
            cerr << "�޷�ִ�о�����ˣ���һ����������������ڵڶ������������" << endl;
            exit(1);  // ��ֹ����ִ��
        }

        Matrix result(iRow, other.iCol, 0); // ����������󣬳�ʼԪ�ظ���Ϊ0

        // ������һ�������ÿһ��
        for (int i = 0; i < iRow; i++) {
            // �����ڶ��������ÿһ��
            for (int j = 0; j < other.iCol; j++) {
                ElemType value = 0;
                Node* pTemp1 = RowHead[i];    // ��һ������ĵ�ǰ��
                Node* pTemp2 = other.ColHead[j];  // �ڶ�������ĵ�ǰ��

                // ������������Ķ�ӦԪ�أ�������˲��ۼ�
                while (pTemp1 != nullptr && pTemp2 != nullptr) {
                    if (pTemp1->j == pTemp2->i) {
                        value += pTemp1->e * pTemp2->e;  // ��ӦԪ����˲��ۼӵ������
                        pTemp1 = pTemp1->pRight;         // �ƶ�����һ���������һ��Ԫ��
                        pTemp2 = pTemp2->pDown;          // �ƶ����ڶ����������һ��Ԫ��
                    }
                    else if (pTemp1->j < pTemp2->i) {
                        pTemp1 = pTemp1->pRight;  // ��һ�������Ԫ����������С���ƶ�����һ��Ԫ��
                    }
                    else {
                        pTemp2 = pTemp2->pDown;  // �ڶ��������Ԫ����������С���ƶ�����һ��Ԫ��
                    }
                }

                if (value != 0) {
                    result.AddNode(i, j, value);  // ������õ��Ľ����ӵ����������
                }
            }
        }

        cout << "�˺���������ص��Գɹ���" << endl << endl;
        return result;  // ������˺�Ľ������
    }

    //��ת�ú���
    Matrix GetTranspose() {
        Matrix transposedMatrix(iCol, iRow, terms); // ����һ���µ�CrossList���󣬽����к��У����ڵ�������

        // ����ԭ�����ÿһ��
        for (int i = 0; i < iRow; i++) {
            Node* pTemp = RowHead[i];  // ��ȡ��ǰ�е�ͷ���ָ��

            // ������ǰ�е�����Ԫ��
            while (pTemp != nullptr) {
                // ���µľ����н�����������������ӽڵ�
                transposedMatrix.AddNode(pTemp->j, pTemp->i, pTemp->e);
                pTemp = pTemp->pRight;  // �ƶ�����ǰ�е���һ��Ԫ��
            }
        }

        cout << "ת�ú������Գɹ���" << endl << endl;
        return transposedMatrix;  // ����ת�ú�ľ���
    }



    //-���������
    Matrix operator-(const Matrix& other) const {
        // �������Ƿ�ƥ��
        if (iRow != other.iRow || iCol != other.iCol) {
            cerr << "�������ƥ����������" << endl;
            return Matrix(0, 0);  // ����һ���վ���
        }

        Matrix result(iRow, iCol);  // �����������

        for (int i = 0; i < iRow; i++) {
            Node* thisRowPtr = RowHead[i];      // ��ǰ�������ָ��
            Node* otherRowPtr = other.RowHead[i];  // ��һ���������ָ��

            while (thisRowPtr || otherRowPtr) {
                ElemType diff = 0;  // �洢����Ԫ�صĲ�ֵ
                int col;  // ������

                if (thisRowPtr && otherRowPtr) {
                    // ��������������������
                    if (thisRowPtr->j < otherRowPtr->j) {
                        col = thisRowPtr->j;  // ʹ�õ�ǰ�����������
                        diff = thisRowPtr->e;  // ʹ�õ�ǰ�����Ԫ��ֵ
                        thisRowPtr = thisRowPtr->pRight;
                    }
                    else if (thisRowPtr->j > otherRowPtr->j) {
                        col = otherRowPtr->j;  // ʹ����һ�������������
                        diff = -otherRowPtr->e;  // ����һ�������м�ȥԪ��ֵ
                        otherRowPtr = otherRowPtr->pRight;
                    }
                    else {
                        col = thisRowPtr->j;  // ʹ�õ�ǰ�����������
                        diff = thisRowPtr->e - otherRowPtr->e;  // �����������м�ȥԪ��ֵ
                        thisRowPtr = thisRowPtr->pRight;
                        otherRowPtr = otherRowPtr->pRight;
                    }
                }
                else if (thisRowPtr) {
                    col = thisRowPtr->j;  // ʹ�õ�ǰ�����������
                    diff = thisRowPtr->e;  // ʹ�õ�ǰ�����Ԫ��ֵ
                    thisRowPtr = thisRowPtr->pRight;
                }
                else {
                    col = otherRowPtr->j;  // ʹ����һ�������������
                    diff = -otherRowPtr->e;  // ����һ�������м�ȥԪ��ֵ
                    otherRowPtr = otherRowPtr->pRight;
                }

                if (diff != 0) {
                    result.AddNode(i, col, diff);  // �������ӵ��������
                }
            }
        }
        cout << "������������ص��Գɹ���" << endl << endl;
        return result;  // ���������Ľ������
    }
};
int main()
{
    int r1, c1, e1, r2, c2, e2;
    cout << "���������1�����������ͷ���Ԫ�ظ�����" << endl;
    cin >> r1 >> c1 >> e1;        
    Matrix matrix1(r1, c1, e1);
    cin >> matrix1;
    cout << "���������2�����������ͷ���Ԫ�ظ�����" << endl;
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
    cout << "matrix1��ת�ã�" << endl;
    Matrix matrix5(matrix1.GetTranspose());
    cout << matrix5<< endl;
    matrix2 = matrix1;cout << matrix2;




    return 0;
}
