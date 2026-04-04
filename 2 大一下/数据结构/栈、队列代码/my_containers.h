#ifndef MY_CONTAINERS_H
#define MY_CONTAINERS_H

template <typename T>
class Stack {
private:
    struct Node {
        T data;
        Node* next;
        Node(T val) : data(val), next(nullptr) {}
    };
    Node* topNode;
    int count;  // 添加计数器成员
    
public:
    Stack() : topNode(nullptr), count(0) {}  // 初始化计数器
    
    ~Stack() {
        while (!empty()) {
            pop();
        }
    }
    
    void push(T val) {
        Node* newNode = new Node(val);
        newNode->next = topNode;
        topNode = newNode;
        count++;  // 增加计数
    }
    
    void pop() {
        if (empty()) return;
        Node* temp = topNode;
        topNode = topNode->next;
        delete temp;
        count--;  // 减少计数
    }
    
    int size() const {
        return count;
    }
    
    T top() const {
        if (empty()) throw "Stack is empty";
        return topNode->data;
    }
    
    bool empty() const {
        return topNode == nullptr;
    }
};

template <typename T>
class Queue {
private:
    struct Node {
        T data;
        Node* next;
        Node(T val) : data(val), next(nullptr) {}
    };
    Node* frontNode;
    Node* rearNode;
    int count;  // 添加计数器成员
    
public:
    Queue() : frontNode(nullptr), rearNode(nullptr), count(0) {}  // 初始化计数器
    
    ~Queue() {
        while (!empty()) {
            dequeue();
        }
    }
    
    void enqueue(T val) {
        Node* newNode = new Node(val);
        if (empty()) {
            frontNode = rearNode = newNode;
        } else {
            rearNode->next = newNode;
            rearNode = newNode;
        }
        count++;  // 增加计数
    }
    
    void dequeue() {
        if (empty()) return;
        Node* temp = frontNode;
        frontNode = frontNode->next;
        if (frontNode == nullptr) {
            rearNode = nullptr;
        }
        delete temp;
        count--;  // 减少计数
    }
    
    int size() const {
        return count;
    }
    
    T front() const {
        if (empty()) throw "Queue is empty";
        return frontNode->data;
    }
    
    bool empty() const {
        return frontNode == nullptr;
    }
};

#endif // MY_CONTAINERS_H