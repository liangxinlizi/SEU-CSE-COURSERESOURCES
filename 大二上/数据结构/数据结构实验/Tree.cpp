#include<iostream>
#include<queue>
#include<fstream>
using namespace std;
//定义节点的结构体和初始化函数
struct btNode
{
	int key;
	btNode* right;
	btNode* left;
	btNode():left(NULL),right(NULL){}
	btNode(int x, btNode* l = NULL, btNode* r = NULL)
	{key = x;
	right = r;
	left = l;}
};
int con = -1;	
int pre[26];
class BSTree
{
public:
	int treenum = 0;
	//构造函数，传入文件，从中读取节点值来构造
	BSTree(fstream& file)
	{
		if (file.is_open())//读取文件
		{
			fstream ftmp("construct_tmp.txt", ios::out);//显示构造过程的输出文件
			file >> treenum;//先输入总数目的个数
			int key;
			for (int i = 0;i < treenum;i++)//循环输入每个key值
			{
				file >> key;
				Insert(key, root);//调用插入函数
				cout << "第" << i + 1 << "次构造：" << endl;
				PrintTree(root, 1, ftmp);
			}
			ftmp.close();
		}
		file.close();//关闭文件
	}
	//插入函数，传入节点值和根节点地址来插入
	void Insert(int k, btNode*& root)
	{
		if (root == NULL)
		{
			root = new btNode(k);
		}
		else if (k < root->key) {
			Insert(k, root->left);
		}
		else if (k > root->key) {
			Insert(k, root->right);
		}
		else
			cout << "invalid number!" << endl;
	}
	//输出函数，同时输出到屏幕和文件中
	void PrintTree(btNode* n, int level, fstream& file)
	{
		if (n == NULL) return;
		PrintTree(n->right, level + 1, file);
		for (int j = 0; j < level - 1; j++)
		{
			file << "    ";
			cout << "    ";
		}
		file << ".." << (char)n->key << endl;
		cout << ".." << (char)n->key << endl;
		PrintTree(n->left, level + 1, file);
	}
	//中序遍历
	void InOrder(btNode* root)
	{
		if (root->left != NULL)InOrder(root->left);//递归访问左子树
		cout << (char)root->key << ' ';
		if (root->right != NULL)InOrder(root->right);
	}	
	//先序遍历
	void PreOrder(btNode* root)
	{	
		cout << (char)root->key << ' ';
		pre[++con] = root->key;//遍历的同时构造先序序列数组，便于析构
		if (root->left != NULL)	PreOrder(root->left);
		if (root->right != NULL) PreOrder(root->right);
	}
	//层次遍历
	void LevelOrder(void(*visit)(btNode*p))
	{
		queue<btNode*>Q;
		btNode* p = root;
		Q.push(p);
		while (!Q.empty())//队列不为空
		{
			p = Q.front();
			Q.pop();
			cout << (char)p->key <<' ';
			if (p->left != NULL)Q.push(p->left);//左子女进队
			if (p->right != NULL)Q.push(p->right);
		}
	}
	//删除节点，传入节点值和根节点地址
	bool Remove(int k,btNode*&root)
	{
		if (root == NULL) return false; // 添加对根节点为空的判断
		btNode* current = root;//当前指针
		btNode* parent = NULL;//定义父亲指针
		bool isleft = true;
		while(current->key != k)
		{
			parent = current;
			if (k < current->key)
			{
				isleft = true;
				current = current->left;
			}
			else
			{
				isleft = false;
				current = current->right;
			}
			if (current == NULL)
				return false;
		}
		//没有子节点的情况
		if(current->right==NULL&&current->left==NULL)
		{ 
			//根节点
		if (current == root)
			root = NULL;
			//其他结点
		else
			if (isleft == true)parent->left = NULL;
			else parent->right = NULL;
		delete current;
		}
		//有一个子节点的情况
		else if (current->left == NULL || current->right == NULL)
		{
			//找到不为空的那个子树
			btNode* child = (current->left != NULL) ? current->left : current->right;
			if (current == root) {
				root = child;
			}//要删除的是根节点，直接让孩子节点等于根节点
			else if (isleft) {
				parent->left = child;
			}
			else {
				parent->right = child;
			}
			delete current;//删除这个节点
		}
		//有两个子节点的情况
		else
		{
			//先找到节点的后继，调用找后继节点的函数
			btNode* successor = GetSuccessor(current);
			if (current == root) {
				root = successor;
			}//根节点直接赋值后继节点
			else if (isleft) {
				parent->left = successor;
			}
			else {
				parent->right = successor;
			}
			successor->left = current->left;
			delete current;

		}
		return true;//删除成功
	}
	//获取给定结点的后继
	btNode* GetSuccessor(btNode* node) {
		if (node->right == NULL) {
			return node;//右子树为空：直接返回此节点
		}
		//右子树不为空
		btNode* parent = node;
		btNode* successor = node;
		btNode* current = node->right;//开始遍历右子树
		//找到右子树中最左边的结点
		while (current != NULL) {
			parent = successor;
			successor = current;
			current = current->left;
		}
		//如果后继节点不是原节点的右子节点，将后继节点的右子树连接到后继节点的父节点的左子树上
		if (successor != node->right) {
			parent->left = successor->right;
			//将后继节点的右子树设为原节点的右子树
			successor->right = node->right;
		}
		//原节点的左子树设为空，因为它已经成为后继节点的左子树
		successor->left = NULL;
		return successor;//返回找到的后继节点
	}
	//查找函数
	bool Search(int k, btNode* n)
	{
		while (n!=NULL)//树不为空
		{
			if (k == n->key)return true;//符合时搜索成功，返回正确
			else if (k < n->key)//小于时找左子树
			{
				n = n->left;
			}
			else//大于时找右子树
			{
				n = n->right;
			}		
		}return false;//搜索失败
	}
	//析构函数
	~BSTree()
	{
		makeEmpty();
	}
	btNode* root = NULL;//定义根节点
	//清空函数
	void makeEmpty()
	{
		fstream file("destruct_tmp.txt", ios::out);
		for (int i = 0;pre[i] >= 65 && pre[i] <= 90;i++)
		{
			cout << "第" << i + 1 << "次析构后：" << endl;
			Remove(pre[i], root);
			PrintTree(root, 1, file);
		}
		delete root;
		cout << "析构完成！" << endl;
		file.close();
	}
	
};

