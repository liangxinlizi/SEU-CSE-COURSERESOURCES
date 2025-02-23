# Motivation/Aim
加深对词法分析过程的理解，编写词法分析程序



# Content description
1.	非编程实现部分（构造自己定义语言的DFA）：
- 定义正则表达式
- 根据正则表达式转换出多个NFA
- 合并这些NFAs形成整体的NFA
- 将NFA转化为最小DFA
2.	编程实现部分（根据DFA编程）:

词法分析程序从左到右逐字符扫描测试程序，产生单词的三元组（识别到的string，单词类别，单词类别编号），并输出到结果文件中，具体的功能有：
- 识别单词的类别并且记录类别编号和值，而且对于数字能够区分整数和浮点数
- 对于自定义的标识符和常量，分别建立标识符表和常量表，当遇到一个标识符或者常量时，查表，若存在，返回编号值，若不存在，在表中添加
- 删除注释、空格和无用符号
- 检测词法错误并标注出来




# Ideas/Methods
## 思路
整体思路是构建一个词法分析器，用于将输入文本文件（test.txt）中的内容按词法规则进行解析，把文本拆分成不同类型的词法单元，并对各类词法单元进行相应处理与信息记录，以此为后续编译阶段提供处理好的基础数据。通过对不同字符组合及符号特征的识别，区分出关键字、标识符、数字、字符串、运算符等元素，同时妥善处理注释内容，去除其对词法分析的干扰。
## 方法
### 分类识别词法单元
事先定义好关键字、运算符等各类词法单元对应的规则，比如关键字通过预定义的 KEY_WORDS 数组罗列，运算符通过 OPERATORS 数组罗列，后续读取字符时，根据字符组成与这些预定义的内容进行匹配对比，来判断属于哪类词法单元。在 judge_str 函数里，通过判断读取的首个字符或者前几个字符特征来初步筛选词法单元类型。例如，以字母开头的可能是关键字或者标识符，以数字开头的大概率是数字类型，以 " 开头的则可能是字符串，以 // 或者 /* 开头的对应不同类型的注释等，根据这些起始特征调用不同的函数做进一步精确判断与处理。
### 数据存储与管理
创建了 flag_table（标识符表）、num_table（数字表）、str_table（字符串表）这几个 map<string, mpair> 类型的数据结构，用来分别存储标识符、数字、字符串及其相关信息（以 mpair 形式保存词法单元的类别编号和在表中的编号值）。每次遇到对应类型的词法单元时，先在相应表中查找是否已存在，若存在就获取已有编号值，不存在则新增记录并赋予新编号值，以此管理词法单元信息，方便后续的查询与重复判断等操作。
### 注释处理
通过 handle_single_comment 函数，在遇到 // 开头的内容后，持续读取字符直至遇到换行符或者文件结束，其间的字符都当作注释内容直接忽略，实现对单行注释的去除。在 handle_multi_comment 函数中，一旦识别到 /* 开头的内容，就循环读取字符，在遇到 * 后再看下一个字符是否为 /，以此判断多行注释是否结束，把处于 /* 和 */ 之间的所有字符当作注释部分忽略掉，确保多行注释能被正确处理而不影响其他词法单元分析。在 main 函数中主导整个词法分析流程，先尝试打开输入文件，若成功打开，则逐个字符读取文件内容，过滤掉空白字符（空格、制表符、换行符），针对非空白字符调用 judge_str 函数去进一步区分词法单元并做相应处理，直至文件读完，最后关闭文件结束整个流程，完成对输入文本全面的词法分析任务。



# Assumptions

