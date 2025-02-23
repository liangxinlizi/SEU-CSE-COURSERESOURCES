#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <iomanip>
#include <map>
#include <ctype.h>
#define TOKEN_SIZE 1000
using namespace std;

// Define a type alias'mpair' which is a pair of two integers, representing the token type and its own value respectively.
typedef pair<int, int> mpair;

// Map to store identifiers, where the key is the identifier string and the value is an'mpair'.
map<string, mpair> flag_table;
// Map to store numbers, where the key is the number string and the value is an'mpair'.
map<string, mpair> num_table;
// Map to store strings, where the key is the string content and the value is an'mpair'.
map<string, mpair> str_table;

// Array of constant character pointers storing keywords in the language.
const char* KEY_WORDS[] = { "main", "int", "char", "if", "else", "for", "while", "return", "void", "float", "then", "switch", "break", "continue", "do", "const" };
// Array of constant character pointers storing operators in the language.
const char* OPERATORS[] = { "=", "+", "-", "*", "/", "(", ")", "[", "]", "{", "}", ",", ":", ";", ">", "<", ">=", "<=", "==", "\"" };

// String representing the start of a multi-line comment.
const char* COMMENT_START_MULTI = "/*";
// String representing the end of a multi-line comment.
const char* COMMENT_END_MULTI = "*/";
int mark_key[10];
int mark_ope[50];
// Spacing width for output formatting, set to 15 for the first column.
int width1 = 15;
// Spacing width for output formatting, set to 7 for the second column.
int width2 = 7;
// Spacing width for output formatting, set to 7 for the third column.
int width3 = 7;


// Function to check if a given character is part of a floating-point number.
// It returns true if the character is '.', 'e', 'E' or a digit.
bool isFloatPart(char ch)
{
    int asciiCode = static_cast<int>(ch);
    return (asciiCode == 46 || asciiCode == 101 || asciiCode == 69 || isdigit(static_cast<int>(ch)));
}



// Function to check if a given string is a keyword.
// It iterates through the KEY_WORDS array and compares with each element.
// If a match is found, it returns the index of the keyword in the array, otherwise returns -1.
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

// Function to check if a given string is an operator.
// It iterates through the OPERATORS array and compares with each element.
// If a match is found, it returns the index of the operator in the array, otherwise returns -1.
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

// Function to get the keyword or identifier from the input stream.
// It reads characters until a non-alphanumeric character is encountered, then forms a token.
// Checks if the token is a keyword or an identifier and processes accordingly.
void get_keyorid(char* token, char* ptr, FILE* fp)
{
    while (isalnum(*ptr)) {
        *++ptr = fgetc(fp);
    }
    ungetc(*ptr, fp);
    *ptr = '\0';
    int flag = iskey(token);
    if (flag != -1) {
        if (!mark_key[flag])
            mark_key[flag] = 1;
        cout << "(" << token << ",keyword," << flag + 1 << ")" << endl;
    }
    else {
        string s = "";
        map<string, mpair>::iterator it;
        s.append(token);
        it = flag_table.find(s);
        mpair mp;
        if (it == flag_table.end()) {
            mp = make_pair(10, flag_table.size() + 1);
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

// Function to get the number (integer or floating-point) from the input stream.
// It reads characters as long as they form a valid number representation.
// Determines if it's a float or an integer and stores it in the num_table accordingly.
void get_number(char* token, char* ptr, FILE* fp)
{
    bool isFloat = false;
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
            mp = make_pair(30, num_table.size() + 1);
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

// Function to check if the input stream contains a valid string.
// It reads characters starting from a '"' until another '"' is found or the end of file is reached.
// If a matching '"' is found, it stores the string in the str_table.
// Otherwise, it outputs an error message indicating the missing terminal '"'.
void try_string(char* token, char* ptr, FILE* fp)
{
    *++ptr = fgetc(fp);
    while (!feof(fp) && *ptr != '"') {
        *++ptr = fgetc(fp);
    }
    if (!feof(fp))
        *++ptr = '\0';
    else
        *ptr = '\0';
    string s = "", sub;
    s.append(token);
    if (s.size() > 0) {
        if (*(ptr - 1) == '"') {
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
        else {
            int i;
            int len = strlen(token);
            for (i = 0; i < len - 1; i++)
                ungetc(*--ptr, fp);
            cout << "(" << s << ",error,missing terminal '\"')" << endl;
        }
    }
}

// Function to handle a potential double operator.
// It reads the next character to form a possible double operator token and checks if it's a valid operator.
// If valid, it marks the operator and outputs relevant information. Otherwise, it tries to handle it as a single operator.
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

// Function to handle a potential single operator.
// It checks if the given token is a valid operator.
// If valid, it marks the operator and outputs relevant information. Otherwise, it outputs an error message for an unknown symbol.
void try_single_ope(char* token, char* ptr, FILE* fp)
{
    *++ptr = '\0';
    int sub = isope(token);
    if (sub != -1) {
        mark_ope[sub] = 1;
        cout << "(" << token << ",operator," << sub + 21 << ")" << endl;
    }
    else {
        if (token[0] < 0 || token[0] > 127)
            token[0] = '?';
        cout << "(" << token << ",error,unknown symbol)" << endl;
    }
}

// Function to handle a single-line comment.
// It reads characters until a newline character or the end of file is reached, effectively skipping the comment content.
void handle_single_comment(FILE* fp)
{
    char ch;
    while ((ch = fgetc(fp)) != '\n' && ch != EOF) {
    }
}

// Function to handle a multi-line comment.
// It reads characters until the end of the multi-line comment sequence "*/" is found or the end of file is reached.
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

// Function to judge the type of a string starting from a given character read from the input stream.
// Depending on the first character, it calls the appropriate function to handle keywords/identifiers, numbers, strings, operators or comments.
void judge_str(char ch, FILE* fp)
{
    char token[TOKEN_SIZE];
    char* ptr = token;
    *ptr = ch;
    char next_char = fgetc(fp);
    ungetc(next_char, fp);

    if (isalpha(*ptr)) {
        get_keyorid(token, ptr, fp);
    }
    else if (isdigit(*ptr)) {
        get_number(token, ptr, fp);
    }
    else if (*ptr == '"') {
        try_string(token, ptr, fp);
    }
    else if (*ptr == '>' || *ptr == '<' || *ptr == '=') {
        try_double_ope(token, ptr, fp);
    }
    else if (*ptr == '/' && next_char == '/') {
        handle_single_comment(fp);
    }
    else if (strncmp(COMMENT_START_MULTI, ptr, 2) == 0) {
        handle_multi_comment(fp);
    }
    else {
        try_single_ope(token, ptr, fp);
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
    // Output the identifier table.
    cout << "identifier table:" << endl;
    for (auto& it : flag_table) {
        cout << it.second.second << "   " << it.first << endl;
    }

    // Output the integer table.
    cout << "num table:" << endl;
    for (auto& it : num_table) {
        if (it.second.first == 20) {
            cout << it.second.second << "   " << it.first << endl;
        }
    }

    // Output the floating-point number table.
    cout << "float table:" << endl;
    for (auto& it : num_table) {
        if (it.second.first == 30) {
            cout << it.second.second << "   " << it.first << endl;
        }
    }

    return 0;
}