int main()
{
	fstream fileo("in.txt",ios::out); // 打开文件进行读取
	if (fileo.is_open())
	{
		int n = rand() % 16 + 11;
		fileo << n << ' ';
		for (int i = 0;i < n;i++)
		{
			fileo << rand() % 26 + 65 << ' ';
		}
		fileo.close();//保证文件关闭
	}
	fstream filei("in.txt", ios::in);
	BSTree bst(filei); // 创建二叉搜索树对象并从文件中读取数据

	// 测试插入元素
	bst.Insert(90, bst.root);


	// 测试搜索元素
	int key = 68;
	if (bst.Search(key, bst.root))
		cout << "Key " << (char)key << " found in the tree." << endl;
	else
		cout << "Key " << (char)key << " not found in the tree." << endl;


	// 测试中序遍历
	cout << "InOrder Traversal: ";
	bst.InOrder(bst.root);
	cout << endl;

	// 测试前序遍历
	cout << "PreOrder Traversal: ";
	bst.PreOrder(bst.root);
	cout << endl;

	// 测试层序遍历
	cout << "LevelOrder Traversal: ";
	bst.LevelOrder(NULL);
	cout << endl;

	//测试删除元素
	bst.Remove(68, bst.root);

	// 测试打印树的结构
	cout << "Print Tree:" << endl;
	fstream fileou("out.txt", ios::out);
	bst.PrintTree(bst.root, 1, fileou);
	fileou.close();

	//析构过程测试
	//bst.makeEmpty();
	return 0;
}