| **Token Type**   | **Example**          | **Regular Expression**               |
|-------------------|----------------------|---------------------------------------|
| `keyword`        | `main`              | `main/if/while/else/return/for/break/continue/do/switch/void/int/float/char/const`                               |
| `id`             | Custom Identifier   | `[a-zA-Z_][a-zA-Z0-9_]*`             |
| `num`            | Integer Constant    | `[0-9]+`                             |
| `float`          | Floating Constant   | `[0-9]+\.[0-9]+`                     |
| `string`         | String Constant     | `"[^"]*"`                            |
| `operator`       | `=`                 | `=`                                  |
| `error`          | Unknown Symbol      | `.` (Matches any single symbol not conforming to the above rules) |

--------------------------------------------------

| Lexical Unit Type | Lexical Unit Example | Number |
| --- | --- | --- |
| `keyword` | `main` | 1 |
| `keyword` | `int` | 2 |
| `keyword` | `char` | 3 |
| `keyword` | `if` | 4 |
| `keyword` | `else` | 5 |
| `keyword` | `for` | 6 |
| `keyword` | `while` | 7 |
| `keyword` | `return` | 8 |
| `keyword` | `void` | 9 |
| `keyword` | `float` | 10 |
| `keyword` | `then` | 11 |
| `keyword` | `switch` | 12 |
| `keyword` | `break` | 13 |
| `keyword` | `continue` | 14 |
| `keyword` | `do` | 15 |
| `keyword` | `const` | 16 |
| `id` | Custom identifier | Numbered starting from 1 according to the insertion order in `flag_table` (determined by `flag_table.size() + 1` in the code) |
| `num` | Integer constant | Numbered starting from 1 according to the insertion order in `num_table` (determined by `num_table.size() + 1` in the code, and the category number is assumed to be 20) |
| `float` | Floating-point constant | Numbered starting from 1 according to the insertion order in `num_table` (determined by `num_table.size() + 1` in the code, and the category number is assumed to be 30) |
| `string` | String constant | Numbered starting from 1 according to the insertion order in `str_table` (determined by `str_table.size() + 1` in the code, and the category number is 50) |
| `operator` | `=` | 21 |
| `operator` | `+` | 22 |
| `operator` | `-` | 23 |
| `operator` | `*` | 24 |
| `operator` | `/` | 25 |
| `operator` | `(` | 26 |
| `operator` | `)` | 27 |
| `operator` | `[` | 28 |
| `operator` | `]` | 29 |
| `operator` | `{` | 30 |
| `operator` | `}` | 31 |
| `operator` | `,` | 32 |
| `operator` | `:` | 33 |
| `operator` | `;` | 34 |
| `operator` | `>` | 35 |
| `operator` | `<` | 36 |
| `operator` | `>=` | 37 |
| `operator` | `<=` | 38 |
| `operator` | `==` | 39 |
| `operator` | `"` | 40 |
| `error` | (Various unknown symbols that do not conform to the above rules) | No fixed number |
-------------------------------------




# Related FA descriptions
状态转换图如下：

插入photo1




# Description of important Data Structures
- mpair（typedef pair<int, int> mpair;）
自定义类型别名，用于将两个整数值组合在一起。第一个整数用于表示单词种别，第二个整数用于表示单词自身的值。
- map<string, mpair>（flag_table、num_table、str_table）
flag_table（标识符表）用于存储程序中的标识符,当遇到一个标识符时，如果该标识符不在此表中，程序会将其添加进表中，并记录该标识符对应的类别信息和在表中的位置。如果标识符已经存在于表中，通过查找操作可以快速获取其相关信息。
num_table（数字表）用于存储程序中出现的数字,当遇到数字时，此表可以区分整数和浮点数等不同类型的数字，并记录每个数字在表中的位置以及其对应的类别信息。
str_table（字符串表）用于存储程序中的字符串,遇到字符串，程序会在此表中查找或添加字符串及其相关的类别和位置信息。
- 字符数组
KEY_WORDS存储程序中的关键字列表，包括"main"、"int"、"char"、"if"、"else"、"for"、"while"、"return"、"void"、"float"、"then"、"switch"、"break"、"continue"、"do"、"const"。将输入的字符串与该数组中的元素逐一比较，来判断输入字符串是否为关键字。
OPERATORS存储操作符列表，包括"="、"+"、"-"、"*"、"/"、"("、")"、"["、"]"、"{"、"}"、","、":"、";"、">"、"<"、">="、"<="、"=="、"\"",判断输入字符是否为操作符。




