#pragma once
#include<iostream>
using namespace std;
typedef int ElemType;
typedef struct seqList{
    int length;
    ElemType element[100];
}SqList;

void InitList(SqList& L) {
    L.length = 0;
}
bool ListInsert(SqList& L, ElemType e, int i)
{
    int j;
    if (i<-1 || i>L.length + 1)
        return false;

    for (j = L.length - 1; j >= i - 1; j--) {
        L.element[j + 1] = L.element[j];
    }
    L.element[i - 1] = e;
    L.length++;
    return true;
}
void PrintList(SqList L) {
    if (L.length == 0)
    {
        cout << endl;
        return;
    }
    cout << "(";
    for (int i = 0; i < L.length; i++) {
        if (i == L.length - 1)
            cout << L.element[i];
        else
            cout << L.element[i] << ",";
    }
    cout << ")";
    cout << endl;
}
//题目1
// 有序插入元素
bool ListInsert2(SqList& L, int x) {
    int i;
    for (i = 0; i < L.length; i++) {
        if (L.element[i] >= x) {
            break;
        }
    }
    for (int j = L.length; j > i; j--) {
        L.element[j] = L.element[j - 1];
    }
    L.element[i] = x;
    L.length++;
    return true;
}
void algorithm_1(){
    SqList L;
    InitList(L);
    int data[] = { 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 };
    for (int i = 0; i < 10; i++) {
        L.element[i] = data[i];
        L.length++;
    }
    int x[] = { 25, 85, 110, 8 };
    for (int i = 0; i < 4; i++) {

        if (ListInsert2(L, x[i])) {
            cout << "插入 " << x[i] << " 后的顺序表: ";
            PrintList(L);
        }
    }
}
//题目2
// 分解顺序表
void SplitList(const SqList& L, SqList& oddList, SqList& evenList) {
    for (int i = 0; i < L.length; ++i) {
        if (L.element[i] % 2 == 1) {
            ListInsert(oddList, L.element[i], oddList.length + 1);
        }
        else {
            ListInsert(evenList, L.element[i], evenList.length + 1);
        }
    }
}
void algorithm_2()
{
    //第一组数据
    SqList L1, oddList1, evenList1;
    InitList(L1);
    InitList(oddList1);
    InitList(evenList1);
    int data1[] = { 1,2,3,4,5,6,7,8,9,10,10, 30, 40, 50, 60 };
    for (int i = 0; i < 15; i++) {
        ListInsert(L1, data1[i], L1.length + 1);
    }
    cout << "第一组数据原顺序表: ";
    PrintList(L1);
    SplitList(L1, oddList1, evenList1);
    cout << "奇数顺序表: ";
    PrintList(oddList1);
    cout << "偶数顺序表: ";
    PrintList(evenList1);
    // 第二组数据
    SqList L2, oddList2, evenList2;
    InitList(L2);
    InitList(oddList2);
    InitList(evenList2);
    int data2[] = { 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 };
    for (int i = 0; i < 10; ++i) {
        ListInsert(L2, data2[i], L2.length + 1);
    }
    cout << "第二组数据原顺序表: ";
    PrintList(L2);
    SplitList(L2, oddList2, evenList2);
    cout << "奇数顺序表: ";
    PrintList(oddList2);
    cout << "偶数顺序表: ";
    PrintList(evenList2);
}
//题目3
// 求两个顺序表的公共元素
void FindCommonElements(const SqList& L1, const SqList& L2, SqList& L3) {
    int i = 0, j = 0;
    if (L1.length == 0 || L2.length == 0)
    {
        return;
    }
    while (i < L1.length && j < L2.length) {
        if (L1.element[i] == L2.element[j]) {
            ListInsert(L3, L1.element[i], L3.length + 1);
            i++;
            j++;
        }
        else if (L1.element[i] < L2.element[j]) {
            i++;
        }
        else {
            j++;
        }
    }
}
void algorithm_3() {
    // 第一组数据
    SqList L1_1, L2_1, L3_1;
    InitList(L1_1);
    InitList(L2_1);
    InitList(L3_1);
    int data1_1[] = { 1, 3, 6, 10, 15, 16, 17, 18, 19, 20 };
    int data2_1[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 18, 20, 30 };
    for (int i = 0; i < 10; i++) {
        ListInsert(L1_1, data1_1[i], L1_1.length + 1);
    }
    for (int i = 0; i < 13; i++) {
        ListInsert(L2_1, data2_1[i], L2_1.length + 1);
    }
    cout << "第一组数据：" << endl;
    cout << " 第一个顺序表: ";
    PrintList(L1_1);
    cout << "第二个顺序表: ";
    PrintList(L2_1);
    FindCommonElements(L1_1, L2_1, L3_1);
    cout << " 公共元素组成的顺序表: ";
    PrintList(L3_1);
    // 第二组数据
    SqList L1_2, L2_2, L3_2;
    InitList(L1_2);
    InitList(L2_2);
    InitList(L3_2);
    int data1_2[] = { 1, 3, 6, 10, 15, 16, 17, 18, 19, 20 };
    int data2_2[] = { 2, 4, 5, 7, 8, 9, 12, 22 };
    for (int i = 0; i < 10; ++i) {
        ListInsert(L1_2, data1_2[i], L1_2.length + 1);
    }
    for (int i = 0; i < 8; ++i) {
        ListInsert(L2_2, data2_2[i], L2_2.length + 1);
    }
    cout << "第二组数据：" << endl;
    cout << "第一个顺序表: ";
    PrintList(L1_2);
    cout << " 第二个顺序表: ";
    PrintList(L2_2);
    FindCommonElements(L1_2, L2_2, L3_2);
    cout << "公共元素组成的顺序表: ";
    PrintList(L3_2);
    // 第三组数据
    SqList L1_3, L2_3, L3_3;
    InitList(L1_3);
    InitList(L2_3);
    InitList(L3_3);
    int data2_3[] = { 1, 2, 3, 4, 5 , 6 ,7 ,8 ,9 ,10 };
    for (int i = 0; i < 10; i++) {
        ListInsert(L2_3, data2_3[i], L2_3.length + 1);
    }
    cout << "第三组数据：" << endl;
    cout << " 第一个顺序表: ";
    PrintList(L1_3);
    cout << "第二个顺序表: ";
    PrintList(L2_3);
    FindCommonElements(L1_3, L2_3, L3_3);
    cout << " 公共元素组成的顺序表: ";
    PrintList(L3_3);
}
//题目4
// 删除递增有序顺序表中的重复元素并统计移动元素次数
int DeleteDuplicates(SqList& L) {
    int n = L.length;
    if (n <= 1) return 0;
    int i = 0;
    int move_count = 0;
    for (int j = 1; j < n; ++j) {
        if (L.element[j] != L.element[i]) {
            i++;
            if (i != j) {
                L.element[i] = L.element[j];
                move_count++;
            }
        }
    }
    L.length = i + 1;
    return move_count;
}
void algorithm_4(){
    // 第一组数据
    SqList L1;
    InitList(L1);
    int data1[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
    for (int i = 0; i < 9; ++i) {
        ListInsert(L1, data1[i], L1.length + 1);
    }
    cout << "第一组数据：" << endl;
    cout << " 原顺序表: ";
    PrintList(L1);
    int moveCount1 = DeleteDuplicates(L1);
    cout << " 移动元素次数: " << moveCount1 << endl;
    cout << " 调整后顺序表: ";
    PrintList(L1);
    // 第二组数据
    SqList L2;
    InitList(L2);
    int data2[] = { 1, 1, 2, 2, 3, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8, 9 };
    for (int i = 0; i < 16; ++i) {
        ListInsert(L2, data2[i], L2.length + 1);
    }
    cout << "第二组数据：" << endl;
    cout << "原顺序表: ";
    PrintList(L2);
    int moveCount2 = DeleteDuplicates(L2);
    cout << " 移动元素次数: " << moveCount2 << endl;
    cout << "调整后顺序表: ";
    PrintList(L2);
    // 第三组数据
    SqList L3;
    InitList(L3);
    int data3[] = { 1, 2, 3, 4, 5, 5, 6, 7, 8, 8, 9, 9, 9, 9, 9 };
    for (int i = 0; i < 15; ++i) {
        ListInsert(L3, data3[i], L3.length + 1);
    }
    cout << "第三组数据：";
    cout << "原顺序表: ";
    PrintList(L3);
    int moveCount3 = DeleteDuplicates(L3);
    cout << " 移动元素次数: " << moveCount3 << endl;
    cout << "调整后顺序表: ";
    PrintList(L3);
}