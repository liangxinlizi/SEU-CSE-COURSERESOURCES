#include<iostream>
#include<fstream>
#include<map>
#include<iomanip>
#include<stack>
#include<cstring>
#pragma warning(disable:4996)
using namespace std;

struct HN
{
    char data;  //�ڵ��ַ�����
    int value;  // �ڵ����ݳ���Ƶ��
    int leftChild, rightChild, parent;  // ���Һ��ӵ��±�͸��ڵ��±�
    char* code;  //���Ĺ���������
    int bit;  //����λ��

    HN() : leftChild(0), rightChild(0), parent(0), code(nullptr), bit(0) {}
};

class HT
{
public:
    HT(int n, map<char, int> mp);//HT�Ĺ��캯��
    ~HT();//��������
    void show(int n);
    void encode(int n);
    void generateCodes(HN* node, char* code);//��ÿ���ַ��������������
    void decode(int n);
    void select(int n, int& s1, int& s0);//ѡ��ǰn�����Ĳ�Ϊ0�Ľ�����С�ʹ�Сֵ
private:
    HN* root;//���ĵ�ַ
    HN* ht;
};

map<char, int> getcount()
{
    ifstream in;
    in.open("para.txt", ios::in);
    map<char, int> count;
    if (!in.is_open())
    {
        cerr << "Fail to open!" << endl;
        return count;
    }
    else
    {
        char c;
        while (in.get(c))//��ȡ�ַ�
        {
            if (islower(c))
            {
                c = toupper(c);//Сд�ַ�ת��Ϊ��д�ַ�
            }
            if (isalpha(c))
            {
                count[c]++;//Ƶ�ʼ�һ
            }
        }
    }
    in.close();
    return count;
}
HT::HT(int n, map<char, int> mp)
{
    if (n <= 1) return;//��data�Ľ��������<=1
    int m = 2 * n - 1;//�ܹ��Ľ����ĿΪ2n-1
    ht = new HN[m + 1];//����λ��Ӧ���ǽڵ���Ŀ+1
    int i = 1;
    for (auto it = mp.begin(); i <= n; i++, it++)
    {
        ht[i].data = it->first;
        ht[i].value = it->second;
        ht[i].code = nullptr;

    }
    for (int i = n + 1; i <= m; i++)
    {
        int minmin; int minmax;//�ֱ�Ϊ��Сֵ�ʹ�Сֵ
        select(i - 1, minmin, minmax);
        ht[minmin].parent = i;
        ht[minmax].parent = i;
        ht[i].leftChild = minmax;
        ht[i].rightChild = minmin;
        ht[i].value = ht[minmin].value + ht[minmax].value;//Ƶ��ֵ���
        ht[i].data = '.';
        ht[i].code = nullptr;
        ht[i].bit = 0;
    }
    root = &ht[m];
    generateCodes(root, const_cast<char*>(""));//Ϊ���нڵ㸳����������

}
HT::~HT()
{
    delete[] ht;
}
void HT::select(int n, int& s1, int& s0)
{
    s1 = s0 = 0;//�������ã���˿��Ըı���Сֵ�ʹ�Сֵ���±�ֵ
    for (int i = 1; i <= n; i++)
    {
        if (ht[i].parent == 0) {//�и��ڵ�ģ����ܱ��������൱�ڱ����Ƴ���
            if (s1 == 0)
                s1 = i;
            else
                s0 = i;
        }
    }
    for (int i = 1; i <= n; i++)
    {
        if (ht[i].parent == 0 && ht[s1].value > ht[i].value) {
            s1 = i;//�ҵ���С���±�ֵ
        }
    }
    for (int j = 1; j <= n; j++)
    {
        if (ht[j].parent == 0 && j != s1) {
            s0 = j;
            break;
        }
    }
    for (int j = 1; j <= n; j++)
    {
        if (ht[j].parent == 0 && j != s1 && ht[s0].value > ht[j].value) {
            s0 = j;//�ҵ���С���±�ֵ
        }
    }
}
void HT::decode(int n)//����
{
    fstream fs("codeinput.txt", ios::in);
    if (fs.is_open())
    {
        char c[10] = "";
        char tmp;
        int im = 0;
        cout << "Decoded Text: " << endl;

        while (fs >> tmp)
        {
            if (im < 9)
            {
                c[im] = tmp;
                im++;
                for (int i = 1; i <= n; i++)
                {
                    if (strncmp(c, ht[i].code, im) == 0)//ע�������õ�strncmp����Ϊÿ�αȽ������λ�����Ȳ�ͬ
                    {
                        if (strlen(ht[i].code) == im)
                        {
                            cout << ht[i].data;
                            im = 0;
                            break;
                        }
                    }
                }
            }
        }
        cout << endl;
    }
}
void HT::generateCodes(HN* node, char* code)
{
    if (node->leftChild == 0 && node->rightChild == 0)
    {
        node->code = new char[strlen(code) + 1];
        strcpy(node->code, code);
        node->bit = strlen(node->code);
    }
    else
    {
        char leftCode[100];  
        char rightCode[100];  
        strcpy(leftCode, code);
        strcpy(rightCode, code);
        strcat(leftCode, "0");
        strcat(rightCode, "1");

        generateCodes(&ht[node->leftChild], leftCode);
        generateCodes(&ht[node->rightChild], rightCode);
    }
}
void HT::encode(int n)
{
    char text[200048] = "";//����һ���㹻����������洢
    ifstream fs("para.txt", ios::in);
    if (fs.is_open())
    {
        char c;
        while (fs.get(c))
        {
            if (islower(c))
                c = toupper(c);
            if (isalpha(c))
            {
                for (int i = 1; i <= n; i++)
                {
                    if (ht[i].data == c)
                    {
                        strcat(text, ht[i].code);//��ʶ�𵽵�ÿһ����ĸ�ı���ƴ�ӵ����еı����� 
                        break;//����ƥ���ʱ������ѭ��
                    }
                }
            }
        }
        cout << "Encoded Text: " << endl << text << endl;
    }
    fs.close();
}
void HT::show(int n)
{
    cout << "index value data Lchild Rchild Parent code      bits" << endl;//���
    cout << left;//�����
    int m = 2 * n - 1;
    for (int i = 1; i <= m; i++)
    {
        cout << setw(5) << i << " ";
        cout << setw(6) << ht[i].value << " ";
        cout << setw(4) << ht[i].data << " ";
        cout << setw(6) << ht[i].leftChild << " ";
        cout << setw(6) << ht[i].rightChild << " ";
        cout << setw(6) << ht[i].parent << " ";
        if (i <= n)
        {
            cout << setw(9) << ht[i].code << " ";
            cout << setw(4) << ht[i].bit << " ";
        }
        cout << endl;
    }
}



int main()
{
    map<char, int> charcount = getcount();
    fstream result("result.txt", ios::out);
    result << "�ַ�\t����" << endl;
    for (auto it = charcount.begin(); it != charcount.end(); ++it)
    {
        result << it->first << "\t" << it->second << endl;
    }
    HT ht(charcount.size(), charcount);
    ht.show(charcount.size());
    ht.encode(charcount.size());
    ht.decode(charcount.size());
    return 0;
}