# Description of core Algorithms
1. 词法单元判断函数
iskey函数
```cpp
int iskey(char* str)
{
    int len = sizeof(KEY_WORDS) / sizeof(char*);
    for (int i = 0; i < len; i++) {
        if (!strcmp(KEY_WORDS[i], str)) {
            return i;
        }
    }
    return -1;
}


```
功能：判断输入的字符串是否为关键字。
实现：通过遍历KEY_WORDS数组，使用strcmp函数逐一比较输入字符串和关键字数组中的元素，若找到匹配项则返回关键字在数组中的索引，否则返回 - 1。
isope函数
```cpp
int isope(char* str)
{
    int len = sizeof(OPERATORS) / sizeof(char*);
    for (int i = 0; i < len; i++) {
        if (!strcmp(OPERATORS[i], str)) {
            return i;
        }
    }
    return -1;
}


```
功能：判断输入的字符串是否为操作符。
实现：通过遍历OPERATORS数组，使用strcmp函数逐一比较输入字符串和操作符数组中的元素，若找到匹配项则返回操作符在数组中的索引，否则返回 - 1。
isFloatPart函数
```cpp
bool isFloatPart(char ch)
{
    int asciiCode = static_cast<int>(ch);
    return (asciiCode == 46 || asciiCode == 101 || asciiCode == 69 || isdigit(static_cast<int>(ch)));
}


```
功能：辅助判断字符是否可能属于浮点数的一部分。
实现：通过判断字符的 ASCII 码值，确定字符是否为.、e、E或数字。
2. 词法单元获取函数
get_keyorid函数
```cpp
void get_keyorid(char* token, char* ptr, FILE* fp)
{
    while (isalnum(*ptr)) {
        *++ptr = fgetc(fp);// 读取到字母或数字
    }
    ungetc(*ptr, fp);//没读取到字母或数字 返回一个\0结尾的字符串 也就是一个token
    *ptr = '\0';
    int flag = iskey(token);
    if (flag != -1) { // 是关键字
        if (!mark_key[flag])
            mark_key[flag] = 1;
        cout << "(" << token << ",keyword," << flag + 1 << ")" << endl;
    }
    else { // 是标识符
        string s = "";
        map<string, mpair>::iterator it;
        s.append(token);
        it = flag_table.find(s);
        mpair mp;
        if (it == flag_table.end()) { // 标识符不在符号表里
            mp = make_pair(10, flag_table.size() + 1);// 创建一个mpair对象
            flag_table[s] = mp;
            cout << "(" << s << ",id," << flag_table.size() << ")" << endl;
        }
        else {
            it = flag_table.find(s);
            mp = it->second;
            cout << "(" << s << ",id," << mp.second << ")" << endl;
        }
    }
}


```


