# Motivation/Aim
加深对语法分析过程的理解，编写LR(1)文法的语法分析程序
# Content description
1.	非编程实现部分：
(1)	定义上下文无关文法
(2)	根据定义的文法画出DFA，每一个状态的实现需要通过构建LR(1)项目的闭包，通过构造树来实现
(3)	根据DFA画出Action表和Goto表
2.	编程实现部分（根据各产生式、Action表和Goto表编程）


# Ideas/Methods
LR(1)文法采用自底向上分析方法，语法分析器从左到右逐字符扫描表达式，放入符号栈，根据Action表和Goto表进行移入或规约操作，同时修改符号栈和状态栈，输出动作说明（移入还是规约，规约使用的产生式是什么）。若当前分析的符号和状态栈栈顶状态无对应的Action操作，则报错，认为输入符号串非法。

主要方法是循环分析读取当前状态和输入字符串中的当前符号，根据动作表确定应执行的动作。
移进动作：如果动作表指示移进（动作值大于 0），将当前符号压入符号栈，将动作值对应的状态压入状态栈，然后移动到输入字符串的下一个符号。
归约动作：若动作表指示归约（动作值小于 0），根据动作值确定要应用的语法产生式。从符号栈和状态栈中弹出与产生式右部符号数量相同的元素，然后根据当前状态和产生式左部符号，通过转移表得到新的状态，将新状态压入状态栈，产生式左部符号压入符号栈。
接受动作：当动作值为 0 时，表示输入字符串已成功分析，符合语法规则。
错误处理：如果动作值为 -1 ，表示遇到了无法处理的符号，输入字符串不符合语法规则。
# Assumptions

使用project1中定义的tokens，构造一个上下文无关文法：

```plaintext
S' -> S
S -> L = R
S -> R
L -> * R
L -> i
R -> L
R -> i
R -> n
```

为了写起来简洁，把project1的identifier定义为i，num定义为n，并且使用operator中的=号，*号来构建此文法。
画出状态转换图DFA：
here is a photo DFA
here is a table

# Related FA descriptions
画出状态转换图DFA：
here is a photo DFA
here is a table
# Description of important Data Structures

## 类**LRAnalyseTable**为LR分析表类

成员变量包含 ：所有产生式，终结符，非终结符，终结符个数，非终结符个数，构造出的Action表，Goto表

