// Libraries
#include <iostream>
#include <fstream>
#include <filesystem>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <unordered_set>

using namespace std;
using namespace std::filesystem;

// Structs
struct FileAnalysis
{
    string fileName;
    size_t lineCount;
    size_t wordCount;
    vector<pair<string, int>> commonWords;
    size_t avgWordLength;
    size_t charCount;
    size_t vowelCount;
    size_t consonantCount;
};

// Function Prototypes
char checkTasks();
string getStringInput(string text);
void openFileForDisplay(string path);
vector<FileAnalysis> performFileAnalysis(string path);
vector<string> getFileNamesInDirectory(string directoryPath);
void reportResults(const vector<FileAnalysis> &results, string reportPath);

// Main Function
int main()
{
    try
    {
        const string rootPath = "E:/Compiler Construction Lab/Compiler Construction/Lab2/";
        char option = checkTasks();
        if (option == '3')
        {
            cout << "Exiting the program." << endl;
            return 0;
        }
        else if (option == '1')
        {
            string pathForRead = rootPath + "Files/data.txt";
            openFileForDisplay(pathForRead);
        }
        else if (option == '2')
        {
            string pathForAnalysis = getStringInput("Enter the folder path for analysis(Absolute): ");
            string pathForReport = getStringInput("Enter the file path for report(Absolute): ");
            const vector<FileAnalysis> analysisResults = performFileAnalysis(pathForAnalysis);
            reportResults(analysisResults, pathForReport);
        }
        return 0;
    }
    catch (exception &e)
    {
        cout << "Error occurred: " << e.what() << endl;
    }
}

char checkTasks()
{
    bool check = true;
    char option;
    while (check)
    {
        cout << "Choose an option: " << endl;
        cout << "1. Read from file and Display" << endl;
        cout << "2. File Analysis" << endl;
        cout << "3. Exit" << endl;
        cin >> option;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        if (option == '1' || option == '2' || option == '3')
        {
            check = false;
        }
        else
        {
            cout << "Invalid Option! Please try again." << endl;
        }
    }
    return option;
}

void openFileForDisplay(string path)
{
    try
    {
        ifstream fileRead(path, ios::in);
        if (!fileRead)
        {
            cerr << "File could not be opened!" << endl;
            return;
        }
        cout << "Contents of the file are: " << endl
             << endl;
        cout << fileRead.rdbuf();
        fileRead.close();
    }
    catch (exception &e)
    {
        cout << "Unable to Open file: " << e.what() << endl;
    }
}

string getStringInput(string text)
{
    string value;
    cout << text;
    getline(cin, value);
    return value;
}

vector<string> getFileNamesInDirectory(string directoryPath)
{
    vector<string> fileNames;
    try
    {
        for (const auto &checkName : directory_iterator(directoryPath))
        {
            if (is_regular_file(checkName) && checkName.path().extension() == ".txt")
            {
                fileNames.push_back(checkName.path().filename().string());
            }
        }
    }
    catch (const exception &e)
    {
        cerr << "Error reading directory: " << e.what() << '\n';
    }
    return fileNames;
}