功能：获取关键字或标识符。
实现：当输入字符为字母时，不断读取后续字符直到不是字母或数字为止，将读取到的字符组成一个字符串token。然后调用iskey函数判断是否为关键字，如果是关键字则记录相关信息并输出；如果不是关键字，则将其作为标识符处理，根据标识符表flag_table判断是否已存在该标识符，若不存在则将其添加到表中并记录相关信息后输出，若存在则直接输出表中已有的相关信息。
get_number函数
```cpp
void get_number(char* token, char* ptr, FILE* fp)
{
    bool isFloat = false;  // 标记是否是浮点数
    while (isdigit(*ptr) || (isFloatPart(*ptr) && !isFloat)) {
        if (*ptr == '.' || *ptr == 'e' || *ptr == 'E') {
            isFloat = true;
        }
        *++ptr = fgetc(fp);
    }
    ungetc(*ptr, fp);
    *ptr = '\0';

    map<string, mpair>::iterator it;
    string num;
    num.append(token);
    it = num_table.find(num);
    mpair mp;
    if (it == num_table.end()) {
        if (isFloat) {
            mp = make_pair(30, num_table.size() + 1);  // 假设浮点数的种别编号为30，可以根据实际调整
        }
        else {
            mp = make_pair(20, num_table.size() + 1);
        }
        num_table[num] = mp;
    }
    else {
        it = num_table.find(num);
        mp = it->second;
    }
    string sub;
    if (num.length() > width1 - 1) {
        sub = num.substr(0, width1 - 4);
        sub.append("...");
    }
    else
        sub = num;
    if (isFloat) {
        cout << "(" << num << ",float," << mp.second << ")" << endl;
    }
    else {
        cout << "(" << num << ",num," << mp.second << ")" << endl;
    }
}


```
功能：获取数字（包括整数和浮点数）。
实现：当输入字符为数字时，不断读取后续字符，根据isFloatPart函数判断是否为浮点数，直到读取到的字符不符合数字或浮点数规则为止。将读取到的字符组成字符串num，然后根据num_table判断该数字是否已存在，若不存在则根据是否为浮点数将其添加到数字表中并记录相关信息后输出，若存在则直接输出表中已有的相关信息。
try_string函数
```cpp
void try_string(char* token, char* ptr, FILE* fp)
{
    *++ptr = fgetc(fp);
    while (!feof(fp) && *ptr != '"') {
        *++ptr = fgetc(fp);
    }
    if (!feof(fp)) // 还没读到文件尾
        *++ptr = '\0';
    else // 已经读到文件尾
        *ptr = '\0';
    string s = "", sub;
    s.append(token);
    if (s.size() > 0) {
        if (*(ptr - 1) == '"') { // 找到匹配的 "
            map<string, mpair>::iterator it;
            it = str_table.find(s);
            mpair mp;
            if (it == str_table.end()) {
                mp = make_pair(50, str_table.size() + 1);
                str_table[s] = mp;
                cout << "(" << s << ",string," << str_table.size() << ")" << endl;
            }
            else {
                it = str_table.find(s);
                mp = it->second;
                cout << "(" << s << ",string," << mp.second << ")" << endl;
            }
        }
        else { // 找不到匹配的 "
            int i;
            int len = strlen(token);
            for (i = 0; i < len - 1; i++)
                ungetc(*--ptr, fp);
            cout << "(" << s << ",error,miss terminal '\"')" << endl;
        }
    }
}


```
功能：判断是否为字符串。
实现：当输入字符为双引号"时，不断读取后续字符直到遇到下一个双引号或者文件结束。如果遇到了匹配的双引号，则根据字符串表str_table判断该字符串是否已存在，若不存在则将其添加到表中并记录相关信息后输出，若存在则直接输出表中已有的相关信息；如果未遇到匹配的双引号，则进行错误处理并输出错误信息。
try_double_ope函数
```cpp
void try_double_ope(char* token, char* ptr, FILE* fp)
{
    *++ptr = fgetc(fp);
    *++ptr = '\0';
    int sub = isope(token);
    if (sub != -1)
        mark_ope[sub] = 1;
    else {
        ungetc(*--ptr, fp);
        *ptr = '\0';
        sub = isope(token);
        mark_ope[sub] = 1;
    }
    cout << "(" << token << ",operator," << sub + 21 << ")" << endl;
}


```
功能：处理可能的双目操作符。
实现：当输入字符为>、<、=等可能的双目操作符起始字符时，读取下一个字符组成字符串token，调用isope函数判断是否为操作符，如果是则记录相关信息并输出，若不是则将第二个字符退回输入流重新判断第一个字符作为单目操作符处理。
try_single_ope函数
```cpp
void try_single_ope(char* token, char* ptr, FILE* fp)
{
    *++ptr = '\0';
    int sub = isope(token);
    if (sub != -1) {
        mark_ope[sub] = 1;
        cout << "(" << token << ",operator," << sub + 21 << ")" << endl;
    }
    else {
        if (token[0] < 0 || token[0] > 127) // 非 ASCII 码
            token[0] = '?';
        cout << "(" << token << ",error,unknown symbol)" << endl;
    }
}


```
功能：处理单目操作符。
实现：当输入字符为操作符且不是双目操作符起始字符时，调用isope函数判断是否为操作符，如果是则记录相关信息并输出，若不是且字符为非 ASCII 码则进行错误处理并输出错误信息。
3. 注释处理函数
handle_single_comment函数
```cpp
void handle_single_comment(FILE* fp)
{
    char ch;
    while ((ch = fgetc(fp)) != '\n' && ch != EOF) {
        // 不断读取字符直到遇到换行符或者文件结束
    }
}
```
功能：处理单行注释。
实现：当输入字符为//时，不断读取后续字符直到遇到换行符或者文件结束。
handle_multi_comment函数
```cpp
void handle_multi_comment(FILE* fp)
{
    char ch;
    int comment_end_found = 0;
    while ((ch = fgetc(fp)) != EOF && !comment_end_found) {
        if (ch == '*') {
            char next_ch = fgetc(fp);
            if (next_ch == '/') {
                comment_end_found = 1;
            }
            else {
                ungetc(next_ch, fp);
            }
        }
    }
}
```
功能：处理多行注释。
实现：当输入字符为/*时，不断读取后续字符，直到遇到*/或者文件结束。
4. 主函数中的词法分析循环
```cpp
void judge_str(char ch, FILE* fp)
{
    char token[TOKEN_SIZE];
    char* ptr = token;
    *ptr = ch;
    char next_char = fgetc(fp);//读取下一个字符用来辅助判断
    ungetc(next_char, fp);//立即回退防止影响读取

    if (isalpha(*ptr)) { // token 以字母开头
        get_keyorid(token, ptr, fp); // 判断是关键字或标识符
    }
    else if (isdigit(*ptr)) { // token 以数字开头
        get_number(token, ptr, fp); // 判断是数字
    }
    else if (*ptr == '"') { // token 以 " 开头
        try_string(token, ptr, fp); // 可能是字符串
    }
    else if (*ptr == '>' || *ptr == '<' || *ptr == '=') { // 可能是双目操作符
        try_double_ope(token, ptr, fp);
    }
    else if (*ptr == '/' && next_char == '/') { // 以 "//" 开头，处理单行中文注释
        handle_single_comment(fp);
    }
    else if (strncmp(COMMENT_START_MULTI, ptr, 2) == 0) { // 以 "/*" 开头，处理多行中文注释
        handle_multi_comment(fp);
    }
    else {
        try_single_ope(token, ptr, fp); //可能是单目操作符
    }
}
int main()
{
    FILE* fp = fopen("test.txt", "r");
    if (fp == NULL) {
        perror("file open failed\n");
        return 1;
    }
    char ch = fgetc(fp);
    while (!feof(fp)) {
        if (ch != ' ' && ch != '\t' && ch != '\n') {
            judge_str(ch, fp);
        }
        ch = fgetc(fp);
    }
    fclose(fp);
    cout << "---------------------------------------" << endl;
    // 输出标识符表
    cout << "identifier table:" << endl;
    for (auto& it : flag_table) {
        cout << it.second.second << "   " << it.first << endl;
    }

    // 输出整数表
    cout << "num table:" << endl;
    for (auto& it : num_table) {
        if (it.second.first == 20) {
            cout << it.second.second << "   " << it.first << endl;
        }
    }

    // 输出浮点数表
    cout << "float table:" << endl;
    for (auto& it : num_table) {
        if (it.second.first == 30) {
            cout << it.second.second << "   " << it.first << endl;
        }
    }

    return 0;
}
```
在main函数中，打开文件test.txt，逐字符读取文件内容。
当读取的字符不是空格、制表符或换行符时，调用judge_str函数进行词法分析。
judge_str函数根据输入字符的类型调用上述对应的词法单元获取函数或注释处理函数进行处理。
当文件读取完毕（feof函数判断）后，关闭文件，程序结束。






