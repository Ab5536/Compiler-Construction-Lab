import re

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
            return SymbolNode(identifier, data_type, scope, line_no)
        
        if identifier < node.identifier:
            node.left = self._insert_helper(node.left, identifier, data_type, scope, line_no)
        elif identifier > node.identifier:
            node.right = self._insert_helper(node.right, identifier, data_type, scope, line_no)
        else:
            # Duplicate identifier - keep first declaration
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
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        
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
    
    def display_all(self):
        """Display all symbols in sorted order (inorder traversal)"""
        print(f"\n{'='*50}")
        print("SYMBOL TABLE CONTENTS (Sorted by Identifier)")
        print(f"{'='*50}")
        if not self.root:
            print("Symbol table is empty")
        else:
            print(f"{'Identifier':<15} | {'Type':<12} | {'Scope':<10} | Line")
            print("-" * 50)
            self._inorder_display(self.root)
        print(f"{'='*50}\n")
    
    def _inorder_display(self, node):
        """Inorder traversal to display symbols"""
        if node:
            self._inorder_display(node.left)
            print(f"{node.identifier:<15} | {node.data_type:<12} | {node.scope:<10} | {node.line_no}")
            self._inorder_display(node.right)


# ============= LEXICAL ANALYZER =============

class LexicalAnalyzer:
    """Lexical Analyzer for Pascal subset"""
    
    # Pascal keywords
    KEYWORDS = {
        'program', 'var', 'begin', 'end', 'if', 'then', 'else', 'while', 
        'do', 'for', 'to', 'downto', 'repeat', 'until', 'procedure', 
        'function', 'integer', 'real', 'boolean', 'char', 'string',
        'true', 'false', 'not', 'and', 'or', 'div', 'mod', 'read', 
        'write', 'readln', 'writeln', 'const', 'type', 'array', 'of'
    }
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_scope = "global"
    
    def analyze(self, code):
        """Analyze Pascal code and populate symbol table"""
        print("\n" + "="*60)
        print("     LEXICAL ANALYSIS IN PROGRESS")
        print("="*60)
        
        lines = code.strip().split('\n')
        in_var_section = False
        program_name = None
        
        for line_no, line in enumerate(lines, 1):
            # Remove comments
            line = re.sub(r'\{.*?\}', '', line)
            line = re.sub(r'\(\*.*?\*\)', '', line)
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            line_lower = line.lower()
            
            # Handle PROGRAM declaration
            if line_lower.startswith('program'):
                match = re.search(r'program\s+(\w+)', line, re.IGNORECASE)
                if match:
                    program_name = match.group(1)
                    self.symbol_table.insert('program', 'keyword', 'global', line_no)
                    self.symbol_table.insert(program_name, 'program_name', 'global', line_no)
                    print(f"✓ Program '{program_name}' found at line {line_no}")
                continue
            
            # Handle VAR section
            if line_lower.startswith('var'):
                in_var_section = True
                self.symbol_table.insert('var', 'keyword', 'global', line_no)
                print(f"✓ Variable declaration section starts at line {line_no}")
                continue
            
            # Handle BEGIN - end of var section
            if line_lower.startswith('begin'):
                in_var_section = False
                self.current_scope = 'local'
                self.symbol_table.insert('begin', 'keyword', 'local', line_no)
                print(f"✓ Begin block at line {line_no}")
                continue
            
            # Handle END
            if line_lower.startswith('end'):
                self.symbol_table.insert('end', 'keyword', 'local', line_no)
                print(f"✓ End statement at line {line_no}")
                continue
            
            # Process variable declarations in VAR section
            if in_var_section:
                # Pattern: variable_name : type;
                # Also handles: var1, var2, var3 : type;
                match = re.match(r'^\s*([a-zA-Z_]\w*(?:\s*,\s*[a-zA-Z_]\w*)*)\s*:\s*(\w+)', line, re.IGNORECASE)
                if match:
                    var_names = match.group(1)
                    var_type = match.group(2).lower()
                    
                    # Split multiple variables
                    variables = [v.strip() for v in var_names.split(',')]
                    
                    # Add type as keyword if it's a standard type
                    if var_type in {'integer', 'real', 'boolean', 'char', 'string'}:
                        self.symbol_table.insert(var_type, 'keyword', 'global', line_no)
                    
                    # Add each variable
                    for var in variables:
                        self.symbol_table.insert(var, var_type, 'local', line_no)
                        print(f"✓ Variable '{var}' : {var_type} declared at line {line_no}")
        
        print("\n✓ Lexical analysis completed!")
        print(f"✓ Symbols stored in AVL tree-based symbol table")
    
    def tokenize(self, line):
        """Split line into tokens"""
        pattern = r"'[^']*'|:=|<>|<=|>=|\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|[+\-*/=<>()[\];,.:{}]"
        tokens = re.findall(pattern, line)
        return tokens


# ============= MAIN PROGRAM =============

def main():
    """Main program"""
    
    print("\n" + "="*60)
    print("     PASCAL LEXICAL ANALYZER")
    print("     Symbol Table Implementation using AVL Tree")
    print("="*60)
    print("\nPaste your Pascal code below.")
    print("Type 'END_CODE' on a new line when finished:")
    print("-" * 60)
    
    # Read multi-line Pascal code
    code_lines = []
    while True:
        try:
            line = input()
            if line.strip() == 'END_CODE':
                break
            code_lines.append(line)
        except EOFError:
            break
    
    pascal_code = '\n'.join(code_lines)
    
    if not pascal_code.strip():
        print("\n✗ No code provided. Exiting.")
        return
    
    # Create analyzer and process code
    analyzer = LexicalAnalyzer()
    analyzer.analyze(pascal_code)
    
    # Display symbol table
    analyzer.symbol_table.display_all()
    
    # Interactive menu for additional operations
    while True:
        print("\n" + "="*60)
        print("     ADDITIONAL OPERATIONS")
        print("="*60)
        print("1. Search for a symbol")
        print("2. Delete a symbol")
        print("3. Display symbol table again")
        print("4. Analyze new code")
        print("5. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            identifier = input("Enter identifier to search: ").strip()
            result = analyzer.symbol_table.search(identifier)
            if result:
                print(f"\n✓ Found '{identifier}':")
                result.display()
            else:
                print(f"\n✗ '{identifier}' not found")
        
        elif choice == '2':
            identifier = input("Enter identifier to delete: ").strip()
            analyzer.symbol_table.delete(identifier)
        
        elif choice == '3':
            analyzer.symbol_table.display_all()
        
        elif choice == '4':
            print("\nPaste your Pascal code below.")
            print("Type 'END_CODE' on a new line when finished:")
            print("-" * 60)
            code_lines = []
            while True:
                try:
                    line = input()
                    if line.strip() == 'END_CODE':
                        break
                    code_lines.append(line)
                except EOFError:
                    break
            pascal_code = '\n'.join(code_lines)
            analyzer = LexicalAnalyzer()
            analyzer.analyze(pascal_code)
            analyzer.symbol_table.display_all()
        
        elif choice == '5':
            print("\n" + "="*60)
            print("Thank you for using the Pascal Lexical Analyzer!")
            print("="*60 + "\n")
            break
        
        else:
            print("\n✗ Invalid choice")


if __name__ == "__main__":
    main()