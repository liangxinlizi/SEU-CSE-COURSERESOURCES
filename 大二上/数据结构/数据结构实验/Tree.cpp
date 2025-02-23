#include<iostream>
#include<queue>
#include<fstream>
using namespace std;
//����ڵ�Ľṹ��ͳ�ʼ������
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
	//���캯���������ļ������ж�ȡ�ڵ�ֵ������
	BSTree(fstream& file)
	{
		if (file.is_open())//��ȡ�ļ�
		{
			fstream ftmp("construct_tmp.txt", ios::out);//��ʾ������̵�����ļ�
			file >> treenum;//����������Ŀ�ĸ���
			int key;
			for (int i = 0;i < treenum;i++)//ѭ������ÿ��keyֵ
			{
				file >> key;
				Insert(key, root);//���ò��뺯��
				cout << "��" << i + 1 << "�ι��죺" << endl;
				PrintTree(root, 1, ftmp);
			}
			ftmp.close();
		}
		file.close();//�ر��ļ�
	}
	//���뺯��������ڵ�ֵ�͸��ڵ��ַ������
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
	//���������ͬʱ�������Ļ���ļ���
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
	//�������
	void InOrder(btNode* root)
	{
		if (root->left != NULL)InOrder(root->left);//�ݹ����������
		cout << (char)root->key << ' ';
		if (root->right != NULL)InOrder(root->right);
	}	
	//�������
	void PreOrder(btNode* root)
	{	
		cout << (char)root->key << ' ';
		pre[++con] = root->key;//������ͬʱ���������������飬��������
		if (root->left != NULL)	PreOrder(root->left);
		if (root->right != NULL) PreOrder(root->right);
	}
	//��α���
	void LevelOrder(void(*visit)(btNode*p))
	{
		queue<btNode*>Q;
		btNode* p = root;
		Q.push(p);
		while (!Q.empty())//���в�Ϊ��
		{
			p = Q.front();
			Q.pop();
			cout << (char)p->key <<' ';
			if (p->left != NULL)Q.push(p->left);//����Ů����
			if (p->right != NULL)Q.push(p->right);
		}
	}
	//ɾ���ڵ㣬����ڵ�ֵ�͸��ڵ��ַ
	bool Remove(int k,btNode*&root)
	{
		if (root == NULL) return false; // ��ӶԸ��ڵ�Ϊ�յ��ж�
		btNode* current = root;//��ǰָ��
		btNode* parent = NULL;//���常��ָ��
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
		//û���ӽڵ�����
		if(current->right==NULL&&current->left==NULL)
		{ 
			//���ڵ�
		if (current == root)
			root = NULL;
			//�������
		else
			if (isleft == true)parent->left = NULL;
			else parent->right = NULL;
		delete current;
		}
		//��һ���ӽڵ�����
		else if (current->left == NULL || current->right == NULL)
		{
			//�ҵ���Ϊ�յ��Ǹ�����
			btNode* child = (current->left != NULL) ? current->left : current->right;
			if (current == root) {
				root = child;
			}//Ҫɾ�����Ǹ��ڵ㣬ֱ���ú��ӽڵ���ڸ��ڵ�
			else if (isleft) {
				parent->left = child;
			}
			else {
				parent->right = child;
			}
			delete current;//ɾ������ڵ�
		}
		//�������ӽڵ�����
		else
		{
			//���ҵ��ڵ�ĺ�̣������Һ�̽ڵ�ĺ���
			btNode* successor = GetSuccessor(current);
			if (current == root) {
				root = successor;
			}//���ڵ�ֱ�Ӹ�ֵ��̽ڵ�
			else if (isleft) {
				parent->left = successor;
			}
			else {
				parent->right = successor;
			}
			successor->left = current->left;
			delete current;

		}
		return true;//ɾ���ɹ�
	}
	//��ȡ�������ĺ��
	btNode* GetSuccessor(btNode* node) {
		if (node->right == NULL) {
			return node;//������Ϊ�գ�ֱ�ӷ��ش˽ڵ�
		}
		//��������Ϊ��
		btNode* parent = node;
		btNode* successor = node;
		btNode* current = node->right;//��ʼ����������
		//�ҵ�������������ߵĽ��
		while (current != NULL) {
			parent = successor;
			successor = current;
			current = current->left;
		}
		//�����̽ڵ㲻��ԭ�ڵ�����ӽڵ㣬����̽ڵ�����������ӵ���̽ڵ�ĸ��ڵ����������
		if (successor != node->right) {
			parent->left = successor->right;
			//����̽ڵ����������Ϊԭ�ڵ��������
			successor->right = node->right;
		}
		//ԭ�ڵ����������Ϊ�գ���Ϊ���Ѿ���Ϊ��̽ڵ��������
		successor->left = NULL;
		return successor;//�����ҵ��ĺ�̽ڵ�
	}
	//���Һ���
	bool Search(int k, btNode* n)
	{
		while (n!=NULL)//����Ϊ��
		{
			if (k == n->key)return true;//����ʱ�����ɹ���������ȷ
			else if (k < n->key)//С��ʱ��������
			{
				n = n->left;
			}
			else//����ʱ��������
			{
				n = n->right;
			}		
		}return false;//����ʧ��
	}
	//��������
	~BSTree()
	{
		makeEmpty();
	}
	btNode* root = NULL;//������ڵ�
	//��պ���
	void makeEmpty()
	{
		fstream file("destruct_tmp.txt", ios::out);
		for (int i = 0;pre[i] >= 65 && pre[i] <= 90;i++)
		{
			cout << "��" << i + 1 << "��������" << endl;
			Remove(pre[i], root);
			PrintTree(root, 1, file);
		}
		delete root;
		cout << "������ɣ�" << endl;
		file.close();
	}
	
};

int main()
{
	fstream fileo("in.txt",ios::out); // ���ļ����ж�ȡ
	if (fileo.is_open())
	{
		int n = rand() % 16 + 11;
		fileo << n << ' ';
		for (int i = 0;i < n;i++)
		{
			fileo << rand() % 26 + 65 << ' ';
		}
		fileo.close();//��֤�ļ��ر�
	}
	fstream filei("in.txt", ios::in);
	BSTree bst(filei); // �����������������󲢴��ļ��ж�ȡ����

	// ���Բ���Ԫ��
	bst.Insert(90, bst.root);


	// ��������Ԫ��
	int key = 68;
	if (bst.Search(key, bst.root))
		cout << "Key " << (char)key << " found in the tree." << endl;
	else
		cout << "Key " << (char)key << " not found in the tree." << endl;


	// �����������
	cout << "InOrder Traversal: ";
	bst.InOrder(bst.root);
	cout << endl;

	// ����ǰ�����
	cout << "PreOrder Traversal: ";
	bst.PreOrder(bst.root);
	cout << endl;

	// ���Բ������
	cout << "LevelOrder Traversal: ";
	bst.LevelOrder(NULL);
	cout << endl;

	//����ɾ��Ԫ��
	bst.Remove(68, bst.root);

	// ���Դ�ӡ���Ľṹ
	cout << "Print Tree:" << endl;
	fstream fileou("out.txt", ios::out);
	bst.PrintTree(bst.root, 1, fileou);
	fileou.close();

	//�������̲���
	//bst.makeEmpty();
	return 0;
}
