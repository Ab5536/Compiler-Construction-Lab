#include <iostream>
#include <stack>
#include <string>
#include <sstream>
using namespace std;

bool isOperator(const string &op)
{
    return (op == "+" || op == "-" || op == "*" || op == "/");
}

int applyOperator(const string &op, int left, int right)
{
    if (op == "+")
        return left + right;
    if (op == "-")
        return left - right;
    if (op == "*")
        return left * right;
    if (op == "/")
        return (right == 0 ? 0 : left / right);
    return 0;
}

bool isUselessToken(const string &t)
{
    return (t == "(" || t == ")" || t == "[" || t == "]" || t == "{" || t == "}" || t == "," || t == "");
}

int evaluatePrefixValue(string expression)
{
    stack<int> solutionStack;
    stack<string> tokens;

    stringstream stream(expression);
    string token;

    while (stream >> token)
    {
        tokens.push(token);
    }

    while (!tokens.empty())
    {
        string t = tokens.top();
        tokens.pop();

        cout << "Token: " << t << endl;

        if (isUselessToken(t))
        {
            continue;
        }

        if (isOperator(t))
        {
            int left = 0, right = 0;
            if (!solutionStack.empty())
            {
                left = solutionStack.top();
                solutionStack.pop();
            }
            if (!solutionStack.empty())
            {
                right = solutionStack.top();
                solutionStack.pop();
            }

            int result = applyOperator(t, left, right);

            cout << "Applied operator: " << t
                 << "\nLeft: " << left
                 << " Right: " << right
                 << " Result: " << result << endl;

            solutionStack.push(result);
        }
        else
        {
            try
            {
                solutionStack.push(stoi(t));
            }
            catch (invalid_argument)
            {
                cout << "Ignoring invalid token: " << t << endl;
            }
        }
    }

    if (solutionStack.empty())
        return 0;
    return solutionStack.top();
}

int main()
{
    string input;
    cout << "Enter prefix expression (tokens separated by space): ";
    getline(cin, input);

    cout << "Expression: " << input << endl;

    int answer = evaluatePrefixValue(input);

    cout << "Result: " << answer << endl;

    return 0;
}
