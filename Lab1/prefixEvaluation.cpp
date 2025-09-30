#include <iostream>
#include <stack>
#include <string>
#include <sstream>
using namespace std;

// Check if a string is a mathematical operator
bool isOperator(const string &op)
{
    return (op == "+" || op == "-" || op == "*" || op == "/");
}

// Apply an operator to two numbers
double applyOperator(const string &op, double left, double right)
{
    if (op == "+")
        return left + right;
    if (op == "-")
        return left - right;
    if (op == "*")
        return left * right;
    if (op == "/")
        return (right == 0 ? 0 : left / right); // avoid division by zero
    return 0; // if operator not recognized
}

// Eliminate if a token is useless i.e., brackets, commas, or empty
bool isUselessToken(const string &t)
{
    return (t == "(" || t == ")" || t == "[" || t == "]" || t == "{" || t == "}" || t == "," || t == "");
}

// Main function that evaluates a prefix expression
double evaluatePrefixValue(string expression)
{
    stack<double> solutionStack;   // stack for storing intermediate results (numbers)
    stack<string> tokens;          // stack for storing all tokens from the input

    stringstream stream(expression); // turn the whole input line into a stream
    string token;

    // Break the expression into tokens and push them into "tokens" stack
    while (stream >> token)
    {
        tokens.push(token);
    }

    // Now process tokens one by one (from right to left because we used a stack)
    while (!tokens.empty())
    {
        string t = tokens.top();
        tokens.pop();

        cout << "Token: " << t << endl; // debugging

        // Skip useless tokens like brackets or commas
        if (isUselessToken(t))
        {
            continue;
        }

        // If the token is an operator (+,-,*,/), apply it
        if (isOperator(t))
        {
            double right = 0, left = 0;

            // Pop two numbers from the solution stack
            if (!solutionStack.empty())
            {
                right = solutionStack.top();
                solutionStack.pop();
            }
            if (!solutionStack.empty())
            {
                left = solutionStack.top();
                solutionStack.pop();
            }

            // Apply operator to these numbers
            double result = applyOperator(t, left, right);

            // Debug info
            cout << "Applied operator: " << t
                << "\nLeft: " << left
                << " Right: " << right
                << " Result: " << result << endl;

            // Push result back into the stack
            solutionStack.push(result);
        }

        else
        {
            // If the token is a number, convert string -> double and push to stack
            try
            {
                solutionStack.push(stod(t));
            }
            catch (invalid_argument &)
            {
                cout << "Ignoring invalid token: " << t << endl;
            }
        }
    }

    // If nothing is in stack, return 0
    if (solutionStack.empty())
        return 0;
    return solutionStack.top(); // final answer is at the top
}

int main()
{
    string input;
    cout << "Enter prefix expression (tokens separated by space): ";
    getline(cin, input); // read whole line from user

    cout << "Expression: " << input << endl;

    double answer = evaluatePrefixValue(input); // evaluate expression

    cout << "Result: " << answer << endl; // show result

    return 0;
}