Action表和Coto表初始化如下，其中，-1表示没有对应的操作，即表中对应格子没有填写任何操作，小于-10的数字表示规约，在该数字上+10再取相反数即得到规约所用产生式的标号（产生式标号范围为0-7）
```cpp
class LRParseTable {
private:
    // Productions
    string grammar[15] = { "T->S", "S->L=R", "S->R", "L->*R", "L->i", "R->L", "R->i", "R->n" };
    // Terminals
    char terminalChars[10] = { '*', '=', 'i', '#', 'n' };
    // Non-terminals
    char nonTerminalChars[10] = { 'S', 'L', 'R' };
    // Number of terminals
    int numTerminals = 5;
    // Number of non-terminals
    int numNonTerminals = 3;

    // Action table
    int Action[20][5] = {
        {1, -1, 5, -1, 6}, {-1, -1, 9, -1, 10}, {-1, 11, -1, -15, -1}, {-1, -1, -1, -12, -1},
        {-1, -1, -1, 0, -1}, {-1, -1, -1, -14, -1}, {-1, -1, -1, -17, -1}, {-1, -15, -1, -15, -1},
        {-1, -13, -1, -13, -1}, {-1, -14, -1, -14, -1}, {-1, -17, -1, -17, -1}, {12, -1, 15, -1, 6},
        {12, -1, 15, -1, 6}, {-1, -1, -1, -15, -1}, {-1, -1, -1, -11, -1}, {-1, -1, -1, -16, -1}, {-1, -1, -1, -13, -1}
    };
    // Goto table
    int Goto[20][4] = {
        {4, 2, 3}, {-1, 7, 8}, {-1, -1, -1}, {-1, -1, -1}, {-1, -1, -1},
        {-1, -1, -1}, {-1, -1, -1}, {-1, -1, -1}, {-1, -1, -1},
        {-1, -1, -1}, {-1, -1, -1}, {-1, 13, 14}, {-1, 13, 16},
        {-1, -1, -1}, {-1, -1, -1}, {-1, -1, -1}, {-1, -1, -1}
    };

public:
    LRParseTable() {}
    ~LRParseTable() {}
    int getTerminalIndex(char ch);
    int getNonTerminalIndex(char ch);
    int getAction(int state, char ch);
    int getGoto(int state, char ch);
    string getGrammar(int idx);
};
```
构造的操作（函数）包括：
根据终结符字符获取该终结符字符在终结符数组中的下标
根据非终结符字符获取其在非终结符数组中的下标
根据栈顶状态和当前符号查询Action表，获得对应动作
根据栈顶状态和当前符号查询Goto表，获得对应动作（该函数用于规约后）
根据规约使用的产生式编号，查找产生式数组获得相应的产生式
## 类**Analyser**为语法分析器
成员变量包含：待分析的字符串，记录当前为第几步操作，当前分析的符号在待分析字符串中的下标，符号栈，状态栈
```cpp
class Parser {
private:
    string inputString; // String to be parsed
    int step;           // Step count
    int currentIndex;   // Current index of the input string
    vector<char> symbolStack; // Symbol stack
    vector<int> stateStack;   // State stack
public:
    Parser();
    ~Parser();
    bool startParsing(string input);
    string stackToString(int option);
};
Parser::Parser() {
    this->step = 1;
    this->currentIndex = 0;
    symbolStack.push_back('#');
    stateStack.push_back(0);
}
```
构造的操作（函数）包括：
初始化语法分析器：步骤初始化为1，当前分析符号的下标初始化为0
返回状态栈或符号栈中的所有状态或字符：用于输出展示（该函数根据传入参数选择是返回状态栈中内容还是符号栈中内容）
核心分析函数：实现对读入字符串的分析，判断当前字符是否合法，如合法时进行移入操作还是规约操作，同时修改符号栈和状态栈，若是规约操作规约完成后还需要查询Goto表修改状态栈。具体算法在第五部分核心算法中描述。

# Description of core Algorithms
LR核心算法是startParsing函数，具体算法如下：
```cpp

bool Parser::startParsing(string input) {
    this->inputString = input;
    LRParseTable table;
    int currentState = 0;

    cout << setw(10) << "Step" << setw(15) << "State Stack" << setw(10) << "Symbol Stack" << setw(15) << "Current Symbol" << setw(15) << "Remaining String" << setw(20) << "Action" << endl;

    while (true) {
        int action = table.getAction(currentState, inputString[currentIndex]);
        if (action == 0) {
            cout << setw(10) << step << setw(15) << stackToString(0) << setw(10) << stackToString(1) << setw(15) << inputString[currentIndex] << setw(15) << inputString.substr(currentIndex) << setw(20) << "Parsing complete" << endl;
            return true;
        }
        if (action == -1) {
            cerr << "Error: Unexpected symbol '" << inputString[currentIndex] << "' at index " << currentIndex << endl;
            return false;
        }
        if (action > 0) {
            cout << setw(10) << step << setw(15) << stackToString(0) << setw(10) << stackToString(1) << setw(15) << inputString[currentIndex] << setw(15) << inputString.substr(currentIndex) << setw(20) << "Action[S" << currentState << "][" << inputString[currentIndex] << "]=S" << action << " (Shift)" << endl;
            stateStack.push_back(action);
            symbolStack.push_back(inputString[currentIndex]);
            currentIndex++;
        }
        else {
            int ruleIdx = -(action + 10);
            string rule = table.getGrammar(ruleIdx);
            if (rule.empty()) return false;

            cout << setw(10) << step << setw(15) << stackToString(0) << setw(10) << stackToString(1) << setw(15) << inputString[currentIndex] << setw(15) << inputString.substr(currentIndex) << setw(20) << "R" << ruleIdx + 1 << ": " << rule << " (Reduce)" << endl;

            for (size_t i = 0; i < rule.size() - 3; i++) {
                if (stateStack.empty() || symbolStack.empty()) {
                    cerr << "Error: Stack underflow during reduction." << endl;
                    return false;
                }
                stateStack.pop_back();
                symbolStack.pop_back();
            }
            currentState = stateStack.back();
            int gotoResult = table.getGoto(currentState, rule[0]);
            if (gotoResult == -1) return false;
            cout << setw(10) << ++step << setw(15) << stackToString(0) << setw(10) << stackToString(1) << setw(15) << rule[0] << setw(15) << inputString.substr(currentIndex) << setw(20) << "Goto[S" << currentState << "][" << rule[0] << "]=" << gotoResult << " (State Transition)" << endl;
            stateStack.push_back(gotoResult);
            symbolStack.push_back(rule[0]);
        }
        currentState = stateStack.back();
        step++;
    }
}
```
首先进行初始化操作，将输入字符串存储在inputString中，设定步骤数step为 1，当前索引currentIndex为 0，同时把'#'压入符号栈symbolStack，初始状态 0 压入状态栈stateStack。然后进入循环分析阶段，获取当前状态currentState下，输入字符串当前位置inputString[currentIndex]对应的动作action，并依据action的值进行不同类型的动作判断：若action == 0，表示分析成功，输出分析完成信息并返回true；若action == -1，意味着遇到意外符号，输出错误信息并返回false；若action > 0，执行移进操作，即将状态action压入状态栈，当前符号inputString[currentIndex]压入符号栈，然后将currentIndex加 1；若action < 0，则进行归约操作，先根据action计算出要应用的语法产生式的索引ruleIdx，接着从状态栈和符号栈中弹出与产生式右部符号数量相同的元素，之后获取当前状态currentState并计算应用产生式后的转移状态gotoResult，最后将gotoResult压入状态栈，把产生式左部符号压入符号栈。完成一次动作判断后，将当前状态更新为状态栈的栈顶元素，并增加步骤数step，如此循环直至分析结束 。

