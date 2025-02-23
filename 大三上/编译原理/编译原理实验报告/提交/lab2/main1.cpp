#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
using namespace std;

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

int LRParseTable::getTerminalIndex(char ch) {
    for (int i = 0; i < numTerminals; i++) {
        if (ch == terminalChars[i]) {
            return i;
        }
    }
    return -1;
}

int LRParseTable::getNonTerminalIndex(char ch) {
    for (int i = 0; i < numNonTerminals; i++) {
        if (ch == nonTerminalChars[i]) {
            return i;
        }
    }
    return -1;
}

int LRParseTable::getAction(int state, char ch) {
    int terminalIdx = getTerminalIndex(ch);
    if (terminalIdx == -1) {
        cerr << "Error: Unknown terminal character: " << ch << endl;
        return -1;
    }
    return Action[state][terminalIdx];
}

int LRParseTable::getGoto(int state, char ch) {
    int nonTerminalIdx = getNonTerminalIndex(ch);
    if (nonTerminalIdx == -1) {
        cerr << "Error: Unknown non-terminal character: " << ch << endl;
        return -1;
    }
    return Goto[state][nonTerminalIdx];
}

string LRParseTable::getGrammar(int idx) {
    if (idx < 0 || idx >= 15) {
        cerr << "Error: Invalid grammar index: " << idx << endl;
        return "";
    }
    return grammar[idx];
}

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

Parser::~Parser() {}

string Parser::stackToString(int option) {
    string result = "";
    if (option == 0) {
        for (int state : stateStack) {
            if (!result.empty()) result += "_";
            result += to_string(state);
        }
    }
    else {
        for (char symbol : symbolStack) {
            result += symbol;
        }
    }
    return result;
}

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
