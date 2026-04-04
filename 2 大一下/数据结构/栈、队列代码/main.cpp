#include <iostream>
#include <vector>
#include "my_containers.h"
using namespace std;

// 1. 括号匹配检查
bool isBracketMatched(const string& s) {
    Stack<char> st;
    for (char c : s) {
        if (c == '{' || c == '[' || c == '(') {
            st.push(c);
        } else {
            if (st.empty()) return false;
            char top = st.top();
            if ((c == '}' && top != '{') || 
                (c == ']' && top != '[') || 
                (c == ')' && top != '(')) {
                return false;
            }
            st.pop();
        }
    }
    return st.empty();
}

// 2. 所有可能的出栈序列
void getAllPopSequences(int n, vector<int>& current, Stack<int>& st, vector<vector<int>>& result) {
    if (current.size() == n) {
        result.push_back(current);
        return;
    }
    
    // 出栈操作
    if (!st.empty()) {
        int val = st.top();
        st.pop();
        current.push_back(val);
        getAllPopSequences(n, current, st, result);
        current.pop_back();
        st.push(val);
    }
    
    // 入栈操作
    if (st.size() < n - current.size()) {
        int next = current.size() + st.size() + 1;  // 修改为按顺序入栈
        st.push(next);
        getAllPopSequences(n, current, st, result);
        st.pop();
    }
}

// 3. 约瑟夫环问题（队列实现）
vector<int> josephusQueue(int n, int k, int m) {
    Queue<int> q;
    for (int i = 1; i <= n; ++i) {
        q.enqueue(i);
    }
    
    while (q.size() > m) {
        for (int i = 1; i < k; ++i) {
            q.enqueue(q.front());
            q.dequeue();
        }
        q.dequeue();
    }
    
    vector<int> result;
    while (!q.empty()) {
        result.push_back(q.front());
        q.dequeue();
    }
    return result;
}

int main() {
    // 测试括号匹配
    cout << "括号匹配测试:" << endl;
    string test1 = "{[](){}}";
    string test2 = "{[(})]";
    cout << test1 << ": " << (isBracketMatched(test1) ? "匹配" : "不匹配") << endl;
    cout << test2 << ": " << (isBracketMatched(test2) ? "匹配" : "不匹配") << endl;
    
    // 测试出栈序列
    cout << "\n请输入n的值: ";
    int n;
    cin >> n;
    cout << "出栈序列测试(n=" << n << "):" << endl;
    vector<vector<int>> sequences;
    vector<int> current;
    Stack<int> st;  // 修改为使用自定义Stack
    getAllPopSequences(n, current, st, sequences);
    for (auto& seq : sequences) {
        for (int num : seq) cout << num << " ";
        cout << endl;
    }
    cout << "总共有 " << sequences.size() << " 种可能的出栈序列" << endl;
    
    // 测试约瑟夫环
    cout << "\n约瑟夫环测试:" << endl;
    vector<int> result1 = josephusQueue(9, 2, 1);
    cout << "9 2 1: ";
    for (int num : result1) cout << num << " ";
    
    vector<int> result2 = josephusQueue(6, 5, 1);
    cout << "\n6 5 1: ";
    for (int num : result2) cout << num << " ";
    
    vector<int> result3 = josephusQueue(11, 3, 2);
    cout << "\n11 3 2: ";
    for (int num : result3) cout << num << " ";
    
    return 0;
}
 