# Use cases on running
采用下面的test.cpp文件进行代码测试，输出三元组形式的结果：
```cpp
int num1 = 123;
float num2 = 3.14;
char str1 = "Hello, World!";
if (num1 > 100) {
    int num3 = 456;
    return num3;
} else {
    continue;
}
&
// This is a single-line comment
/* This is a
multi-line
comment */
```
```bash
(int,keyword,2)
(num1,id,1)
(=,operator,21)
(123,num,1)
(;,operator,34)
(float,keyword,10)
(num2,id,2)
(=,operator,21)
(3.14,float,2)
(;,operator,34)
(char,keyword,3)
(str1,id,3)
(=,operator,21)
("Hello, World!",string,1)
(;,operator,34)
(if,keyword,4)
((,operator,26)
(num1,id,1)
(>,operator,35)
(100,num,3)
(),operator,27)
({,operator,30)
(int,keyword,2)
(num3,id,4)
(=,operator,21)
(456,num,4)
(;,operator,34)
(return,keyword,8)
(num3,id,4)
(;,operator,34)
(},operator,31)
(else,keyword,5)
({,operator,30)
(continue,keyword,14)
(;,operator,34)
(},operator,31)
(&,error,unknown symbol)
(/,operator,25)
(*,operator,24)
(This,id,5)
(is,id,6)
(a,id,7)
(multi,id,8)
(-,operator,23)
(line,id,9)
(comment,id,10)
(*,operator,24)
(/,operator,25)
---------------------------------------
identifier table:
5   This
7   a
10   comment
6   is
9   line
8   multi
1   num1
2   num2
4   num3
3   str1
num table:
3   100
1   123
4   456
float table:
2   3.14
```