main函数如下：
```cpp

int main() {
    FILE* in;
    FILE* out;
    if (freopen_s(&in, "test.txt", "r", stdin) != 0) {
        cerr << "Error: Unable to open test.txt for reading." << endl;
        return 1;
    }
    if (freopen_s(&out, "result.txt", "w", stdout) != 0) {
        cerr << "Error: Unable to open result.txt for writing." << endl;
        return 1;
    }

    string str;
    int caseCount = 1;
    while (getline(cin, str)) {
        cout << "Case " << caseCount++ << ": " << str << endl;
        Parser parser;
        if (parser.startParsing(str)) {
            cout << "The input string '" << str << "' is valid." << endl;
        }
        else {
            cout << "The input string '" << str << "' is invalid." << endl;
        }
        cout << endl;
    }
    return 0;
}
```
在main函数中，程序从test.txt文件读取输入字符串，对每个输入字符串进行 LR 分析，并将结果输出到result.txt文件。







# Use cases on running
测试用例test.txt：
```plaintext
i=i#
*i=i#
*i#
i#
=i#
ii#
```
终端输出结果bash：
```bash
Error: Unexpected symbol '=' at index 1
Error: Unexpected symbol '=' at index 0
Error: Unexpected symbol 'i' at index 1
```


输出结果result.txt：
```plaintext
Case 1: i=i#
      Step    State StackSymbol Stack Current SymbolRemaining String              Action
         1              0         #              i           i=i#            Action[S0][i]=S5 (Shift)
The input string 'i=i#' is invalid.

Case 2: *i=i#
      Step    State StackSymbol Stack Current SymbolRemaining String              Action
         1              0         #              *          *i=i#            Action[S0][*]=S1 (Shift)
         2            0_1        #*              i           i=i#            Action[S1][i]=S9 (Shift)
         3          0_1_9       #*i              =            =i#                   R5: L->i (Reduce)
         4            0_1        #*              L            =i#              Goto[S1][L]=7 (State Transition)
         5          0_1_7       #*L              =            =i#                   R6: R->L (Reduce)
         6            0_1        #*              R            =i#              Goto[S1][R]=8 (State Transition)
         7          0_1_8       #*R              =            =i#                   R4: L->*R (Reduce)
         8              0         #              L            =i#              Goto[S0][L]=2 (State Transition)
         9            0_2        #L              =            =i#            Action[S2][=]=S11 (Shift)
        10         0_2_11       #L=              i             i#            Action[S11][i]=S15 (Shift)
        11      0_2_11_15      #L=i              #              #                   R7: R->i (Reduce)
        12         0_2_11       #L=              R              #              Goto[S11][R]=14 (State Transition)
        13      0_2_11_14      #L=R              #              #                   R2: S->L=R (Reduce)
        14              0         #              S              #              Goto[S0][S]=4 (State Transition)
        15            0_4        #S              #              #    Parsing complete
The input string '*i=i#' is valid.

Case 3: *i#
      Step    State StackSymbol Stack Current SymbolRemaining String              Action
         1              0         #              *            *i#            Action[S0][*]=S1 (Shift)
         2            0_1        #*              i             i#            Action[S1][i]=S9 (Shift)
         3          0_1_9       #*i              #              #                   R5: L->i (Reduce)
         4            0_1        #*              L              #              Goto[S1][L]=7 (State Transition)
         5          0_1_7       #*L              #              #                   R6: R->L (Reduce)
         6            0_1        #*              R              #              Goto[S1][R]=8 (State Transition)
         7          0_1_8       #*R              #              #                   R4: L->*R (Reduce)
         8              0         #              L              #              Goto[S0][L]=2 (State Transition)
         9            0_2        #L              #              #                   R6: R->L (Reduce)
        10              0         #              R              #              Goto[S0][R]=3 (State Transition)
        11            0_3        #R              #              #                   R3: S->R (Reduce)
        12              0         #              S              #              Goto[S0][S]=4 (State Transition)
        13            0_4        #S              #              #    Parsing complete
The input string '*i#' is valid.

Case 4: i#
      Step    State StackSymbol Stack Current SymbolRemaining String              Action
         1              0         #              i             i#            Action[S0][i]=S5 (Shift)
         2            0_5        #i              #              #                   R5: L->i (Reduce)
         3              0         #              L              #              Goto[S0][L]=2 (State Transition)
         4            0_2        #L              #              #                   R6: R->L (Reduce)
         5              0         #              R              #              Goto[S0][R]=3 (State Transition)
         6            0_3        #R              #              #                   R3: S->R (Reduce)
         7              0         #              S              #              Goto[S0][S]=4 (State Transition)
         8            0_4        #S              #              #    Parsing complete
The input string 'i#' is valid.

Case 5: =i#
      Step    State StackSymbol Stack Current SymbolRemaining String              Action
The input string '=i#' is invalid.

Case 6: ii#
      Step    State StackSymbol Stack Current SymbolRemaining String              Action
         1              0         #              i            ii#            Action[S0][i]=S5 (Shift)
The input string 'ii#' is invalid.
```




