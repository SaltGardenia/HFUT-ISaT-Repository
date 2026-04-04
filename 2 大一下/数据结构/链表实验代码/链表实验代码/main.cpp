#include <iostream>
#include "linkedList.h" 
using namespace std;

int main() {
    // 1) 将单链表Ｌ中的奇数项和偶数项结点分解开 
    cout << "任务1：分解奇数偶数项" << endl;
    cout << "第一组数据：" << endl;
    LinkedList L1; int data1[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60 };
    for (int val : data1) {
        L1.insert(val);
    }
    LinkedList oddList1, evenList1;
    L1.splitOddEven(oddList1, evenList1);
    cout << "原链表: ";
    L1.print();
    cout << "奇数链表: ";
    oddList1.print();
    cout << "偶数链表: ";
    evenList1.print();
    cout << endl;
    // 2) 求两个递增有序单链表L1和L2中的公共元素，放入新的单链表L3中 
    cout << "任务2：求公共元素" << endl;
    LinkedList L3, L4, L5;
    int data3[] = { 1, 3, 6, 10, 15, 16, 17, 18, 19, 20 };
    int data4[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 18, 20, 30 };
    for (int val : data3) {
        L3.insert(val);
    }
    for (int val : data4) {
        L4.insert(val);
    }
    LinkedList L6;
    LinkedList::findCommonElements(L3, L4, L6);
    cout << "第一个链表: ";
    L3.print();
    cout << "第二个链表: ";
    L4.print();
    cout << "公共元素链表: ";
    L6.print();
    // 3) 删除递增有序单链表中的重复元素 
    cout << "\n任务3：删除重复元素" << std::endl;
    LinkedList L7;
    int data5[] = { 1, 1, 2, 2, 2, 3, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8, 9 };
    for (int val : data5) {
        L7.insert(val);
    }
    cout << "原链表: ";
    L7.print();
    L7.removeDuplicates();
    cout << "删除重复元素后的链表: ";
    L7.print();
    // 4) 递增有序单链表L1、L2，不申请新结点，利用原表结点对两表进行合并 
    cout << "\n任务4：合并链表" << endl;
    LinkedList L8, L9;
    int data6[] = { 1, 3, 6, 10, 15, 16, 17, 18, 19, 20 };
    int data7[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 18, 20, 30 };
    for (int val : data6) {
        L8.insert(val);
    }
    for (int val : data7) {
        L9.insert(val);
    }
    LinkedList::mergeLists(L8, L9);
    cout << "合并后的链表: ";
    L8.print();
    // 5) 查找链表中倒数第k个位置上的结点 
    cout << "\n任务5：查找倒数第k个结点" << endl;
    LinkedList L10;
    int data8[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
    for (int val : data8) {
        L10.insert(val);
    }
    int k = 3;
    int result = L10.findKthToLast(k);
    if (result == 0) {
        cout << "未找到倒数第" << k << "个结点" << endl;
    }
    return 0;
}