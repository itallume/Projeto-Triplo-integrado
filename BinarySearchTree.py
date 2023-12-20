class Node:
    def __init__(self,data:any):
        self.__data = data
        self.__leftChild = None
        self.__rightChild = None

    def addLeft(self, data:any):
        if self.__leftChild == None:
            self.__leftChild = Node(data)	

    def addRight(self,data:any):
        if self.__rightChild == None:
            self.__rightChild = Node(data)

    @property
    def leftChild(self)->'Node':
        return self.__leftChild

    @leftChild.setter
    def leftChild(self, newLeftChild:'Node'):
        self.__leftChild = newLeftChild

    @property
    def rightChild(self)->'Node':
        return self.__rightChild

    @rightChild.setter
    def rightChild(self, newRightChild:'Node'):
        self.__rightChild = newRightChild
    
    @property
    def data(self)->any:
        return self.__data
    
    @data.setter
    def data(self,newData:any):
        self.__data = newData
    
    def hasLeftChild(self)->bool:
        return self.__leftChild != None

    def hasRightChild(self)->bool:
        return self.__rightChild != None
    
    def __str__(self):
        return str(self.__data)


        
class BinarySearchTree:
    # Constructor that initializes the BST with no root node
    def __init__(self):
        self.__root = None

    def getRoot(self)->any:
        return self.__root.data if self.__root is not None else None

    def isEmpty(self)->bool:
        return self.__root == None

    # Insert a new node in the right place according to BST properties
    # The left subtree of a node contains only nodes with keys lesser than the node’s key.
    # The right subtree of a node contains only nodes with keys greater than the node’s key.
    def add(self, data:any):
        if(self.__root == None):
            self.__root = Node(data)
        else:
            self.__add(data,self.__root)

    def __add(self, data:any, node:'Node'):
        if ( data < node.data):
            if( node.leftChild != None):
                self.__add(data, node.leftChild)
            else:
                node.addLeft(data)
        else:
            if( node.rightChild != None):
                self.__add(data, node.rightChild)
            else:
                node.addRight(data)
    
    # Search for a node with the given key
    def search(self, key:any ):
        if( self.__root != None ):
            node = self.__searchData(key, self.__root)
            return node.data if node is not None else None
        else:
            return None
        
    def __searchData(self, key:any, node:'Node'):
        if ( key == node.data):
            return node
        elif ( key < node.data and node.leftChild != None):
            return self.__searchData( key, node.leftChild)
        elif ( key > node.data and node.rightChild != None):
            return self.__searchData( key, node.rightChild)
        else:
            return None
        
    def GetAndMajorOccurrences(self, key: any):  #retorna todos o valor inserido e todos os outros acima dele
        MajorOccurrences = []

        if self.__root is not None:
            self.__MajorOccurrences(key, self.__root, MajorOccurrences)

        return MajorOccurrences if MajorOccurrences else None        
    
    def __MajorOccurrences(self, key: any, node: 'Node', MajorOccurrences: list): # recursão do getAndMajorOccurrences, 
                                                                                  #coleta os valores maiores condição de parada = não ter mais nenhum maior

        if( node != None):
            self.__MajorOccurrences(key, node.leftChild, MajorOccurrences)
            if node.data >= key :
                MajorOccurrences.append(node.data)
            self.__MajorOccurrences(key, node.rightChild, MajorOccurrences)

    def GetEqualOrMajor(self, key: any):#retorna key ou o maior, o primeiro valor que encontrar

        if( self.__root != None ):
            node = self.__EqualOrMajor(key, self.__root)
            return node.data if node is not None else None
        else:
            return None
    
    def __EqualOrMajor(self, key, node): #recursão do getEqualOrMajor, condição de parada = encontrar key or >
        if ( node.data >= key):
            return node
        elif ( key < node.data and node.leftChild != None):
            return self.__EqualOrMajor( key, node.leftChild)
        elif ( key > node.data and node.rightChild != None):
            return self.__EqualOrMajor( key, node.rightChild)
        else:
            return None   
                 


        
    # Returns the number of nodes of the tree
    def count(self)->int:
        return self.__count(self.__root)

    def __count(self, node:'Node'):
        if ( node == None):
            return 0
        else:
            return 1 + self.__count(node.leftChild) + self.__count(node.rightChild)

    def __len__(self)->int:
        return self.count()

    # Traverse the tree in pre-order
    def preorder(self):
        self.__preorder(self.__root)
        print()

    # Traverse the tree in in-order
    def inorder(self):
        self.__inorder(self.__root)
        print()

    # # Traverse the tree in post-order
    def postorder(self):
        self.__postorder(self.__root)
        print()
        
    def __preorder(self, node:'Node'):
        if( node != None):
            print(f'{node.data} ',end='')
            self.__preorder(node.leftChild)
            self.__preorder(node.rightChild)

    def __inorder(self, node):
        if( node != None):
            self.__inorder(node.leftChild)
            print(f'{node.data} ',end='')
            self.__inorder(node.rightChild)

    def __postorder(self, node):
        if( node != None):
            self.__postorder(node.leftChild)
            self.__postorder(node.rightChild)
            print(f'{node.data} ',end='')

    # delete all nodes of the tree
    def deleteTree(self):
        # garbage collector fará o trabalho de remoção dos nós automaticamente. 
        self.__root = None

    # delete a node with the given key and return its data
    def deleteNode(self, key:any)->'Node':
        node = self.__searchData(key,self.__root)
        if node is not None:
            self.__root = self.__deleteNode(self.__root, key)
            return node.data
        else:
            return None
        
    
    # Dado um nó de uma BST e uma chave busca, este método
    # deleta o nó que contém a chave e devolve o novo nó raiz
    def __deleteNode(self,root:'Node', key:any):
        # Caso primário: não há raiz
        if root is None: 
            return root
  
        # Se a chave a ser deletada é menor do que a chave do nó raiz 
        # (da vez), então a chave se encontra na subárvore esquerda
        if key < root.data:
            root.leftChild = self.__deleteNode(root.leftChild, key) 
        # Se a chave a ser deletada é maior do que a chave do nó raiz (da vez),
        # então a chave se encontra na subárvore esquerda
        elif(key > root.data):
            root.rightChild = self.__deleteNode(root.rightChild, key) 
  
        # Se a chave é igual à chave do nó raiz, então estamos no nó 
        # a ser removido
        else:
            # (1) Nó com apenas 1 filho ou nenhum filho
            if root.leftChild is None : 
                temp = root.rightChild  
                root = None 
                return temp

            elif root.rightChild is None :
                temp = root.leftChild  
                root = None
                return temp 
  
            # (2) Nó com dois filhos: obtem o sucessor inorder
            # (o menor nó da subárvore direita) 
            temp = self.__minValueNode(root.rightChild) 
  
            # copia o conteúdo do sucessor inorder para este nós
            root.data = temp.data 
  
            # Deletao sucessor inorder
            root.rightChild = self.__deleteNode(root.rightChild , temp.data)

        return root

    # Dada uma BST não vazia, retorna o nó
    # com a menor chave encontrada na árvore. Note que a árvore
    # inteira não precisa ser percorrida
    def __minValueNode(self, node:'Node')->'Node':
        current = node 
  
        # loop para baixo a fim de encontrar a folha mais a esquerda
        while(current.leftChild is not None): 
            current = current.leftChild  
  
        return current

    # Dada uma BST não vazia, retorna o nó
    # com o maior valor de chave encontrada na árvore. Note que a árvore
    # inteira não precisa ser percorrida 
    def __maxValueNode(self, node:'Node')->'Node':
        current = node 
  
         # loop para baixo a fim de encontrar a folha mais a direita
        while(current.rightChild is not None): 
            current = current.rightChild
  
        return current
    

