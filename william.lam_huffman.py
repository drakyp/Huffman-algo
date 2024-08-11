__license__ = 'Junior (c) EPITA'
__docformat__ = 'reStructuredText'
__revision__ = '$Id: huffman.py 2023-03-24'

"""
Huffman homework
2023-03
@author: william.lam
"""

from algo_py import bintree
from algo_py import heap


###############################################################################
# Do not change anything above this line, except your login!
# Do not add any import

###############################################################################
## COMPRESSION


def __height(ref):
    """Compute height of Tree.

    Args:
        ref (BinTree).

    Returns:
        int: The maximum depth of any leaf.

    """

    if ref == None:
        return -1
    else:
        return 1 + max(__height(ref.left), __height(ref.right))






def build_frequency_list(dataIN):
    """
    Builds a tuple list of the character frequencies in the input.
    """
    L=[]
    hist=[]
    for i in range (256):
        hist.append(0)
    for c in dataIN:
        hist[ord(c)]+=1
    for i in range (256):
        if hist[i]!=0:
            L.append((hist[i],chr(i)))
    return L


def build_Huffman_tree(inputList):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """
    Sort=[]
    for i in range (len(inputList)):
        Sort.append((inputList[i][0], bintree.BinTree(inputList[i][1],None,None)))
    H=heap.Heap()
    for i in range (len(Sort)):
        H.push(Sort[i])
    while len(H.elts)>2 :
        x=H.pop()
        y=H.pop()
        H.push((x[0]+y[0],bintree.BinTree(None,x[1],y[1])))

    return H.pop()[1]

def __where(huffmanTree, key):
            """
            gives the path of a key in a tree using '1' or '0' to go left or right
            """
            if huffmanTree.key == key:
                return ''
            else:
                if huffmanTree.left != None:
                    res = __where(huffmanTree.left, key)
                    if res != None:
                        return '0' + res
                if huffmanTree.right != None:
                    res = __where(huffmanTree.right, key)
                    if res != None:
                        return '1' + res
                return None




def encode_data(huffmanTree, dataIN):
    """
    Encodes the input string to its binary string representation.
    """
    res=""
    for c in dataIN:
        res+=__where(huffmanTree,c)
    return res


def __int_to_bin(n):
    """
    Converts an integer into its binary representation.
    """
    res=""
    while n>0:
        res=str(n%2)+res
        n=n//2
    while len(res)<8:
        res="0"+res
    return res

def encode_tree(huffmanTree):
    """
    Encodes a huffman tree to its binary representation using a preOrder traversal:
        * each leaf key is encoded into its binary representation on 8 bits preceded by '1'
        * each time we go left we add a '0' to the result
    """
    res=""
    if huffmanTree.left==None and huffmanTree.right==None:
        res+="1"+__int_to_bin(ord(huffmanTree.key))
    else:
        res+="0"
        res+=encode_tree(huffmanTree.left)
        res+=encode_tree(huffmanTree.right)
    return res

def to_binary(dataIN):
    """
    Compresses a string containing binary code to its real binary value.
    """

    res=""
    temp=""
    start= len(dataIN)//8
    left=(8-len(dataIN)%8)%8
    for i in range (start):
         res+=chr(__bin_to_int(str(dataIN[8*i])+str(dataIN [8*i+1])+str(dataIN [8*i+2])+str(dataIN [8*i+3])+str(dataIN [8*i+4])+str(dataIN [8*i+5])+str(dataIN [8*i+6])+str(dataIN [8*i+7])))
    if left!=0:
        while left>0 and len(temp)<8:
            temp+="0"
            left-=1
        for i in range (len(dataIN)-len(dataIN)%8, len(dataIN)):
            temp+= dataIN[i]
        res+=chr(__bin_to_int(temp))
    return (res, (8-len(dataIN)%8)%8)






def compress(dataIn):
    """
    The main function that makes the whole compression process.
    """

    return (to_binary(encode_data(build_Huffman_tree(build_frequency_list(dataIn)),dataIn)),to_binary( encode_tree(build_Huffman_tree(build_frequency_list(dataIn)))))

    
################################################################################
## DECOMPRESSION

def decode_data(huffmanTree, dataIN):
    """
    Decode a string using the corresponding huffman tree into something more readable.
    """
    res=""
    cur=huffmanTree
    n=len(dataIN)
    for i in range (n):
        if dataIN[i]=='0':
            cur=cur.left
        else:
            cur=cur.right
        if cur.left==None and cur.right==None:
            res+=cur.key
            cur=huffmanTree
    return res



    
def decode_tree(dataIN):
    """
    Decodes a huffman tree from its binary representation:
        * a '0' means we add a new internal node and go to its left node
        * a '1' means the next 8 values are the encoded character of the current leaf         
    """
    root= bintree.BinTree(None,None,None)
    cur=root
    i=0
    stack=[]
    while i<len(dataIN):
        if dataIN[i]=='0':
            stack.append(cur)
            cur.left=bintree.BinTree(None,None,None)
            cur=cur.left
            i+=1
        else:
                cur.key=chr(__bin_to_int( str(dataIN[i+1])+ str(dataIN[i+2])+ str(dataIN[i+3])+ str (dataIN[i+4])+ str (dataIN[i+5])+ str (dataIN[i+6])+ str (dataIN[i+7])+ str(dataIN[i+8])))
                i+=9
                if len(stack)>0:
                    cur=stack.pop()
                    cur.right=bintree.BinTree(None,None,None)
                    cur=cur.right
    return root

def __bin_to_int(s):
    """
    Converts a binary string into its integer representation.
    """
    res=0
    for i in range (len(s)):
       res+=int(s[i])*2**(len(s)-i-1)
    return res






def from_binary(dataIN, align):
    """
    Retrieve a string containing binary code from its real binary value (inverse of :func:`toBinary`).
    """

    aux = ""
    final = ""
    temp = align
    i = 0
    while i < len(dataIN):
        value = ord(dataIN[i])
        aux += __int_to_bin(value)
        i += 1
    j = 0
    while j < len(aux):
        if j < len(aux) - 8:
            final += aux[j]
        else:
            if temp <= 0:
                final += aux[j]
            temp -= 1
        j += 1

    return final

def decompress(data, dataAlign, tree, treeAlign):
    """
    The whole decompression process.
    """
    auxd = from_binary(data, dataAlign)
    auxt = from_binary(tree, treeAlign)

    newT = decode_tree(auxt)
    res = decode_data(newT, auxd)
    return res










