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
    char data;  //节点字符数据
    int value;  // 节点数据出现频率
    int leftChild, rightChild, parent;  // 左右孩子的下标和父节点下标
    char* code;  //结点的哈夫曼编码
    int bit;  //编码位数

    HN() : leftChild(0), rightChild(0), parent(0), code(nullptr), bit(0) {}
};

class HT
{
public:
    HT(int n, map<char, int> mp);//HT的构造函数
    ~HT();//析构函数
    void show(int n);
    void encode(int n);
    void generateCodes(HN* node, char* code);//给每个字符创造哈夫曼编码
    void decode(int n);
    void select(int n, int& s1, int& s0);//选择前n个结点的不为0的结点的最小和次小值
private:
    HN* root;//树的地址
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
        while (in.get(c))//读取字符
        {
            if (islower(c))
            {
                c = toupper(c);//小写字符转化为大写字符
            }
            if (isalpha(c))
            {
                count[c]++;//频率加一
            }
        }
    }
    in.close();
    return count;
}
HT::HT(int n, map<char, int> mp)
{
    if (n <= 1) return;//带data的结点数必须<=1
    int m = 2 * n - 1;//总共的结点数目为2n-1
    ht = new HN[m + 1];//数组位数应该是节点数目+1
    int i = 1;
    for (auto it = mp.begin(); i <= n; i++, it++)
    {
        ht[i].data = it->first;
        ht[i].value = it->second;
        ht[i].code = nullptr;

    }
    for (int i = n + 1; i <= m; i++)
    {
        int minmin; int minmax;//分别为最小值和次小值
        select(i - 1, minmin, minmax);
        ht[minmin].parent = i;
        ht[minmax].parent = i;
        ht[i].leftChild = minmax;
        ht[i].rightChild = minmin;
        ht[i].value = ht[minmin].value + ht[minmax].value;//频率值相加
        ht[i].data = '.';
        ht[i].code = nullptr;
        ht[i].bit = 0;
    }
    root = &ht[m];
    generateCodes(root, const_cast<char*>(""));//为所有节点赋哈夫曼编码

}
HT::~HT()
{
    delete[] ht;
}
void HT::select(int n, int& s1, int& s0)
{
    s1 = s0 = 0;//传入引用，因此可以改变最小值和次小值的下标值
    for (int i = 1; i <= n; i++)
    {
        if (ht[i].parent == 0) {//有父节点的，不能被搜索，相当于被树移除了
            if (s1 == 0)
                s1 = i;
            else
                s0 = i;
        }
    }
    for (int i = 1; i <= n; i++)
    {
        if (ht[i].parent == 0 && ht[s1].value > ht[i].value) {
            s1 = i;//找到最小的下标值
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
            s0 = j;//找到次小的下标值
        }
    }
}
void HT::decode(int n)//解码
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
                    if (strncmp(c, ht[i].code, im) == 0)//注意这里用的strncmp，因为每次比较数组的位数长度不同
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
    char text[200048] = "";//建立一个足够大的数组来存储
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
                        strcat(text, ht[i].code);//把识别到的每一个字母的编码拼接到现有的编码中 
                        break;//可以匹配的时候跳出循环
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
    cout << "index value data Lchild Rchild Parent code      bits" << endl;//输出
    cout << left;//左对齐
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
    result << "字符\t数量" << endl;
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