if __name__ == '__main__':
    bst = BinarySearchTree()

    print('Adicionando os nós 17, 17, 76, 9, 14, 12, 54, 72 e 67 à arvore...')

    bst.add(2)
    bst.add(3)
    bst.add(9)
    bst.add(4)
    bst.add(12)
    bst.add(12)
    bst.add(16)
    bst.add(15)
    bst.add(18)
    bst.add(80)
    bst.add(17)


    print("todas ocorrencias:", bst.GetEqualOrMajor(17) )
    print("teste")
    # print('Consultando o nó raiz:')
    # print('Root:',bst.getRoot())

    # print('Travessia em preordem:')
    # bst.preorder()
    # print('Travessia em inordem:')
    # bst.inorder()
    # print('Travessia em posordem:')
    # bst.postorder()
    

    # chave = 72
    # print('Pesquisando a chave',chave,' na árvore:')
    # if( bst.search( chave )):
    #     print('\nChave',chave,'está na árvore')
    # else:
    #     print('\nChave',chave,'NÃO está na árvore')
        
    # print('\nTentando apagar o nó de chave',chave)
    # print('No removido:',bst.deleteNode(chave))


    # print('Contagem de nós: ', bst.count())
            
    # bst.preorder()
    bst.inorder()
    # bst.postorder()
