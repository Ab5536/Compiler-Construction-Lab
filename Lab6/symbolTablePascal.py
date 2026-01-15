
class SymbolNode:
    """Node structure for AVL tree containing symbol information"""
    
    def __init__(self, identifier, data_type, scope, line_no):
        # Symbol information
        self.identifier = identifier      # Variable/function name
        self.data_type = data_type       # int, real, boolean, etc.
        self.scope = scope               # global, local, etc.
        self.line_no = line_no           # Line number where declared
        
        # AVL tree structure
        self.left = None
        self.right = None
        self.height = 1
    
    def display(self):
        """Display symbol information"""
        print(f"\n{'='*50}")
        print(f"Identifier Name: {self.identifier}")
        print(f"Data Type: {self.data_type}")
        print(f"Scope: {self.scope}")
        print(f"Line Number: {self.line_no}")
        print(f"{'='*50}")


class SymbolTable:
    """AVL Tree based Symbol Table"""
    
    def __init__(self):
        self.root = None
    
    def get_height(self, node):
        """Get height of node"""
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node):
        """Get balance factor of node"""
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def right_rotate(self, y):
        """Right rotation for AVL balancing"""
        x = y.left
        T2 = x.right
        
        # Perform rotation
        x.right = y
        y.left = T2
        
        # Update heights
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        
        return x
    
    def left_rotate(self, x):
        """Left rotation for AVL balancing"""
        y = x.right
        T2 = y.left
        
        # Perform rotation
        y.left = x
        x.right = T2
        
        # Update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        
        return y
    
    def insert(self, identifier, data_type, scope, line_no):
        """Insert a symbol into the table"""
        self.root = self._insert_helper(self.root, identifier, data_type, scope, line_no)
        return True
    
    def _insert_helper(self, node, identifier, data_type, scope, line_no):
        """Helper function for insertion with AVL balancing"""
        
        # Standard BST insertion
        if not node:
            print(f"✓ '{identifier}' inserted successfully")
            return SymbolNode(identifier, data_type, scope, line_no)
        
        if identifier < node.identifier:
            node.left = self._insert_helper(node.left, identifier, data_type, scope, line_no)
        elif identifier > node.identifier:
            node.right = self._insert_helper(node.right, identifier, data_type, scope, line_no)
        else:
            # Duplicate identifier - update information
            print(f"⚠ '{identifier}' already exists. Updating information...")
            node.data_type = data_type
            node.scope = scope
            node.line_no = line_no
            return node
        
        # Update height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        
        # Get balance factor
        balance = self.get_balance(node)
        
        # Left Left Case
        if balance > 1 and identifier < node.left.identifier:
            return self.right_rotate(node)
        
        # Right Right Case
        if balance < -1 and identifier > node.right.identifier:
            return self.left_rotate(node)
        
        # Left Right Case
        if balance > 1 and identifier > node.left.identifier:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        
        # Right Left Case
        if balance < -1 and identifier < node.right.identifier:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        
        return node
    
    def search(self, identifier):
        """Search for an identifier in the symbol table"""
        return self._search_helper(self.root, identifier)
    
    def _search_helper(self, node, identifier):
        """Helper function for searching"""
        if not node:
            return None
        
        if identifier == node.identifier:
            return node
        elif identifier < node.identifier:
            return self._search_helper(node.left, identifier)
        else:
            return self._search_helper(node.right, identifier)
    
    def delete(self, identifier):
        """Delete an identifier from the symbol table"""
        self.root = self._delete_helper(self.root, identifier)
    
    def _delete_helper(self, node, identifier):
        """Helper function for deletion with AVL balancing"""
        
        if not node:
            print(f"✗ '{identifier}' not found")
            return node
        
        # Standard BST deletion
        if identifier < node.identifier:
            node.left = self._delete_helper(node.left, identifier)
        elif identifier > node.identifier:
            node.right = self._delete_helper(node.right, identifier)
        else:
            # Node found - delete it
            print(f"✓ '{identifier}' deleted successfully")
            
            # Node with one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            # Node with two children
            # Get the inorder successor (smallest in right subtree)
            temp = self._get_min_value_node(node.right)
            node.identifier = temp.identifier
            node.data_type = temp.data_type
            node.scope = temp.scope
            node.line_no = temp.line_no
            node.right = self._delete_helper(node.right, temp.identifier)
        
        if not node:
            return node
        
        # Update height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        
        # Get balance factor
        balance = self.get_balance(node)
        
        # Balance the tree
        # Left Left Case
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        
        # Left Right Case
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        
        # Right Right Case
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        
        # Right Left Case
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        
        return node
    
    def _get_min_value_node(self, node):
        """Get node with minimum value"""
        current = node
        while current.left:
            current = current.left
        return current
    
    def modify(self, identifier, data_type, scope, line_no):
        """Modify an existing symbol's information"""
        node = self.search(identifier)
        if node:
            node.data_type = data_type
            node.scope = scope
            node.line_no = line_no
            print(f"✓ '{identifier}' modified successfully")
            return True
        else:
            print(f"✗ '{identifier}' not found")
            return False
    
    def display_all(self):
        """Display all symbols in sorted order (inorder traversal)"""
        print(f"\n{'='*50}")
        print("SYMBOL TABLE CONTENTS (Sorted by Identifier)")
        print(f"{'='*50}")
        if not self.root:
            print("Symbol table is empty")
        else:
            self._inorder_display(self.root)
        print(f"{'='*50}\n")
    
    def _inorder_display(self, node):
        """Inorder traversal to display symbols"""
        if node:
            self._inorder_display(node.left)
            print(f"{node.identifier:15} | {node.data_type:10} | {node.scope:10} | Line: {node.line_no}")
            self._inorder_display(node.right)