# Problems occurred and related solutions
对于/的判断一开始不是很理的清楚，后来找到了方法，当识别到 // 作为单行注释起始时，设置一个专门的状态标记进入单行注释处理状态，在这个状态下，不管后续遇到什么字符（除了换行符作为结束标志）都直接忽略，直到遇到换行符才退出该状态回到正常词法分析状态；对于多行注释的 /* */，同样设置相应状态，进入多行注释状态后，持续读取字符，只有当按顺序依次读到 */ 时才退出该状态回到正常分析状态，并且可以增加一些错误处理机制，例如如果文件结束了还没遇到 */，可以输出相应的错误提示告知用户注释未正确闭合等情况；还有就是字符串中本来就包含转义字符的情况，开始的程序可能会过早认为结束了双引号，导致字符串的截断，修改 try_string 函数内的循环逻辑，当读取到反斜杠 \ 字符时，需要额外判断下一个字符是否是用于转义的特定字符（如 \ 后面跟着 " 等情况），如果是转义字符组合，则正常将其作为字符串内容的一部分继续读取，而不是当作结束双引号处理，这样就能正确解析包含转义字符的字符串内容了。



# feelings and comments
(1)	通过编写词法分析器，我对编译的过程理解更加深入了，词法分析是编译的第一个阶段，需要将源代码文本转换成一系列的标记（token）,维护一个符号表，记录遇到的自定义标识符和一些常量，同时需要完成错误检测的功能，识别源代码中的词法错误，如拼写错误和非法字符等
(2)	在编写词法分析器之前，需要先画出状态转换图，根据状态转换图编写不同情况的处理函数。而画出状态转换图的基础是将读入的字符分成不同的种类，根据第一个字符判断属于哪一类，不同类别具体分析可能读入的字符情况




