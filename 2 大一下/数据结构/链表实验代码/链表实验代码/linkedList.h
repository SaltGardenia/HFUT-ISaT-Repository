#include <iostream>
using namespace std;
// 定义单链表节点结构 
struct ListNode {
    int data;
    ListNode* next;
    ListNode(int val) : data(val), next(nullptr) {}
};
// 定义单链表类 
class LinkedList {
public:
    ListNode* head;
    LinkedList() {
        head = new ListNode(0); // 头结点 
    }
    // 插入元素到链表尾部 
    void insert(int val) {
        ListNode* newNode = new ListNode(val);
        ListNode* cur = head;
        while (cur->next) {
            cur = cur->next;
        }
        cur->next = newNode;
    }
    // 打印链表 
    void print() {
        ListNode* cur = head->next;
        while (cur) {
            cout << cur->data << " ";
            cur = cur->next;
        }
        cout << endl;
    }
    // 1) 将单链表Ｌ中的奇数项和偶数项结点分解开 
    void splitOddEven(LinkedList& oddList, LinkedList& evenList) {
        ListNode* cur = head->next;
        while (cur) {
            if (cur->data % 2 == 1) {
                oddList.insert(cur->data);
            }
            else {
                evenList.insert(cur->data);
            }
            cur = cur->next;
        }
    }
    // 2) 求两个递增有序单链表L1和L2中的公共元素，放入新的单链表L3中 
    static void findCommonElements(LinkedList& L1, LinkedList& L2, LinkedList& L3) {
        ListNode* p1 = L1.head->next;
        ListNode* p2 = L2.head->next;
        while (p1 && p2) {
            if (p1->data < p2->data) {
                p1 = p1->next;
            }
            else if (p1->data > p2->data) {
                p2 = p2->next;
            }
            else {
                L3.insert(p1->data);
                p1 = p1->next;
                p2 = p2->next;
            }
        }
    }
    // 3) 删除递增有序单链表中的重复元素 
    void removeDuplicates() {
        ListNode* cur = head->next;
        while (cur && cur->next) {
            if (cur->data == cur->next->data) {
                ListNode* temp = cur->next;
                cur->next = cur->next->next;
                delete temp;
            }
            else {
                cur = cur->next;
            }
        }
    }
    // 4) 递增有序单链表L1、L2，不申请新结点，利用原表结点对两表进行合并 
    static void mergeLists(LinkedList& L1, LinkedList& L2) {
        ListNode* p1 = L1.head->next;
        ListNode* p2 = L2.head->next;
        ListNode* prev = L1.head;
        while (p1 && p2) {
            if (p1->data < p2->data) {
                prev = p1;
                p1 = p1->next;
            }
            else if (p1->data > p2->data) {
                ListNode* temp = p2;
                p2 = p2->next;
                prev->next = temp;
                temp->next = p1;
                prev = temp;
            }
            else {
                ListNode* temp = p2;
                p2 = p2->next;
                delete temp;
                prev = p1;
                p1 = p1->next;
            }
        }
        if (p2) {
            prev->next = p2;
        }
        delete L2.head;
    }
    // 5) 查找链表中倒数第k个位置上的结点 
    int findKthToLast(int k) {
        ListNode* fast = head->next;
        ListNode* slow = head->next;
        // 快指针先走k步 
        for (int i = 0; i < k; ++i) {
            if (!fast) {
                return 0;
            }
            fast = fast->next;
        }
        // 快慢指针同时走 
        while (fast) {
            fast = fast->next;
            slow = slow->next;
        }
        if (slow) {
            cout << "倒数第" << k << "个位置的结点值为: " << slow->data << endl;
            return 1;
        }
        return 0;
    }
};