# Problems occurred and related solutions
一开始对于action表和goto表的构造错误，导致程序运行结果的错误，解析器进入无限循环，后来手动解决了这个问题，程序能够准确运行。
在ACTION表中既有移入操作又有规约操作，为区分这两种操作，规约操作用小于-10的负数表示，具体转换方法为：规约所用产生式标号+10后取相反数
在从状态栈和符号栈中弹出元素的数量不正确，导致试图访问空栈，我修改了负责归约操作的代码，使其能够根据产生式规则的长度正确计算要弹出的符号数量。

# Your feelings and comments
(1)	通过本次实验，我对LR(1)分析有了更加深入的理解，因为这是一种自底向上的分析方法，所以可以边扫描待分析字符边分析。构造LR(1)语法分析器之前需要进行一些准备操作，首先要画出DFA，对于LR(1)分析，分析时要向后多看一位，所以LR(1)项目中不仅有产生式，还需要带上预测符，即使产生式相同，如果预测符不同也是表示不同的状态。之后需要根据DFA画出ACTION和GOTO表，并以此编写程序。
(2)	规约之后还需要根据更新后的符号栈和状态栈顶的符号和状态查询GOTO表更新状态栈顶，这是我在之前的学习中没有注意到的细节，同时也体现了GOTO表的作用，做实验前我也不太清楚为什么要分ACTION和GOTO两个表，经过此次实验后理解得更加深刻了。