vector<FileAnalysis> performFileAnalysis(string path)
{
    vector<FileAnalysis> fileData;
    const unordered_set<string> stopWords = {
        "the", "and", "in", "of", "on", "a", "an", "is", "it", "to", "for", "with",
        "at", "by", "from", "that", "this", "these", "those", "as", "be", "been",
        "are", "was", "were", "or", "but", "if", "then", "so", "because"," "};
    try
    {
        cout << "Performing file analysis on: " << path << endl;
        vector<string> fileNames = getFileNamesInDirectory(path);
        for (const string &name : fileNames)
        {
            cout << "Found text file: " << name << endl;
            const string filePath = path + "/" + name;
            vector<string> words;
            ifstream fileRead(filePath, ios::in);
            if (!fileRead)
            {
                cerr << "File could not be opened!" << endl;
                continue;
            }

            FileAnalysis analysis;
            analysis.fileName = name;
            int lineCounter = 0;
            int wordCounter = 0;
            int vowelCounter = 0;
            int consonantCounter = 0;
            int charCounter = 0;
            string line = "";

            while (getline(fileRead, line))
            {
                lineCounter++;
                for (char c : line)
                {
                    vector<char> singleWord;
                    if (isalpha(c))
                    {
                        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ||
                            c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U')
                        {
                            singleWord.push_back(c);
                            vowelCounter++;
                            charCounter++;
                        }
                        else
                        {
                            singleWord.push_back(c);
                            consonantCounter++;
                            charCounter++;
                        }
                    }
                    else if (isdigit(c))
                    {
                        singleWord.push_back(c);
                        charCounter++;
                    }
                    else if (isspace(c))
                    {
                        words.push_back(string(singleWord.begin(), singleWord.end()));
                        wordCounter++;
                        singleWord.clear();
                    }
                    else
                    {
                        charCounter++;
                    }
                }
            }

            unordered_map<string, int> wordCount;
            for (const string &word : words)
            {
                if(word.empty() || stopWords.find(word) != stopWords.end())
                    continue;
                wordCount[word]++;
            }

            analysis.commonWords.assign(wordCount.begin(), wordCount.end());
            sort(analysis.commonWords.begin(), analysis.commonWords.end(), [](const pair<string, int> &a, const pair<string, int> &b)
                 { return b.second < a.second; });

            analysis.lineCount = lineCounter;
            analysis.wordCount = wordCounter;
            analysis.vowelCount = vowelCounter;
            analysis.consonantCount = consonantCounter;
            analysis.charCount = charCounter;
            analysis.avgWordLength = (wordCounter == 0) ? 0 : charCounter / wordCounter;
            fileRead.close();
            fileData.push_back(analysis);
        }
    }
    catch (exception &e)
    {
        cout << "Unable to Open file: " << e.what() << endl;
    }
    return fileData;
}

void reportResults(const vector<FileAnalysis> &results, string reportPath)
{
    try
    {
        // const string filePath = reportPath + "/\report.txt";
        const int n = 5;
        ofstream fileOutput(reportPath, ios::out);
        if (!fileOutput)
        {

            cerr << "Report file could not be created!" << endl;
            return;
        }
        fileOutput << "Total Number of Files: " << results.size() << endl;
        fileOutput << "{" << endl;
        for (const FileAnalysis &analysis : results)
        {

            fileOutput << "{";
            fileOutput << " File Name: " << analysis.fileName << "," << endl;
            fileOutput << " Line Count: " << analysis.lineCount << "," << endl;
            fileOutput << " Word Count: " << analysis.wordCount << "," << endl;
            fileOutput << " Most Common Words: ";
            for (int i = 0; i < n && i < analysis.commonWords.size(); i++)
            {
                fileOutput << "{\"" << analysis.commonWords[i].first << "\","
                           << analysis.commonWords[i].second << "}";
                if (i < n - 1 && i < analysis.commonWords.size() - 1)
                    fileOutput << ",";
            }
            fileOutput << " Average Word Length: " << analysis.avgWordLength << "," << endl;
            fileOutput << " Vowel to Consonant Ratio: 1 : "
                       << (analysis.vowelCount == 0 ? 0.0
                                                    : analysis.consonantCount / analysis.vowelCount)
                       << endl;

            fileOutput << " Consonant Count: " << analysis.consonantCount << "," << endl;
            fileOutput << " Character Count: " << analysis.charCount << "," << endl;
            fileOutput << "}," << endl;

            cout << "Reporting analysis for file: " << analysis.fileName << endl;
        }
        fileOutput << "}" << endl;
        fileOutput.close();
        cout << "Report generated at: " << reportPath << endl;
    }
    catch (exception &e)
    {
        cout << "Unable to write report: " << e.what() << endl;
    }
}