# ============= DEMONSTRATION =============

def main():
    """Demonstrate symbol table operations"""
    
    print("\n" + "="*60)
    print("     SYMBOL TABLE - AVL TREE IMPLEMENTATION")
    print("     Pascal Subset Lexical Analyzer")
    print("="*60)
    
    st = SymbolTable()
    
    # Insert some Pascal identifiers
    print("\n--- INSERTION OPERATIONS ---")
    st.insert("program", "keyword", "global", 1)
    st.insert("begin", "keyword", "global", 2)
    st.insert("end", "keyword", "global", 3)
    st.insert("counter", "integer", "local", 5)
    st.insert("sum", "integer", "local", 6)
    st.insert("average", "real", "local", 7)
    st.insert("flag", "boolean", "local", 8)
    
    # Display all symbols
    st.display_all()
    
    # Search operations
    print("\n--- SEARCH OPERATIONS ---")
    result = st.search("counter")
    if result:
        print(f"✓ Found 'counter':")
        result.display()
    else:
        print("✗ 'counter' not found")
    
    result = st.search("xyz")
    if result:
        print(f"✓ Found 'xyz':")
        result.display()
    else:
        print("✗ 'xyz' not found in symbol table")
    
    # Modify operation
    print("\n--- MODIFY OPERATION ---")
    st.modify("counter", "real", "global", 10)
    
    result = st.search("counter")
    if result:
        print(f"✓ Updated 'counter':")
        result.display()
    
    # Delete operation
    print("\n--- DELETE OPERATION ---")
    st.delete("flag")
    st.delete("notexist")
    
    # Display final table
    st.display_all()
    
    print("\n--- ADDITIONAL PASCAL TOKENS ---")
    st.insert("if", "keyword", "global", 12)
    st.insert("then", "keyword", "global", 12)
    st.insert("else", "keyword", "global", 13)
    st.insert("while", "keyword", "global", 15)
    st.insert("do", "keyword", "global", 15)
    
    st.display_all()


if __name__ == "__main__":
    main()